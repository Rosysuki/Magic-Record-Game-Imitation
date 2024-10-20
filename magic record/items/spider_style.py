# -*- coding: utf-8 -*-
# @To Spider Memoria

import requests as rqs
from lxml import etree
from collections import deque
from typing import NoReturn ,Any ,Deque
from tkinter.messagebox import showerror
from pprint import pp ,pformat
from os import path ,mkdir
from time import sleep

class Memoria(object):


    headers:dict = {
        "User-Agent": 
        r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/131"
        }

    keys:list[str] = [
            "img" ,
            "name" ,
            "star" ,
            "type" ,
            "HP" ,"ATK" ,"DEF" ,
            #"effect" ,
            #"round"
        ]

    #headers=Memoria.headers
    def __init__(self ,
                 filename:str = "memoriaHTML.dat" ,
                 * ,
                 url:str = r"https://magireco.moe/wiki/%E8%AE%B0%E5%BF%86%E7%BB%93%E6%99%B6%E5%88%97%E8%A1%A8_(%E7%AE%80%E4%B8%AD%E6%9C%8D)" ,
                 save:bool = False ,
                 load:bool = False
                 ) -> NoReturn:
        """
        function self.__init__

        """

        if save and load:
            showerror("X" ,"SAVE and LOAD!")
            return

        if load:
            with open(filename ,'r' ,encoding='utf-8') as file:
                self.html:str = file.read()
        else:
            if not (respond:=rqs.get(url=url ,headers=Memoria.headers)).ok:
                return showerror("X" ,"Respond Error!")
            self.respond:Any = respond
            print("GET OK!")

            if save:
                with open(filename ,'w' ,encoding="utf-8") as file:
                    file.write(self.respond.text)
                print("SAVE OK!")
            self.html:str = self.respond.text

        self.memoria:dict[str:dict[str:Any]] = {}
        print("INIT OK!")


    def get(self ,target:Any) -> list:
        return [each for index ,each in enumerate(target)]


    def set(self ,xpath:str) -> Any:
        return etree.HTML(self.html).xpath(xpath)


    def parser(self ,
               filename:str = r"memoriaDATA.dat",
               * ,
               img_xpath:str = r'//tbody/tr//td[@style="padding: 0;"]/a/@href' ,
               name_xpath:str = r"//tbody/tr//td[2]/a/text()" ,
               star_xpath:str = r"//tbody/tr//td[3]/span[1]/text()" ,
               type_xpath:str = r"//tbody/tr//td[3]/span[2]/text()" ,
               HP_xpath:str = r'//tbody/tr//td[@style="text-align: right;"][1]/text()' ,
               ATK_xpath:str = r'//tbody/tr//td[@style="text-align: right;"][2]/text()',
               DEF_xpath:str = r'//tbody/tr//td[@style="text-align: right;"][3]/text()' ,
               effect_xpath:str = r'//tbody/tr//td[@style="border-left-width: 0;"]//span/text()'
               ) -> NoReturn:
        """
        function self.parser
            convert self.html -> self.text...
        """
        
        img:list = self.get(self.set(img_xpath))
        name:list = self.get(self.set(name_xpath))
        star:list = self.get(self.set(star_xpath))
        tp:list = self.get(self.set(type_xpath))
        HP:list = self.get(self.set(HP_xpath))
        ATK:list = self.get(self.set(ATK_xpath))
        DEF:list = self.get(self.set(DEF_xpath))
        effect:list = self.get(self.set(effect_xpath))

        print(f"img:{len(img)}\nname:{len(name)}\nstar:{len(star)}\ntp:{len(tp)}\nHP:{len(HP)}\nATK:{len(ATK)}\nDEF:{len(DEF)}\neffect:{len(effect)}")

        lexicon:dict[str:Any] = dict(zip(Memoria.keys ,[img ,name ,star ,tp ,HP ,ATK ,DEF]))

        for index ,title in enumerate(name ,start=0):
            self.memoria[title]:dict = {}
            for i ,(key ,each) in enumerate(lexicon.items() ,start=0):
                self.memoria[title][key]:dict[str:Any] = each[index]
            else:
                if not index % 10:
                    print(f"{index}OK!")
        else:
            print(f"AllOver!")

            with open(filename ,'w' ,encoding='utf-8') as file:
                file.write(repr(pformat(self.memoria)))
            print("Parser OK!")


    @staticmethod
    def check(filename:str ,
              * ,
              mode:str = "-check" ,
              stop:int|None = None
              ) -> NoReturn:
        with open(filename ,'r' ,encoding='utf-8') as file:
            data:dict[str:dict[str:Any]] = file.read()

        match mode:
            case "-check":
                pp(data)
            case "-len":
                print(f"length:{len(data)}")
            case _:
                print("Mode Args Error!")


class ImgDownloader(object):

    def __init__(self ,
                 filename:str
                 ) -> NoReturn:

        with open(filename ,'r' ,encoding='utf-8') as file:
            self.data:dict[str:dict[str:Any]] = eval(eval(file.read()))

        if isinstance(self.data ,dict):
            print(f"LOAD TEXT OKK!")
        else:
            print(f"ERROR!")
            raise


    def run(self ,
            file:str ,
            * ,
            xpath:str = r'//img[@class="thumbimage"]/@src'
            ) -> NoReturn:

        if not path.exists(file):
            mkdir(file)
        sleep(1.0)

        for index ,(name ,each) in enumerate(self.data.items() ,start=1):
            if index < 122:
                continue
            try:
                if (respond:=rqs.get(r"https://magireco.moe/"+each["img"] ,headers=Memoria.headers)).ok:
                    image_url:str = etree.HTML(respond.text).xpath(xpath)[0]
                    with open(f"{file}//{name}.png" ,'wb') as file_ptr:
                        file_ptr.write(rqs.get(image_url ,headers=Memoria.headers).content)
                    print(f"{index} OKK!")
                else:
                    print(f"{index} FAILED!")

                sleep(0.6)
            except:
                pass


    def seek(self ,name:str) -> int:
        for index ,(key ,each) in enumerate(self.data.items() ,start=1):
            if name in key:
                print(f"{key} in {index}.")
                return index


if __name__ == "__main__":
    #memoria = Memoria(load=True)
    #memoria.parser("memoriaDATA2.dat")
    #Memoria.check(r"memoriaDATA2.dat" ,mode="-len")
    #122

    downloader = ImgDownloader(r"memoriaDATA2.dat")
    #downloader.run("Memoria")
    #downloader.seek("最后的作品")
    pass
    













    
