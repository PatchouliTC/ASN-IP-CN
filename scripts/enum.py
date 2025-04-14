import os
from pathlib import Path
from datetime import datetime, timezone

OUTPUT_DIR_NAME="output"
FINAL_RELEASE_FILE_NAME="ASN-IP-Data.zip"
CURRENT_ROOT_PATH = Path.cwd()
LOCAL_TIME = datetime.now(timezone.utc)
REPO_NAME = os.environ['github.repository'] if 'github.repository' in os.environ else "PatchouliTC/ASN-IP-CN"
REPO_AUTHOR = REPO_NAME.split("/")[0]