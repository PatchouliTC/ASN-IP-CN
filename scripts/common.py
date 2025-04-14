import requests
from lxml import etree
from datetime import datetime, timezone
import os
from pathlib import Path
import uuid
import zipfile
from scripts.enum import *

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
    
def WriteHeader(file_name:str,file_type:str,write_at:datetime):
    with open(file_name, "w+" ,encoding='utf-8') as fs:
        fs.write(f'// DataType:{file_type} \n')
        fs.write(f"// {file_type} Information in China. (https://github.com/{REPO_NAME}) \n")
        fs.write(f"// Last Updated: {write_at} \n\n")

def WriteBody(file_name:str,data:list[str]):
    with open(file_name, "a+" ,encoding='utf-8') as fs:
        fs.writelines(data)

def WriteEnd(file_name:str,data:list[str]):
    with open(file_name, "a+" ,encoding='utf-8') as fs:
        fs.writelines(data)

def get_url_data(url:str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url = url, headers = headers,timeout=120)
        if response.status_code != 200:
            print(f"Target unreachable({response.status_code})")
            return response.status_code,None
        with open(gen_data_storage_path("ipip.html"), "w",encoding='utf-8') as f:
            f.write(response.text)
        parse_result=etree.HTML(response.text)
        return 200,parse_result
    except requests.ConnectTimeout as e:
        print(f"Target unreachable(timeout 30s)")
        return 500,None
    except requests.ConnectionError as e:
        print(f"Target unreachable[ConnectionError]({e})")
        return 500,None
    except requests.RequestException as e:
        print(f"Target unreachable[RequestException]({e.errno})")
        return 500,None
    except requests.HTTPError as e:
        print(f"Target unreachable[HTTPError]({e.errno})")
        return 500,None
    except Exception as e:
        print(f"Target unreachable({e})")
        return 500,None
    
        