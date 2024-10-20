# -*- coding: utf-8 -*-

__all__:list = []

from Character import *
from pprint import pprint

screen:Callable = PyScreen(size=(W ,H) ,name="MAIN")


@screen.SHOW_MAIN_MENU
def main(*args:tuple ,**kwargs:dict) -> NoReturn:
    """
    MainCharacter is utilised when buff/defuff

    : arg discs
        0      1          2          3
        (disc ,character ,disc_name ,self._name)

    :note
        character_list  ->  main_list
        ALL_CHARACTER   ->  main_dict

        rival_list      ->  vice_list
        rival           ->  vice_dict
        ALL_VICE_CHARACTER  ->  vice_dict
        
    """

    #mixer = SimpleMixer(fromlist=glob(r"magic record/items/music/*"))
    #MyMixer = Thread(target=mixer.run ,name="music")
    #MyMixer.start()

    charge:int = 0b0
    all_hurt:int = None
    TIMESTAPM:float = time()

    #death_vice:list = []
    #death_main:list = []
    
    clock ,run ,disc_ok ,pointer ,_pointer ,rounds = pygame.time.Clock() ,True ,False ,0b0 ,0b0 ,0b1
    madoka_skill:dict[str ,Callable] = {'q':Skill.Effect.HP_plus ,'a':Skill.Buff.MP}
    
    #screen:PyScreen = PyScreen(size=(W ,H) ,name="MAIN")
    root:Callable = screen.character

    test:Character = Template("Iroha_Miko" ,
                              HP=30003 ,ATK=8547 ,DEF=8606 ,MP=50 ,
                              pos=Grid.c2l2 ,
                              character=root ,
                              skill=["Begin a Hunt" ,"少女的决心" ,"盛装出行" ,"三位天才"] ,
                              )
    
    madoka:Character = Ultimate_Madoka_Sprite(pos=Grid.c1l1 ,character=root ,skill=madoka_skill)
    re_madoka:Character = Ultimate_Madoka_Sprite(pos=Grid.re_c3l1 ,character=root ,skill=madoka_skill ,toward='re')
    iroha_miko:Character = Iroha_Miko(pos=Grid.re_c2l2 ,character=root ,skill=madoka_skill ,toward="re")#
    nanami_yachiyo:Character = Nanami_Yachiyo(pos=Grid.c3l3 ,character=root ,skill=madoka_skill)

    discs:dict[str ,tuple[Any ,Any]] = Character.shuffle_disc(madoka.disc ,nanami_yachiyo.disc ,test.disc) #@TEST@#
    memoria:dict[str ,tuple[Any ,Any]] = {**discs}
    #vice_discs:dict[str ,tuple[Any ,Any]] = Character.shuffle_disc(iroha_miko.disc ,re_madoka.disc)
    discs_getlist:list[tuple] = []
    discs_getdict:dict[tuple ,Character] = {}
    

    character_list:list = [madoka ,nanami_yachiyo ,test] #@TEST@#
    
    rival_name:list = [iroha_miko._name ,re_madoka._name]
    rival_list:list = [iroha_miko ,re_madoka]
    rival:dict[str ,Character] = dict(zip(rival_name ,rival_list))
    ALL_VICE_CHARACTER = rival

    InitCharLen:int = len(character_list)
    InitViceLen:int = len(rival_list)

    MainCharacter:Callable = character_list[pointer]
    ViceCharacter:Callable = rival_list[_pointer]
    
    pointer:int = (pointer + 1) % len(character_list)
    disc_pos:list[tuple[int ,int]] = Character.disc_pos(x=190 ,y=H-130) #gap=160

    our_name:list[str] = [madoka._name ,nanami_yachiyo._name ,test._name] #@TEST@#
    ALL_CHARACTER:dict[str ,Character] = dict(zip(our_name ,character_list))
    #print(ALL_CHARACTER)

    choice(character_list).effect.effect("start")

    # *Partial Function* #
    re_all:list = [each.disc for each in character_list]
    re:Callable = partial(Skill.re ,discs_getlist=discs_getlist ,discs_getdict=discs_getdict ,Character=Character)

    # * TEST * #
    #madoka.data["Status"]["effect"]["HP+"] = (True ,1)

    #print("ALL_CHARACTER:" ,ALL_CHARACTER)
    #print("character_list" ,character_list)
    #return


    def SHOWTIME() -> NoReturn: #@TEST@#
        """
        function SHOWTIME
            show all-character in screen

        """
        #screen.SHOW_EFFECT_PIC(pos=() ,character=MainCharacter)
        screen.simple_pic(show_abspath_single("back1.jpg") ,x=0 ,y=0)
        screen.simple_say(text=f"Round{rounds}" ,x=20 ,y=H-120 ,color=(255 ,0 ,0) ,size=40)
        #screen.simple_say(text=f"Time{abs(int(TIMESTAPM-time()))}s" ,x=20 ,y=H-40 ,color=(238 ,138 ,248))
        screen.simple_say(text=f"{MainCharacter}" ,x=W//2-150 ,y=10 ,color=(145 ,255 ,214))
        screen.show_rival(x=ViceCharacter.x+20 ,y=ViceCharacter.y+36 ,color=(214 ,255 ,233) ,size=220)
        screen.show_chara(x=MainCharacter.x+20 ,y=MainCharacter.y+36 ,color=(255 ,20 ,240) ,size=220)

        #screen.simple_pic(r"C:\Users\sfuch\Desktop\Download\117791959_p1_master1200.jpg" ,x=0 ,y=0)
        
        madoka.character(info=madoka.data ,
                         ch_dict=ALL_CHARACTER ,
                         ch_list=character_list ,
                         ri_list=rival_list ,
                         ri_dict=rival)
        
        iroha_miko.character(info=iroha_miko.data ,
                             ch_dict=ALL_CHARACTER ,
                             ch_list=character_list ,
                             ri_list=rival_list ,
                             ri_dict=rival)
        
        nanami_yachiyo.character(info=nanami_yachiyo.data ,
                                 ch_dict=ALL_CHARACTER ,
                                 ch_list=character_list ,
                                 ri_list=rival_list ,
                                 ri_dict=rival)
        
        re_madoka.character(info=re_madoka.data ,
                            ch_dict=ALL_CHARACTER ,
                            ch_list=character_list ,
                            ri_list=rival_list ,
                            ri_dict=rival)

        test.character(info=test.data ,
                       ch_dict=ALL_CHARACTER ,
                       ch_list=character_list ,
                       ri_list=rival_list ,
                       ri_dict=rival)

    while run:

        clock.tick(args[0])
        pygame.event.set_allowed([MOUSEBUTTONDOWN ,MOUSEMOTION ,KEYDOWN ,QUIT])

        if screen.AutoKeyDowner:
            InitCharLen ,InitViceLen = len(character_list) ,len(rival_list)
            _pointer ,pointer = (_pointer + 1) % InitViceLen ,(pointer + 1) % InitCharLen
            MainCharacter ,ViceCharacter = character_list[pointer] ,rival_list[_pointer]
            screen.AutoKeyDowner:bool = False
            re_all:list = [each.disc for each in character_list]
            re:Callable = partial(Skill.re ,discs_getlist=discs_getlist ,discs_getdict=discs_getdict ,Character=Character)
            if not (run := screen.isOver(main_list=character_list ,vice_list=rival_list)):
                break

        SHOWTIME()

        # * three-discs * #
        Character.pic_disc(screen.root ,discs_getlist ,x=20 ,y=10 ,gap=136)
        
        #if not disc_ok:
        Character.pic_disc(screen.root ,discs ,x=190 ,y=H-130)

        if charge:
            #screen.simple_pic(show_abspath_single(r"disc/Charge.png") ,x= ,y=)
            screen.simple_say(f"Charge{charge}" ,x=20 ,y=H-80 ,color=(240 ,255 ,16) ,size=38)
            
        screen.flash()

        for event in pygame.event.get():
            match event.type:

                case pygame.KEYDOWN:
                    KEY = pygame.key.get_pressed()

                    if KEY[pygame.K_0]:
                        print(111)
                        break

                    if KEY[pygame.K_RIGHT]:
                        MainCharacter:Callable = character_list[pointer]
                        pointer:int = (pointer + 1) % InitCharLen
                        break

                    if KEY[pygame.K_LEFT]:
                        _pointer:int = (_pointer + 1) % InitViceLen
                        ViceCharacter:Callable = rival_list[_pointer]
                        break

                    if KEY[pygame.K_TAB]:
                        #discs:dict[str ,tuple[Any ,Any]] = re()
                        discs_getlist[:]:list = []
                        discs_getdict:dict = {}
                        discs = {**memoria}
                        #Character.pic_disc(screen.root ,memoria ,x=190 ,y=H-130)
                        break

                    if KEY[pygame.K_p]:
                        print(f"\ndiscs_dict:{discs_getdict}\n")
                        print(f"\ndiscs_list:{discs_getlist}\n")

                    try:
                        match (key := chr(event.key)):
                            case '1'|'2'|'3'|'4'|'5':
                                if len(discs_getlist) >= 3:
                                    break
                                for index ,(keys ,items) in enumerate(discs.items() ,start=1):
                                    #print(index ,key ,item)
                                    if keys == eval(key):
                                        ALL_CHARACTER[items[3]].effect.effect("choose")
                                        discs_getlist.append(items) #item is dict
                                        discs_getdict[items] = ViceCharacter
                                        try:
                                            discs.pop(keys)
                                        except KeyError as KE:
                                            pass
                                        print(f"append disc {index} ok!")
                                        break

                            case '\r':
                                if len(discs_getlist) == 3:

                                    for index ,(DISC ,TARGET) in enumerate(discs_getdict.items()):
                                        charge ,all_hurt = PyScreen.battle(ALL_CHARACTER=ALL_CHARACTER ,
                                                                 ViceCharacter=TARGET ,
                                                                 charge=charge ,
                                                                 discs_getlist=[DISC])
                                        
                                        screen.show_all_hurt(all_hurt ,target=TARGET)
                                        SHOWTIME()
                                        screen.flash()
                                    else:
                                        discs_getdict:dict = {}
                                        
                                    #print(f"charge : {charge}\nall_hurt : {all_hurt}")

                                    #re_all:list = [each.disc for each in character_list]

                                    ### check1 ! ###
                                    if not (run := screen.isOver(main_list=character_list ,vice_list=rival_list)):
                                        break

                                    # start to vice-battle #
                                    #print("START VICE ATTACK!!!")

                                    __discs:list[tuple[Any]] = [e for i ,e in Character.shuffle_disc(iroha_miko.disc ,re_madoka.disc).items()]
                                    for index ,each in enumerate([choice(__discs) for _ in range(3)] ,start=1):
                                        chosen_vice:Character = choice(character_list)
                                        _ ,_hurt = PyScreen.battle(ALL_CHARACTER=ALL_VICE_CHARACTER ,
                                                        ViceCharacter=chosen_vice ,
                                                        charge=0 ,
                                                        discs_getlist=[each])
                                        
                                        screen.show_all_hurt(_hurt ,target=chosen_vice)
                                        SHOWTIME()
                                        screen.flash()
                                        
                                    else:
                                        #del _ ,_hurt

                                        ### check2 ! ###
                                        if not (run := screen.isOver(main_list=character_list ,vice_list=rival_list)):
                                            break
                                        
                                        re_all:list = [each.disc for each in character_list]
                                        discs:dict[str ,tuple[Any ,Any]] = re(re_all=re_all)
                                        memoria:dict[str ,tuple[Any ,Any]] = {**discs}
                                        
                                        pygame.event.clear()
                                        rounds:int = rounds + 0b1
                                        MainCharacter.countdown()
                                else:
                                    showerror("X" ,"需要选满3个盘！")
                                    
                                break
                                
                                    
                            case '6'|'7'|'8'|'9'|'0':
                                MainCharacter << key
                                #MainCharacter.countdown()

                            case _:
                                pass
                            
                    except ValueError as VE:
                        print(f"**\nCommon Error :\n{VE}\n**")

                case pygame.MOUSEBUTTONDOWN:
                    x ,y = event.pos
                    for index ,each in enumerate(character_list):
                        if each.x <= x <= each.x+512*Grid.ratio and each.y <=y <= each.y+512*Grid.ratio:
                            screen._SHOW_EFFECT_PIC(each)
                            screen.flash()
                            while True:
                                event = pygame.event.wait()
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        break
                                    
                            #sleep(5)
                            break
                    pass

                case pygame.MOUSEMOTION:
                    pass

                case pygame.QUIT:
                    run:bool = not run
                    # #
                    break

                case _: pass # match #

        else: pass # for #
    else: pass # while #


if __name__ == "__main__":
    main()
    pygame.quit()
