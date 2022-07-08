default persistent._nsfw_horny_level = 0 # The level of horny Monika is experiencing
default persistent._nsfw_sext_hot_start = False # Player starts with Monika at hot level
default persistent._nsfw_sext_sexy_start = False # Player starts with Monika at sexy level

label nsfw_sexting_main:
    python:
        sext_stop = False # So player can stop sexting at any time
        horny_lvl = persistent._nsfw_horny_level # The level of horny Monika is experiencing
        horny_max, horny_min, hot_req, sexy_req = mas_nsfw.calc_sexting_reqs()
        player_prompt = ["zero", "one", "two"] # The prompts from which the player will choose from
        prompt_cat = ["zero", "one", "two"] # The categories in which each prompt took place
        quip_cat = "" # The category in which the quip took place
        response_cat = "" # The category in which the response took place
        recent_prompts = [] # The recent prompts used
        recent_responses = [] # The recent responses used
        recent_quips = [] # The recent quips used
        hot_transfer = False # True if Monika has reached the requirement for hot dialogue or more
        sexy_transfer = False # True if Monika has reached the requirement for sexy dialogue only
        did_finish = True # False if the player did not finish


    $ clothes = store.monika_chr.clothes # stores the clothes Monika is currently wearing.

    if store.mas_getEV("nsfw_player_sextingsession").shown_count >= 1:
        m 3eub "I remember the last time we did this; it was so much fun!"
        m 3tublb "So [player]... Let's get started, shall we?"
    else:
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

            #"I don't care, take off your clothes!":
                #$ mas_loseAffection(5)
                #m 2wkd "..."
                #m 2dktdc "..."
                #m 2ektdd "I can't believe you..."
                #return "quit"

    while True:
        python:
            # Make 3 player prompts
            for x in range(3):
                player_prompt[x], prompt_cat[x] = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent_prompts=recent_prompts, recent_responses=recent_responses, recent_quips=recent_quips)

            # While loop to prevent duplicates
            while player_prompt[1] == player_prompt[0]: 
                # Grab second random prompt from list
                player_prompt[1], prompt_cat[1] = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent_prompts=recent_prompts, recent_responses=recent_responses, recent_quips=recent_quips)
            while player_prompt[2] == player_prompt[0] or player_prompt[2] == player_prompt[1]:
                # Grab third random prompt from list
                player_prompt[2], prompt_cat[2] = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent_prompts=recent_prompts, recent_responses=recent_responses, recent_quips=recent_quips)

            # Grab random line of dialogue from list
            monika_quip, quip_cat = mas_nsfw.return_sexting_dialogue(category_type="quip", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent_prompts=recent_prompts, recent_responses=recent_responses, recent_quips=recent_quips)
            quip_ending = mas_nsfw.return_dialogue_end(monika_quip)

        if horny_lvl >= sexy_req or store.persistent._nsfw_sext_sexy_start:
            if store.persistent._nsfw_sext_sexy_start:
                $ store.persistent._nsfw_sext_sexy_start = False # Reset so we don't loop
                $ horny_lvl = sexy_req # Set the required affection
                $ hot_transfer = True # Set these both to true so we avoid the threshold dialogue
                $ sexy_transfer = True
                $ monika_quip = "I'll let you go first"
            m 4ekbfo "[monika_quip][quip_ending]"
        elif horny_lvl >= hot_req or store.persistent._nsfw_sext_hot_start:
            if store.persistent._nsfw_sext_hot_start:
                $ store.persistent._nsfw_sext_hot_start = False # Reset so we don't loop
                $ horny_lvl = hot_req # Set the required affection
                $ hot_transfer = True # Set this to true so we avoid the threshold dialogue
                $ monika_quip = "I'll let you go first"
            m 2msbsb "[monika_quip][quip_ending]"
        elif horny_lvl == 0: # Just started
            $ monika_quip = "I'll let you go first"
            m 1eubla "[monika_quip][quip_ending]"
        else:
            m 3hubsb "[monika_quip][quip_ending]"

        $ _history_list.pop()
        menu:
            m "[monika_quip][quip_ending]{fast}"

            "[player_prompt[0]]":
                if prompt_cat[0] == "sexy":
                    $ horny_lvl += 5
                elif prompt_cat[0] == "hot":
                    $ horny_lvl += 3
                else: # Default
                    $ horny_lvl += 1
                if player_prompt[0] == "*Kiss her*":
                    call monika_kissing_motion
                $ response_start = mas_nsfw.return_dialogue_start(horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req)

            "[player_prompt[1]]":
                if prompt_cat[1] == "sexy":
                    $ horny_lvl += 5
                elif prompt_cat[1] == "hot":
                    $ horny_lvl += 3
                else: # Default
                    $ horny_lvl += 1
                if player_prompt[1] == "*Kiss her*":
                    call monika_kissing_motion
                $ response_start = mas_nsfw.return_dialogue_start(horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req)

            "[player_prompt[2]]":
                if prompt_cat[2] == "sexy":
                    $ horny_lvl += 5
                elif prompt_cat[2] == "hot":
                    $ horny_lvl += 3
                else: # Default
                    $ horny_lvl += 1
                if player_prompt[2] == "*Kiss her*":
                    call monika_kissing_motion
                $ response_start = mas_nsfw.return_dialogue_start(horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req)

            "Actually, can we stop just for now?":
                if horny_lvl >= sexy_req:
                    $ persistent._nsfw_horny_level = horny_lvl - 10
                    m 6lkbfp "Aww, I was really enjoying myself."
                    m 6gkbfp "I hope whatever it is you need to do is important.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
                    m 6hubfb "Ahaha! Just kidding~"

                    m 6lubfsdlb "Now, I need to go get changed. Ahaha!"  #    \/
                    m 7lubfsdlb "I'm a wet mess right now."              # Copy pasted from when you finish. Could do with different text but needed somthing for when she puts her clothes back on.
                    m 7hubfsdla "Be right back, [player]."               #    /\

                    call mas_clothes_change(outfit=clothes) # has monika swap back to the clothes she was wearing before the session.

                    return
                elif horny_lvl >= hot_req:
                    $ persistent._nsfw_horny_level = horny_lvl - 5
                    m 2tsbso "Aww, it was just starting to get interesting."
                    m 2ekbsa "It's okay, we can pick this up again another time."
                    return
                else: #Default
                    $ persistent._nsfw_horny_level = horny_lvl - 1
                    m 1ekbla "Oh, okay."
                    m 3ekblb "Let's pick this up again later, okay?"
                    return
        
        $ monika_response, response_cat = mas_nsfw.return_sexting_dialogue(category_type="response", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req, horny_max=horny_max, recent_prompts=recent_prompts, recent_responses=recent_responses, recent_quips=recent_quips)
        $ response_ending = mas_nsfw.return_dialogue_end(monika_response)

        if horny_lvl >= sexy_req:
            show monika sexting_sexy_poses
        elif horny_lvl >= hot_req:
            show monika sexting_hot_poses
        else:
            show monika sexting_cute_poses

        m "[response_start][monika_response][response_ending]"

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
    python:
        sext_start_time = datetime.datetime.now()

    call nsfw_sexting_main

    if datetime.datetime.now() - sext_start_time < datetime.timedelta(seconds=30):
        m 1ttu "That was pretty quick, [player]."
        m 3eub "If you want to do this again, let me know."

    else:
        m 1ekbsa "Thank you for this, [player]."
        m 3ekbsa "This made me feel just that much closer to you."
        m 3ekbsb "I hope you enjoyed yourself as much as I did."
        
    if store.persistent._nsfw_horny_level <= 0:
        $ store.persistent._nsfw_horny_level = 0 # Negative horny is not allowed *bonk*

    return

