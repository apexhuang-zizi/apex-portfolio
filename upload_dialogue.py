# -*- coding: utf-8 -*-
"""
越南语对话上传工具
将对话内容通过 URL 参数上传到越南语情景对话模块
使用 Python 确保 UTF-8 编码正确处理越南语音调符号
"""
import urllib.parse
import webbrowser
import json
import sys

def upload_dialogue(date, topic, content_lines):
    """
    上传对话到越南语模块
    
    参数:
        date: 日期 "YYYY-MM-DD"
        topic: 越南文标题
        content_lines: 对话行列表，格式为:
            [
                ("A", "越南语句子", "中文翻译"),
                ("B", "越南语句子", "中文翻译"),
                ...
            ]
    """
    # 构建内容：A/B 格式（匹配 translateAndSave 和 parseVietnameseLines 的期望）
    formatted_lines = []
    for speaker, vi_text, zh_text in content_lines:
        formatted_lines.append(f"{speaker}: {vi_text}")
        formatted_lines.append(f"{speaker}: {zh_text}")
    
    content = "\n".join(formatted_lines)
    
    # URL 编码
    encoded_date = urllib.parse.quote(date, safe='')
    encoded_topic = urllib.parse.quote(topic, safe='')
    encoded_content = urllib.parse.quote(content, safe='')
    
    base_url = "https://apexhuang-zizi.github.io/apex-portfolio/vietnamese.html"
    url = f"{base_url}?date={encoded_date}&topic={encoded_topic}&content={encoded_content}"
    
    # 打印信息
    print(f"日期: {date}")
    print(f"标题: {topic}")
    print(f"对话行数: {len(content_lines)}")
    print(f"URL长度: {len(url)} 字符")
    print(f"\n内容预览:")
    for speaker, vi_text, zh_text in content_lines:
        print(f"  {speaker}: {vi_text}")
        print(f"  {speaker}: {zh_text}")
    print()
    
    # 检查 URL 长度（大多数浏览器限制约 2000 字符）
    if len(url) > 80000:
        print(f"⚠️ 警告: URL 长度 {len(url)} 超过安全范围，可能会被截断")
    elif len(url) > 2000:
        print(f"⚠️ 注意: URL 较长 ({len(url)} 字符)，但现代浏览器通常支持")
    
    # 打开浏览器
    webbrowser.open(url)
    print("✅ 已在浏览器中打开")
    
    return url


if __name__ == "__main__":
    # 测试数据
    test_dialogue = [
        ("A", "Chào buổi tối, nhà hàng chúng tôi xin chào. Bạn có đặt bàn chưa ạ?", "晚上好，欢迎光临本餐厅。请问您预订了吗？"),
        ("B", "Dạ, mình đã đặt bàn cho hai người dưới tên Minh, lúc bảy giờ tối.", "是的，我已经订了两个人的桌，名字叫 Minh，晚上七点。"),
        ("A", "Vâng, để tôi kiểm tra lại ạ. À có rồi, bàn số 5 bên cửa sổ nhé.", "好的，让我查一下。啊找到了，5号桌靠窗的位置。"),
        ("B", "Tốt quá. Cho mình xem thực đơn trước được không ạ?", "太好了。能让我先看看菜单吗？"),
        ("A", "Dạ được ạ, đây là thực đơn. Món đặc biệt hôm nay là cá kho tộ.", "好的，这是菜单。今天的特色菜是鱼露炖鱼。"),
        ("B", "Nghe ngon quá! Cho mình một phần cá kho tộ và một phần rau muống xào tỏi.", "听起来很好吃！我要一份鱼露炖鱼和一份炒空心菜。"),
        ("A", "Dạ vâng. Bạn muốn uống gì không ạ?", "好的。您想喝点什么吗？"),
        ("B", "Cho mình hai ly nước ép mía ạ.", "给我来两杯甘蔗汁。"),
        ("A", "Dạ, hai ly nước ép mía. Tôi sẽ gọi bếp chuẩn bị ngay ạ. Chờ mình một chút nhé.", "好的，两杯甘蔗汁。我马上叫厨房准备。请稍等一下。"),
    ]
    
    upload_dialogue("2026-04-14", "Đặt bàn tại nhà hàng", test_dialogue)
