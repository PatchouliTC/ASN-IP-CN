import os
from pathlib import Path
from datetime import datetime, timezone

OUTPUT_DIR_NAME="output"
FINAL_RELEASE_FILE_NAME="ASN-IP-Data.zip"
CURRENT_ROOT_PATH = Path.cwd()
LOCAL_TIME = datetime.now(timezone.utc)