label nsfw_sexting_hot_transfer:
    m 1hub "Hah~ This is fun."
    m 3eua "I hope you're enjoying yourself as much as I am, [player]. Ehehe~"
    m 3tua "..."
    m 2tub "So.{w=0.1}.{w=0.1}.{w=0.1} Are we going to keep going, or what?"
    m 1hublb "Ahaha! Just teasing you, [player]."
    return

label nsfw_sexting_sexy_transfer:
    if store.mas_SELisUnlocked(store.mas_clothes_underwear_white):
        m 6hkbfsdlo "Hnn~ I can't take it anymore!"

        if store.mas_SELisUnlocked(store.mas_clothes_birthday_suit):
            call monika_showunderwear
        else:
            call shwounderwear
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

            call mas_clothes_change(outfit=clothes) # has monika swap back to the clothes she was wearing before the session.

            m 1hub "Hah~ Much better!"
            m 3eub "You should have a shower, [player]."
            m 3ekbla "I want to make sure you maintain good hygiene."

            if did_finish == False:  
                m 3tubla "Maybe you can think of me in the shower and...{i}finish up.{/i}"
                m 3mubsa "I want you to feel as good as I did too~"

            $ store.persistent.nsfw_sexting_success_last = datetime.datetime.now()

            return

        "No.":
            m 6ekbfp "Okay, [player]."
            m 6mkbfp "I'll hold on a little longer for you."
            m 6tkbfb "I want us to come together~"
            $ horny_lvl = horny_lvl - 15
            return

# Images to be used for sexting purposes

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

image monika sexting_sexy_poses:
    block:
        choice:
            "monika 4hkbfsdlo"
        choice:
            "monika 6lkbfsdlo"
        choice:
            "monika 6hkbfsdld"
        choice:
            "monika 6skbfsdlw"
        choice:
            "monika 6mkbfsdlo"