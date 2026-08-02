import tkinter as tk
from tkinter import ttk,PhotoImage
from main import detect_qrcode,resource_path

# 导入 tkinterdnd2 库

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    print("错误: 请先安装 'tkinterdnd2' 库。")
    print("你可以通过运行 'pip install tkinterdnd2' 来安装。")
    exit()


def drop(event):
    """
    当文件被拖放到窗口上时调用此函数。
    event.data 包含拖放的数据，通常是文件路径列表。
    """
    # 获取拖放的文件路径列表
    # event.data 是一个字符串，格式为 {file_path1} {file_path2} ...
    # 使用 str.split() 分割，并移除可能存在的花括号 {}
    paths = []
    # 直接按空格分割可能会出错，因为路径中可能包含空格
    # 更可靠的方法是使用正则表达式或手动解析
    # 但tkinterdnd2通常会用大括号包围带空格的路径，如 {C:/My Folder/file.txt}
    data_str = event.data
    # 简单处理：先去除首尾可能的空格
    data_str = data_str.strip()

    # 使用正则表达式解析路径
    # import re
    # 正则表达式匹配 {path} 或独立的 path (如果中间没有空格)
    # 这里假设路径中的空格都被大括号包围了
    # \{([^}]*)\}: 匹配 { } 内的内容
    # |: 或者
    # ([^"\s]+): 匹配不带引号且不含空格的连续字符
    # 注意：这个简单的正则可能无法完美处理所有边缘情况，但对大多数常见路径有效
    # 更严谨地解析可以参考 shlex.split
    import shlex

    try:
        # 使用 shlex.split 解析被引号或大括号包围的路径
        file_paths = shlex.split(data_str)
        for path in file_paths:
            if path:  # 确保路径不为空
                paths.append(path)
    except ValueError as e:
        # 如果 shlex.split 失败，回退到简单的大括号处理
        print(f"shlex.split 处理失败: {e}")
        # 手动解析：查找 { 和 } 并提取路径
        start = 0
        while start < len(data_str):
            if data_str[start] == '{':
                end = data_str.find('}', start)
                if end != -1:
                    path = data_str[start + 1:end]
                    paths.append(path)
                    start = end + 1
                else:
                    # 格式错误，找不到对应的 }
                    break
            elif data_str[start] != ' ':  # 跳过空格
                # 可能是一个没有空格的路径（不太可能，但以防万一）
                # 从当前位置开始找下一个空格或结束符
                end_space = data_str.find(' ', start)
                if end_space == -1:
                    end_space = len(data_str)
                path = data_str[start:end_space]
                if path and not path.startswith('{'):
                    paths.append(path)
                    start = end_space
                else:
                    # 如果以 { 开头，说明上面的逻辑应该已经处理了
                    start += 1
            else:
                start += 1

    # 清空之前的文本内容
    text_widget.delete(1.0, tk.END)

    if paths:
        for path in paths:
            # 获取文件名（从路径中提取最后一部分）
            import os
            filename = os.path.basename(path)

            # 将路径和文件名打印到 Text 控件中
            # text_widget.insert(tk.END, f"文件名: {filename}\n")
            # text_widget.insert(tk.END, f"完整路径: {path}\n")
            # text_widget.insert(tk.END, "-" * 40 + "\n")  # 添加分隔线
            print(f"文件名: {filename}")
            print(f"完整路径: {path}")
            print("-" * 40)

            # image_path = "1.webp"  # 替换为你的图片路径
            qrcodes = detect_qrcode(path)

            if qrcodes:
                for i, content in enumerate(qrcodes, 1):
                    text_widget.insert(tk.END, "识别到的二维码内容："+content + "\n")  # 添加分隔线
            else:
                print("未识别到二维码")
                text_widget.insert(tk.END, "未识别到二维码" + "\n")  # 添加分隔线
    else:
        text_widget.insert(tk.END, "未检测到有效的文件路径。\n")
        print("未检测到有效的文件路径。")


# 创建主窗口，并应用 TkinterDnD
root = TkinterDnD.Tk()
root.title("简易二维码识别工具")
root.geometry("600x200")

# 创建一个标签提示用户操作
label = ttk.Label(root, text="请将文件拖拽到此窗口", font=("Arial", 14))
label.pack(pady=20)

# 创建一个 Text 控件用于显示拖放的文件信息
text_widget = tk.Text(root, wrap=tk.WORD, height=15, width=70)
text_widget.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)


# 注册窗口为拖放目标，接受文件类型
root.drop_target_register(DND_FILES)
# 绑定拖放事件到 drop 函数
root.dnd_bind('<<Drop>>', drop)
root.resizable(width=False, height=False)
root.iconbitmap(resource_path('main2.ico'))  # False表示默认大小，也可以传入True来指定图标用于高DPI显示
# 启动 GUI 主循环
root.mainloop()
