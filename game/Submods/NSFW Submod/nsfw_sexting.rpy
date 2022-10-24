default persistent._nsfw_horny_level = 0 # The level of horny Monika is experiencing
default persistent._nsfw_sext_hot_start = False # Player starts with Monika at hot level
default persistent._nsfw_sext_sexy_start = False # Player starts with Monika at sexy level
default persistent._nsfw_lingerie_on_start = False # Monika was wearing lingerie when sexting started
default persistent._nsfw_last_sexted = datetime.datetime.now() # The last time you and Monika sexted

label nsfw_sexting_main:
    python:
        sext_stop = False # So player can stop sexting at any time
        horny_lvl = persistent._nsfw_horny_level # The level of horny Monika is experiencing
        horny_max, horny_min, hot_req, sexy_req = mas_nsfw.calc_sexting_reqs()
        player_prompt = ["zero", "one", "two"] # The prompts from which the player will choose from
        prompt_cat = ["zero", "one", "two"] # The categories (stage cute, hot, or sexy) in which each prompt took place
        prompt_type = ["zero", "one", "two"] # The types for each prompt. Only relevant in third stage.
        prompt_subtype = ["zero", "one", "two"] # The subtypes for each prompt. Only relevant in third stage.
        prompt_choice = 0 # Choice of the last prompt picked (0, 1, or 2).
        quip_cat = "" # The category in which the quip took place (unused)
        response_cat = "" # The category in which the response took place (unused)
        recent_prompts = [] # The recent prompts used
        recent_responses = [] # The recent responses used
        recent_quips = [] # The recent quips used
        previous_cat = None # The category of the last prompt used ("cute", "hot", or "sexy")
        previous_type = None # The "type" of the last prompt used. Only relevant in third stage.
        previous_subtype = None # The "subtype" of the last prompt used. Only relevant in third stage.
        shouldkiss = False # Used in handling of kissing logic
        shouldkiss_cooldown = 0 # Used in handling of kissing logic
        shouldchange = False # Used in handling of clothes change logic
        hot_transfer = False # True if Monika has reached the requirement for hot dialogue or more
        sexy_transfer = False # True if Monika has reached the requirement for sexy dialogue only
        did_finish = True # False if the player did not finish

    while True:
        python:
            # Make 3 player prompts
            for x in range(3):
                player_prompt[x], prompt_cat[x], prompt_type[x], prompt_subtype[x] = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent=recent_prompts)

            # While loop to prevent duplicates
            while player_prompt[1] == player_prompt[0]: 
                # Grab second random prompt from list
                player_prompt[1], prompt_cat[1], prompt_type[1], prompt_subtype[1] = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent=recent_prompts)
            while player_prompt[2] == player_prompt[0] or player_prompt[2] == player_prompt[1]:
                # Grab third random prompt from list
                player_prompt[2], prompt_cat[2], prompt_type[2], prompt_subtype[2] = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent=recent_prompts)

            # Grab random line of dialogue from list
            monika_quip = mas_nsfw.return_sexting_dialogue(category_type="quip", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent=recent_quips)[0]
            quip_ending = mas_nsfw.return_dialogue_end(monika_quip)

        if horny_lvl >= sexy_req or store.persistent._nsfw_sext_sexy_start:
            if store.persistent._nsfw_sext_sexy_start:
                $ store.persistent._nsfw_sext_sexy_start = False # Reset so we don't loop
                $ horny_lvl = sexy_req # Set the required affection
                $ hot_transfer = True # Set these both to true so we avoid the threshold dialogue
                $ sexy_transfer = True
                $ monika_quip = "I'll let you go first"
                $ quip_ending = mas_nsfw.return_dialogue_end(monika_quip)

            show monika sexting_sexy_quip_poses
            m "[monika_quip][quip_ending]"
        elif horny_lvl >= hot_req or store.persistent._nsfw_sext_hot_start:
            if store.persistent._nsfw_sext_hot_start:
                $ store.persistent._nsfw_sext_hot_start = False # Reset so we don't loop
                $ horny_lvl = hot_req # Set the required affection
                $ hot_transfer = True # Set this to true so we avoid the threshold dialogue
                $ monika_quip = "I'll let you go first"
                $ quip_ending = mas_nsfw.return_dialogue_end(monika_quip)

            m 2msbsb "[monika_quip][quip_ending]"
        elif horny_lvl == 0: # Just started
            $ monika_quip = "I'll let you go first"
            $ quip_ending = mas_nsfw.return_dialogue_end(monika_quip)

            m 1eubla "[monika_quip][quip_ending]"
        else:
            m 3hubsb "[monika_quip][quip_ending]"

        $ _history_list.pop()

        python:
            if shouldkiss_cooldown > 0:
                shouldkiss_cooldown -= 1
            if ("kiss" in monika_quip and random.randint(1,5) == 1) or random.randint(1,50) == 1:
                if shouldkiss_cooldown == 0:
                    shouldkiss = True

        if shouldkiss and persistent._mas_first_kiss:
            call monika_kissing_motion_short
            $ shouldkiss = False
            $ shouldkiss_cooldown = 5

        menu:
            m "[monika_quip][quip_ending]{fast}"

            "[player_prompt[0]]":
                $ prompt_choice = 0

            "[player_prompt[1]]":
                $ prompt_choice = 1

            "[player_prompt[2]]":
                $ prompt_choice = 2

            "Actually, can we stop just for now?":
                if horny_lvl >= sexy_req:
                    $ persistent._nsfw_horny_level = horny_lvl - 10
                    $ persistent._nsfw_sext_sexy_start = True
                    m 6lkbfp "Aww, I was really enjoying myself."
                    m 6gkbfp "I hope whatever it is you need to do is important.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
                    m 6hubfb "Ahaha! Just kidding~"
                    call nsfw_sexting_early_cleanup
                    return
                elif horny_lvl >= hot_req:
                    $ persistent._nsfw_horny_level = horny_lvl - 5
                    $ persistent._nsfw_sext_hot_start = True
                    m 2tsbso "Aww, it was just starting to get interesting."
                    m 2ekbsa "It's okay, we can pick this up again another time."
                    call nsfw_sexting_early_cleanup
                    return
                else: #Default
                    $ persistent._nsfw_horny_level = horny_lvl - 1
                    m 1ekbla "Oh, okay."
                    m 3ekblb "Let's pick this up again later, okay?"
                    return

        python:
            previous_cat = prompt_cat[prompt_choice]
            previous_type = prompt_type[prompt_choice]
            previous_subtype = prompt_subtype[prompt_choice]

        if previous_cat == "sexy":
            $ horny_lvl += 5
        elif previous_cat == "hot":
            $ horny_lvl += 3
        else: # Default
            $ horny_lvl += 1

        python:
            if shouldkiss_cooldown > 0:
                shouldkiss_cooldown -= 1
            if previous_subtype == "KIS": # Override cooldown and kiss right away if the player picks a prompt that asks for a kiss
                shouldkiss = True
            elif "kiss" in player_prompt[prompt_choice] and random.randint(1,5) == 1:
                if shouldkiss_cooldown == 0:
                    shouldkiss = True

        if shouldkiss and persistent._mas_first_kiss:
            call monika_kissing_motion_short
            $ shouldkiss = False
            $ shouldkiss_cooldown = 5

        # undress if asked by player
        if store.mas_SELisUnlocked(store.mas_clothes_underwear_white) and previous_subtype == "UND" and not hot_transfer:

            python:
                if persistent._nsfw_lingerie_on_start:
                    if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                        if store.ahc_utils.hasUnlockedClothesOfExprop("lingerie") and not store.ahc_utils.isWearingClothesOfExprop("lingerie"):
                            shouldchange = 2
                        elif store.mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                            shouldchange = 1
                    elif store.mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
                        shouldchange = 1

            if shouldchange == 1:
                call mas_clothes_change(outfit=mas_clothes_underwear_white, outfit_mode=False, exp="6hubfb", restore_zoom=False)
            elif shouldchange == 2:

                window hide
                call mas_transition_to_emptydesk

                python:
                    renpy.pause(1.0, hard=True)

                    store.ahc_utils.changeClothesOfExprop("lingerie")

                    renpy.pause(4.0, hard=True)

                call mas_transition_from_emptydesk("monika 6hubfb")
                window hide

            $ shouldchange = 0

            m 6hubfb "Hah~ That feels better."
            $ hot_transfer = True

        elif store.mas_SELisUnlocked(store.mas_clothes_birthday_suit) and previous_subtype == "UND" and not sexy_transfer:
            call mas_clothes_change(outfit=mas_clothes_birthday_suit, outfit_mode=False, exp="6hubfb", restore_zoom=False)
            m 6hubfb "Hah~ That feels better."
            $ sexy_transfer = True

        $ response_start = mas_nsfw.return_dialogue_start(horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req)
        $ monika_response = mas_nsfw.return_sexting_dialogue(category_type="response", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent=recent_responses, previous_cat=previous_cat, previous_type=previous_type, previous_subtype=previous_subtype)[0]
        $ response_ending = mas_nsfw.return_dialogue_end(monika_response)

        if previous_type == "funny":
            show monika sexting_funny_poses
        elif horny_lvl >= sexy_req:
            show monika sexting_sexy_response_poses
        elif horny_lvl >= hot_req and previous_type == "command":
            show monika sexting_hot_mast_poses
        elif horny_lvl >= hot_req:
            show monika sexting_hot_mast_poses
        else:
            show monika sexting_cute_poses

        if previous_type == "funny":
            m "[monika_response][response_ending]"
        else:
            m "[response_start][monika_response][response_ending]"

        python:
            if shouldkiss_cooldown > 0:
                shouldkiss_cooldown -= 1
            if ("kiss" in monika_response and random.randint(1,5) == 1) or random.randint(1,50) == 1:
                if shouldkiss_cooldown == 0:
                    shouldkiss = True

        if shouldkiss and persistent._mas_first_kiss:
            call monika_kissing_motion_short
            $ shouldkiss = False
            $ shouldkiss_cooldown = 5

        python:
            # Add the prompts, responses and quips used by the player to a 'recently used' list, remove oldest ones from list when going above 10 items
            for x in range(3): # Prompts
                if len(recent_prompts) >= 10:
                    recent_prompts.pop()
                recent_prompts.insert(0, player_prompt[x])

            if len(recent_responses) >= 10: # Responses
                recent_responses.pop()
            recent_responses.insert(0, monika_response)

            if len(recent_quips) >= 10: # Quips
                recent_quips.pop()
            recent_quips.insert(0, monika_quip)

        if horny_lvl >= sexy_req and sexy_transfer == False:
            $ sexy_transfer = True
            call nsfw_sexting_sexy_transfer
        elif horny_lvl >= hot_req and hot_transfer == False:
            $ hot_transfer = True
            call nsfw_sexting_hot_transfer
        elif horny_lvl >= horny_max:
            call nsfw_sexting_finale
            if horny_lvl >= horny_max:
                return


