import tkinter as tk

# 设置窗口及多个页面
root = tk.Tk()
root.title("人脸识别登录与注册页面")
root.geometry("800x600")
# 定义一个容器来包含所有用户及管理员登录相关的组件
login_frame = tk.Frame(root)
login_frame.pack(pady=100)
# 定义一个容器来包含所有用户注册相关的组件
register_frame = tk.Frame(root)
# 定义一个容器来包含所有用户主页面相关的组件
main_frame = tk.Frame(root)
# 定义一个容器来包含所有管理员主页面相关的组件
manager_frame = tk.Frame(root)
# 定义一个容器来包含所有管理员修改页面相关的组件
revise_frame = tk.Frame(root)
# 定义一个容器来包含所有管理员删除页面相关的组件
delete_frame = tk.Frame(root)


# 切换到注册视图的函数
def show_register_view():
    main_frame.pack_forget()
    login_frame.pack_forget()  # 隐藏登录相关组件
    register_frame.pack(pady=100)  # 显示注册相关组件


# 切换到登录视图的函数
def show_login_view():
    main_frame.pack_forget()
    register_frame.pack_forget()  # 隐藏注册相关组件
    manager_frame.pack_forget()
    login_frame.pack(pady=100)  # 显示登录相关组件


# 切换到用户主视图的函数
def show_main_view():
    login_frame.pack_forget()  # 隐藏登录相关组件
    main_frame.pack(pady=100)  # 显示登录相关组件


# 切换到管理员主视图的函数
def show_manager_view():
    login_frame.pack_forget()  # 隐藏登录相关组件
    revise_frame.pack_forget()
    delete_frame.pack_forget()
    manager_frame.pack(pady=100)  # 显示登录相关组件


# 切换到管理员修改视图的函数
def show_revise_view():
    manager_frame.pack_forget()  # 隐藏登录相关组件
    revise_frame.pack(pady=100)  # 显示登录相关组件


# 切换到管理员删除视图的函数
def show_delete_view():
    manager_frame.pack_forget()  # 隐藏登录相关组件
    delete_frame.pack(pady=100)  # 显示登录相关组件