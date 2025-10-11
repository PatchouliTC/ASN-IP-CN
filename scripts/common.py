import requests
from lxml import etree
from datetime import datetime, timezone
import time
import os
from pathlib import Path
import uuid
import zipfile
from scripts.enum import *
from typing import List

def zip_dir(path_with_filename:Path,work_dir:Path,comment:str=None)->None:
    if path_with_filename.suffix is None or path_with_filename.suffix != '.zip':
        path_with_filename.suffix = '.zip'
    output = str(path_with_filename.absolute())
    with zipfile.ZipFile(output, "w") as zip:
        if comment:
            zip.comment = comment.encode('utf-8')
        for f in work_dir.iterdir():
            _scan_dir(zip, f, work_dir)

def _scan_dir(zip:zipfile.ZipFile, dir:Path, base_dir:Path):
    if dir.is_file():
        zip.write(dir, str(dir)[len(str(base_dir)):])
    else:        
        for f in dir.iterdir():
            if f.is_dir():
                _scan_dir(zip, f, base_dir)
            else:
                zip.write(f, str(f)[len(str(base_dir)):])
            
def get_output_locate()->Path:
    return CURRENT_ROOT_PATH.joinpath(OUTPUT_DIR_NAME).absolute()

def gen_data_storage_path(file_name:str)->Path:
    return CURRENT_ROOT_PATH.joinpath(OUTPUT_DIR_NAME).joinpath(file_name).absolute()

def set_singleline_output(name:str,value:any)->None:
    if 'GITHUB_OUTPUT' not in os.environ:
        print(f"{name}={value}")
        return
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{name}={value}', file=fh)
        
def set_multiline_output(name:str, value:str)->None:
    if 'GITHUB_OUTPUT' not in os.environ:
        print(f"{name}={value}")
        return
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        delimiter = uuid.uuid1()
        print(f'{name}<<{delimiter}', file=fh)
        print(value, file=fh)
        print(delimiter, file=fh)
        


def pre_check(file_name:Path):
    directory = file_name.resolve().parent
    os.makedirs(directory, exist_ok=True)
    
def WriteHeader(file_name:str,file_type:str,write_at:datetime,extra_lines:List[str]=None):
    with open(file_name, "w+" ,encoding='utf-8') as fs:
        fs.write(f'// DataType:{file_type} \n')
        fs.write(f"// {file_type} Information in China. (https://github.com/{REPO_NAME}) \n")
        fs.write(f"// Last Updated: {write_at} \n")
        fs.write(f"// Made by {REPO_AUTHOR}, All rights reserved. \n")
        if extra_lines:
            fs.writelines(extra_lines)
        fs.write('\n\n')

def WriteBody(file_name:str,data:List[str]):
    with open(file_name, "a+" ,encoding='utf-8') as fs:
        fs.writelines(data)

def WriteEnd(file_name:str,data:List[str]):
    with open(file_name, "a+" ,encoding='utf-8') as fs:
        fs.writelines(data)

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
            # with open(gen_data_storage_path("ipip.html"), "w",encoding='utf-8') as f:
            #     f.write(response.text)
            parse_result=etree.HTML(response.text)
            code=response.status_code
            result=parse_result
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


def write_dir_all_asn_to_bird_conf(dir_path:Path):
    if dir_path is None or not dir_path.exists() or not dir_path.is_dir():
        print('dir_path not exist or not a directory')
        return
    file_name = 'asn_cn.conf'
    str_start = 'define china_asn = [\n'
    str_end = '];'
    with open(dir_path.joinpath(file_name), 'w',encoding='utf-8') as file:
        file.writelines(str_start)
        asn_ids=[]
        def __write_asn_list_to_file(asn_ids:list,file_path:Path):
            if file_path.is_file() and file_path.suffix == '.list':
                with open(file_path, 'r') as f:
                    for line in f:
                        line=line.strip()
                        if line=='' or line.startswith('//'):
                            continue
                        asn=line.split(' ')[0].strip()
                        if asn.isdigit():
                            asn_ids.append("    "+str(asn)+",\n")
                
        def __write_asn_to_file(asn_ids:list,file_path:Path):
            if file_path.is_file():
                __write_asn_list_to_file(asn_ids,file_path)
            elif file_path.is_dir():
                for f in file_path.iterdir():
                    __write_asn_to_file(asn_ids,f)
            else:
                pass
        __write_asn_to_file(asn_ids,dir_path)
        
        asn_ids=list(set(asn_ids))
        if asn_ids:
            asn_ids[-1] = asn_ids[-1].rstrip(',\n') + '\n'
        file.writelines((asn_ids))
        file.writelines(str_end)