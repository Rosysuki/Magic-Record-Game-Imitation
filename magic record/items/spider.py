# -*- coding: utf-8 -*-

from os import path ,mkdir
import requests as rqs
from lxml import etree
from typing import NoReturn
from time import sleep
from glob import glob

class MagicRecord(object):
    
    headers:dict = {
        "User-Agent": 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/131"
        }
    
    def __init__(self ,
                 * ,
                 file:str = "pic" ,
                 xpath:str = "//img/@src"
                 ) -> NoReturn:
        """
        :param pic  -> 图片地址
        :param task -> 图片内容
        :param file -> 文件夹地址
        """
        if not path.exists(file):
            mkdir(file)
            sleep(1)
            print(f"{file}文件夹创建完毕！")
        
        self.file:str = file
        self.xpath:str = xpath
        self.pics:list[list[str]] = []
        self.task:list[bytes] = []

    def run(self ,fmt='png') -> NoReturn:
        for index ,each in enumerate(self.pics ,start=1):
            #if "https" not in each:
            #    each:str = "https"
            try:
                respond = rqs.get(each)
                with open(self.file+r"/test{}.{}".format(index ,fmt) ,'wb') as fp:
                    fp.write(respond.content)
                print(f"test{index} well download!")
            except:
                pass
            sleep(1)
        
    def start(self ,
                 * ,
                 #fromlist:list[str]|tuple[str],
                 fmt:str = "png"
                 ) -> NoReturn:
        """
        function download
            download pics
        """
        for index ,each in enumerate(self.task ,start=1):
            #with open(self.file+r"/{}{}.{}".format(fromlist[index-1] ,index ,fmt) ,'wb') as fp:
            with open(self.file+r"/test{}.{}".format(index ,fmt) ,'wb') as fp:
                fp.write(each)
            #print(f"{fromlist[index-1]} well download!")
            
    def parser(self ,html:str) -> NoReturn:
        ALL:list = [each for each in etree.HTML(html).xpath(self.xpath)]
        self.pics:list = ALL
        print("parser ok!")
        
    #def load(self) -> NoReturn:
    #    for index ,each in enumerate(self.pics ,start=1):
    #        self.task.append(rqs.get(each).content)
    #        print(f"load img{iindex}")
    #        sleep(1)
    #    print("load ok!")
    
    def HTML(self ,url:str ,/) -> str:
        if (respond:=rqs.get(url ,headers=MagicRecord.headers)).ok:
            with open(self.file+r"/{}.dat".format(self.file) ,'w' ,encoding='utf-8') as file:
                file.write(respond.text)
            print("html ok!")
            return respond.text

    def LOAD_HTML(self ,file:str) -> str:
        with open(file ,'r' ,encoding='utf-8') as f:
            print("read html ok")
            return f.read()
    
    @property
    def text(self) -> list:
        return self.pics
        
def download(url:str) -> NoReturn:
    magic:MagicRecord = MagicRecord()
    magic.parser(magic.LOAD_HTML(file="pic//pic.dat"))
    #magic.load()
    magic.run()
    print("all ok!")
    
if __name__ == "__main__":
    #print(glob("pic//test[1-10].png"))
    xpath:str = '//table[@class="wikitable"]//span/text()'
    magic:MagicRecord = MagicRecord(file="text" ,xpath=xpath)#'//td//div[@id="bodyContent"]//span/text()')
    magic.parser(magic.LOAD_HTML(file=r"pic/pic.dat"))
    print(magic.text)
    #download(url = r"https://magireco.moe/wiki/%E6%8A%80%E8%83%BD%E5%92%8C%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C%E5%88%97%E8%A1%A8")
