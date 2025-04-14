# version :Python 3.7.3
import os
import re
import urllib.error
import urllib.request

file_name = 'asn_cn.conf'
define_line = 'define china_asn = ['
end_line = '];'
# data_source = 'https://whois.ipip.net/countries/CN'
data_source = 'https://whois.ipip.net/iso/CN'

try:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    response = urllib.request.urlopen(data_source,timeout=30,headers=headers)
except urllib.error.HTTPError as e:
    print("HTTPError: ", e.code)
    print(f"IPIP不可达({e.code})")
    exit(1)
if response.getcode() != 200:
    print("获取数据失败，请检查网络连接或URL是否正确")
    exit(1)
    
html = response.read().decode('utf-8')
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