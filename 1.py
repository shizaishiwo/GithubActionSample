#!/usr/bin/env python
# coding: utf-8

# In[3]:


"""
文件夹移动
"""

import os
import os
import shutil
# 指定文件夹路径
path = input('请输入原始路径（包括10000文件夹的大路径）')
destination_path = input('请输入目标文件夹路径')
# 获取指定路径下所有文件和文件夹
contents = os.listdir(path)

# 仅保留文件夹路径
folders = [os.path.join(path, item) for item in contents if os.path.isdir(os.path.join(path, item)) ]

# 遍历每个文件夹
biaoge = []
for folder in folders:
    for file in os.listdir(folder):
        #if file.endswith('.xlsx'):
            biaoge.append(os.path.join(folder, file))

print(biaoge)


if not os.path.exists(destination_path):
    os.makedirs(destination_path)
# 遍历每个文件路径
for file_path in biaoge:
    # 提取文件名
    file_name = os.path.basename(file_path)
    
    # 构建目标文件路径
    destination_file_path = os.path.join(destination_path, file_name)
    try:
        # 移动文件
        shutil.move(file_path, destination_file_path)
    except:
        pass

print("文件移动完成！")