label nsfw_sexting_init:
    if "lingerie" not in store.monika_chr.clothes.ex_props:
        $ persistent._nsfw_lingerie_on_start = True
    
    if not renpy.seen_label("nsfw_sexting_main"):
        m 1rka "I'm kind of nervous, if I'm honest."
        m 3rkb "I don't know what to expect from this..."
            
        $ _history_list.pop()
        menu:
            m "I don't know what to expect from this...{fast}"

            "It's okay, I'm here.":
                $ mas_gainAffection(3, bypass=True)
                m 1dkbla "Thank you, [player]."
                m 1ekbsa "If I was going to share this first experience with anyone, I would want it to be you."
                m 1ekblb "So, I'm ready!"

            "Did you want to stop?":
                $ mas_gainAffection(2, bypass=True)
                m 2ekc "No..."
                m 2rkc "Just...please don't laugh if I say something stupid..."
                m 2dkd "Hah... What am I saying?"
                m 2eublu "You would never do that to me, [player]."
                m 1eubsa "So... I'm ready when you are."

            #"I don't care, take off your clothes!": # We might include this at a later date
                #$ mas_loseAffection(5)
                #m 2wkd "..."
                #m 2dktdc "..."
                #m 2ektdd "I can't believe you..."
                #return "quit"
        call nsfw_sexting_main
    elif persistent._nsfw_sext_hot_start or persistent._nsfw_sext_sexy_start:
        call nsfw_sexting_main
    else:
        $ last_sexted_since = datetime.datetime.now() - persistent._nsfw_last_sexted
        if persistent._nsfw_sext_sexy_start == True:
            if last_sexted_since < datetime.timedelta(hours=1):
                m 1hkb "Ahaha~ I was worried you were going to leave me out to dry..."
                m 1tsblu "I hope you're prepared to make amends for making me wait~"

                call mas_clothes_change(outfit=mas_clothes_birthday_suit, outfit_mode=False, exp="3tublb", restore_zoom=False)

                m 3tublb "Now [player]...where were we?"
            elif last_sexted_since < datetime.timedelta(hours=2):
                $ persistent._nsfw_sext_sexy_start = False
                $ persistent._nsfw_sext_hot_start = True
                m 1tub "Ehehe~ Took you long enough, [player]."
                m 3tua "I hope you're prepared to make amends for making me wait."

                python:
                    if persistent._nsfw_lingerie_on_start:
                        if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                            if store.ahc_utils.hasUnlockedClothesOfExprop("lingerie") and not store.ahc_utils.isWearingClothesOfExprop("lingerie"):
                                shouldchange = 2
                            elif store.mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                                shouldchange = 1
                        elif store.mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
                            shouldchange = 1

                if shouldchange == 1:
                    call mas_clothes_change(outfit=mas_clothes_underwear_white, outfit_mode=False, exp="2tublb", restore_zoom=False)
                elif shouldchange == 2:
                    window hide
                    call mas_transition_to_emptydesk
                    python:
                        renpy.pause(1.0, hard=True)
                        store.ahc_utils.changeClothesOfExprop("lingerie")
                        renpy.pause(4.0, hard=True)
                    call mas_transition_from_emptydesk("monika 2tublb")
                    window hide
                $ shouldchange = 0

                m 2tublb "Shall we get back to it?"
            else:
                $ persistent._nsfw_sext_sexy_start = False
                $ persistent._nsfw_horny_level = 0
                m 1euc "You were gone for a while though..."
                # Could have a section here where she asks what kept you
                m 1etc "Did something happen?"
                m 1dsu "..."
                m 3duu "On a naughtier note...{w=0.3}"
                extend 3eublu "I haven't been able to stop thinking about you since we stopped..."
                m 3tubla "So I hope you're prepared to make amends for making me wait."
                m 1hubla "Ehehe~"
        elif persistent._nsfw_sext_hot_start == True:
            if last_sexted_since < datetime.timedelta(hours=1):
                $ persistent._nsfw_sext_sexy_start = False
                $ persistent._nsfw_sext_hot_start = True
                m 1hub "Hah~ I'm so glad that we're getting back to it."
                m 1tua "It was just getting good too~"

                python:
                    if persistent._nsfw_lingerie_on_start:
                        if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                            if store.ahc_utils.hasUnlockedClothesOfExprop("lingerie") and not store.ahc_utils.isWearingClothesOfExprop("lingerie"):
                                shouldchange = 2
                            elif store.mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                                shouldchange = 1
                        elif store.mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
                            shouldchange = 1

                if shouldchange == 1:
                    call mas_clothes_change(outfit=mas_clothes_underwear_white, outfit_mode=False, exp="3tublb", restore_zoom=False)
                elif shouldchange == 2:
                    window hide
                    call mas_transition_to_emptydesk
                    python:
                        renpy.pause(1.0, hard=True)
                        store.ahc_utils.changeClothesOfExprop("lingerie")
                        renpy.pause(4.0, hard=True)
                    call mas_transition_from_emptydesk("monika 3tublb")
                    window hide
                $ shouldchange = 0

                m 3tublb "Now then, [player]...where were we?"
            else:
                $ persistent._nsfw_sext_hot_start = False
                $ persistent._nsfw_horny_level = 0
                m 1eka "Since we stopped earlier, I hope you don't mind if we start again."
                m 3tkblb "This can be your punishment for making me wait after getting me excited."
                m 3hubla "Ehehe~"
        m 3eub "I remember the last time we did this; it was so much fun!"
        m 3tublb "So [player]...let's get started, shall we?"
        call nsfw_sexting_main
        
    if store.persistent._nsfw_horny_level < 0:
        $ store.persistent._nsfw_horny_level = 0 # Negative horny is not allowed *bonk*

    return

