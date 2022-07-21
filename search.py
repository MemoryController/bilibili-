# 搜索模块
import requests
import json
import re


# duration ： 时长
# title : 视频标题
# author : 作者
# tag : 标签
# arcurl : 地址
class Search:
    keyword = ''
    result_list = []
    display_list = []  # 拿给窗口显示用的

    def __init__(self, keyword: str):
        if keyword != '':
            self.keyword = keyword
            self.result_list = self.search_video(keyword=keyword)  # 获得搜索结果
            self.get_display_style()

    def get_url(self, order: int):
        # 通过序号获得url
        return self.result_list[order]['arcurl']

    def get_display_style(self):
        # 获得给窗口显示用的结果列表
        for res in self.result_list:
            # 标题 作者 时长 标签
            dis = res['title'] + '  ' + res['author'] + '  ' + res['duration'] + '  ' + res['tag']
            self.display_list.append(dis)

    def search_video(self, keyword):
        headers_ = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
            'referer': 'https://www.bilibili.com',
        }

        url = 'https://api.bilibili.com/x/web-interface/search/type?__refresh__=true&_extra=&context=&page=1&page_size=50&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=' + keyword + '&category_id=&search_type=video&dynamic_offset=0&preload=true&com2co=true'

        page_text = requests.get(url=url, headers=headers_).text
        data_dict = json.loads(page_text)
        result_list = data_dict['data']['result']  # 获得结果的列表
        # 将结果中的标题格式化
        for result in result_list:
            result['title'] = self.get_tit(result['title'])

        return result_list  # 返回搜索到的列表

    # def search_person(name:str):

    # def person_videos(id:str):
    #

    def get_tit(self, resp: str):
        rule = r'(.*?)<em class="keyword">(.*?)</em>(.*?)'

        try:
            tit_list = re.findall(rule, resp)[0]

            result_ = ''
            for tit in tit_list:
                result_ = result_ + tit
            return result_
        except:
            return resp

# if __name__ == '__main__':
#     se = search('新宝岛')
#     print(se.result_list[0]['arcurl'])
