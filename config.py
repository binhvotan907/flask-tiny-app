import os

class Config:
    """Cấu hình chung cho ứng dụng Flask."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')  # Khóa bí mật cho bảo mật session & forms
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Kết nối DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Tắt cảnh báo theo dõi thay đổi DB
    DEBUG = os.getenv('DEBUG', True)  # Bật/tắt chế độ debug dựa trên biến môi trường
