#!/usr/bin/python3
# -*- coding: UTF-8 -*-
 
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
 
window = tk.Tk()
window.title("窗口缩放")
 
#设置窗口大小，并将窗口放置在屏幕中央
width = 400
height = 400
g_screenwidth = window.winfo_screenwidth()
g_screenheight = window.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (g_screenwidth-width)/2, (g_screenheight-height)/2)
window.geometry(alignstr)
 
#设置窗口背景为白色
window.config(bg='white')
#设置窗口最小尺寸
window.minsize(width, height)
 
#采用frame上添加Text方式，可根据窗口进行像素级缩放
scrollable_frame = tk.Frame(window, width=360, height=340)
scrollable_frame.pack_propagate(0)
scrollable_frame.place(x=20, y=10)
 
#Text内部支持复制，粘贴
menubar = tk.Menu(window, tearoff=False)
 
def cut(editor, event=None):
	editor.event_generate("<<Cut>>")
def copy(editor, event=None):
	editor.event_generate("<<Copy>>")
def paste(editor, event=None):
	editor.event_generate('<<Paste>>')
def rightKey(event, editor):
	menubar.delete(0, 'end')
	menubar.add_command(label='剪切',command=lambda:cut(editor))
	menubar.add_command(label='复制',command=lambda:copy(editor))
	menubar.add_command(label='粘贴',command=lambda:paste(editor))
	menubar.post(event.x_root,event.y_root)

 
save_width = width
save_height = height
 
#窗口尺寸调整处理函数
def WindowResize(event):
	global save_width
	global save_height
	
	new_width = window.winfo_width()
	new_height = window.winfo_height()
	
	if new_width == 1 and new_height == 1:
		return
	if save_width != new_width or save_height != new_height:
		scrollable_frame.config(width=new_width-40, height=new_height-60)
	save_width = new_width
	save_height = new_height
 
#绑定窗口变动事件
window.bind('<Configure>', WindowResize)


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
 
    filename = filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
 
    if filename:
        global_selectFilePath = filename
        print(f"选择的文件path是：{global_selectFilePath}")
        file_path_label.config(text=filename)
    

global_selectFilePath = "D:/workspace/mirror1/xiaomi.log"
selectBugType = 'no type'
selectAdditiontags = []


select_type_lable = tk.Label(scrollable_frame, text='选择要分析的Bug类型', anchor='w', width=30,bg='yellow')
select_type_lable.pack(side='top',fill='x')

# 创建下拉列表
combo = ttk.Combobox(scrollable_frame, width=20)
combo.pack(anchor='nw')

def selected_item(event):
    selectBugType = combo.get()
   
    print(f"选择的bug分析类型为: {selectBugType}")

 
# 设置下拉列表的内容
combo['values'] = ('连接异常断开', '回连失败', '消息发送失败', '设备未正确上报')
 
# 设置下拉列表默认选中的项
combo.current(0)
 
# 绑定事件，当选中项变更时触发
combo.bind("<<ComboboxSelected>>", selected_item)


select_button = tk.Button(scrollable_frame, text='选择要分析的文件', command=select_file)
select_button.pack(anchor='nw')
 
file_path_label = tk.Label(scrollable_frame, text='已选择的文件路径：None', anchor='w', width=30)
file_path_label.pack(anchor='nw')


# 创建一个标签用于显示提示信息
label = tk.Label(scrollable_frame, text="请输入需要补充的tag或info:")
label.pack(anchor='nw')
 
# 创建一个输入框
entry = tk.Entry(scrollable_frame)
entry.pack(side='top',fill='x')
 
# 创建一个按钮，点击后获取输入框的内容
def print_entry():
    print(entry.get())
    
button = tk.Button(scrollable_frame, text="获取输入", command=print_entry)
button.pack(side='top',fill='x')


def filter_lines_with_keywords(file_path, keywords):
    """
    过滤文件中包含指定关键词的行。
    
    参数:
    file_path: 文件路径
    keywords: 关键词列表
    
    返回:
    包含匹配行的列表。
    """
    filtered_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for keyword in keywords:
                if keyword in line:
                    filtered_lines.append(line)
                    break
    return filtered_lines


def on_button_click():
    keywords = ['ChannelProcessor', 'fail']  # 关键词列表
    filtered_lines = filter_lines_with_keywords(global_selectFilePath, keywords)
    code = ''
    global_filtered_code_text = ''
    for line in filtered_lines:
        code += line.strip()
        code += '\n'
        print(line.strip())  # 打印过滤后的行，去除两端空白字符
    global_filtered_code_text = code
    filter_code_Text.insert("end",global_filtered_code_text)
button = tk.Button(scrollable_frame, text="开始分析", command=on_button_click)
button.pack(anchor='n')


# 创建一个标签用于显示提示信息
filter_code_lable = tk.Label(scrollable_frame, text="以下为过滤的相关信息:")
filter_code_lable.pack(anchor='nw')
# 过滤相关代码展示区

global_filtered_code_text = "暂无分析结果"


# 创建垂直滚动条
vbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)
# 设置Text高度为10行
filter_code_Text = tk.Text(scrollable_frame, yscrollcommand=vbar.set)

# 将Text组件放置到窗口中
filter_code_Text.pack(fill="both",expand=True)

vbar.config(command=filter_code_Text.yview)
filter_code_Text.insert("end", global_filtered_code_text)
print(f"wiess = {filter_code_Text.winfo_width()}")


 
window.mainloop()