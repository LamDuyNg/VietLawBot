# Hướng dẫn chạy dự án

## Chuẩn bị môi trường
* Code được viết và chạy trên **Kaggle Notebook** (`backend.ipynb`).
* Yêu cầu GPU để chạy mô hình.
* Trong trường hợp cần thiết, hãy thay `GEMINI_API_KEY` bằng API key của bạn.

## Import dữ liệu
Trước khi chạy, cần upload dữ liệu lên Kaggle bằng cách tạo **New Dataset**:
1. `\data\embedded_file\precedent_embeddings.jsonl` → dataset đặt tên **precedent-embedding**
2. `\data\embedded_file\law_embeddings.jsonl` → dataset đặt tên **law-embedding**
3. `\data\chunk_file\summary_an_le.jsonl` → dataset đặt tên **summary-an-le**
4. Các file data sẽ khá lớn nên hãy tải từ đường link GG sau: https://drive.google.com/drive/folders/1lrLXz2VpPlZY798qNYup70Dwt4BLuGa5?usp=drive_link

## Chạy backend
1. Mở và chạy toàn bộ cell trong file **`backend.ipynb`**.
2. Sau khi kích hoạt thành công, ở **cell cuối** sẽ xuất hiện một đường dẫn **Ngrok**.

## Kết nối giao diện (UI)
1. Lấy đường dẫn Ngrok trên và thay vào biến `api_url` trong file **`ui.py`**
   > Lưu ý: chỉ thay phần trước `/chat`.
2. Mở CMD (hoặc terminal) tại thư mục chứa `ui.py`, chạy lệnh:
   ```bash
   streamlit run ui.py
   ```
3. Giao diện web sẽ tự động mở trong trình duyệt.
## Lưu ý khi sử dụng
* Thời gian xử lý trung bình cho một câu hỏi khoảng **60-120 giây**.
* Hãy kiểm tra lại kết nối mạng nếu UI không nhận được phản hồi.
