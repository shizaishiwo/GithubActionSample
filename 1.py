import os
import shutil
from tkinter import Tk, Label, Entry, Button, filedialog

# 创建主窗口
root = Tk()
root.title("文件夹移动")

# 创建标签和输入框
Label(root, text="原始文件夹路径：").pack()
initial_dir_entry = Entry(root, width=50)
initial_dir_entry.pack()

Label(root, text="目标文件夹路径：").pack()
destination_dir_entry = Entry(root, width=50)
destination_dir_entry.pack()

# 定义浏览文件夹的函数
def browse_directory():
    path = filedialog.askdirectory(title='选择原始文件夹路径')
    initial_dir_entry.delete(0, 'end')
    initial_dir_entry.insert(0, path)

def browse_destination():
    path = filedialog.askdirectory(title='选择目标文件夹路径')
    destination_dir_entry.delete(0, 'end')
    destination_dir_entry.insert(0, path)

# 定义移动文件和文件夹的函数
def move_items(src_path, dest_path):
    
    for item in os.listdir(src_path):
        item_src = os.path.join(src_path, item)
        item_dest = os.path.join(dest_path, item)
        try:
            shutil.move(item_src, dest_path)
        except Exception as e:
            pass
    status_label.config(text="文件和文件夹移动完成！", fg="green")


# 创建状态标签
status_label = Label(root, text="", fg="black")
status_label.pack()

# 创建移动文件按钮
move_button = Button(root, text="移动文件和文件夹", command=lambda: move_items(initial_dir_entry.get(), destination_dir_entry.get()))
move_button.pack()

# 运行主循环
root.mainloop()