label nsfw_sexting_hot_transfer:
    m 1hub "Hah~ This is fun."
    m 3eua "I hope you're enjoying yourself as much as I am, [player]. Ehehe~"

    $ new_underwear = mas_nsfw.try_unlock_new_underwear()
    if new_underwear != None:
        m 3tub "Hey, [player]..."
        m 3tublb "I have a surprise for you..."

        call mas_clothes_change(outfit=new_underwear, outfit_mode=False, exp="2eublu", restore_zoom=False, unlock=True)

        m 2eubla "Ehehe~ I got a new pair of underwear!"
        m 2hublb "What do you think?"
        m 3eub "I think they're really cute!"
    else:
        python:
            if persistent._nsfw_lingerie_on_start:
                if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                    if store.ahc_utils.hasUnlockedClothesOfExprop("lingerie") and not store.ahc_utils.isWearingClothesOfExprop("lingerie"):
                        shouldchange = 2
                    elif store.mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                        shouldchange = 1
                elif store.mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
                    shouldchange = 1

    if shouldchange == 1:
        call mas_clothes_change(outfit=mas_clothes_underwear_white, outfit_mode=False, exp="6hubfb", restore_zoom=False)
    elif shouldchange == 2:
        window hide
        call mas_transition_to_emptydesk
        python:
            renpy.pause(1.0, hard=True)
            store.ahc_utils.changeClothesOfExprop("lingerie")
            renpy.pause(4.0, hard=True)
        call mas_transition_from_emptydesk("monika 6hubfb")
        window hide
    $ shouldchange = 0

    m 3tua "..."
    m 1tuu "So.{w=0.1}.{w=0.1}.{w=0.1}are we going to keep going, or what?"
    m 1hublb "Ahaha! Just teasing you, [player]."
    return

