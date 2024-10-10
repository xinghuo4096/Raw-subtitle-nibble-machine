# main.py
import importlib
import os
import sys

def load_config(config_path:str='my_zhipu_fy'):
    
    # 动态加载 config 模块
    # 显示当前工作目录
    current_directory = os.getcwd()
    print(f"当前工作目录: {current_directory}")

    # 检查当前目录的config文件夹是否存在
    config_path = os.path.join(current_directory, 'config')
    if os.path.exists(config_path):
        # 将config目录添加到模块搜索路径
        sys.path.append(config_path)
        print(f"'config'目录已添加到模块搜索路径：{config_path}")
    else:
        print(f"'config'目录不存在：{config_path}")

    config_module = importlib.import_module('my_zhipu_fy')

    # 访问配置信息
    model = config_module.config['model']
    system_content = config_module.config['system_content']
    top_p = config_module.config['top_p']
    temperature = config_module.config['temperature']
    max_tokens = config_module.config['max_tokens']

    # 打印配置信息
    print(f"Model: {model}")
    print(f"System Content (truncated): {system_content}")
    print(f"Top P: {top_p}")
    print(f"Temperature: {temperature}")
    print(f"Max Tokens: {max_tokens}")

if __name__ == "__main__":
    load_config()