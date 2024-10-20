# -*- coding: utf-8 -*-

__all__:list = ["Skill" ,"test"]

class Skill(object):

    @classmethod
    def re(cls ,
           * ,
           discs_getlist:list ,
           Character ,
           discs_getdict:dict ,
           re_all:tuple
           ) -> dict[str ,tuple]:

        discs_getlist[:]:list = []
        discs_getdict = {}
        return Character.shuffle_disc(*tuple(re_all))

    class Buff(object):

        @classmethod
        def HP(cls ,
               __HP__:int ,
               * ,
               level:int = 1 ,
               init:float = 0.12) -> int:
            """
            Skill HP
                单次回复HP

            level:
                Ⅰ -> 0.12
                Ⅱ -> 0.18
                Ⅲ -> 0.24
                Ⅳ -> 0.30
                Ⅴ -> 0.36   
            """
            if level > 5:
                raise AttributeError
            return int(__HP__*init*level)


        @classmethod
        def MP(cls ,
               * ,
               level:int = 1 ,
               init:int = 12
               ) -> int:
            if level > 3:
                raise AttributeError
            return level*init

        @classmethod
        def defUP(cls ,
                  __DEF__:int ,
                  * ,
                  level:int = 1 ,
                  init:int = 0.10
                  ) -> int:
            """
            Skill def_UP
                增加防御力

            level:
                Ⅰ -> 0.10
                Ⅱ -> 0.14
                Ⅲ -> 0.20
                Ⅳ -> 0.26
                Ⅴ -> 0.32 
                
            """
            if any([level<0 ,level>5]):
                raise AttributeError
            return int(__DEF__*level*init)
            

    class Debuff(object):

        pass

    class Effect(object):

        @classmethod
        def HP_plus(cls ,
                    __HP__:int ,
                    * ,
                    level:int = 1 ,
                    init:int = 0.10) -> int:
            """
            Skill HP_plus
                自动回复HP

            level:
                Ⅰ -> 0.10
                Ⅱ -> 0.14
                Ⅲ -> 0.20
                Ⅳ -> 0.26
                Ⅴ -> 0.32 
                
            """
            if level > 5:
                raise AttributeError
            return int(__HP__*init*level)


        @classmethod
        def ATK_plus(cls ,
                     * ,
                     level:int = 1 ,
                     init:float = 0.05) -> int:
            """
            Skill def_UP
                持续增伤

            level:
                Ⅰ -> 0.05
                Ⅱ -> 0.10
                Ⅲ -> 0.15
                Ⅳ -> 0.20
                Ⅴ -> 0.25
                
            """
            if not 0 < level <= 5:
                raise AttributeError
            return int(1+init*level)


        @classmethod
        def atkUP(cls ,
                  ATK:int ,
                  __ATK__:int ,
                  * ,
                  level:int = 1 ,
                  init:float = 0.05) -> int:
            """
            Skill def_UP
                增加防御力

            level:
                Ⅰ -> 0.05
                Ⅱ -> 0.10
                Ⅲ -> 0.15
                Ⅳ -> 0.20
                Ⅴ -> 0.25
                
            """
            if not 0 < level <= 5:
                raise AttributeError
            return int(ATK + __ATK__*init*level)


def test():
    print(123456)













            
