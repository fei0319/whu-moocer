# whu-moocer

武大慕课机是一款基于 Python 和 Selenium 开发的脚本，能够自动观看武汉大学在线教学平台的慕课视频。

## 安装

确保您的设备上已安装 Python。本程序基于 Python 3.9.12 开发，但对其他版本的 Python 也具有很好的兼容性。

在终端运行指令 `pip install selenium==4.9.0`，安装 Selenium。

根据您偏好的浏览器下载对应的驱动。此处以 Chrome 为例。

- 在 [https://chromedriver.storage.googleapis.com/index.html](https://chromedriver.storage.googleapis.com/index.html) 找到适合版本的驱动并下载
- 解压下载文件，将 `main.py` 第 1 行的 `DRIVER_PATH` 的值修改为驱动的绝对路径，例如 `r'C:/Users/me/Downloads/chromedriver.exe'`

# 使用

运行 `main.py`，在弹出网页中登录您的学习通账号，随后根据终端提示操作即可。

# 注意事项

- 请输入您的学习通账号或通过智慧珞珈手机 app 扫码登录，而非输入武汉大学统一身份认证账号
- 请下载正确版本的驱动。**Chrome 可能会在您查看其版本时自动更新**，导致您下载的驱动版本与 Chrome 的实际版本不一致，这点请务必注意
- 可以通过 `main.py` 中的 `DOUBLE_RATE` 控制是否以二倍速观看视频
- 若您的网络状况较差，可以适当调大 `main.py` 中 `IMPLICITLY_WAIT` 的值
- 因使用此软件造成的一切后果均由使用者本人承担
