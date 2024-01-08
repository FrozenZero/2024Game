"""
@Author  ：段龙
@Date    ：2024/1/6 15:14 
打压缩包
"""

import zipfile
import os
def zip_files(folder_path,zip_file_path='files/article.zip',suffix='pdf'):
    # 创建一个ZIP文件对象
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历文件夹中的所有文件
        for root, _, files in os.walk(folder_path):
            for file in files:
                # 检查文件扩展名是否为.pdf
                if file.lower().endswith(suffix):
                    # 获取文件的完整路径
                    full_path = os.path.join(root, file)
                    # 将文件添加到ZIP文件中
                    zipf.write(full_path, os.path.relpath(full_path, folder_path))
                    os.remove(full_path)

# zip_files("./",suffix='.py')