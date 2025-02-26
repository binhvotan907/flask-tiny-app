from flask import current_app
from flask_login import current_user
from functools import wraps

# Hàm kiểm tra quyền truy cập
def admin_required(f):
    """
    Decorator để kiểm tra người dùng có phải là admin hay không.
    Nếu không phải admin, chuyển hướng về trang chủ.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return current_app.login_manager.unauthorized()
        return f(*args, **kwargs)
    return decorated_function


# Hàm định dạng ngày tháng
def format_date(date, format='%Y-%m-%d %H:%M:%S'):
    """
    Định dạng đối tượng datetime thành chuỗi.
    """
    return date.strftime(format)


# Hàm kiểm tra định dạng email
def is_valid_email(email):
    """
    Kiểm tra xem một chuỗi có phải là email hợp lệ hay không.
    """
    import re
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


# Hàm tạo mật khẩu ngẫu nhiên
def generate_random_password(length=8):
    """
    Tạo mật khẩu ngẫu nhiên với độ dài cho trước.
    """
    import random
    import string
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


# Hàm gửi email
def send_email(subject, recipients, body):
    """
    Gửi email đến một hoặc nhiều người nhận.
    """
    from flask_mail import Message
    from app import mail

    msg = Message(subject, recipients=recipients)
    msg.body = body
    mail.send(msg)


# Hàm xử lý tệp tin tải lên
def save_uploaded_file(file, folder='uploads'):
    """
    Lưu tệp tin tải lên vào thư mục chỉ định.
    Trả về đường dẫn tệp tin.
    """
    import os
    from werkzeug.utils import secure_filename

    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = secure_filename(file.filename)
    file_path = os.path.join(folder, filename)
    file.save(file_path)
    return file_path