from Button_Action import *
from Jump_View import *


def setup_gui():
    # 登录页面
    # 创建标签和输入框用于用户名
    username_label = tk.Label(login_frame, text="账号:")
    username_label.pack(pady=(10, 10))
    username_entry = tk.Entry(login_frame, width=30)
    username_entry.pack()

    # 创建标签和输入框用于密码
    password_label = tk.Label(login_frame, text="密码:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(login_frame, width=30, show="*")
    password_entry.pack()

    # 登录按钮在登录视图中
    login_button = tk.Button(login_frame, text="登录并验证人脸",
                             command=lambda: on_login_button_clicked(username_entry.get(), password_entry.get()))
    login_button.pack(pady=20)

    # 注册按钮在登录视图中
    switch_to_register_button = tk.Button(login_frame, text="注册新用户", command=show_register_view)
    switch_to_register_button.pack(pady=10)

    # 管理员登录按钮在登录视图中
    switch_to_register_button = tk.Button(login_frame, text="管理员登录", command=lambda: on_manager_login_button_clicked(username_entry.get(), password_entry.get()))
    switch_to_register_button.pack(pady=10)

    # 注册页面
    # 输入框和标签用于注册新用户
    new_name_label = tk.Label(register_frame, text="姓名:")
    new_name_label.pack(pady=(20, 10))
    new_name_entry = tk.Entry(register_frame, width=30)
    new_name_entry.pack()

    new_username_label = tk.Label(register_frame, text="账号:")
    new_username_label.pack(pady=(20, 10))
    new_username_entry = tk.Entry(register_frame, width=30)
    new_username_entry.pack()

    new_password_label = tk.Label(register_frame, text="密码:")
    new_password_label.pack(pady=10)
    new_password_entry = tk.Entry(register_frame, width=30)
    new_password_entry.pack()

    # 注册和返回登录的按钮在注册视图中
    confirm_register_button = tk.Button(
        register_frame,
        text="确认注册并存入人脸",
        command=lambda: on_register_button_clicked(new_name_entry.get(), new_username_entry.get(), new_password_entry.get())
    )
    confirm_register_button.pack(pady=20)

    return_to_login_button = tk.Button(register_frame, text="返回登录", command=show_login_view)
    return_to_login_button.pack(pady=10)

    # 已登录用户主页面
    # 在主视图中显示用户信息
    tk.Label(main_frame, text=f"您好！{username_entry.get()}").pack(pady=20)

    # 退出登录按钮在主视图中
    switch_to_login_button = tk.Button(main_frame, text="退出登录", command=show_login_view)
    switch_to_login_button.pack(pady=20)

    # 注册新用户按钮在主视图中
    switch_to_register_button = tk.Button(main_frame, text="注册新用户", command=show_register_view)
    switch_to_register_button.pack(pady=10)

    # 管理员用户主页面
    # 在主视图中显示用户信息
    tk.Label(manager_frame, text=f"您好！{username_entry.get()} 欢迎来到管理员页面").pack(pady=20)

    # 修改按钮在主视图中
    update_button = tk.Button(manager_frame, text="修改用户信息", command=show_revise_view)
    update_button.pack(pady=20)

    # 删除按钮在主视图中
    delete_button = tk.Button(manager_frame, text="删除用户信息", command=show_delete_view)
    delete_button.pack(pady=20)

    # 退出登录按钮在主视图中
    switch_to_login_button = tk.Button(manager_frame, text="退出登录", command=show_login_view)
    switch_to_login_button.pack(pady=20)

    # 删除页面
    # 创建标签和输入框用于用户名
    delete_username_label = tk.Label(delete_frame, text="需要删除的账号:")
    delete_username_label.pack(pady=(10, 10))
    delete_username_entry = tk.Entry(delete_frame, width=30)
    delete_username_entry.pack()

    # 删除按钮
    delete_button = tk.Button(
        delete_frame,
        text="确认删除",
        command=lambda: on_delete_button_clicked(delete_username_entry.get())
    )
    delete_button.pack(pady=20)

    # 返回管理员界面按钮在删除视图中
    switch_to_manager_button = tk.Button(delete_frame, text="返回主页面", command=show_manager_view)
    switch_to_manager_button.pack(pady=10)

    # 修改页面
    # 创建标签和输入框用于用户名
    update_username_label = tk.Label(revise_frame, text="需要修改的账号:")
    update_username_label.pack(pady=(10, 10))
    update_username_entry = tk.Entry(revise_frame, width=30)
    update_username_entry.pack()

    update1_username_label = tk.Label(revise_frame, text="修改后的账号:")
    update1_username_label.pack(pady=(10, 10))
    update1_username_entry = tk.Entry(revise_frame, width=30)
    update1_username_entry.pack()

    # 修改按钮
    update_button = tk.Button(
        revise_frame,
        text="确认修改",
        command=lambda: on_update_button_clicked(update_username_entry.get(), update1_username_entry.get())
    )
    update_button.pack(pady=20)

    # 返回管理员界面按钮在删除视图中
    switch_to_manager_button = tk.Button(revise_frame, text="返回主页面", command=show_manager_view)
    switch_to_manager_button.pack(pady=10)
    return root


# 启动GUI
if __name__ == "__main__":
    root = setup_gui()
    root.mainloop()