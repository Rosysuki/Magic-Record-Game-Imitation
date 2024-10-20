# -*- coding: utf-8 -*-

from spider import MagicRecord ,NoReturn
from os import rename

def set_names(start:int ,
              final:int ,
              / ,
              pointer:int = 0 ,
              change:list=["火" ,"水" ,"木" ,"光" ,"暗"]
              ) -> NoReturn:
    xpath:str = '//table[@class="wikitable"]//span/text()'
    magic:MagicRecord = MagicRecord(file="text" ,xpath=xpath)
    magic.parser(magic.LOAD_HTML(file=r"pic/pic.dat"))

    for index in range(start ,final):
        try:
            name:str = magic.text[index-4]
            
            if name in {"重抽为同属性" ,"重抽为自己的Disc"}:
                pointer:int = 0 if pointer>4 else pointer
                name:str = name + change[pointer]
                pointer += 1
                
            rename(f"pic//test{index}.png" ,f"pic//{name}.png")

            print(f"{index} ok!")
            
        except:
            print(f"{index} ERROR!")


if __name__ == "__main__":
    set_names(102 ,149)
