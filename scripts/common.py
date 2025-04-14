import requests
from lxml import etree
from datetime import datetime, timezone
import time
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
            zip.comment = comment
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
    with open(file_name, "w") as asnFile:
        asnFile.write(f"// {file_type} Information in China. (https://github.com/PatchouliTC/ASN-IP-CN) \n")
        asnFile.write(f"// Last Updated: {write_at} \n")
