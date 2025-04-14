import requests
from lxml import etree
from datetime import datetime, timezone
import time
import os
from scripts.enum import LOCAL_TIME
from scripts.common import gen_data_storage_path, pre_check, WriteHeader

file_name=gen_data_storage_path('ASN.IPIP.China.list')
file_type='ASN'
source='https://whois.ipip.net/iso/CN'

def process()->bool:
    pre_check(file_name)
    WriteHeader(file_name, file_type, LOCAL_TIME)
    
    
    return True