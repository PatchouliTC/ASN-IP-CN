from scripts.enum import LOCAL_TIME
from scripts.common import gen_data_storage_path, pre_check, WriteHeader,WriteBody,WriteEnd,get_url_data

file_name=gen_data_storage_path('ASN.POTAROO.China.list')
file_type='ASN'
source='https://bgp.potaroo.net/cidr/autnums.html'

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
    header_extra_data=[f"// FROM:{source} \n",
                       "// Format: ASN //FULLNAME \n"
                       ]
    code,data=get_url_data(source,5)
    if code!=200:
        return False
    all_rows = data.xpath('//pre//a')
    write_data=[]
    for i, row in enumerate(all_rows):
        if not row.tail.strip().endswith('CN'):
            continue
        cell_texts = [row.text.strip(),row.tail.strip()]
        write_data.append(f"{cell_texts[0].replace('AS','')} //{cell_texts[1]} \n")
    if len(write_data)==0:
        print('receive empty,may be ipip web style changed?')
        return False
    header_extra_data.append(f"// Total {len(write_data)} records \n")
    WriteHeader(file_name, file_type, LOCAL_TIME, header_extra_data)
    WriteBody(file_name,write_data)
    return True