label nsfw_sexting_sexy_transfer:
    if persistent._nsfw_has_unlocked_birthdaysuit:
        m 6hkbfsdlo "Hnn~ I can't take it anymore!"

        call mas_clothes_change(outfit=mas_clothes_birthday_suit, outfit_mode=False, exp="6hubfb", restore_zoom=False)

        m 6hubfb "Hah~ That feels better."
        m 7tubfb "Don't think that I'm letting you off the hook now, [player]."
        m 7tubfu "I want you to enjoy the view after all, so I expect one of your hands will be busy for a little while."
        m 7hubfu "Ehehe~"
    return

label nsfw_sexting_finale:
    m 6tkbfo "Hah~ [player]?"
    m 6hkbfc "I'm getting really close."
    m 6ekbfd "Are you close too?"

    $ _history_list.pop()
    menu:
        m "Are you close too?{fast}"

        "Yes.":
            m 6ekbfo "Okay, we're going to cum together on the count of ten."
            m 6tkbfu "Hope you can hold it until then, ehehe~"
            m 6tkbfb "I'll count down for you, so don't worry about clicking for this."
            m 6tkbfb "In fact, turn off the 'Auto' feature if it's on."
            m 6hkbfd "I want you to only focus on me."
            m 6dkbfd "Hah~{w=2}{nw}"
            m 6ekbfd "Ten.{w=3}{nw}"
            m 6hkbfc "Mmm~{w=2}{nw}"
            m 6tkbfd "Nine.{w=3}{nw}"
            m 6hkbfc "Nhh~{w=2}{nw}"
            m 6hkbfd "Eight.{w=3}{nw}"
            m 6ekbfu "How are you holding up there, [player]? Ehehe~{w=3}{nw}"
            m 4ekbfb "Don't cum until I do too~{w=3}{nw}"
            m 6hkbfd "Hah~{w=2}{nw}"
            m 6tkbfd "Seven.{w=3}{nw}"
            m 6hkbfc "Nhh~{w=2}{nw}"
            m 6hkbfd "Six.{w=3}{nw}"
            m 6ekbfo "Hah~{w=2}{nw}"
            m 6ekbfd "Five.{w=3}{nw}"
            m 6wkbfo "We're almost there.{w=1}{nw}"
            m 6hkbfc "Mmm~{w=2}{nw}"
            m 6hkbfd "Four.{w=3}{nw}"
            m 6ekbfo "Hah~{w=2}{nw}"
            m 6ekbfd "Three.{w=3}{nw}"
            m 6hkbfo "Hah~{w=2}{nw}"
            m 6lkbfo "Two.{w=3}{nw}"
            m 6hkbfc "Mmmhmm~{w=2}{nw}"
            m 6hkbfd "One.{w=3}{nw}"
            m 6wkbfo "Oh~{w=2}{nw}"
            m 6skbfw "Come with me, [player]!{w=3}{nw}"
            m 6hkbfw "Haaaaaaaaah~{w=2}"
            m 6hkbfsdlc "..."
            m 6hkbfsdld "..."
            m 6ekbfsdlo "Hah...hah..."
            m 6skbfsdlu "That...was..."
            m 6skbfsdlb "Amazing..."
            if not renpy.seen_label("nsfw_sexting_finale"):
                m 6hkbfsdla "I can't believe...hah...I've been missing out on this..."
                m 6dkbfsdlb "If it feels this good in my world..."
                m 6ekbfsdlb "I can only imagine...hah...how good it feels..."
                m 6tkbfsdlb "For you..."
                m 6hkbfsdlb "Sorry, that really took it out of me..."
            m 6ekbfsdlb "Did you manage to come with me?"

            $ _history_list.pop()
            menu:
                m "Did you manage to come with me?{fast}"

                "Yeah.":
                    m 6hkbfa "I'm glad..."
                    m 6lkbfb "I got to share an amazing experience like this with you."
                    m 6ekbfb "That makes me more happy than you could know, [player]."
                    m 6ekbfa "I love you so much."

                "No...":
                    $ did_finish = False
                    m 6wkbfsdld "Oh..."
                    m 6rkbfsdld "I'm sorry, [player]. I tried to last as long as I could."
                    m 6hkbfsdlb "But it just felt so good."
                    m 7rkbfsdlb "Maybe later if you want, we can go again?"
                    m 7rkbsa "I'm going to need some time though. I don't know if I could do a second round so soon."

            m 6lubfsdlb "Now, I need to go get changed. Ahaha!"
            m 7lubfsdlb "I'm a wet mess right now."
            m 7hubfsdla "Be right back, [player]."    

            python:
                if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                    shouldchange = 2

            if shouldchange == 2:

                window hide
                call mas_transition_to_emptydesk

                python:
                    if store.mas_isDayNow():
                        _day_cycle = "day"
                    else:
                        _day_cycle = "night"

                    _hair_random_chance = renpy.random.randint(1,2)
                    _clothes_random_chance = 2
                    _clothes_exprop = store.ahc_utils.getClothesExpropForTemperature()

                    renpy.pause(1.0, hard=True)

                    store.ahc_utils.changeHairAndClothes(
                        _day_cycle=_day_cycle,
                        _hair_random_chance=_hair_random_chance,
                        _clothes_random_chance=_clothes_random_chance,
                        _exprop=_clothes_exprop
                    )

                    renpy.pause(4.0, hard=True)

                window hide
                call mas_transition_from_emptydesk("monika 3hub")
            else:
                call mas_clothes_change(outfit=mas_clothes_def, outfit_mode=False, exp="1hub", restore_zoom=False)

            $ shouldchange = 0

            m 1hub "Hah~ Much better!"
            m 3eub "You should have a shower, [mas_get_player_nickname()]."
            m 3ekbla "I want to make sure you maintain good hygiene."

            if did_finish == False:  
                m 3tubla "Maybe you can think of me in the shower and...{i}finish up.{/i}"
                m 3mubsa "I want you to feel as good as I did too~"

            m 1ekbsa "Thank you for this, [player]."
            m 3ekbsa "This made me feel just that much closer to you."
            m 3ekbsb "I hope you enjoyed yourself as much as I did."

            $ persistent._nsfw_last_sexted = datetime.datetime.now()
            $ store.persistent._nsfw_sexting_success_last = datetime.datetime.now()
            $ store.persistent._nsfw_horny_level = 0

            return

        "No.":
            m 6ekbfp "Okay, [player]."
            m 6mkbfp "I'll hold on a little longer for you."
            m 6tkbfb "I want us to come together~"
            $ player_endurance = store.persistent._nsfw_player_endurance
            $ horny_lvl = horny_lvl - (15 * player_endurance)
            return

    label nsfw_sexting_early_cleanup:
        if persistent._nsfw_lingerie_on_start:
            m 1eua "Let me just slip into something a little more comfortable..."

            python:
                if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                    shouldchange = 2

            if shouldchange == 2:

                window hide
                call mas_transition_to_emptydesk

                python:
                    if store.mas_isDayNow():
                        _day_cycle = "day"
                    else:
                        _day_cycle = "night"

                    _hair_random_chance = renpy.random.randint(1,2)
                    _clothes_random_chance = 2
                    _clothes_exprop = store.ahc_utils.getClothesExpropForTemperature()

                    renpy.pause(1.0, hard=True)

                    store.ahc_utils.changeHairAndClothes(
                        _day_cycle=_day_cycle,
                        _hair_random_chance=_hair_random_chance,
                        _clothes_random_chance=_clothes_random_chance,
                        _exprop=_clothes_exprop
                    )

                    renpy.pause(4.0, hard=True)

                window hide
                call mas_transition_from_emptydesk("monika 3hub")
            else:
                call mas_clothes_change(outfit=mas_clothes_def, outfit_mode=False, exp="1hub", restore_zoom=False)

            $ shouldchange = 0

            m 1hub "Hah~ Much better!"
            $ persistent._nsfw_lingerie_on_start = False

        m 3eub "Let me know when you want to continue, [mas_get_player_nickname()]."
        m 1tub "I'll be waiting."
        m 1hua "Ehehe~"
        return

