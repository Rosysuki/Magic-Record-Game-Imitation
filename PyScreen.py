# -*- coding: utf-8 -*-

#__all__:list = ["PyScreen" ,"PyMixer" ,"show_abspath_single" ,"Grid"]

from typing import NoReturn ,Any ,Callable ,Self ,NewType
from re import findall as re_findall
from glob import iglob ,glob
from functools import partial ,wraps
from time import sleep ,time
from sys import stdout
from threading import Thread #,Event
from multiprocessing import Process
from random import randint ,shuffle ,choice
import pygame
from pygame.locals import *
from os import path
from tkinter.messagebox import showerror ,showinfo
#from copy import deepcopy


W ,H = 0b10010110000 ,0b1100100000
AutoKeyDowner:bool = False


class Grid(object):
    line_gap:int = 180
    ratio:float = 0.45
    
    c1l1:tuple[int] = (W//2 ,H//2-400)
    c1l2:tuple[int] = (c1l1[0]+line_gap ,c1l1[1])
    c1l3:tuple[int] = (c1l2[0]+line_gap ,c1l2[1])
    
    c2l1:tuple[int] = (W//2 ,H//2-450//2)
    c2l2:tuple[int] = (c2l1[0]+line_gap ,c2l1[1])
    c2l3:tuple[int] = (c2l2[0]+line_gap ,c2l1[1])
    
    c3l1:tuple[int] = (W//2 ,H//2-50)
    c3l2:tuple[int] = (c3l1[0]+line_gap ,c3l1[1])
    c3l3:tuple[int] = (c3l2[0]+line_gap ,c3l1[1])

    re_c1l1:tuple[int] = (c1l1[0]-line_gap-50 ,c1l1[1])
    re_c1l2:tuple[int] = (re_c1l1[0]-line_gap ,re_c1l1[1])
    re_c1l3:tuple[int] = (re_c1l2[0]-line_gap ,re_c1l1[1])

    re_c2l1:tuple[int] = (c2l1[0]-line_gap-50 ,c2l1[1])
    re_c2l2:tuple[int] = (re_c2l1[0]-line_gap ,re_c2l1[1])
    re_c2l3:tuple[int] = (re_c2l2[0]-line_gap ,re_c2l1[1])

    re_c3l1:tuple[int] = (c3l1[0]-line_gap-50 ,c3l1[1])
    re_c3l2:tuple[int] = (re_c3l1[0]-line_gap ,re_c3l1[1])
    re_c3l3:tuple[int] = (re_c3l2[0]-line_gap ,re_c3l1[1])


def show_abspath(target:str|list[str] ,* ,fromlist:iter) -> list[str]:
    if not len(target): return []
    target:list[str] = [target] if not isinstance(target ,list) else target
    return [ieach for each in target for ieach in fromlist if len(re_findall(r".+?{}.*?".format(each) ,ieach))]

def show_abspath_single(target:str) -> str:
    return r"magic record/items/photo/" + target


class MetaPyScreen(type):

    SINGLEMODE:None = None

    def __new__(mcls ,name:str ,base:tuple ,attrs:dict) -> None:
        if not mcls.SINGLEMODE:
            attrs["abspath"]:str = '/'.join(__file__.split('\\')[:-1])
            mcls.SINGLEMODE:None = type.__new__(mcls ,name ,base ,attrs)
        return mcls.SINGLEMODE


class PyMixer(object):

    @classmethod
    def ALL_BGM(cls) -> iter:
        return iglob(cls.abspath + "//data//bgm//*")

    def __repr__(self) -> repr:
        return "<class 'PyMixer'>"

    def __init__(self ,
                 * ,
                 fromlist:list|tuple = []
                 ) -> NoReturn:
        self._show_abspath:Callable = partial(show_abspath ,fromlist=PyMixer.ALL_BGM)
        self.song:str|None = None
        self.vol:float = 0.6
        self.fromlist:list = list(fromlist) if not isinstance(fromlist ,list) else fromlist

    def __lshift__(self ,
                   song:str
                   ) -> NoReturn:
        self.song:str = self._show_abspath(song)

    def __rshift__(self ,
                   mode:int ,
                   ) -> NoReturn:
        if self.song is not None:
            pygame.mixer.music.load(self.song)
            pygame.mixer.music.set_volume(self.vol)
            pygame.mixer.music.play(mode)

    def __add__(self ,
                vol:float
                ) -> NoReturn:
        self.vol:float = self.vol+vol

    def __eq__(self ,
               vol:float
               ) -> NoReturn:
        self.vol:float = vol

    @property
    def isAiring(self) -> bool:
        return pygame.mixer.music.get_busy()


class SimpleMixer(object):

    def __init__(self ,
                 fromlist:list[str] ,
                 * ,
                 vol:float=0.6
                 ) -> NoReturn:
        """
        function SimpleMixer.__init__
            first initialize mixer
        """
        super(SimpleMixer ,self).__init__()
        pygame.mixer.init()
        self.fromlist:list[str] = fromlist
        self.running:bool = True
        self.length:int = len(self.fromlist)
        self.pointer:int = randint(0 ,self.length-1)
        pygame.mixer.music.set_volume(vol)

    def air(self ,music:str) -> NoReturn:
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(1)

    def run(self) -> NoReturn:
        while self.running:
            try:
                if not pygame.mixer.music.get_busy():
                    self.air(self.fromlist[self.pointer])
                    self.pointer:int = (self.pointer + 0b1) % self.length
                sleep(3.8)
            except:
                return


class SimpleEffect(object):

    def __init__(self ,
                 fromlist:str ,
                 * ,
                 init:bool=False
                 ) -> NoReturn:
        """
        function SimpleEffect.__init__
            init in SimpleMixer
        """
        if init:
            pygame.mixer.init()
        _list:iter = iglob(r"magic record/items/style/" + fromlist + r"/*.mp3")
        self.choose:list[str] = [each for each in _list if len(re_findall(r".*?(choose).\.mp3" ,each))]
        self.ok:list[str] = [each for each in _list if len(re_findall(r".*?(ok).\.mp3" ,each))]
        self.start:str = r"magic record/items/style/" + fromlist + r"/start.mp3"
        self.die:str = r"magic record/items/style/" + fromlist + r"/die.mp3"

    def effect(self ,
               act:str ,
               * ,
               vol:int = 1.2) -> NoReturn:

        effect = pygame.mixer.Sound(choice(self.ok) if act=='ok' else choice(self.choose) if act=='choose' else self.start if act=='start' else self.die)
        effect.set_volume(vol)
        effect.play()
        


class PyScreen(object ,metaclass=MetaPyScreen):

    @staticmethod
    def SLEEP_TIME(char:str) -> float:
        return 0.16 if char in {',' ,'，' ,'.' ,'。' ,'；' ,';'} else 0.06

    @classmethod
    def ALL_PIC(cls) -> iter:
        return iglob(cls.abspath + "//data//pic//*")

    @property
    def root(self) -> Self:
        """
        To Share This-Screen!
        """
        return self.screen

    @root.setter
    def root(self ,new_root:Self) -> NoReturn:
        """
        To Rebind This-Screen -> Game-Screen!
        """
        self.screen:Self = new_root


    def __init__(self ,
                 * ,
                 size:Callable[[str] ,tuple[int ,int]] ,
                 name:str
                 #data:Callable[[None] ,list[dict]] = list()
                 ) -> NoReturn:
        """
        function PyScreen.__init__
            pass
        """

        #self.mixer = PyMixer()
        self.pointer:int = 0b0
        self.__width ,self.__heigth = size
        pygame.init()
        self.screen = pygame.display.set_mode(size ,vsync=True)
        pygame.display.set_caption(name)
        #self.data:list[dict] = data
        self._show_abspath:Callable = partial(show_abspath ,formlist=PyScreen.ALL_PIC)

        #self.effect_x ,self.effect_

        self.AutoKeyDowner:bool = False
        #self.Animate:bool = True


    def _say(self ,
            text:str ,
            x:int ,
            y:int ,
            * ,
            font:str ,
            size:int ,
            color:tuple
            ) -> NoReturn:
        
        self.screen.blit(pygame.font.Font(font ,size).render(text ,True ,color) ,(x ,y))


    def _said(self ,
             x:int ,
             y:int ,
             * ,
             font:str ,
             size:int ,
             color:tuple
             ) -> NoReturn:

        x_init:int = x
        for index ,char in enumerate(self.text ,start=1):
            self.say(x ,y ,font=font ,size=size ,color=color)
            x:int = x if (x:=x+size) <= self.__width-x else x_init
            y:int = y if x != x_init else y+size
            sleep(PyScreen.SLEEP_TIME(char))
        else:
            pass


    def ispicable(self ,start:int ,final:int ,steps:int ,/) -> bool:
        return all(list(map(lambda n: n>0 ,[start ,final ,steps])) + [start>final ,start>steps ,final<256])


    def pic_info(path:str ,
                 / ,
                 pixel=False ,
                 resize=False ,
                 transparent=False ,
                 **info:dict
                 ) -> None:
        """
        param path
        
        param pixel
        param resize
        param angel size
        param transparent colorkey
        """
        photo = pygame.image.load(path).convert_alpha() if pixel else pygame.image.load(path).convert()
        photo = pygame.transform.rotozoom(photo ,info["angel"] ,info["size"]) if resize else photo
        photo.set_colorkey(info["colorkey"]) if transparent else None
        return photo

    
    def pic_mode(self ,**info:dict) -> tuple:
        try:
            animated:bool = info["animated"]
            start ,final ,steps = info["start"] ,info["final"] ,info["steps"]
            if not self.ispicable(start ,final ,steps):
                raise KeyError
        except KeyError as KE:
            return (0 ,15**2 ,15 ,True)
        return (start ,final ,steps ,animated)

    def pic(self ,
            path:str ,
            x:int ,
            y:int ,
            **mode:dict
            ) -> NoReturn:
        #start ,final ,steps ,animated = mode
        photo = pygame.image.load(path).convert_alpha() if mode["pixel"] else pygame.image.load(path).convert()
        photo = pygame.transform.rotozoom(photo ,0 ,mode["ratio"]) if mode["resize"] else photo
        photo.set_colorkey(mode["colorkey"]) if mode["transparent"] else None

        if not mode["animated"]:
            self.screen.blit(photo ,(x ,y))
            return

        try:
            start ,final ,steps = mode["start"] ,mode["final"] ,mode["steps"]
            if not self.ispicable(start ,final ,steps):
                raise KeyError
        except KeyError as KE:
            start ,final ,steps = 0 ,14**2 ,16
    
        for index ,pixel in enumerate(range(start ,final ,steps)):
            if pixel >= 200:
                break
            photo.set_alpha(pixel)
            self.screen.blit(photo ,(x ,y))
            self.flash()
            sleep(0.06)
        return


    def simple_pic(self ,
                   address:str ,
                   x:int ,
                   y:int ,
                   * ,
                   alpha:int = 255 ,
                   ratio:float = 1.0
                   ) -> NoReturn:
        picture = pygame.image.load(address).convert_alpha()
        photo = pygame.transform.rotozoom(picture ,0 ,ratio)
        photo.set_alpha(alpha)
        self.screen.blit(photo ,(x ,y))


    def dye(self ,**dye_info) -> NoReturn:
        try:
            color:tuple = dye_info["color"]
        except KeyError as KE:
            pass
        else:
            self.screen.fill(color)


    def bind_all_once(self) -> NoReturn:
        pass


    def __repr__(self) -> repr:
        return "<class 'PyScreen'>"


    def say(self ,
            text:str ,
            x:int ,
            y:int ,
            size:int ,
            color:tuple ,
            auto:bool=False ,
            font:str = r"magic record\font\SIMYOU.TTF"
            ) -> NoReturn:
        self.screen.blit(pygame.font.Font(font ,size).render(text ,True ,color) ,(x ,y))
        if auto: PyScreen.flash()


    def simple_say(self ,
                   text:str ,
                   x:int ,
                   y:int ,
                   color:tuple ,
                   size:int = 28 ,
                   font:str = r"magic record\font\SIMYOU.TTF"
                   ) -> NoReturn:

        self.say(text=text ,x=x ,y=y ,size=size ,color=color ,font=font)


    def said(self ,text:str ,x:int ,y:int ,size:int ,color:tuple ,auto:bool=False): #animation say -> said
        _x ,_y = x ,y
        for index ,char in enumerate(text):
            _x ,_y = (x ,_y+46) if _x >= self.width-x else (_x ,_y)
            self.say(char ,_x ,_y ,size ,color ,auto)
            PyScreen.flash()
            _x += 33
            sleep(0.04)
        else:
            print(f"Say Animation Show Done!")


    def flash(self ,isnew:bool=True) -> NoReturn:
        pygame.display.flip() if isnew else pygame.display.update()


    def show_HP_bar(self ,
                    HP_or_MP:int ,
                    x:int ,
                    y:int ,
                    * ,
                    color:tuple = (255 ,0 ,0) ,
                    target:str = "HP"
                    ) -> NoReturn:

        inter_color:tuple = (255 ,0 ,0) if target == "HP" else (45 ,92 ,255)
        #random_color:tuple = tuple([randint(0 ,255) for _ in range(3)]) if target == "HP" else (100 ,200 ,255)
        pygame.draw.rect(self.screen ,color=inter_color ,rect=(x+42+34 ,y+72 ,HP_or_MP ,10))
        pygame.draw.rect(self.screen ,color=tuple([255 for _ in range(3)]) ,rect=(x+42+34 ,y+72 ,HP_or_MP ,10) ,width=3)


    def show_rival(self ,
                    * ,
                    x:int ,
                    y:int ,
                    color:tuple[int ,int ,int] ,
                    size:int = 512
                    ) -> NoReturn:

        pygame.draw.rect(self.screen ,color=color ,rect=(x ,y ,size ,size) ,width=2)


    def show_chara(self ,
                   * ,
                   x:int ,
                   y:int ,
                   color:tuple[int ,int ,int] ,
                   size:int = 512
                   ) -> NoReturn:

        pygame.draw.rect(self.screen ,color=color ,rect=(x ,y ,size ,size) ,width=2)


    def character(self ,
                  name:str ,
                  * ,
                  root:Self ,
                  pos:tuple[int] ,
                  element:str ,
                  info:dict = {},
                  color:tuple[tuple[int]] = ((255 ,255 ,255) ,(255 ,255 ,255)) ,
                  magic_pic:str = "magic.jpg" ,
                  ch_dict:dict ,
                  ch_list:list ,
                  ri_dict:dict ,
                  ri_list:list
                  ) -> NoReturn:

        """
        function PyScreen.character
            draw character and basic info

        :param info -> dict
            HP(now) && __HP__
            MP(now)
            :param HP
            :param __HP__
            :param MP
            
        :param element -> str
            element name ,just name ,no suffix

        :param color -> tuple
            colorkey

        :param magic_pic -> str
            magic pic .png
        """

        if not info["alive"]:
            return

        if (HP := info["HP"]) < 0b0 :
            info["alive"] = False

            basename:str = path.basename(name)
            removed_name:str = basename[:basename.index('.')]
            print(f"!!!{name} DIED!!!")

            try:
                # start with ri #
                ri_list.remove(ri_dict[removed_name])
            except:
                ch_list.remove(ch_dict[removed_name])
            finally:
                self.AutoKeyDowner:bool = True
                return

        x ,y ,_x ,_y = (*pos ,*pos)

        _y:int = _y+2 if root.Animate else _y-2
        root.Animate:bool = not root.Animate
       
        __HP__ ,MP = info["__HP__"] ,info["MP"]
        HP:int = self.convert_HP(new=HP ,old=__HP__)

        element_name:str = show_abspath_single("element//"+element+".png")
        magic_pic:str = show_abspath_single(magic_pic)
        self.show_effects(x=x+50 ,y=y+35 ,info=info)
        self.pic(path=magic_pic ,x=x-36 ,y=y+50 ,animated=False ,resize=True ,pixel=False ,transparent=True ,colorkey=color[0] ,ratio=0.16)
        self.pic(path=show_abspath_single(name) ,x=_x ,y=_y ,animated=False ,resize=True ,pixel=False ,transparent=True ,colorkey=color[1] ,ratio=0.45)
        self.pic(path=element_name ,x=x+42 ,y=y+60 ,animated=False ,resize=False ,pixel=False ,transparent=True ,colorkey=color[1])
        self.show_HP_bar(HP ,x=x ,y=y)
        self.show_HP_bar(MP ,x=x ,y=y-12 ,target="MP")

    
    def convert_HP(self ,new:int ,old:int) -> int:
        return new*100//old
    

    def show_effects(self ,x:int ,y:int ,info:dict) -> NoReturn:
        """
        data -> Status -> effect -> dict[ str[effect_name] : tuple[1->round  0->buff/defuff <-> True/False] ]

        key ->  effect_name
        item -> tuple[round]
        """

        if not len((data:=info["Status"]["effect"])):
            return

        #base:list[str] = [*glob(show_abspath_single(r"buff/*")) ,*glob(show_abspath_single(r"debuff/*"))]
        base:str = show_abspath_single('')
        for index ,(key ,item) in enumerate(data.items()):
            mid:str = "buff" if item[0] else "debuff"
            self.pic(path=f"{base}{mid}//{key}.png" ,x=x ,y=y ,animated=False ,resize=True ,pixel=True ,transparent=True ,colorkey=(0 ,0 ,0) ,ratio=0.8)
            x ,y = x+30 ,y


    def PyBtn(path:str) -> Callable:
        def button(function:Callable) -> Callable:
            @warps(function)
            def decorator(* ,
                          x:int ,
                          y:int ,
                          pos:tuple[int ,int] ,
                          colorkey:tuple[int ,int ,int]
                          ) -> bool|None:

                btn_pic = pygame.image.load(path).convert_alpha()
                btn_pic.set_colorkey(colorkey)
                pic_w ,pic_h = btn_pic.get_width() ,btn_pic.get_height()
                if all([x <= pos[0] <= x+pic_w ,y <= pos[1] <= y+pic_h]):
                    function(x=x ,y=y ,pos=pos ,colorkey=colorkey)
            return decorator
        return button


    @staticmethod
    def battle(* ,
               ALL_CHARACTER:dict[str ,Any] ,
               ViceCharacter:list[Any] ,
               charge:int ,
               discs_getlist:list[tuple[Any]]
               ) -> int:
        charge:int = 0 if not charge else charge
        all_hurt:int = 0
                                    
        for index ,each in enumerate(discs_getlist ,start=1):           
            match each[2]:
                case "Accele":
                    print(f"{index} is Accele")
                    ALL_CHARACTER[each[3]].data["MP"] += randint(10 ,15)
                    
                case "Blast1" | "Blast2":
                    all_hurt += ALL_CHARACTER[each[3]].blast(ViceCharacter ,index=index ,charge=charge)
                    charge:int = 0
                    print(f"{index} is Blast")
                    continue
                
                case "Charge":
                    charge += 0b1
                    print(f"{index} is Charge")
                    
            all_hurt += ALL_CHARACTER[each[3]] >> ViceCharacter
            print(f"Disc{index} Fire!")
        return charge ,int(all_hurt)


    def show_all_hurt(self ,
                      all_hurt:int ,
                      * ,
                      target:Callable
                      ) -> NoReturn:
        self.simple_say(f"-{all_hurt}" ,x=target.x+66 ,y=target.y+30 ,color=(255 ,0 ,0))
        self.flash()
        sleep(1.26)


    def isOver(self ,
               * ,
               main_list:list ,
               vice_list:list
               ) -> bool:

        if not len(vice_list):
            showinfo("☺" ,"You Did It!")
            return False
        if not len(main_list):
            showinfo("ㄒoㄒ" ,"You Are Lost!")
            return False
        return True


    def SHOW_EFFECT_PIC(self ,character:Any) -> NoReturn:
        x_init ,y_init = 100 ,0
        x ,y = x_init ,y_init
        self.simple_pic(show_abspath_single("alpha_back.png") ,x=0 ,y=0 ,alpha=200 ,ratio=1.2)
        for index ,each in enumerate(character.style ,start=6):
            if index == 8:
                x ,y = x_init ,y_init+500
            self.simple_say(f"<{index}>" ,x=x-100 ,y=y ,color=(0 ,0 ,0) ,size=40)
            self.simple_pic(each ,x=x ,y=y ,alpha=245 ,ratio=0.45)
            x += 600


    def _SHOW_EFFECT_PIC(self ,character:Any) -> NoReturn:
        x_init ,y_init = 630 ,0
        x ,y = x_init ,y_init
        self.simple_pic(show_abspath_single("alpha_back.png") ,x=0 ,y=0 ,alpha=200 ,ratio=1.2)
        self.simple_pic(choice(character.self) ,x=0 ,y=0 ,ratio=0.81 ,alpha=210)
        self.simple_say(f"HP:{character.data['HP']}/{character.data['__HP__']}" ,x=50 ,y=H//2 ,color=(255 ,0 ,0) ,size=36)
        self.simple_say(f"MP:{character.data['MP']}/100" ,x=50 ,y=H//2+50 ,color=(0 ,190 ,255) ,size=36)
        self.simple_say(f"ATK:{character.data['ATK']}/{character.data['__ATK__']}" ,x=50 ,y=H//2+120 ,color=(255 ,160 ,30) ,size=36)
        self.simple_say(f"DEF:{character.data['DEF']}/{character.data['__DEF__']}" ,x=50 ,y=H//2+190 ,color=(100 ,180 ,55) ,size=36)
        ratio:float = 0.68 if len(re_findall(r".*?Memoria.*?" ,character.style[0])) else 0.45
        for index ,each in enumerate(character.style ,start=6):
            if index == 8:
                x ,y = x_init ,y_init+500
            self.simple_say(f"<{index}>" ,x=x-100 ,y=y ,color=(0 ,0 ,0) ,size=40)
            self.simple_pic(each ,x=x ,y=y ,alpha=245 ,ratio=ratio)
            x += 350
        else:
            pass


    def SHOW_MAIN_MENU(self ,MainFunc:Callable) -> Callable:
        @wraps(MainFunc)
        def MagicRecord(*args:tuple ,**kwargs:dict) -> NoReturn:
            clock ,run ,pointer ,animate ,FPS = pygame.time.Clock() ,True ,0b0 ,True ,10
            back:str = show_abspath_single(r"Menu.png")

            menu_mixer = SimpleMixer([0])
            #menu_mixer.air()
            menu_say:Callable = partial(self.simple_say ,font=r"magic record\font\SNAP____.TTF")
            menu_txt:tuple[dict] = (
                {"text":"Start" ,"color":(255 ,121 ,233)} ,
                {"text":"Load" ,"color":(97 ,255 ,255)} ,
                {"text":"Gallery" ,"color":(248 ,255 ,31)} ,
                {"text":"Config" ,"color":(255 ,0 ,0)} ,
                {"text":"Quit" ,"color":(0 ,0 ,0)}
                )
    
            while run:
                clock.tick(FPS)
                
                self.pic(path=back ,x=0 ,y=0 ,animated=animate ,resize=True ,pixel=True ,transparent=False ,ratio=1.6)
                if animate:
                    sleep(0.2)
                    animate:bool = False

                for index ,each in enumerate(menu_txt ,start=1):
                    menu_say(each["text"] ,W//2-100 ,H//3+80*index ,color=each["color"] ,size=52)

                pygame.draw.circle(self.screen ,menu_txt[pointer]["color"] ,(W//2-130 ,H//3+80*(pointer+1)+34) ,16 ,width=0)

                self.flash()
                
                pygame.event.set_allowed([KEYDOWN ,QUIT])
                for event in pygame.event.get():
                    match event.type:
                        case pygame.QUIT:
                            run:bool = not run
                            break
                        case pygame.KEYDOWN:
                            try:
                                match event.key:
                                    case pygame.K_w|pygame.K_UP|pygame.K_a|pygame.K_LSHIFT|pygame.K_LEFT:
                                        pointer:int = abs((pointer - 1) % 5)
                                    case pygame.K_s|pygame.K_DOWN|pygame.K_d|pygame.K_RSHIFT|pygame.K_RIGHT:
                                        pointer:int = (pointer + 1) % 5
                                    case pygame.K_RETURN|pygame.K_SPACE:
                                        match pointer:
                                            case 0:
                                                MainFunc(FPS ,**kwargs)
                                                print("\n*Game Over*")
                                                return
                                            case 1:
                                                print(1)
                                            case 2:
                                                print(2)
                                            case 3:
                                                pointer3:int = 0
                                                """
                                                while True:
                                                    break
                                                    EVENT = pygame.event.wait()
                                                    if EVENT.type == pygame.QUIT:
                                                        pygame.quit()
                                                        return
                                                    elif EVENT.type == pygame.KEYDOWN:
                                                        match EVENT.key:
                                                            case pygame.K_LEFT|pygame.K_LSHIFT:
                                                                pass
                                                """
                                                
                                            case 4:
                                                pygame.quit()
                                                return
                                            case _:
                                                pass
                                    case _:
                                        pass
                            except ValueError:
                                print("*** ***")
        return MagicRecord



if __name__ == "__main__":
    #effect = SimpleEffect("Ultimate_Madoka_Sprite")
    #effect.effect('start')
    screen = PyScreen(size=(W ,H) ,name="test")

    #menu:Callable = screen.SHOW_MAIN_MENU()

    #menu()

    ###screen.simple_pic(show_abspath_single("back1.jpg") ,x=0 ,y=0)
    #path = show_abspath_single("Ultimate_Madoka_Sprite//Ultimate_Madoka_Sprite.png")
    #screen.pic(path=path ,x=0 ,y=0 ,animated=False ,resize=True ,pixel=False ,transparent=True ,colorkey=(255 ,255 ,255) ,ratio=0.5)
    
    ###screen.character("Ultimate_Madoka_Sprite//Ultimate_Madoka_Sprite.png" ,pos=Grid.re_c3l1 ,element="Light" ,info={"__HP__":22345 ,"HP":22345 ,"MP":100})
    ###screen.character("Iroha_Miko//Iroha_Miko.png" ,pos=Grid.re_c3l2 ,element="Light" ,info={"__HP__":23121 ,"HP":12345 ,"MP":80})
    ###screen.character("Nanami_Yachiyo/Nanami_Yachiyo.png" ,pos=Grid.re_c3l3 ,element="Water" ,info={"__HP__":20000 ,"HP":10000 ,"MP":10})
    
    ###screen.flash()

    pass






