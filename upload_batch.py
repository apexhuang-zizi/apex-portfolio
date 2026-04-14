# -*- coding: utf-8 -*-
import urllib.parse, webbrowser, time

def upload(date, topic, lines):
    # 只上传越南语，让页面的 translateAndSave 自动添加中文翻译
    formatted = []
    for speaker, vi in lines:
        formatted.append(f"{speaker}: {vi}")
    content = "\n".join(formatted)
    url = f"https://apexhuang-zizi.github.io/apex-portfolio/vietnamese.html?date={urllib.parse.quote(date)}&topic={urllib.parse.quote(topic)}&content={urllib.parse.quote(content)}"
    print(f"\n📅 {date} | {topic} | {len(lines)}句")
    for s, vi in lines:
        print(f"  {s}: {vi}")
    print(f"  URL: {len(url)}字符")
    webbrowser.open(url)
    return url

d1 = [
    ("A", "Chào anh, anh muốn mở loại tài khoản gì ạ?"),
    ("B", "Chào chị, mình muốn mở tài khoản thanh toán để nhận lương hàng tháng."),
    ("A", "Dạ được ạ. Anh mang theo CMND và sổ hộ khẩu chưa ạ?"),
    ("B", "Mình mang theo CMND rồi, còn sổ hộ khẩu thì không có."),
    ("A", "Không sao ạ, chỉ cần CMND là đủ rồi. Anh điền mẫu đơn này nhé."),
    ("B", "Vâng, cho mình hỏi mở tài khoản có phí gì không ạ?"),
    ("A", "Hoàn toàn miễn phí ạ. Nếu anh duy trì số dư trên hai triệu thì không mất phí thường niên."),
    ("B", "Tốt quá. Mình có thể đăng ký ngân hàng trực tuyến không ạ?"),
    ("A", "Dạ được chứ, mình sẽ kích hoạt cho anh luôn ạ."),
    ("B", "Cảm ơn chị nhiều nhé."),
]

d2 = [
    ("A", "Chào anh, hôm nay rạp chiếu phim có phim gì hay ạ?"),
    ("B", "Mình muốn xem phim hành động, có phim nào đang chiếu không ạ?"),
    ("A", "Dạ có, hiện đang chiếu Biệt đội siêu anh hùng 6."),
    ("B", "Phim này được đánh giá khá cao, mình muốn xem phim này."),
    ("A", "Anh muốn xem suất mấy giờ ạ? Suất hai giờ, bốn giờ và bảy giờ rưỡi tối vẫn còn chỗ."),
    ("B", "Cho mình hai vé suất bảy giờ rưỡi nhé, ngồi ghế đôi ở giữa."),
    ("A", "Dạ, hai vé tổng cộng hai trăm ngàn đồng ạ."),
    ("B", "Có thể thanh toán bằng thẻ không ạ?"),
    ("A", "Dạ được ạ, quầy bên kia có máy POS ạ."),
    ("B", "Ok, mình biết rồi. Cảm ơn anh nhiều nhé."),
    ("A", "Phim bắt đầu bảy giờ rưỡi, nhưng có quảng cáo khoảng mười lăm phút trước ạ."),
]

upload("2026-04-15", "Mở tài khoản ngân hàng", d1)
print("\n⏳ 等待8秒后上传第二段...")
time.sleep(8)
upload("2026-04-15", "Mua vé xem phim", d2)
print("\n✅ 两段对话均已上传（纯越南语，自动翻译会添加中文）")
