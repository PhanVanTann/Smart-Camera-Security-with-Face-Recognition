# Smart-Camera-Security-with-Face-Recognition
# Cấu Trúc Thư Mục
- Thư mục app : chứ toàn bộ logic của ứng dụng, trong thư mục app chứa các thư mục con như: 
Api: đây là nơi chứa các "Routes" hoặc "Endpoints". Đây là nơi định nghĩa các đường dẫn và điều hướng yêu cầu từ người dùng ( cái này sẽ phát triển trong tương lai )
Core : Chứa các cấu hình cốt lõi của dự án như kết nối Database, cài đặt bảo mật (Security), hoặc file config.py để đọc biến môi trường.
ModelAI : Đây là fodel chứa các model Al như detection, segmenttion….. và các logic liên quan đến AI.
Schemas : Nơi định nghĩa các khuôn mẫu dữ liệu để kiểm tra dữ liệu đầu vào (Request) và định dạng dữ liệu trả về (Response).
Services : Chứa "Logic nghiệp vụ" (Business Logic).
UI : chứa các file giao diện của ứng dụng.
Upload : Thư mục lưu trữ tạm các file người dùng tải lên (ảnh, tài liệu) trong quá trình xử lý.
Utils : Các tiện ích bổ trợ. Chứa các hàm nhỏ dùng chung ở nhiều nơi 
Main.py : File quan trọng nhất. Đây là điểm khởi chạy của ứng dụng.
Tesst.py : File dùng để test chức năng của ứng dụng.

- Thư mục Dataset : Thư mục chứa dữ liệu Thô, thường dùng để huấn luyện và Đánh Giá Model AI.
- Thư Mục Scripts : Chứa các đoạn mã kịch bản chạy độc lập. Dùng để viết các hàm đánh giá model.
- Thư Mục venv : Viết tắt của Virtual Environment (Môi trường ảo). Nơi chứa các thư viện Python được cài đặt riêng cho dự án này để không xung đột với các dự án khác.
- File .env : File chứa Biến môi trường. Đây là nơi lưu các thông tin nhạy cảm như mật khẩu Database, API Key, Secret Key. File này không bao giờ được đưa lên Git.
- File .gitignore : File cấu hình cho Git, liệt kê những file/thư mục mà Git sẽ bỏ qua 
- File README.md : File văn bản hướng dẫn. Dùng để viết mô tả dự án, cách cài đặt và cách chạy ứng dụng.
- File requirements.txt : Danh sách các thư viện cần thiết. Người khác muốn chạy dự án này sẽ dùng file này để cài đặt thư viện (pip install -r requirements.txt).
# Hứong dẫn cài đặt và chạy app.
- cài các thư viện cần thiết bằng cách gõ pip install -r requirements.txt
- sau đó cài đặt venv : python -m venv venv
- chạy venv : source venv/bin/activate (mac), venv\Scripts\activate (window)
- chạy dự án : python app/main.py