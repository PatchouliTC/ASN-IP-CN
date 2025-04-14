from scripts.enum import LOCAL_TIME
from scripts.common import gen_data_storage_path, pre_check, WriteHeader,WriteBody,WriteEnd,get_url_data

file_name=gen_data_storage_path('ASN.BGPHE.China.list')
file_type='ASN'
source='https://bgp.he.net/country/CN'

# 0 =
# ''
# 1 = ASN
# 'AS140731'
# 2 = NAME
# 'TOHU Public Internet'
# 3 = v4 count
# '612'
# 4 = v4 route
# '1'
# 5 = v6 count
# '803'
# 6 = v4 route
# '19'

def process()->bool:
    pre_check(file_name)
    WriteHeader(file_name, file_type, LOCAL_TIME, 
                [f"// FROM:{source} \n","// Format: ASN //FULLNAME [IPv4-count,IPv6-count]<IPv4-route,IPV6-route>\n"])
    code,data=get_url_data(source,5)
    if code!=200:
        return False
    all_rows = data.xpath('//*[@id="asns"]/tbody/tr')
    write_data=[]
    for i, row in enumerate(all_rows):
        cells = row.xpath('./td | ./td/a')
        if len(cells) != 7:
            continue
        cell_texts = [cell.text.strip() if cell.text else "" for cell in cells]
        write_data.append(f"{cell_texts[1]} //{cell_texts[2]}, CN [{cell_texts[3].replace(',','')},{cell_texts[4].replace(',','')}]<{cell_texts[5].replace(',','')},{cell_texts[6].replace(',','')}>\n")
    if len(write_data)==0:
        print('receive empty,may be ipip web style changed?')
        return False
    WriteBody(file_name,write_data)
    return True