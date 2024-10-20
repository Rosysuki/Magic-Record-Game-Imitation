# -*- coding: utf-8 -*-

from Character import Template ,NoReturn ,Any
from pprint import pformat ,pp
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sys import exit as os_exit


class Register(Tk):

    HEADERS:dict[str : str] = {
            "inow":"初始化技能持续点数*4" ,
            "igap":"初始化技能回复点数*4" ,
            "now":"技能持续点数*4" ,
            "gap":"技能回复点数*4" ,
            "tp":"技能类别*4" ,
            "name":"技能名称*4" ,
            "ATK":"ATK加成*4" ,
            "DFE":"DEF加成*4" ,
            "HP":"HP加成*4" ,
            "text":"描述"
        }


    @staticmethod
    def load(name:str ,
             * ,
             fmt:str = r'.dat'
             ) -> repr:
        path:str = r"magic record\items\style\{}\\".format(name)
        with open(path+name+fmt ,'r' ,encoding='utf-8') as file:
            return file.read()

    def __init__(self ,
                 name:str = "Register" ,
                 * ,
                 size:str ,
                 pos:str = '' ,
                 ) -> NoReturn:
        """
        function self.__init__

        :param size
            "w x h"
        """

        super(Register ,self).__init__()
        self.title(name)
        self.geometry(size+pos)
        self.memory:dict[str : Any] = {}
        self.re_memory:dict[str : Any] = {}
        self.__memory:dict[None] = {}
        self.var = StringVar()
        

    def process(self) -> NoReturn:
        self.name:str = self.var.get()
        for index ,(label ,var) in enumerate(self.memory.items() ,start=0):
            data:list[str] = var.get().split() if label in {'tp' ,'name' ,'text'} else list(map(int ,var.get().split()))
            Register.HEADERS[label]:dict[str ,Any] = data
        else:
            print(pformat(Register.HEADERS))


    def shutdown(self) -> NoReturn:

        headers:list[str] = list(Register.HEADERS)

        for index ,each in enumerate(Register.HEADERS["name"] ,start=0):
            memory:dict = {}
            for iindex ,ieach in enumerate(headers ,start=0):
                memory[ieach] = Register.HEADERS[ieach][index]

            else:
                self.__memory[each]:dict[str : dict[str:Any]] = memory
                
        else:
            #self.memory:dict[str : Any] = self.re_memory
            print("self.__memory:")
            print(pformat(self.__memory))

            path:str = r"magic record\items\style\{}\\".format(self.name)
            with open(r"{}{}.dat".format(path ,self.name) ,'w' ,encoding='utf-8') as file:
                file.write(repr(self.__memory))
            print("Save OK!")

            self.destroy()
            


    def run(self) -> NoReturn:
        global RUN
        ttk.Label(self ,text="名字：").pack()
        ttk.Entry(self ,textvariable=self.var).pack()
        for index ,(label ,each) in enumerate(Register.HEADERS.items() ,start=0):
            ttk.Label(self ,text=each).pack()
            var = StringVar()
            ttk.Entry(self ,textvariable=var).pack()
            self.memory[label]:dict[str : Any] = var
            self.re_memory[label]:dict[str : Any] = var
        else:
            ttk.Button(self ,text="Check" ,command=lambda : print(pformat(self.memory))).pack()
            ttk.Button(self ,text="Bind" ,command=lambda : self.process()).pack()
            ttk.Button(self ,text="OK Next" ,command=lambda : self.shutdown()).pack()
            ttk.Button(self ,text="Stop!" ,command=lambda : self.stop()).pack()
            self.mainloop()


    def stop(self) -> NoReturn:
        self.destroy()
        os_exit(0)


def main(*args:tuple ,**kwargs:dict) -> NoReturn:
    RUN:bool = True
    while RUN:
        register = Register(size="600x600")
        register.run()


if __name__ == "__main__":

    #inow:list[int ,int ,int ,int] = [1 for _ in range(4)]
    #igap:list[int ,int ,int ,int] = [2 for _ in range(4)]
    #now:list[int ,int ,int ,int] = [3 for _ in range(4)]
    #gap:list[int ,int ,int ,int] = [4 for _ in range(4)]
    #tp:list[str ,str ,str ,str] = ['a' for _ in range(4)]
    #name:list[str ,str ,str ,str] = ['b' for _ in range(4)]
    #ATK:list[int ,int ,int ,int] = [5 for _ in range(4)]
    #DEF:list[int ,int ,int ,int] = [6 for _ in range(4)]
    #HP:list[int ,int ,int ,int] = [7 for _ in range(4)]
    #text:list[str ,str ,str ,str] = ["NO" for _ in range(4)]
    #template:Template = Template()

    """
    TEST:dict = Template.skill(inow=inow ,
                   igap=igap ,
                   now=now ,
                   gap=gap ,
                   tp=tp ,
                   name=name ,
                   ATK=ATK ,
                   DEF=DEF ,
                   HP=HP ,
                   text=text)

    print(pformat(TEST))
    """
    
    main()
