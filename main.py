import cv2
import sys
import os


def resource_path(relative_path):
    """ 获取资源文件的绝对路径，适用于 PyInstaller 打包后的环境 """
    try:
        # PyInstaller 创建临时文件夹，并将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def detect_qrcode(image_path):
    # 初始化 WeChat QRCode 检测器
    try:
        detector = cv2.wechat_qrcode_WeChatQRCode(
            resource_path('detect.prototxt'),
            resource_path('detect.caffemodel'),
            resource_path('sr.prototxt'),
            resource_path('sr.caffemodel')
        )
    except Exception as e:
        print("初始化 WeChatQRCode 失败")
        print("请确认模型文件已正确放置到脚本目录中")
        return []

    # 读取图像并进行亮度与对比度增强
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图片: {image_path}")
        return []

    img = cv2.convertScaleAbs(img, alpha=1.2, beta=40)

    # 检测并解码二维码
    results, _ = detector.detectAndDecode(img)
    return [res for res in results if res]

if __name__ == "__main__":
    image_path = "1.webp"  # 替换为你的图片路径
    qrcodes = detect_qrcode(image_path)

    if qrcodes:
        print("识别到的二维码内容：")
        for i, content in enumerate(qrcodes, 1):
            print(f"{i}. {content}")
    else:
        print("未识别到二维码")

