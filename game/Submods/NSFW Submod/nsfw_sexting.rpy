default persistent._nsfw_horny_level = 0 # The level of horny Monika is experiencing
default persistent._nsfw_sext_hot_start = False # Player starts with Monika at hot level
default persistent._nsfw_sext_sexy_start = False # Player starts with Monika at sexy level
default persistent._nsfw_lingerie_on_start = False # Monika was wearing lingerie when sexting started
default persistent._nsfw_last_sexted = datetime.datetime.now() # The last time you and Monika sexted
default persistent._nsfw_sexting_count = 0 # The amount of times we have sexted with Monika, only counts successes

label nsfw_sexting_main:
    python:
        sext_stop = False # So player can stop sexting at any time
        prompt_choice = 0 # Choice of the last prompt picked (0, 1, or 2).
        horny_lvl = persistent._nsfw_horny_level # The level of horny Monika is experiencing
        horny_reqs = mas_nsfw.calc_sexting_reqs() # The requirements for horny levels [min, hot_req, sexy_req, max]
        player_prompts = [[None, None, None, None], [None, None, None, None], [None, None, None, None]] # The prompts from which the player will choose from, and their respective category/type/subtype.
        previous_vars = [None, None, None] # The last dialogue Monika said, and the category/type/subtype of the dialogue.
        response_cat = "" # The category in which the response took place (unused)
        recent_prompts = [] # The recent prompts used
        recent_responses = [] # The recent responses used
        recent_quips = [] # The recent quips used
        shouldkiss = False # Used in handling of kissing logic
        shouldkiss_cooldown = 0 # Used in handling of kissing logic
        shouldchange = False # Used in handling of clothes change logic
        hot_transfer = False # True if Monika has reached the requirement for hot dialogue or more
        sexy_transfer = False # True if Monika has reached the requirement for sexy dialogue only
        did_finish = True # False if the player did not finish

    while True:
        # Create new Monika quip
        if horny_lvl == 0:
            $ monika_quip = ["I'll let you go first", "cute", ["STM"], ["GEN"], ""]
            $ monika_quip[4] = mas_nsfw.return_dialogue_end(monika_quip[0])
            $ quip_ending = monika_quip[4]
            # Set new previous category/type/subtype to the new quip's
            $ previous_vars = ["cute", ["STM"], ["GEN"]]
        elif store.persistent._nsfw_sext_hot_start:
            $ monika_quip = store.mas_nsfw.create_sexting_quips(
                horny_lvl=horny_lvl,
                horny_reqs=horny_reqs,
                previous_vars=["hot", ["STM"], ["GEN"]],
                recent_quips=recent_quips
            )
            $ monika_quip[4] = mas_nsfw.return_dialogue_end(monika_quip[0])
            $ quip_ending = monika_quip[4]
            # Set new previous category/type/subtype to the new quip's
            $ previous_vars = [monika_quip[1], monika_quip[2], monika_quip[3]]
        elif store.persistent._nsfw_sext_sexy_start:
            $ monika_quip = store.mas_nsfw.create_sexting_quips(
                horny_lvl=horny_lvl,
                horny_reqs=horny_reqs,
                previous_vars=["sexy", ["STM"], ["GEN"]],
                recent_quips=recent_quips
            )
            $ monika_quip[4] = mas_nsfw.return_dialogue_end(monika_quip[0])
            $ quip_ending = monika_quip[4]
            # Set new previous category/type/subtype to the new quip's
            $ previous_vars = [monika_quip[1], monika_quip[2], monika_quip[3]]
        else:
            $ monika_quip = store.mas_nsfw.create_sexting_quips(
                horny_lvl=horny_lvl,
                horny_reqs=horny_reqs,
                previous_vars=previous_vars,
                recent_quips=recent_quips
            )
            $ quip_ending = monika_quip[4]
            # Set new previous category/type/subtype to the new quip's
            $ previous_vars = [monika_quip[1], monika_quip[2], monika_quip[3]]

        # Check horny level for what type of dialogue and posing to use
        if horny_lvl >= horny_reqs[2] or store.persistent._nsfw_sext_sexy_start: # If we're at the sexy level or higher
            if store.persistent._nsfw_sext_sexy_start:
                $ store.persistent._nsfw_sext_sexy_start = False # Reset so we don't loop
                $ horny_lvl = horny_reqs[2] # Set the required affection
                $ hot_transfer = True # Set these both to true so we avoid the threshold dialogue
                $ sexy_transfer = True
            show monika sexting_sexy_quip_poses
            m "[monika_quip[0]][quip_ending]"
        elif horny_lvl >= horny_reqs[1] or store.persistent._nsfw_sext_hot_start: # If we're at the hot level or higher
            if store.persistent._nsfw_sext_hot_start:
                $ store.persistent._nsfw_sext_hot_start = False # Reset so we don't loop
                $ horny_lvl = horny_reqs[1] # Set the required affection
                $ hot_transfer = True # Set this to true so we avoid the threshold dialogue
            m 2msbsb "[monika_quip[0]][quip_ending]"
        elif horny_lvl == 0: # Just started
            m 1eubla "[monika_quip[0]][quip_ending]"
        else: # If we're at the cute level or lower
            m 3hubsb "[monika_quip[0]][quip_ending]"

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

        python:
            # Generate player prompts
            player_prompts = store.mas_nsfw.create_sexting_prompts(horny_lvl=horny_lvl, horny_reqs=horny_reqs, previous_vars=previous_vars, recent_prompts=recent_prompts)
            #recent_prompts.append(player_prompts[x][2]) # already done elsewhere?

        # Menus work well with 'All Gen Scrollable Menus' installed, so making a config for if the user has it or not
        # $ end_of_prompt = ""

        if not store.mas_submod_utils.isSubmodInstalled("All Gen Scrollable Menus"):
            sext_menu = []

            for x in range(3):
                sext_menu.append((_(player_prompts[x][0]), "player_prompt_" + str(x)))

            sext_menu.append((_("Actually, can we stop just for now?"), "stop_sext"))

            show monika at t21
            $ madechoice = renpy.display_menu(sext_menu, screen="talk_choice")
            show monika at t11

            if madechoice == "player_prompt_0":
                $ prompt_choice = 0
            elif madechoice == "player_prompt_1":
                $ prompt_choice = 1
            elif madechoice == "player_prompt_2":
                $ prompt_choice = 2
            elif madechoice == "stop_sext":
                $ persistent._nsfw_last_sexted = datetime.datetime.now() # We already have a success check, so this can be a check for any previous sexting attempt

                if horny_lvl >= horny_reqs[2]:
                    $ persistent._nsfw_horny_level = horny_lvl - 10
                    $ persistent._nsfw_sext_sexy_start = True
                    m 6lkbfp "Aww, I was really enjoying myself."
                    m 6gkbfp "I hope whatever it is you need to do is important.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
                    m 6hubfb "Ahaha! Just kidding~"
                    call nsfw_sexting_early_cleanup
                    return
                elif horny_lvl >= horny_reqs[1]:
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
        else:
            menu:
                m "[monika_quip[0]][quip_ending]{fast}"

                "[player_prompts[0][0]][end_of_prompt]":
                    $ prompt_choice = 0

                "[player_prompts[1][0]][end_of_prompt]":
                    $ prompt_choice = 1

                "[player_prompts[2][0]][end_of_prompt]":
                    $ prompt_choice = 2

                "Actually, can we stop just for now?[end_of_prompt]":
                    $ persistent._nsfw_last_sexted = datetime.datetime.now() # We already have a success check, so this can be a check for any previous sexting attempt

                    if horny_lvl >= horny_reqs[2]:
                        $ persistent._nsfw_horny_level = horny_lvl - 10
                        $ persistent._nsfw_sext_sexy_start = True
                        m 6lkbfp "Aww, I was really enjoying myself."
                        m 6gkbfp "I hope whatever it is you need to do is important.{w=0.3}.{w=0.3}.{w=0.3}{nw}"
                        m 6hubfb "Ahaha! Just kidding~"
                        call nsfw_sexting_early_cleanup
                        return
                    elif horny_lvl >= horny_reqs[1]:
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

        # Set new previous category/type/subtype to the new prompt's
        $ previous_vars = [player_prompts[prompt_choice][1], player_prompts[prompt_choice][2], player_prompts[prompt_choice][3]]

        if previous_vars[0] == "sexy":
            $ horny_lvl += 5
        elif previous_vars[0] == "hot":
            $ horny_lvl += 3
        else: # Default
            $ horny_lvl += 1

        python:
            if shouldkiss_cooldown > 0:
                shouldkiss_cooldown -= 1
            if "KIS" in previous_vars[2]: # Override cooldown and kiss right away if the player picks a prompt that asks for a kiss
                shouldkiss = True
            elif "kiss" in player_prompts[prompt_choice] and random.randint(1,5) == 1:
                if shouldkiss_cooldown == 0:
                    shouldkiss = True

        if shouldkiss and persistent._mas_first_kiss:
            call monika_kissing_motion_short
            $ shouldkiss = False
            $ shouldkiss_cooldown = 5

        python:
            # Monika's response to prompt
            monika_response = mas_nsfw.create_sexting_response(
                horny_lvl=horny_lvl,
                horny_reqs=horny_reqs,
                previous_vars=previous_vars,
                recent_responses=recent_responses
            )

            response_ending = monika_response[5]
            response_start = monika_response[4]

        if previous_vars[1] == "funny":
            show monika sexting_funny_poses
        elif horny_lvl >= horny_reqs[2]:
            show monika sexting_sexy_response_poses
        elif horny_lvl >= horny_reqs[1] and previous_vars[1] == "command":
            show monika sexting_hot_mast_poses
        elif horny_lvl >= horny_reqs[1]:
            show monika sexting_hot_mast_poses
        else:
            show monika sexting_cute_poses

        if previous_vars[1] == "funny":
            m "[monika_response[0]][response_ending]"
        else:
            m "[response_start][monika_response[0]][response_ending]"

        # undress if asked by player
        if mas_SELisUnlocked(store.mas_clothes_underwear_white) and "UND" in previous_vars[2] and not hot_transfer:
            python:
                if persistent._nsfw_lingerie_on_start:
                    if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                        if store.ahc_utils.hasUnlockedClothesOfExprop("lingerie") and not store.ahc_utils.isWearingClothesOfExprop("lingerie"):
                            shouldchange = 2
                        elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                            shouldchange = 1
                    elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
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

        elif store.mas_SELisUnlocked(store.mas_clothes_birthday_suit) and "UND" in previous_vars[2] and not sexy_transfer:
            call store.mas_clothes_change(outfit=mas_clothes_birthday_suit, outfit_mode=False, exp="6hubfb", restore_zoom=False)
            m 6hubfb "Hah~ That feels better."
            $ sexy_transfer = True

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
                recent_prompts.insert(0, player_prompts[x][0])

            if len(recent_responses) >= 10: # Responses
                recent_responses.pop()
            recent_responses.insert(0, monika_response[0])

            if len(recent_quips) >= 10: # Quips
                recent_quips.pop()
            recent_quips.insert(0, monika_quip[0])

        if horny_lvl >= horny_reqs[2] and sexy_transfer == False:
            $ sexy_transfer = True
            call nsfw_sexting_sexy_transfer
        elif horny_lvl >= horny_reqs[1] and hot_transfer == False:
            $ hot_transfer = True
            call nsfw_sexting_hot_transfer
        elif horny_lvl >= horny_reqs[3]:
            call nsfw_sexting_finale
            if horny_lvl >= horny_reqs[3]:
                return

