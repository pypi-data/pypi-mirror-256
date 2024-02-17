from __future__ import annotations
import logging
from typing import Optional, Sequence

from hydra.types import HydraContext
from hydra.core.singleton import Singleton
from hydra.core.utils import (
    JobReturn,
    configure_log,
    filter_overrides,
    setup_globals,
)
from hydra.plugins.launcher import Launcher
from hydra.types import TaskFunction
from omegaconf import DictConfig, open_dict, OmegaConf

from hydra_plugins.vertex_ai_custom_job_launcher import __version__, __requirements__
from hydra_plugins.vertex_ai_custom_job_launcher._core import (
    read_env_vars_file,
    init_gcs_filesystem,
    get_hydra_sweep_dir_gs_url,
    upload_package_to_gcs,
    pickle_job_specs,
    load_job_returns,
    JOB_STATE_ID_NAME_MAP
)

log = logging.getLogger(__name__)

def launch_custom_jobs(
    launcher: VertexAICustomJobLauncher,
    job_overrides: Sequence[Sequence[str]],
    initial_job_idx: int,
) -> Sequence[JobReturn]:
    """
    Launch as many custom jobs as there are job overrides.
    """

    # Lazy imports, to avoid slowing down the registration of all other plugins
    import os
    import time
    from google.cloud import aiplatform

    # Set up global Hydra variables
    setup_globals()

    # Assert that the launcher has been set up
    assert launcher.config is not None
    assert launcher.hydra_context is not None
    assert launcher.task_function is not None

    # Configure the logging subsystem
    configure_log(launcher.config.hydra.hydra_logging, 
                  launcher.config.hydra.verbose)
    log.debug(f"Hydra logging configured with:" +
              f"- Hydra logging: {launcher.config.hydra.hydra_logging}\n" +
              f"- Verbose: {launcher.config.hydra.verbose}")

    # Set up Vertex AI variables
    project_id = launcher.init.project_id
    location = launcher.init.location
    staging_bucket = launcher.init.staging_bucket
    experiment = launcher.init.experiment
    experiment_tensorboard = launcher.init.experiment_tensorboard
    display_name = launcher.custom_job.display_name
    worker_pool_specs = launcher.custom_job.worker_pool_specs
    base_output_dir = launcher.custom_job.base_output_dir
    labels = launcher.custom_job.labels
    service_account_email = launcher.custom_job.service_account_email

    # Set up environment variables, either from a .env file or from a dictionary in the config
    env_vars = None
    if launcher.env_vars is not None:
        if isinstance(launcher.env_vars, str):
            log.info(f"Reading environment variables from file {launcher.env_vars}...")
            env_vars = read_env_vars_file(launcher.env_vars)
        elif isinstance(launcher.env_vars, dict):
            env_vars = launcher.env_vars
        log.info(f"Environment variables: {env_vars}")
    else:
        log.info("No environment variables.")

    # Set up the filesystem for the staging bucket
    log.info(f"Setting up the filesystem for the staging bucket \"{staging_bucket}\"...")
    fs = init_gcs_filesystem(staging_bucket)

    # Get the GCS directory for the sweep output
    sweep_output_gs_dir = get_hydra_sweep_dir_gs_url(staging_bucket, launcher.config.hydra.sweep.dir)
    log.info(f"Getting the GCS directory for the sweep output: {sweep_output_gs_dir}...")
    fs.makedirs(sweep_output_gs_dir)
    launcher.config.hydra.sweep.dir = sweep_output_gs_dir.replace("gs:/", "/gcs")

    # Zip the package root directory (./hydra_plugins) to a temporary directory and copy it to the GCS directory
    launcher_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    plugins_dir = os.path.abspath(os.path.join(launcher_dir, ".."))
    root_dir = os.path.abspath(os.path.join(plugins_dir, ".."))
    log.info(f"Zipping the package directory hydra_plugins from {root_dir} to a temporary directory" +
             f" and copying it to the GCS directory {sweep_output_gs_dir}...)")
    hydra_plugins_zip_gs_url = upload_package_to_gcs(root_dir, sweep_output_gs_dir, fs)

    # Initialize the global command lines for all jobs with the source installation into a Python directory at root
    global_cmds = [
        "mkdir -p /python",
        "export PYTHONPATH=$PYTHONPATH:/python",
        f"""unzip {hydra_plugins_zip_gs_url.replace("gs:/", "/gcs")} -d /python""",
    ]
    global_cmds.append(f"pip install " + " ".join(__requirements__))
    if env_vars:
        global_cmds.extend([f"export {k}={v}" for k, v in env_vars.items()])
    log.debug(f"Commands for all jobs: {global_cmds}")

    # Initialize Vertex AI
    log.info(f"Initializing Vertex AI with:\n" +
             f"- Project ID: {project_id}\n" +
             f"- Location: {location}\n" +
             f"- Staging bucket: {staging_bucket}\n" +
             f"- Experiment: {experiment}\n" +
             f"- Experiment Tensorboard: {experiment_tensorboard}")
    aiplatform.init(
        project=project_id,
        location=location,
        staging_bucket=staging_bucket,
        experiment=experiment,
        experiment_tensorboard=experiment_tensorboard
    )

    # For each job override:
    # - Load the sweep config and set the job id and job num.
    # - Pickle the job specs (hydra context, sweep config, task function and singleton state) into a temporary directory.
    # - Initialize the Vertex AI Custom Job, setting the container spec command to the task script and
    #   the container spec args to the temporary directory.
    # - Submit the job asynchronously.
    jobs: list[aiplatform.CustomJob] = []
    jobs_dirs_gs_urls: list[str] = []
    log.info(f"Launching {len(job_overrides)} custom jobs on Vertex AI...")
    for idx, overrides in enumerate(job_overrides):

        # Set the job id from the initial job idx and the current idx
        idx = initial_job_idx + idx

        # Log the job id and overrides
        lst = " ".join(filter_overrides(overrides))
        log.info(f"- #{idx} : {lst}")

        # Load the sweep config and set the job num
        log.info(f"Loading sweep config for job #{idx}...")
        sweep_config = launcher.hydra_context.config_loader.load_sweep_config(
            launcher.config, list(overrides)
        )
        with open_dict(sweep_config):
            sweep_config.hydra.job.num = idx

        # Initialize the Hydra GCS directory from :
        # - The staging bucket URL of the Vertex AI Custom Job
        # - The hydra sweep directory
        # - The hydra sweep subdir
        sweep_output_gs_subdir = get_hydra_sweep_dir_gs_url(
            staging_bucket, 
            sweep_config.hydra.sweep.dir,
            sweep_config.hydra.sweep.subdir
        )
        sweep_config.hydra.sweep.dir = sweep_output_gs_subdir.replace("gs:/", "/gcs")
        log.info(f"Setting the sweep directory for job #{idx} to {sweep_config.hydra.sweep.dir}...")
        log.info(f"Initializing the Hydra GCS directory for job #{idx} with {sweep_output_gs_subdir}...")
        jobs_dirs_gs_urls.append(sweep_output_gs_subdir)
        fs.mkdir(sweep_output_gs_subdir)

        # Pickle the job specs, so that they can be passed to the custom job.
        log.debug(f"Pickling job specs for job #{idx} to {sweep_output_gs_subdir}")
        pickle_job_specs(sweep_output_gs_subdir, fs,
                         hydra_context=launcher.hydra_context,
                         sweep_config=sweep_config,
                         task_function=launcher.task_function,
                         singleton_state=Singleton.get_state())

        # Initialize the job command line by adding the global command lines and the execution command
        custom_job_exec_script_path = f"/python/hydra_plugins/vertex_ai_custom_job_launcher/_custom_job_exec.py"
        job_cmds = [
            *global_cmds,
            f"python {custom_job_exec_script_path} {sweep_output_gs_subdir}"
        ]
        log.info(f"Commands for job #{idx}: {job_cmds}")

        # Override the command of the worker pool spec to the execution command
        job_cmd_one_line = " && ".join(job_cmds)
        log.info(f"Overriding the command of the worker pool specs for job #{idx} with {job_cmd_one_line}...")
        for worker_pool_spec in worker_pool_specs:
            worker_pool_spec.container_spec.command = ["sh", "-c", job_cmd_one_line]
            worker_pool_spec.container_spec.args = []

        # Convert the worker pool specs to a list of dictionaries
        worker_pool_specs = OmegaConf.to_container(worker_pool_specs, resolve=True)

        # Initialize the custom job
        log.info(f"Initializing custom job #{idx} with:\n" +
                  f"- Display name: {display_name}\n" +
                  f"- Worker pool specs: {worker_pool_specs}\n" +
                  f"- Base output dir: {base_output_dir}\n" +
                  f"- Labels: {labels}")
        job = aiplatform.CustomJob(
            display_name=display_name,
            worker_pool_specs=worker_pool_specs,
            base_output_dir=base_output_dir,
            labels=labels
        )

        # Submit the job
        log.info(f"Submitting custom job #{idx} with service account {service_account_email}...")
        job.submit(service_account=service_account_email)
        
        # Append the job to the list of jobs
        jobs.append(job)

    # Wait for the jobs to complete
    log.info("Waiting for the jobs to complete...")
    for i, job in enumerate(jobs):
        log.info(f"Waiting for job #{i} \"{job.display_name}\" (Vertex Training Job id. : {job.name}) to complete...")
        while job.state not in [aiplatform.gapic.JobState.JOB_STATE_SUCCEEDED,
                                aiplatform.gapic.JobState.JOB_STATE_FAILED,
                                aiplatform.gapic.JobState.JOB_STATE_CANCELLED]:
            time.sleep(1)
        log.info(f"Job #{i} \"{job.display_name}\" completed with state {JOB_STATE_ID_NAME_MAP[job.state]}.")

    # Read the job returns and delete the temporary directories
    log.info("Reading the jobs returns...")
    jobs_returns: list[JobReturn] = []
    for job_dir_gs_url in jobs_dirs_gs_urls:
        log.info(f"Reading the job return from {job_dir_gs_url}/job_returns.pkl...")
        job_return = load_job_returns(job_dir_gs_url, fs)
        jobs_returns.append(job_return)

    # Return the job returns
    return jobs_returns

class VertexAICustomJobLauncher(Launcher):

    def __init__(
        self,
        **kwargs
    ) -> None:
        
        self.config: Optional[DictConfig] = None
        self.task_function: Optional[TaskFunction] = None
        self.hydra_context: Optional[HydraContext] = None

        for key, value in kwargs.items():
            setattr(self, key, value)

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.config = config
        self.hydra_context = hydra_context
        self.task_function = task_function

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        """
        :param job_overrides: a List of List<String>, where each inner list is the arguments for one job run.
        :param initial_job_idx: Initial job idx in batch.
        :return: an array of return values from run_job with indexes corresponding to the input list indexes.
        """
        return launch_custom_jobs(self, job_overrides, initial_job_idx)