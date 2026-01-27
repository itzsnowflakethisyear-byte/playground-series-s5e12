from pathlib import Path
import yaml
import pandas as pd
from google.cloud import storage
from io import BytesIO

# --- Load YAML config ---
CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.yaml"
with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

# --- Local paths ---
RAW_DIR = Path(cfg["data_ingestion"]["local"]["raw_dir"])
RAW_DIR.mkdir(parents=True, exist_ok=True)

FILES = cfg["data_ingestion"]["files"]

# --- GCS info ---
GCS_BUCKET = cfg["data_ingestion"]["gcs"]["bucket"]
GCS_RAW_PREFIX = cfg["data_ingestion"]["gcs"]["raw_prefix"]

# --- GCP project ---
PROJECT_ID = cfg["gcp"]["project_id"]

# --- GCS Client ---
client = storage.Client(project=PROJECT_ID)
bucket = client.bucket(GCS_BUCKET)

# --- Core function ---
def load_from_gcs(file_key: str) -> pd.DataFrame:
    if file_key not in FILES:
        raise ValueError(f"{file_key} not found in config files")

    local_path = RAW_DIR / FILES[file_key]
    gcs_path = f"{GCS_RAW_PREFIX}/{FILES[file_key]}"

    if not local_path.exists():
        blob = bucket.blob(gcs_path)
        data = blob.download_as_bytes()
        local_path.write_bytes(data)

    return pd.read_csv(local_path)

# --- Convenience dict ---
dfs = {key: load_from_gcs(key) for key in FILES}
train_df = dfs.get("train")
test_df = dfs.get("test")
