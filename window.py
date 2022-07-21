from tkinter import *
from search import Search

import tkinter.messagebox
import download
import threading


class Window:
    root = Tk()
    videos_list = []
    search_ = Search('')  # 声明一个search对象

    videos_box = Listbox()  # 放视频信息的列表
    scrollbar = Scrollbar()  # 滚动条
    input_search = Entry()  # 输入搜索内容的输入框
    input_link = Entry()  # 输入链接的输入框
    # get_url_but = Button()  # 根据选择获得url的按钮
    download_but = Button()  # 下载按钮
    search_but = Button()  # 搜索按钮

    def __init__(self):
        self.root.geometry('450x400')
        self.root.title('bilibili视频下载器')
        self.scrollbar = Scrollbar(self.root)  # 滚动条
        self.videos_box = Listbox(self.scrollbar, height=15, width=60)  # 信息展示框应当在滚动框中
        self.input_search = Entry(self.root)
        self.input_link = Entry(self.root)
        # self.get_url_but = Button(self.root, text='获得视频的url' , command=self.on_get_url_click)
        self.download_but = Button(self.root, text='     下载     ', command=self.on_download_click)
        self.search_but = Button(self.root, text='     搜索     ', command=self.on_search_click)

        # 标签提示
        # Label(self.root, text='url').grid(row=4)
        # Label(self.root , text='关键词').grid(row=3)

        self.search_but.pack()
        self.download_but.pack()
        # self.get_url_but.pack()
        self.input_search.pack()
        self.input_link.pack()
        self.scrollbar.pack()
        self.videos_box.pack()
        self.root.mainloop()

    def insert_data(self, li: list):
        # 在按下按钮后才添加
        # self.videos_box.delete(0, END)
        for l in li:
            self.videos_box.insert("end", l)

    def get_selected(self):
        try:
            return self.videos_box.curselection()[0]
        except:
            return -1

    def on_search_click(self):
        # 搜索按钮按下后
        search_ = Search(keyword=self.get_keyword())
        self.insert_data(search_.display_list)
        self.search_ = search_

    def get_keyword(self):
        # 获得搜索框文字
        return self.input_search.get()

    def get_url(self):
        # 获取下载地址
        return self.input_link.get()

    def on_download_click(self):
        # 下载按钮按下后
        # download.down(url=self.get_url())
        # 多线程下载
        if self.get_url() != '':
            # 若url框中有内容
            down_thread = threading.Thread(target=download.down, args=(self.get_url(),))
            down_thread.start()
        else:
            # 若没有内容
            down_thread = threading.Thread(target=download.down, args=(self.get_selected_url(),))
            down_thread.start()

        tkinter.messagebox.showinfo(title='提示', message='正在下载，不要重复点击')

    def get_selected_url(self):
        index = self.get_selected()
        return self.search_.get_url(index)

    # def on_get_url_click(self):
    #     # 获取链接按钮按下后
    #     index = self.get_selected()
    #     if index != -1:
    #         # 获得的视频url
    #         url = self.search_.get_url(index)
    #         # 载入url框中
    #         self.input_link.set



