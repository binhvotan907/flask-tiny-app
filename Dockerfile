# Sử dụng image Python
FROM python:3.9

# Đặt thư mục làm việc bên trong container
WORKDIR /app

# Copy toàn bộ project vào container
COPY . /app

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Expose cổng 5000 để chạy Flask
EXPOSE 5000

# Chạy ứng dụng Flask
CMD ["python", "app.py"]
