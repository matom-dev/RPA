# Tra Cứu Phạt Nguội - CSGT

## Mô tả
Công cụ tự động tra cứu thông tin vi phạm giao thông trên trang web của Cục Cảnh sát giao thông Việt Nam.

## Website nguồn
[https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm](https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm)

## Tính năng chính
- Tra cứu bằng biển số xe và loại phương tiện
- Tự động giải mã captcha
- Lịch tra cứu tự động hàng ngày

## Cài đặt
1. Cài đặt [Python](https://www.python.org/downloads/) và [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

2. Cài đặt thư viện:
   ```
   pip install -r requirements.txt
   ```

3. Điều chỉnh đường dẫn Tesseract nếu cần:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

## Sử dụng
Chạy script và chương trình sẽ tự động tra cứu theo lịch (6h sáng và 12h trưa hằng ngày):
```
python tra_cuu_vi_pham.py
```

Để thay đổi lịch, chỉnh sửa các dòng:
```python
schedule.every().day.at("06:00").do(kiem_tra)
schedule.every().day.at("12:00").do(kiem_tra)
```