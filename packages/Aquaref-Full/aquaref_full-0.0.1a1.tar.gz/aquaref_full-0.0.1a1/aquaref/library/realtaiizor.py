import os
dir = os.path.abspath(os.path.dirname(__file__))

dir_realtaiizor = os.path.join(dir, "realtaiizor")
dir_realtaiizor_net60 = os.path.join(dir_realtaiizor, "net60-windows7")

libs = {}

if os.path.exists(dir_realtaiizor_net60):
    for lib in os.listdir(dir_realtaiizor_net60):
        path = os.path.join(dir_realtaiizor_net60, lib)
        if os.path.isfile(path):
            if os.path.splitext(path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                libs[lib] = path

from flaterlog import Debug
Debug(f"ReaLTaiizor Library Files {libs}")