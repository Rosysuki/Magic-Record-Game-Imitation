# -*- coding: utf-8 -*-

'''__all__:list = []'''

from PyScreen import *
from Skill import *
from abc import ABC ,abstractmethod
from pprint import pprint

def show_skills(pos:tuple[int ,int] ,
                * ,
                x:int ,
                y:int ,
                ratio:float = Grid.ratio ,
                size:int = 512
                ) -> bool:
    """
    function show_skills
        pos <-> bool
        pos = event.pos
    """
    
    return all([x <= pos[0b0] <= x+size*ratio ,y <= pos[0b1] <= y+size*ratio])


## -*- Character ABC -*- ##


class Character(ABC):
    
    """
    class Character
        abstract class

    note keyboard:
        12345 -> disc
        tab -> character

    !!! disc & character
        
    """

    @staticmethod
    def test() -> NoReturn:
        print("This Is Test!")

    @staticmethod
    def shuffle_disc(*discs:tuple[dict[str ,tuple[Any ,Any]]]) -> dict[int ,tuple[Any ,Any]]:
        """
        function Character.shuffle_disc
            shuffle all character's discs!
            
        :param discs
            args

        HAVE DOWNTIME!
        """
        before_shuffle:list[tuple[Any ,Any]] = [item for each in discs for index ,(key ,item) in enumerate(each.items())]
        shuffle(before_shuffle)
        chosen:list[tuple[Any ,Any]] = [choice(before_shuffle) for _ in range(5)]
        after_shuffle:list[tuple[Any ,Any]] = [each+(time()+index ,) for index ,each in enumerate(chosen ,start=1)]
        return dict(zip(range(1 ,6) ,after_shuffle))


    def __init__(self ,
                 name:str ,
                 pos:tuple[int ,int] ,
                 * ,
                 root:Self ,
                 skill:dict[str ,Callable] ,
                 element:str ,
                 data:dict[str ,int] ,
                 character:Callable
                 ) -> NoReturn:
        """
        function Character.__init__

        :param data
            HP __HP__ MP
            ATK DEF
            :Status
                :hurt
                :any effect...

        :arg character
            #name :str
            info :dict[HP ,__HP__ ,MP]

        :super
            :param
                pos:tuple[int ,int]
                character:Callable

        :note
            data != info
            info ∈ data
            data -> info

            name is abs_name
            _name is real name
        """
        self.skill:dict[str ,Callable] = skill
        self.name:str = r"{}/{}.png".format(name ,name)
        self.character:Callable = partial(character ,name=self.name ,element=element ,pos=pos ,root=root)
        self.data ,self.element ,self.x ,self.y = (data ,element ,*pos)
        self.info:dict[str ,int] = {key:item for index ,(key ,item) in enumerate(data.items()) if key in {"HP" ,"__HP__" ,"MP"}}
        self._name:str = name
        self.effect = SimpleEffect(self._name)
        self.style:list[str] = glob(r"magic record\items\style\{}\*.png".format(name))
        self.self:list[str] = glob(r"magic record\items\style\{}\*.jpg".format(name))
        print("Create Character OK!")

        #self.name:str = name


    def __init_subclass__(self) -> NoReturn:
        self.Animate:bool = True


    def set_skill(self ,skill:dict[str ,Callable]) -> NoReturn:
        self.skill:dict = skill


    def reinfo(self ,**info:dict[dict[str ,int]]) -> NoReturn:
        try:
            self.info:dict[str ,int] = info["info"]
        except KeyError as KE:
            self.info:dict[str ,int] = {key:item for index ,(key ,item) in enumerate(data.items()) if key in {"HP" ,"__HP__" ,"MP"}}
        pass

    
    def status_effort(self) -> NoReturn:
        pass

    
    def cal_hurt(self) -> NoReturn:
        pass


    @property
    def disc(self) -> dict[str ,tuple[Any ,Any]]:
        """
        res:
            {
                "" : (pic ,pic ,"")
            }
        """
        another:dict[str ,Any] = {}
        for index ,each in enumerate(iglob(show_abspath_single("disc/*.png")) ,start=1):
            basename:str = path.basename(each)
            character ,disc = pygame.image.load(show_abspath_single(self.name)).convert_alpha() ,pygame.image.load(each).convert_alpha()
            character ,disc = pygame.transform.rotozoom(character ,0 ,0.3) ,pygame.transform.rotozoom(disc ,0 ,0.68)
            character.set_colorkey((255 ,255 ,255))
            disc.set_colorkey((255 ,255 ,255))
            character.set_alpha(220)
            name:str = basename[:basename.index('.')] #discs name
            another[f"{name}"]:dict = (disc ,character ,name ,self._name)
        else:
            return another


    @staticmethod
    def pic_disc(screen:Any ,
                 disc:dict[str ,tuple[Any ,Any]] ,
                 x:int ,
                 y:int ,
                 gap:int = 160 ,
                 *args:tuple
                 ) -> NoReturn:
        
        if not len(disc):
            return
        
        if isinstance(disc ,dict):
            if not len(args):
                for index ,(key ,item) in enumerate(disc.items()):
                    screen.blit(item[0] ,(x ,y))
                    screen.blit(item[1] ,(x+10 ,y-40))
                    x:int = x + gap
        else:
            for index ,each in enumerate(disc):
                screen.blit(each[0] ,(x ,y))
                screen.blit(each[1] ,(x+10 ,y-40))
                x:int = x + gap


    @staticmethod
    def disc_pos(* ,
                 x:int ,
                 y:int ,
                 gap:int = 160
                 ) -> list[tuple[int ,int]]:
        
        return [(x:=x+gap ,y) for _ in range(5)]


    def blast(self ,
              target:Callable ,
              * ,
              charge:int ,
              index:int
              ) -> int:
        """
        index 1-3
        """
        all_hurt:int = (self.data["ATK"] - target.data["DEF"]//2)*self.data["Status"]["hurt"]*(1.0+0.08*(index-1))*(charge+1) + randint(0 ,100)
        target.data["HP"] -= all_hurt
        return all_hurt
        

    #@abstractmethod
    def __lshift__(self ,keyboard:str) -> NoReturn:
        """
        function Character.__lshift__
            buff / debuff

        example:
            main << keyboard
        """
        pass


    #@abstractmethod
    def __rshift__(self ,target) -> NoReturn:
        """
        function Character.__rshift__
            target.HP --
        """
        #target.data["HP"] -= (self.data["ATK"] - target.data["DEF"]//3)*self.data["Status"]
        all_hurt:int = (self.data["ATK"] - target.data["DEF"]//3)*self.data["Status"]["hurt"] + randint(0 ,100)
        target.data["HP"] -= all_hurt
        return all_hurt


    @staticmethod
    def skill(namelist:list[str ,str ,str ,str] ,
                  * ,
                  file:str = r"magic record\items\memoriaDATA2.dat" ,
                  keys:list[str] = ["type" ,"name" ,"ATK" ,"DEF" ,"HP"]
                  ) -> dict[str:dict[str:Any]]|None:

        if len(namelist) != 4:
            print("Every Character Have Four Skill!")
            return None

        final:dict = {}
        with open(file ,'r' ,encoding='utf-8') as f:
            data:dict[str:dict[str:Any]] = eval(eval(f.read()))
            
        for index ,each in enumerate(namelist ,start=6):
            now ,gap = randint(1 ,3) ,randint(8 ,12)
            init:dict = {
                "init":{"now":now ,"gap":gap} ,"now":now ,"gap":gap ,"open":False ,"type":'' ,"name":'' ,
                "ATK":0 ,"DEF":0 ,"HP":0
            }

            another:dict = data[each]
            for i ,e in enumerate(keys):
                init[e] = eval(another[e].rstrip('\n')) if e not in {"type" ,"name"} else another[e]
            else:
                final[str(index)]:dict[str:dict] = init
        else:
            return final


## -*- New Character Template -*- ##

class Template(Character):
    """
    class Template

    """


    def __init__(self ,
                 name:str ,
                 * ,
                 HP:int ,
                 ATK:int ,
                 DEF:int ,
                 pos:tuple[int ,int] ,
                 character:Callable ,
                 skill:dict[str ,Any],
                 toward:str = ''  ,
                 MP:int = 0 ,
                 __lshift__:Callable = None ,
                 __rshift__:Callable = None
                 ) -> NoReturn:
        """
        function self.__init__

        :param character
            constantly eq screen.character

        :param skill
            {
                '6':{
                    "init":{"now":1 ,"gap":8} ,"now":1 ,"gap":8 ,"open":False ,"type":"skill"/"ability" ,"name":"渺小的真正的希望" ,ATK/HP/DEF
                }
                
                '7':{
                }
                ...
            }

        :note
            _skill -> dict
            skill  -> list[str]
        """

        name:str = "re_"+name if toward == "re" else name
        _skill:dict[str:Any] = Character.skill(skill)
        
        for index ,(key ,item) in enumerate(_skill.items()):
            ATK ,DEF ,HP = ATK+item["ATK"] ,DEF+item["DEF"] ,HP+item["HP"]
        
        data:dict[str ,int] = {
            "HP":HP ,"__HP__":HP ,"ATK":ATK ,"__ATK__":ATK ,"DEF":DEF ,"__DEF__":DEF ,"MP":MP ,"magic":None ,"alive":True ,
            "Status":{
                "hurt":1.0 ,"effect":{}
                }
            }
        
        super(Template ,self).__init__(name ,pos ,skill=_skill ,element="Light" ,data=data ,character=character ,root=self)
        self.skill_dict:dict[str ,dict[Any]] = _skill
        self.style:list[str] = [r"magic record\items\Memoria\{}.png".format(each) for each in skill]
        self.__lshift__: Callable = __lshift__
        self.__rshift__: Callable = __rshift__


    def __rper__(self) -> repr:
        return self._name



## -*- Bad Character Creator -*- ##

    
class Ultimate_Madoka_Sprite(Character):

    def __init__(self ,
                 * ,
                 skill:dict[str ,Callable] ,
                 pos:tuple[int ,int] ,
                 character:Callable ,
                 toward:str = ''
                 ) -> NoReturn:
        """
        function Ultimate_Madoka_Sprite.__init__

        :note
            name != self.name

            call character -> info -> data

        data -> Status -> effect -> dict[ str[effect_name] : tuple[0->round  1->] ]
        
        """

        name:str = "re_Ultimate_Madoka_Sprite" if toward == "re" else "Ultimate_Madoka_Sprite"
        self.repr_name:str = name
        #skill:dict[str ,Callable] = {}
        
        data:dict[str ,int] = {
            "HP":29143 ,"__HP__":29143 ,"ATK":9114 ,"__ATK__":9114 ,"DEF":6265 ,"__DEF__":6265 ,"MP":10 ,"magic":None ,"alive":True ,
            "Status":{
                "hurt":1.0 ,"effect":{}
                }
            }

        # 6 7 8 9 0 #
        data["__HP__"] = data["HP"] = data["__HP__"] + 1125 + 2225 + 2125 + 1825
        data["__DEF__"] = data["DEF"] = data["__DEF__"] + 1225 + 0 + 0 + 2225
        data["__ATK__"] = data["ATK"] = data["__ATK__"] + 0 + 1825 + 0 + 1912
        
        super(Ultimate_Madoka_Sprite ,self).__init__(name ,pos ,skill=skill ,element="Light" ,data=data ,character=character ,root=self)
        print(f"Create {name} OK!")

        #
        self.skill_dict:dict = {
                                '6' : {
                                    "init":{"now":1 ,"gap":8} ,"now":1 ,"gap":8 ,"open":False ,"type":"skill" ,"name":"渺小的真正的希望"} ,
                                '7' : {
                                    "init":{"now":2 ,"gap":None} ,"now":2 ,"gap":None ,"open":False ,"type":"ability" ,"name":"在诞生的光芒中"} ,
                                '8' : {
                                    "init":{"now":3 ,"gap":8} ,"now":3 ,"gap":8 ,"open":False ,"type":"skill" ,"name":"不会绝望的希望之光"} ,
                                '9' : {
                                    "init":{"now":2 ,"gap":None} ,"now":2 ,"gap":None ,"open":False ,"type":"ability" ,"name":"现在，这样就好"}
                                }

        Ultimate_Madoka_Sprite.test()


    def countdown(self) -> NoReturn:
        for index ,(board ,item) in enumerate(self.skill_dict.items()):

            if not item["open"]:
                continue

            else:
                if item["now"]:
                    item["now"] -= 1
                    self.SkillUP(board)
                    continue
                
            # now == 0 #
            if item["open"]: # initialize #
                self.SkillDOWN(board)
                item["open"]:bool = False
            
            if item["gap"] is None:
                continue
            else:
                if item["gap"]:
                    item["gap"] -= 1
                    continue
                
            # gap == 0 #
            item["now"] ,item["gap"] = item["init"]["now"] ,item["init"]["gap"]
            #self.SkillDOWN(board)
            print(f"< KEY {board} READY! >")


    def SkillUP(self ,keyboard:str) -> NoReturn:
        match keyboard:
            case '6':
                pass
            case '7':
                print(f"UP ATK -> {self.data['ATK']}")
                self.data["ATK"] = Skill.Effect.atkUP(self.data["ATK"] ,self.data["__ATK__"] ,level=4)
                self.data["Status"]["effect"]["attackUP"]:tuple[bool ,int] = (True ,1)
                print(f"UP ATK -> {self.data['ATK']}")
            case '8':
                pass
            case '9':
                self.data["Status"]["effect"]["HP+"]:tuple[bool ,int] = (True ,2)
                self.data["Status"]["effect"]["hurtUP"]:tuple[bool ,int] = (True ,2)
                self.data["HP"]=self.data["__HP__"] if (HP:=self.data["HP"]+Skill.Effect.HP_plus(self.data["__HP__"] ,level=3))>=self.data["__HP__"] else HP
                self.data["Status"]["hurt"]:float = Skill.Effect.ATK_plus(level=4)


    def SkillDOWN(self ,keyboard:str) -> NoReturn:
        match keyboard:
            case '6':
                pass
            case '7':
                print(f"DOWN ATK -> {self.data['ATK']}")
                self.data["ATK"]:int = self.data["__ATK__"]
                self.data["Status"]["effect"].pop("attackUP")
                print(f"DOWN ATK -> {self.data['ATK']}")
            case '8':
                pass
            case '9':
                self.data["Status"]["effect"].pop("HP+")
                self.data["Status"]["effect"].pop("hurtUP")
                self.data["Status"]["hurt"]:float = 1.0
                print(f"*** KEY {keyboard} PAUSED! ***")
                        

    def __lshift__(self ,keyboard:str) -> NoReturn:

        if keyboard in {'6' ,'7' ,'8' ,'9'} and not (skill := self.skill_dict[keyboard])["open"]: # open False Enter! #
            skill["open"]:bool = True
            self.SkillUP(keyboard)
            print(f"***KEY {keyboard} OK!***\t{self.skill_dict[keyboard]['open']}")
        else:
            print(f"< SHOW KEY{keyboard} FAIL! >")
            showerror("X" ,f"暂不支持{keyboard}键!")

        """
        match keyboard:
            case 'q':
                #if (HP := self.data["HP"]+self.skill['q'](__HP__=self.data["__HP__"])) >= self.data["__HP__"]:
                #    self.data["HP"]:int = self.data["__HP__"]
                #else:
                #    self.data["HP"] += self.skill['q'](__HP__=self.data["__HP__"])
                
                if (HP := self.data["HP"]+self.skill['q'](__HP__=self.data["__HP__"])) >= self.data["__HP__"]:
                    self.data["HP"]:int = self.data["__HP__"]
                else:
                    self.data["HP"]:int = HP

                self.data["Status"]["effect"]["HP+"] = (True ,3)
                    
            case 'a':
                if (MP := self.data["MP"]+self.skill['a']()) >= 100:
                    self.data["MP"]:int = 100
                else:
                    self.data["MP"] += self.skill['a']()
                    
            case _ : showerror("X" ,f"暂不支持{keyboard}键!")
            """


    def __rshift__(self ,target:Character) -> NoReturn:
        all_hurt:int = (self.data["ATK"] - target.data["DEF"]//3)*self.data["Status"]["hurt"] + randint(0 ,100)
        target.data["HP"] -= all_hurt
        return all_hurt # *disc_hurt

    def __rrshift__(self ,target:Any) -> NoReturn:
        """
        function __rrshift__
            When you hurt by target ,namely < target>>self >.
        """
        print(111111)
        self.data["MP"] = 100 if (MP:=self.data["MP"]+randint(8 ,12)) <= 100 else MP

    def __repr__(self) -> repr:
        return self.repr_name


class Iroha_Miko(Character):

    def __init__(self ,
                 * ,
                 skill:dict[str ,Callable] ,
                 pos:tuple[int ,int] ,
                 character:Callable ,
                 toward:str = ""
                 ) -> NoReturn:
        """
        function Ultimate_Madoka_Sprite.__init__

        :note
            name != self.name

            call character -> info -> data
        """

        name:str = "re_Iroha_Miko" if toward == "re" else "Iroha_Miko"
        data:dict[str ,int] = {
            "HP":30003 ,"__HP__":29143 ,"MP":20 ,"ATK":8547 ,"DEF":8606 ,"__ATK__":8547 ,"__DEF__":8606 ,"alive":True ,
            "Status":{
                "hurt":1.0 ,"effect":{}
                }
            }
        super(Iroha_Miko ,self).__init__(name ,pos ,skill=skill ,element="Light" ,data=data ,character=character ,root=self)
        print(f"Create {name} OK!")
        #Iroha_Miko.test()

    def __lshift__(self ,keyboard:str) -> NoReturn:
        match keyboard:
            case 'w':
                if (HP := self.data["HP"]+self.skill['q'](__HP__=self.data["__HP__"])) >= self.data["__HP__"]:
                    self.data["HP"]:int = self.data["__HP__"]
                else:
                    self.data["HP"] += self.skill['q'](__HP__=self.data["__HP__"])
                    
            case 's':
                if (MP := self.data["MP"]+self.skill['a']()) >= 100:
                    self.data["MP"]:int = 100
                else:
                    self.data["MP"] += self.skill['a']()
                    
            case _ : showerror("X" ,f"暂不支持{keyboard}键!")

    def __rshift__(self ,target:Character) -> NoReturn:
        all_hurt:int = (self.data["ATK"] - target.data["DEF"]//3)*self.data["Status"]["hurt"] + randint(0 ,100)
        target.data["HP"] -= all_hurt
        return all_hurt

    def __repr__(self) -> repr:
        return "re_Iroha_Miko"


class Nanami_Yachiyo(Character):

    def __init__(self ,
                 * ,
                 skill:dict[str ,Callable] ,
                 pos:tuple[int ,int] ,
                 character:Callable ,
                 toward:str = ""
                 ) -> NoReturn:
        """
        function Ultimate_Madoka_Sprite.__init__

        :note
            name != self.name

            call character -> info -> data
        """

        name:str = "re_Nanami_Yachiyo" if toward == "re" else "Nanami_Yachiyo"
        data:dict[str ,int] = {
            "HP":30003 ,"__HP__":29143 ,"MP":20 ,"ATK":8547 ,"DEF":8606 ,"__ATK__":8547 ,"__DEF__":8606 ,"alive":True ,
            "Status":{
                "hurt":1.0 ,"effect":{}
                }
            }
        super(Nanami_Yachiyo ,self).__init__(name ,pos ,skill=skill ,element="Light" ,data=data ,character=character ,root=self)
        print(f"Create {name} OK!")
        #Iroha_Miko.test()

    def __lshift__(self ,keyboard:str) -> NoReturn:
        match keyboard:
            case 'w':
                if (HP := self.data["HP"]+self.skill['q'](__HP__=self.data["__HP__"])) >= self.data["__HP__"]:
                    self.data["HP"]:int = self.data["__HP__"]
                else:
                    self.data["HP"] += self.skill['q'](__HP__=self.data["__HP__"])
                    
            case 's':
                if (MP := self.data["MP"]+self.skill['a']()) >= 100:
                    self.data["MP"]:int = 100
                else:
                    self.data["MP"] += self.skill['a']()
                    
            case _ : showerror("X" ,f"暂不支持{keyboard}键!")


    def __rshift__(self ,target:Character) -> int:
        all_hurt:int = (self.data["ATK"] - target.data["DEF"]//3)*self.data["Status"]["hurt"] + randint(0 ,100)
        target.data["HP"] -= all_hurt
        return all_hurt


    def __repr__(self) -> repr:
        return "Nanami_Yachiyo"



if __name__ == "__main__":
    """
    madoka_skill:dict[str ,Callable] = {'q':Skill.Buff.HP}
    
    screen:PyScreen = PyScreen(size=(W ,H) ,name="MAIN")
    screen.root.fill((100 ,0 ,200))
    madoka:Character = Ultimate_Madoka_Sprite(pos=Grid.c1l2 ,character=screen.character ,skill=madoka_skill)
    #madoka.character(info=madoka.data)

    #madoka.pic_disc(screen.root ,madoka.disc ,x=0 ,y=H-120)
    madoka.pic_disc(screen.root ,Character.shuffle_disc(madoka.disc) ,x=190 ,y=H-130)
    screen.flash()
    """
    
    #print(Character.disc_pos(x=0 ,y=10 ,gap=10))

    #pprint(Character.skill(["Begin a Hunt" ,"少女的决心" ,"盛装出行" ,"三位天才"]))

    #test:Character = Template("Iroha_Miko" ,
    #                          HP=12345 ,ATK=1234 ,DEF=123 ,
    #                          pos=(100 ,100))
    pass


"""
(self ,
 name:str ,
 * ,
 HP:int ,
 ATK:int ,
 DEF:int ,
 pos:tuple[int ,int] ,
 character:Callable ,
 skill:dict[str ,Any],
 toward:str = ''  ,
 MP:int = 0
 ) -> NoReturn:
"""





