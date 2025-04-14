import requests
from lxml import etree
from datetime import datetime, timezone
import time
import os
from scripts.enum import LOCAL_TIME
from scripts.common import gen_data_storage_path, pre_check, WriteHeader,WriteBody,WriteEnd,get_url_data

file_name=gen_data_storage_path('ASN.IPIP.China.list')
file_type='ASN'
source='https://whois.ipip.net/iso/CN'


# 0 =
# ''
# 1 = ASN
# 'AS4134'
# 2 = NAME
# 'CHINANET-BACKBONE - No.31,Jin-rong Street, CN'
# 3 = v4 count
# '110,724,352'
# 4 = v6(64) count
# '17,592,187,682,816'

def process()->bool:
    pre_check(file_name)
    WriteHeader(file_name, file_type, LOCAL_TIME)
    code,data=get_url_data(source)
    if code!=200:
        return False
    all_rows = data.xpath('//table//tr')
    write_data=[]
    for i, row in enumerate(all_rows):
        cells = row.xpath('./td | ./td/a')
        if len(cells) != 5:
            continue
        cell_texts = [cell.text.strip() if cell.text else "" for cell in cells]
        write_data.append(f"{cell_texts[1]} //{cell_texts[2]}[{cell_texts[3].replace(',','')},{cell_texts[4].replace(',','')}]\n")
    WriteBody(file_name,write_data)
    return True