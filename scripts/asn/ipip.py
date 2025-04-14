import requests
from lxml import etree
from datetime import datetime, timezone
import time
import os
from scripts.common import *

file_name='./result/ASN.IPIP.China.list'
localTime = datetime.now(timezone.utc)
file_type='ASN'
source='https://whois.ipip.net/iso/CN'

def process():
    pre_check(file_name)
    WriteHeader(file_name, file_type, localTime)