label nsfw_sexting_init:
    if "lingerie" not in monika_chr.clothes.ex_props:
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
    #elif persistent._nsfw_sext_hot_start or persistent._nsfw_sext_sexy_start: | - Not sure what this is here for, but commenting it out in-case we need it somewhere
    #    call nsfw_sexting_main                                                |
    else:
        $ last_sexted_since = datetime.datetime.now() - persistent._nsfw_last_sexted
        if persistent._nsfw_sext_sexy_start == True:
            if last_sexted_since < datetime.timedelta(hours=1):
                m 1hkb "Ahaha~ I was worried you were going to leave me out to dry..."
                m 1tsblu "I hope you're prepared to make amends for making me wait~"

                if persistent._nsfw_has_unlocked_birthdaysuit:
                    call mas_clothes_change(outfit=mas_clothes_birthday_suit, outfit_mode=False, exp="3tublb", restore_zoom=False)
                else:
                    python:
                        if persistent._nsfw_lingerie_on_start:
                            if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                                if store.ahc_utils.hasUnlockedClothesOfExprop("lingerie") and not store.ahc_utils.isWearingClothesOfExprop("lingerie"):
                                    shouldchange = 2
                                elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                                    shouldchange = 1
                            elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
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

                m 3tublb "Now [player]...where were we?"
            elif last_sexted_since < datetime.timedelta(hours=2):
                $ persistent._nsfw_sext_sexy_start = False
                $ persistent._nsfw_sext_hot_start = True
                m 1tub "Ehehe~ Took you long enough, [player]."
                m 3tua "I hope you're prepared to make amends for making me wait."

                if persistent._nsfw_lingerie_on_start:
                    if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                        if store.ahc_utils.hasUnlockedClothesOfExprop("lingerie") and not store.ahc_utils.isWearingClothesOfExprop("lingerie"):
                            $ shouldchange = 2
                        elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                            $ shouldchange = 1
                    elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
                        $ shouldchange = 1

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

                if persistent._nsfw_lingerie_on_start:
                    if store.mas_submod_utils.isSubmodInstalled("Auto Outfit Change"):
                        if store.ahc_utils.hasUnlockedClothesOfExprop("lingerie") and not store.ahc_utils.isWearingClothesOfExprop("lingerie"):
                            $ shouldchange = 2
                        elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                            $ shouldchange = 1
                    elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
                        $ shouldchange = 1

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
        else:
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
                    elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # unlikely case where player has AHC but no lingerie unlocked
                        shouldchange = 1
                elif mas_SELisUnlocked(store.mas_clothes_underwear_white): # player doesn't have AHC but does have submod underwear
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
    ## Just a little bit of RNG to keep things interesting.
    $ rng = mas_nsfw.return_random_number(1,6)

    if rng == 1:
        m 6hkbfc "I'm getting really close."
    elif rng == 2:
        m 6hkbfc "I'm getting really... really close..."
    elif rng == 3:
        m 6hkbfc "I'm nearly ready to... to finish..."
    elif rng == 4:
        m 6hkbfc "I think... I'm really close..."
    elif rng == 5:
        m 6hkbfc "I-I think I'm... I'm getting really close to..."
    else:
        m 6hkbfc "I-I'm getting really close. I-I can't last much longer."
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

            $ persistent._nsfw_horny_level = 0 # This is roughly where it happens in the real thing right? ... right?

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
                    if mas_isDayNow():
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
            $ persistent._nsfw_sexting_count += 1

            $ persistent._nsfw_sexting_attempts = 0 # Resets Monika sexting attempt count back to 0, if player initiated and Monika was set to low frequency

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
                    if mas_isDayNow():
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
