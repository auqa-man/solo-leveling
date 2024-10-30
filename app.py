import streamlit as st
import sqlite3

# 初始化資料庫
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    conn.close()

# 註冊用戶
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# 登入檢查
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    conn.close()
    return user

# 初始化資料庫
init_db()

# 定義頁面路徑
page = st.sidebar.selectbox("選擇頁面", ["登入", "註冊"])

# 登入頁面
if page == "登入":
    st.title('登入')

    login_username = st.text_input('用戶名', key='login_username')
    login_password = st.text_input('密碼', type='password', key='login_password')

    # 登入按鈕
    if st.button('登入'):
        user = login_user(login_username, login_password)
        if user:
            st.success(f"歡迎, {login_username}！")
        else:
            st.error('無效的用戶名或密碼')

    # 在登入按鈕旁加上 "還沒註冊嗎?" 的連結
    if st.write("還沒註冊嗎? [點此註冊](#)"):
        st.session_state.page = "註冊"

# 註冊頁面
elif page == "註冊":
    st.title('註冊')

    register_username = st.text_input('用戶名', key='register_username')
    register_password = st.text_input('密碼', type='password', key='register_password')

    # 註冊按鈕
    if st.button('注册'):
        if register_username and register_password:
            register_user(register_username, register_password)
            st.success(f"用户 {register_username} 注册成功！请前往登录。")
            st.session_state.page = "登入"  # 注册成功后自动跳转到登录页面
        else:
            st.error('请输入有效的用户名和密码')

    if st.write("已經有帳戶了? [點此登入](#)"):
        st.session_state.page = "登入"
