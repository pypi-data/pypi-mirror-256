import cloudpickle
import logging
import fsspec
import os
import tempfile
from typing import Optional
import zipfile

from hydra.core.utils import JobReturn

log = logging.getLogger(__name__)

HYDRA_PLUGINS_ZIP_NAME = "hydra_plugins.zip"
JOB_SPECS_PICKLE_NAME = "job_specs.pkl"
JOB_RETURNS_PICKLE_NAME = "job_returns.pkl"
JOB_STATE_ID_NAME_MAP = {
    0: "JOB_STATE_UNSPECIFIED",
    1: "JOB_STATE_QUEUED",
    2: "JOB_STATE_PENDING",
    3: "JOB_STATE_RUNNING",
    4: "JOB_STATE_SUCCEEDED",
    5: "JOB_STATE_FAILED",
    6: "JOB_STATE_CANCELLING",
    7: "JOB_STATE_CANCELLED",
    8: "JOB_STATE_PAUSED",
    9: "JOB_STATE_EXPIRED",
    10: "JOB_STATE_UPDATING",
    11: "JOB_STATE_PARTIALLY_SUCCEEDED"
}

def read_env_vars_file(
    env_vars_path: str
) -> dict:
    with open(env_vars_path, "r") as f:
        env_vars = {}
        for line in f:
            ret = line.strip().split("=")
            if len(ret) == 2:
                key, value = ret
                env_vars[key] = value.strip()
    return env_vars

def init_gcs_filesystem(
    staging_bucket: str,
) -> fsspec.AbstractFileSystem:
    fs_url = fsspec.core.url_to_fs(staging_bucket)
    fs: fsspec.AbstractFileSystem = fs_url[0]
    return fs

def get_hydra_sweep_dir_gs_url(
    staging_bucket: str,
    sweep_dir: str,
    sweep_subdir: Optional[str] = None,
) -> str:
    sweep_dir_gs_url = os.path.join(staging_bucket, sweep_dir)
    if sweep_subdir:
        sweep_dir_gs_url = os.path.join(sweep_dir_gs_url, sweep_subdir)
    return sweep_dir_gs_url

def upload_package_to_gcs(
    root_dir: str,
    sweep_dir_gs_url: str,
    fs: fsspec.AbstractFileSystem
) -> str:
    with tempfile.TemporaryDirectory() as source_temp_dir:
        with zipfile.ZipFile(os.path.join(source_temp_dir, HYDRA_PLUGINS_ZIP_NAME), "w") as zipf:
            for root, dirs, files in os.walk(os.path.join(root_dir, "hydra_plugins", "vertex_ai_custom_job_launcher")):
                for file in files:
                    filename = os.path.join(root, file)
                    arcname = os.path.relpath(filename, root_dir)
                    log.info(f"{filename}")
                    log.info(f"{arcname}")
                    zipf.write(filename, arcname)
        source_zip_path = os.path.join(source_temp_dir, HYDRA_PLUGINS_ZIP_NAME)
        source_zip_gs_url = os.path.join(sweep_dir_gs_url, HYDRA_PLUGINS_ZIP_NAME)
        fs.put(source_zip_path, source_zip_gs_url)
    return os.path.join(sweep_dir_gs_url, HYDRA_PLUGINS_ZIP_NAME)

def pickle_job_specs(
    sweep_output_dir: str,
    fs: fsspec.AbstractFileSystem,
    **job_specs: dict
) -> str:
    job_specs_path = os.path.join(sweep_output_dir, JOB_SPECS_PICKLE_NAME)
    with fs.open(job_specs_path, "wb") as f:
        cloudpickle.dump(job_specs, f)
    return job_specs_path

def load_job_returns(
    hydra_job_gcs_dir: str,
    fs: fsspec.AbstractFileSystem
) -> JobReturn:
    with fs.open(f"{hydra_job_gcs_dir}/job_returns.pkl", "rb") as f:
        job_return = cloudpickle.load(f)
    return job_return