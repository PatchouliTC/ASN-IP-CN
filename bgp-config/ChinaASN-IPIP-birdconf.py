# version :Python 3.7.3
import os
import re
import time
import requests

file_name = 'asn_cn.conf'
define_line = 'define china_asn = ['
end_line = '];'
# data_source = 'https://whois.ipip.net/countries/CN'
data_source = 'https://whois.ipip.net/iso/CN'

def get_url_data(url:str,retry_times:int=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    call_times=0
    code=0
    result=None
    while(call_times<retry_times):
        call_times+=1
        print(f"Connection to {url}[{call_times} try]...")
        try:
            response = requests.get(url = url, headers = headers,timeout=60)
            if response.status_code != 200:
                print(f"Target unreachable({response.status_code})")
                code=response.status_code
            code=response.status_code
            result=response.text
            break
        except requests.ConnectTimeout as e:
            print(f"Target unreachable(timeout 30s)")
            code=500
        except requests.ConnectionError as e:
            print(f"Target unreachable[ConnectionError]({e})")
            code=500
        except requests.RequestException as e:
            print(f"Target unreachable[RequestException]({e.errno})")
            code=500
        except requests.HTTPError as e:
            print(f"Target unreachable[HTTPError]({e.errno})")
            code=500
        except Exception as e:
            print(f"Target unreachable({e})")
            code=500
        time.sleep(3)
    return code,result

code,result=get_url_data(data_source,3)
if code !=200:
    print(f"数据获取失败，错误代码：{code}")
    exit(1)

html = result
print("数据获取成功，正在解析数据...")
data=re.findall(', CN\">AS(.*?)</a> </td>', html, re.S)
cn_asn_codes = [i for i in data]
print(f"共获取到 {len(cn_asn_codes)} 个ASN code")

if os.path.exists(file_name):
    print(f"文件 {file_name} 已存在，正在读取文件内容...")
    exist_asn_codes = []
    lines=None
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    try:
        lines = lines[1:-1]
        for line in lines:
            # 去掉行尾的逗号和空白字符
            code = line.strip().rstrip(',').strip()
            if code:  # 确保不是空行
                exist_asn_codes.append(code)
        print(f"文件 {file_name} 中已存在{len(exist_asn_codes)} 个ASN code")
        cn_asn_codes=list(set(cn_asn_codes).union(set(exist_asn_codes)))
        print(f"合并后总共有{len(cn_asn_codes)} 个ASN code")
    except:
        print("文件格式错误,忽略历史数据")
    
with open(file_name, 'w',encoding='utf-8') as f:
    # 写入开头
    f.write(define_line + '\n')
    
    # 写入ASN代码，每个占一行
    for i, asn in enumerate(cn_asn_codes):
        if i < len(cn_asn_codes) - 1:
            f.write(asn + ',\n')
        else:
            # 最后一行不需要逗号
            f.write(asn + '\n')
    
    # 写入结尾
    f.write(end_line)
print(f"文件 {file_name} 已成功更新，包含 {len(cn_asn_codes)} 个ASN code")