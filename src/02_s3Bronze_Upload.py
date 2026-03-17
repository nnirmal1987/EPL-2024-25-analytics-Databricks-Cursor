import boto3
import os
import json
from pathlib import Path
from datetime import datetime
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError

# ── CONFIG ───────────────────────────────────────────────
CONFIG = {
    # Do NOT hardcode AWS credentials in source code.
    # Use environment variables, an AWS profile, or SSO.
    "aws_region": os.getenv("AWS_REGION", "ca-central-1"),
    "bucket_name": os.getenv("S3_BUCKET_NAME", "football-analytics-nirmal"),
}

LOCAL_DATA_DIR = "./kaggle_download"
S3_PREFIX      = "bronze/premier-league/2024-25"

FILES = {
    "premier_league_stats_2024-25.csv": f"{S3_PREFIX}/standings/standings.csv",
    "epl_final.csv"  : f"{S3_PREFIX}/matches/matches.csv",
    "database.csv"  : f"{S3_PREFIX}/players/players.csv",
}

# ── CREATE S3 CLIENT ───────────────────────────────────
s3 = boto3.client("s3", region_name=CONFIG["aws_region"])

# ── ENSURE BUCKET EXISTS ───────────────────────────────
try:
    s3.head_bucket(Bucket=CONFIG["bucket_name"])
except NoCredentialsError:
    raise SystemExit(
        "❌ AWS credentials not found.\n"
        "Fix one of these, then re-run:\n"
        "  - Set env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY (and AWS_SESSION_TOKEN if temporary)\n"
        "  - Or configure a profile: `aws configure` and optionally set AWS_PROFILE\n"
        "  - Or use SSO: `aws configure sso` then `aws sso login`\n"
    )
except ClientError as e:
    # If bucket doesn't exist (404), create it. Otherwise, surface the real error.
    code = e.response.get("Error", {}).get("Code", "")
    status = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    if code in {"404", "NoSuchBucket", "NotFound"} or status == 404:
        if CONFIG["aws_region"] == "us-east-1":
            s3.create_bucket(Bucket=CONFIG["bucket_name"])
        else:
            s3.create_bucket(
                Bucket=CONFIG["bucket_name"],
                CreateBucketConfiguration={"LocationConstraint": CONFIG["aws_region"]},
            )
    else:
        raise

# ── UPLOAD FILES ───────────────────────────────────────
uploaded = {}
for filename, s3_key in FILES.items():
    local_path = os.path.join(LOCAL_DATA_DIR, filename)
    if os.path.exists(local_path):
        s3.upload_file(
            local_path,
            CONFIG["bucket_name"],
            s3_key,
            ExtraArgs={
                "Metadata": {
                    "source": "fbref.com",
                    "layer": "bronze",
                    "uploaded_at": datetime.utcnow().isoformat(),
                    "season": "2024-25"
                },
                "ContentType": "text/csv"
            }
        )
        s3_uri = f"s3://{CONFIG['bucket_name']}/{s3_key}"
        uploaded[filename] = s3_uri
        print(f"Uploaded {filename} → {s3_uri}")
    else:
        print(f"{filename} not found in {LOCAL_DATA_DIR}")

# ── GENERATE DATABRICKS CONFIG ────────────────────────
config = {
    "s3_bucket": CONFIG["bucket_name"],
    "aws_region": CONFIG["aws_region"],
    "s3_prefix": S3_PREFIX,
    "paths": uploaded,
}

with open("./databricks_s3_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("✅ Upload complete. Databricks config saved as databricks_s3_config.json")