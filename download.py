import requests
from bs4 import BeautifulSoup
import re
import os


def down(url: str, cookie=''):  # 设置参数默认值
    # 人工构造请求头
    headers_ = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
        'referer': 'https://www.bilibili.com',
        'cookie': cookie
    }
    # 请求
    res = requests.get(url, headers=headers_)
    # 编码
    res.encoding = res.apparent_encoding
    # print(res.text)

    html = BeautifulSoup(res.text, 'lxml')
    # 标题
    tit = html.find('title').text.split('_')[0]

    # 包含地址的script
    script = html.find_all('script')[3].text

    # info = str(script.split('=')[1:])
    # #查找有用url
    # json_ = json.loads(info)
    # print(json_["video"])

    # 拿到需要的音视频信息
    video_url = re.findall(r'"video":\[{"id":\d+,"baseUrl":"(.*?)",', script)[0]
    audio_url = re.findall(r'"audio":\[{"id":\d+,"baseUrl":"(.*?)",', script)[0]

    # 请求
    audio_ = requests.get(audio_url, headers=headers_)
    video_ = requests.get(video_url, headers=headers_)

    # 创建文件夹
    if not os.path.exists('cache'):
        os.mkdir('cache')

    # 写入缓存
    with open('cache\\audio.mp3', 'wb') as file:
        file.write(audio_.content)

    with open('cache\\video.mp4', 'wb') as file:
        file.write(video_.content)

    # 创建文件夹
    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    # 合并文件
    os.system('ffmpeg-win64-v4.2.2.exe -i "cache\\video.mp4" -i "cache\\audio.mp3" -c copy "downloads\\' + tit + '.mp4"')

    # 打开目录
    os.startfile('downloads')

    # 删除缓存
    #os.system('del cache')



