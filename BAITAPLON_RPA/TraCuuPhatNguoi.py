from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from PIL import Image
import pytesseract, time, schedule, os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def tra_cuu_phat_nguoi(bien_so, loai_xe):
    # 1. Vào website đã chọn.
    url = "https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html"
    options = Options()
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        # 2. Nhập các thông tin Biển số xe, chọn loại phương tiện. 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "BienKiemSoat"))).send_keys(bien_so)

        select = Select(driver.find_element(By.NAME, "LoaiXe"))
        loai_xe = loai_xe.lower().strip()
        if loai_xe == "ô tô":
            select.select_by_value("1")
        elif loai_xe == "xe máy":
            select.select_by_value("2")
        elif loai_xe == "xe đạp điện":
            select.select_by_value("3")
        else:
            print(" Loại xe không hợp lệ.")
            return

        while True:
            try:
                # 3. Trích xuất mã bảo mật bằng thư viện pytesseract hoặc thư viện nào đó ra dạng text rồi nhập tự động vào ô Input, bấm tìm kiếm.
                captcha_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'captcha')]"))
                )

                captcha_path = "captcha.png"
                captcha_element.screenshot(captcha_path)

                img = Image.open(captcha_path).convert("RGB")

                img = img.convert("L")
                img = img.point(lambda x: 0 if x < 140 else 255, '1')

                img.save("processed_captcha.png")
                
                captcha_text = pytesseract.image_to_string(img, config='--psm 8').strip()
                captcha_text = ''.join(filter(str.isalnum, captcha_text))

                print(f" Captcha đọc được: {captcha_text}")

                captcha_input = driver.find_element(By.NAME, "txt_captcha")
                captcha_input.send_keys(captcha_text)

                driver.find_element(By.CLASS_NAME, "btnTraCuu").click()

                time.sleep(2)

                try:
                    error_element = driver.find_element(By.CLASS_NAME, "xe_texterror")
                    if "Mã xác nhận sai" in error_element.text:
                        print(" Captcha sai, thử lại...")
                        continue
                except:
                    pass

                # 4. Kiểm tra kết quả phạt nguội.
                ket_qua = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "bodyPrint123"))
                ).text.strip()

                if "Không tìm thấy kết quả" in ket_qua:
                    print("Không có vi phạm.")
                else:
                    print("Lỗi vi phạm:")
                    print(ket_qua)

                break
                

            except Exception as e:
                print(" Lỗi khi xử lý captcha:", str(e))
                continue

    except Exception as e:
        print(" Lỗi tổng quát:", str(e))

    finally:
        if os.path.exists("captcha.png"):
            os.remove("captcha.png")
        driver.quit()


def thuc_hien_tra_cuu():
    print("\n Tra Cứu Phạt Nguội")
    bien_so = input(" Nhập biển số xe: ")
    loai_xe = input(" Nhập loại xe (ô tô / xe máy / xe đạp điện): ")

    tra_cuu_phat_nguoi(bien_so, loai_xe)
    print("Hoàn thành tra cứu")


# 5. Set lịch chạy 6h sáng và 12h trưa hằng ngày.
schedule.every().day.at("06:00").do(thuc_hien_tra_cuu)
schedule.every().day.at("12:00").do(thuc_hien_tra_cuu)

print(" Đợi đến giờ tra cứu")
while True:
    schedule.run_pending()
    time.sleep(1)