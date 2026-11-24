# POS Tagging tiếng Việt với PhoBERT
 
Dự án gán nhãn từ loại (Part-of-Speech tagging) cho tiếng Việt bằng **PhoBERT** đã fine-tune, hỗ trợ cả câu viết thông tục/không chuẩn. Có sẵn giao diện web (Gradio) để nhập câu và xem kết quả.
 
- **Model:** [`huycdt/phobert_pos5`](https://huggingface.co/huycdt/phobert_pos5) trên Hugging Face Hub (5 nhãn)
- **Demo:** `Src/demo.py` (Gradio, chạy ở cổng `7860`)
- **So sánh model:** PhoBERT so với XLM-R và mBERT, cùng cấu hình huấn luyện (xem `Notebooks/comparing_models.ipynb`)
---
 
## 1. Cấu trúc thư mục
 
```
Pos_tagging/
├── Notebooks/
│   ├── EDA_and_preprocessing.ipynb     # Khám phá và tiền xử lý dữ liệu
│   ├── fine-tuning model PhoBert.ipynb # Fine-tune PhoBERT (chạy trên Colab GPU)
│   └── comparing_models.ipynb          # So sánh PhoBERT, XLM-R, mBERT
├── Src/
│   └── demo.py                         # Ứng dụng Gradio
├── requirements.txt
└── README.md
```
 
> Thư mục `Data/` và `Model/` **không** được đưa lên GitHub vì quá nặng. Dữ liệu tải tại: `<DÁN LINK GOOGLE DRIVE / HUGGING FACE VÀO ĐÂY>`.
 
---
 
## 2. Cài đặt
 
Yêu cầu: **Python 3.10**.
 
```powershell
# 1. Tải code về
git clone https://github.com/<username>/<ten-repo>.git
cd <ten-repo>
 
# 2. Tạo và kích hoạt môi trường ảo
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
# source .venv/bin/activate     # macOS / Linux
 
# 3. Cài thư viện
pip install -r requirements.txt
```
 
Model sẽ **tự động tải** từ Hugging Face Hub (`huycdt/phobert_pos5`) ở lần chạy đầu tiên, không cần tải tay.
 
---
 
## 3. Cách dùng
 
### Cách A: Dùng thử qua link công khai (không cần cài gì)
 
Truy cập: **https://rearview-excretion-battery.ngrok-free.dev**
 
> Link này trỏ vào máy của tác giả nên **chỉ hoạt động khi máy tác giả đang bật và đang chạy server**. Lần đầu mở, ngrok có thể hiện trang cảnh báo, bấm **Visit Site** để vào.
 
### Cách B: Chạy trên máy của bạn (local)
 
```powershell
cd Src
python demo.py
```
 
Mở trình duyệt tại **http://127.0.0.1:7860**, nhập câu tiếng Việt và xem kết quả gán nhãn.
 
### Cách C: Biến máy của bạn thành server công khai bằng ngrok
 
Dùng khi bạn muốn người khác truy cập được ứng dụng đang chạy trên máy bạn qua một đường link.
 
> ⚠️ Domain ngrok của tác giả gắn với tài khoản của tác giả, **bạn không dùng lại được**. Bạn cần tài khoản ngrok và domain riêng (miễn phí).
 
**Bước 1: Tạo tài khoản và lấy thông tin ngrok**
 
1. Đăng ký tại https://ngrok.com (miễn phí).
2. Vào Dashboard → **Your Authtoken**, copy token.
3. Vào Dashboard → **Domains** → tạo một **free dev domain** (dạng `xxx.ngrok-free.dev`), copy lại tên domain.
**Bước 2: Cài ngrok**
 
- Windows: `winget install ngrok.ngrok` hoặc tải từ https://ngrok.com/download
- macOS: `brew install ngrok`
**Bước 3: Gắn token (chỉ làm một lần)**
 
```powershell
ngrok config add-authtoken <TOKEN_CỦA_BẠN>
```
 
**Bước 4: Chạy server (cần mở 2 cửa sổ terminal, để cả hai chạy song song)**
 
Terminal 1: chạy ứng dụng
 
```powershell
cd Src
python demo.py
```
 
Terminal 2: mở đường hầm ngrok
 
```powershell
ngrok http --url=<DOMAIN_CỦA_BẠN> 7860
```
 
Ví dụ: `ngrok http --url=ten-cua-ban.ngrok-free.dev 7860`
 
Sau đó chia sẻ link `https://<DOMAIN_CỦA_BẠN>` cho người khác.
 
**Lưu ý khi làm server bằng máy cá nhân**
 
- Máy phải **bật, có mạng** và **không sleep** thì link mới truy cập được. Tắt terminal nào thì dịch vụ dừng theo.
- Cả hai terminal phải chạy cùng lúc, nếu thiếu `demo.py` thì link sẽ báo lỗi, nếu thiếu `ngrok` thì chỉ truy cập được local.
- Cổng trong lệnh ngrok (`7860`) phải trùng cổng trong `demo.py`.
- Bản miễn phí của ngrok có giới hạn băng thông và hiện trang cảnh báo ở lần truy cập đầu.
---
 
## 4. Xử lý sự cố
 
| Lỗi | Cách xử lý |
|---|---|
| `ModuleNotFoundError` | Chưa kích hoạt `.venv` hoặc chưa chạy `pip install -r requirements.txt` |
| `Address already in use` / cổng 7860 bận | Tắt tiến trình đang dùng cổng 7860, hoặc đổi cổng trong `demo.py` và trong lệnh ngrok |
| `ERR_NGROK_4018` / lỗi authtoken | Chưa chạy `ngrok config add-authtoken ...` |
| `ERR_NGROK_8012` / không kết nối được | `demo.py` chưa chạy hoặc sai cổng |
| Link ngrok báo domain không tồn tại | Gõ sai tên domain, kiểm tra lại ở ngrok Dashboard → Domains |
| Tải model lỗi / chậm | Kiểm tra mạng, thử lại; model được cache lại sau lần tải đầu |
 
---
 
## 5. Huấn luyện lại (tùy chọn)
 
Notebook fine-tune được viết để chạy trên **Google Colab (GPU)**. Cấu hình dùng trong dự án:
 
| Tham số | Giá trị |
|---|---|
| Batch size | 32 |
| Learning rate | 1e-5 |
| Số epoch tối đa | 30 |
| Early stopping patience | 5 |
| Seed | 42 |
| Số nhãn | 5 |
 
---
 
## 6. Tác giả

**Đây là dự án nhóm thực hiện bởi nhóm sinh viên môn NLP tại UEH**
 