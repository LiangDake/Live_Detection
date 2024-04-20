import os
import psycopg2
from tkinter import messagebox
from psycopg2 import sql, errors

from DB_Connect import connect_db
from Face_Capture import capture_and_save_face, capture
from Jump_View import *


# 点击新用户注册按钮后
def on_register_button_clicked(name, username, password):
    folder_path = "/Users/liangdake/Library/Mobile Documents/com~apple~CloudDocs/留学/毕设/Known_Faces"
    status = capture_and_save_face(folder_path, name)
    if status is not True:
        messagebox.showerror("注册失败", f"用户{status}已存在")
    else:
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute(sql.SQL("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)"),
                        (name, username, password))
            conn.commit()
            messagebox.showinfo("注册成功", "您已成功注册！")
        except psycopg2.errors.UniqueViolation:
            messagebox.showerror("注册失败", f"用户{username}已存在")
            conn.rollback()
        finally:
            cur.close()
            conn.close()


# 点击用户登录按钮后
def on_login_button_clicked(username, password):
    name = user_info_verify(username, password)
    if name is not False:
        show_main_view()
    else:
        show_login_view()


# 点击用户登录按钮后，users数据库验证账号密码
def user_info_verify(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    # 若账号密码正确，在用户人脸文件夹中进行人脸对比
    if result and result[0] == password:
        folder_path = "/Users/liangdake/Library/Mobile Documents/com~apple~CloudDocs/留学/毕设/Known_Faces"
        capture(folder_path)
    else:
        messagebox.showerror("登录失败", "用户名或密码错误")
        return False


# 点击管理员登录按钮后
def on_manager_login_button_clicked(username, password):
    name = manager_info_verify(username, password)
    if name is not False:
        show_manager_view()
    else:
        show_login_view()


# 点击管理员登录按钮后，managers数据库验证账号密码
def manager_info_verify(username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT password FROM managers WHERE username = %s", (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    # 若账号密码正确，在管理员人脸文件夹中进行人脸对比
    if result and result[0] == password:
        folder_path = "/Users/liangdake/Library/Mobile Documents/com~apple~CloudDocs/留学/毕设/Maneger_Known_Faces"
        capture(folder_path)
    else:
        messagebox.showerror("登录失败", "用户名或密码错误")
        return False


# 点击删除按钮后
def on_delete_button_clicked(username):
    conn = connect_db()
    cur = conn.cursor()
    try:
        # 执行删除用户的SQL命令
        cur.execute("SELECT name FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        cur.execute(sql.SQL("DELETE FROM users WHERE username = %s"), (username,))

        # 检查是否有行被删除
        if cur.rowcount == 0:
            messagebox.showwarning("删除失败", f"未找到用户名为{username}的用户。")
        else:
            conn.commit()  # 提交更改
            # 设置图片的完整路径
            photo_path = f'/Users/liangdake/Library/Mobile Documents/com~apple~CloudDocs/留学/毕设/Known_Faces/{result[0]}.jpg'
            # 检查文件是否存在
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)  # 删除文件
                    messagebox.showinfo("删除成功", f"用户{username}已被成功删除。")
                except OSError as e:
                    messagebox.showinfo("删除照片时出错", f"{str(e)}")
            else:
                messagebox.showinfo("删除失败", "未找到该照片")
    except Exception as e:
        messagebox.showerror("操作错误", f"在删除用户时发生错误: {str(e)}")
        conn.rollback()  # 出错时回滚
    finally:
        cur.close()
        conn.close()


# 点击更新按钮后
def on_update_button_clicked(username, new_name):
    conn = connect_db()
    cur = conn.cursor()
    try:
        # 执行更新用户信息的SQL命令
        cur.execute(sql.SQL("UPDATE users SET username = %s WHERE username = %s"),
                    (new_name, username))

        # 检查是否有行被更新
        if cur.rowcount == 0:
            messagebox.showwarning("更新失败", f"未找到用户名为{username}的用户。")
        else:
            conn.commit()  # 提交更改
            messagebox.showinfo("更新成功", f"用户{username}的信息已被成功更新。")
    except Exception as e:
        messagebox.showerror("操作错误", f"在更新用户信息时发生错误: {str(e)}")
        conn.rollback()  # 出错时回滚
    finally:
        cur.close()
        conn.close()