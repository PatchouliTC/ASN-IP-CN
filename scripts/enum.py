import os
from pathlib import Path
from datetime import datetime, timezone

#re filter
chinanet = 'china ?telecom|chinanet| ct'
cmcc = '(?:(?:china|henan|ZheJiang|YunNan|ShangHai|TianJin|BeiJing|ChongQing|AnHui|FuJian|GuangDong|GuangXi|GuiZhou|GanSu|HaiNan|HeBei|HeiLongJiang|HuBei|HuNan|JiLin|JiangSu|JiangXi|LiaoNing|NeiMengGu|NingXia|QingHai|ShanXi|ShanXi|ShanDong|SiChuan|XinJiang|YunNan|XiZang) ?mobile)|cmnet|tietong|CHINA ?RAILWAY'
unicom = 'unicom|cnc'
cernet = 'cngi|cernet|China ?Education'
cstnet = 'cstne|CNIC-CAS'

OUTPUT_DIR_NAME="output"
FINAL_RELEASE_FILE_NAME="ASN-IP-Data.zip"
CURRENT_ROOT_PATH = Path.cwd()
LOCAL_TIME = datetime.now(timezone.utc)
REPO_NAME = os.environ['github.repository'] if 'github.repository' in os.environ else "PatchouliTC/ASN-IP-CN"
REPO_AUTHOR = REPO_NAME.split("/")[0]