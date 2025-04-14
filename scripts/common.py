import requests
from lxml import etree
from datetime import datetime, timezone
import time
import os

def pre_check(file_name:str):
    directory = os.path.dirname(file_name)
    if directory:
        os.makedirs(directory, exist_ok=True)
    

def WriteHeader(file_name:str,file_type:str,write_at:datetime):
    with open(file_name, "w") as asnFile:
        asnFile.write(f"// {file_type} Information in China. (https://github.com/PatchouliTC/ASN-IP-CN) \n")
        asnFile.write(f"// Last Updated: {write_at} \n")
