import requests
from lxml import etree
from datetime import datetime, timezone
import time
import os
import uuid
from scripts.enum import *



def get_output_locate()->str:
    return os.path.join(CURRENT_ROOT_PATH,OUTPUT_DIR_NAME)

def set_singleline_output(name:str,value:str)->None:
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
        
def gen_data_storage_path(file_name:str)->str:
    return os.path.join(CURRENT_ROOT_PATH,OUTPUT_DIR_NAME,file_name)

def pre_check(file_name:str):
    directory = os.path.dirname(file_name)
    if directory:
        os.makedirs(directory, exist_ok=True)
    

def WriteHeader(file_name:str,file_type:str,write_at:datetime):
    with open(file_name, "w") as asnFile:
        asnFile.write(f"// {file_type} Information in China. (https://github.com/PatchouliTC/ASN-IP-CN) \n")
        asnFile.write(f"// Last Updated: {write_at} \n")
