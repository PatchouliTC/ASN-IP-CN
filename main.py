import os
import importlib
import inspect
from scripts.common import get_output_locate,set_singleline_output,set_multiline_output,pre_check,gen_data_storage_path,zip_dir
from scripts.enum import *

def run_all_processes(package_name, function_name):
    """
    导入指定包下所有模块，检查是否存在特定函数名，如果存在则依次执行。
    
    Args:
        package_name: 包的导入路径，例如 'scripts.asn'
        function_name: 要查找并执行的函数名，例如 'process'
    """
    # 获取包的物理路径
    try:
        package = importlib.import_module(package_name)
        package_path = Path(str(package.__path__._path[0]))
    except:
        print('Package not exist or unbale to import')
        return
    
    print(f"Checking {package_name} package modules...")
    exec_result=[]
    # 遍历包目录下的所有Python文件
    for filename in package_path.iterdir():
        if (not filename.is_file() or 
            not filename.suffix or 
            filename.suffix != '.py' or
            len(filename.suffixes)!=1 or
            filename.name.startswith('__')):
            continue
        module_name = f'{package_name}.{filename.stem}'         
        try:
            # 导入模块
            module = importlib.import_module(module_name)
            
            # 检查模块是否有指定函数名
            if hasattr(module, function_name):
                func = getattr(module, function_name)
                execute_result=False
                if callable(func):
                    print(f"exec {module_name}.{function_name}()...")
                    execute_result=func()
                    print(f"done {module_name}.{function_name}(),result={execute_result}")
                    exec_result.append({'module':module_name,'result':execute_result})
                    
                    
        except ImportError as e:
            print(f"Error happened when import {module_name}: {e}")
        except Exception as e:
            print(f"exec {module_name}.{function_name}() caused error: {e}")

def set_failure():
    set_singleline_output('generate_result','failure')

def set_success():
    set_singleline_output('generate_result','success')
    
def set_configuration_for_workflow():
    set_singleline_output('output_path',release_locate)
    set_singleline_output('release_file',FINAL_RELEASE_FILE_NAME)
    set_singleline_output('release_file_path',final_file) #include filename


if __name__ == "__main__":
    release_locate=CURRENT_ROOT_PATH
    final_file=release_locate.joinpath(FINAL_RELEASE_FILE_NAME)
    
    set_failure()
    set_configuration_for_workflow
    
    pre_check(final_file)
    pre_check(get_output_locate())
    
    run_all_processes('scripts.asn', 'process')
    
    zip_dir(final_file,get_output_locate(),comment=f'Generate At {LOCAL_TIME}')
    set_success()