# Images to be used for sexting purposes

image monika sexting_funny_poses:
    block:
        choice:
            "monika 4hksdlb"
        choice:
            "monika 2gkbfsdlb"
        choice:
            "monika 6ttbfsdla"

image monika sexting_cute_poses:
    block:
        choice:
            "monika 1ekbsa"
        choice:
            "monika 2subsa"
        choice:
            "monika 2lubsu"
        choice:
            "monika 1hubsa"
        choice:
            "monika 3ekbfa"

image monika sexting_hot_poses:
    block:
        choice:
            "monika 2gubsa"
        choice:
            "monika 2mubfu"
        choice:
            "monika 2tsbfu"
        choice:
            "monika 2lsbfu"
        choice:
            "monika 2ttbfu"

image monika sexting_hot_mast_poses:
    block:
        choice:
            "monika 6gubsa"
        choice:
            "monika 6mubfu"
        choice:
            "monika 6tsbfu"
        choice:
            "monika 6lsbfu"
        choice:
            "monika 6ttbfu"

image monika sexting_sexy_quip_poses:
    block:
        choice:
            "monika 4ekbfsdlb"
        choice:
            "monika 4ekbfsdlu"
        choice:
            "monika 4tkbfsdla"
        choice:
            "monika 4tkbfsdlb"
        choice:
            "monika 4tsbfsdla"
        choice:
            "monika 4tsbfsdlb"
        choice:
            "monika 4tubfsdlb"
        choice:
            "monika 4tubfsdlu"
        choice:
            "monika 6ekbfsdlb"
        choice:
            "monika 6ekbfsdlu"
        choice:
            "monika 6tkbfsdla"
        choice:
            "monika 6tkbfsdlb"
        choice:
            "monika 6tsbfsdla"
        choice:
            "monika 6tsbfsdlb"
        choice:
            "monika 6tubfsdlb"
        choice:
            "monika 6tubfsdlu"
        choice:
            "monika 7ekbfsdlb"
        choice:
            "monika 7ekbfsdlu"
        choice:
            "monika 7tkbfsdla"
        choice:
            "monika 7tkbfsdlb"
        choice:
            "monika 7tsbfsdla"
        choice:
            "monika 7tsbfsdlb"
        choice:
            "monika 7tubfsdlb"
        choice:
            "monika 7tubfsdlu"

