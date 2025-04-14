import os
from datetime import datetime, timezone

OUTPUT_DIR_NAME="output"
FINAL_RELEASE_FILE_NAME="ASN-IP-Data.zip"
ASSET_CONTENT_TYPE='application/zip'
CURRENT_ROOT_PATH = os.getcwd()
LOCAL_TIME = datetime.now(timezone.utc)