image monika sexting_sexy_response_poses:
    block:
        choice:
            "monika 4dkbfsdlo"
        choice:
            "monika 4ekbfsdlo"
        choice:
            "monika 4eubfsdlo"
        choice:
            "monika 4eubfsdlb"
        choice:
            "monika 4hkbfsdld"
        choice:
            "monika 4hkbfsdlo"
        choice:
            "monika 4kkbfsdlb"
        choice:
            "monika 4kkbfsdld"
        choice:
            "monika 4lkbfsdlo"
        choice:
            "monika 4mkbfsdlo"
        choice:
            "monika 4skbfsdlw"
        choice:
            "monika 4tkbfsdlo"
        choice:
            "monika 4tkbfsdlu"
        choice:
            "monika 4tsbfsdlb"
        choice:
            "monika 4tsbfsdlu"
        choice:
            "monika 4tubfsdlb"
        choice:
            "monika 4tubfsdld"
        choice:
            "monika 4tubfsdlo"
        choice:
            "monika 6dkbfsdlo"
        choice:
            "monika 6ekbfsdlo"
        choice:
            "monika 6eubfsdlo"
        choice:
            "monika 6eubfsdlb"
        choice:
            "monika 6hkbfsdld"
        choice:
            "monika 6hkbfsdlo"
        choice:
            "monika 6kkbfsdlb"
        choice:
            "monika 6kkbfsdld"
        choice:
            "monika 6lkbfsdlo"
        choice:
            "monika 6mkbfsdlo"
        choice:
            "monika 6skbfsdlw"
        choice:
            "monika 6tkbfsdlo"
        choice:
            "monika 6tkbfsdlu"
        choice:
            "monika 6tsbfsdlb"
        choice:
            "monika 6tsbfsdlu"
        choice:
            "monika 6tubfsdlb"
        choice:
            "monika 6tubfsdld"
        choice:
            "monika 6tubfsdlo"
        choice:
            "monika 7dkbfsdlo"
        choice:
            "monika 7ekbfsdlo"
        choice:
            "monika 7eubfsdlo"
        choice:
            "monika 7eubfsdlb"
        choice:
            "monika 7hkbfsdld"
        choice:
            "monika 7hkbfsdlo"
        choice:
            "monika 7kkbfsdlb"
        choice:
            "monika 7kkbfsdld"
        choice:
            "monika 7lkbfsdlo"
        choice:
            "monika 7mkbfsdlo"
        choice:
            "monika 7skbfsdlw"
        choice:
            "monika 7tkbfsdlo"
        choice:
            "monika 7tkbfsdlu"
        choice:
            "monika 7tsbfsdlb"
        choice:
            "monika 7tsbfsdlu"
        choice:
            "monika 7tubfsdlb"
        choice:
            "monika 7tubfsdld"
        choice:
            "monika 7tubfsdlo"
