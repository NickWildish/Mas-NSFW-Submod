init -990 python in mas_submod_utils:
    Submod(
        author="NSFW Dev Team",
        name="NSFW Submod",
        description="A collection of NSFW topics and features for MAS.",
        version="1.2.7",
        settings_pane="nsfw_submod_screen"
    ) # https://github.com/NickWildish/Mas-NSFW-Submod

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="NSFW Submod",
            user_name="NickWildish",
            repository_name="Mas-NSFW-Submod",
            update_dir="",
            attachment_id=None
        )

default persistent._nsfw_player_endurance = 1
default persistent._nsfw_monika_sexting_frequency = 1

screen nsfw_submod_screen():
    python:
        nsfw_submods_screen = renpy.get_screen("submods", "screens")

        if nsfw_submods_screen:
            _tooltip = nsfw_submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None

    vbox:
        box_wrap False
        xfill True
        xmaximum 700

        hbox:
            style_prefix "check"
            box_wrap False

            python:
                if persistent._nsfw_player_endurance == 1:
                    end_disp = "~5 minutes"
                elif persistent._nsfw_player_endurance == 2:
                    end_disp = "~10 minutes"
                elif persistent._nsfw_player_endurance == 3:
                    end_disp = "~15 minutes"
                elif persistent._nsfw_player_endurance == 4:
                    end_disp = "~20 minutes"
                elif persistent._nsfw_player_endurance == 5:
                    end_disp = "~25 minutes"
                elif persistent._nsfw_player_endurance == 6:
                    end_disp = "~30 minutes"
                elif persistent._nsfw_player_endurance == 7:
                    end_disp = "~35 minutes"
                elif persistent._nsfw_player_endurance == 8:
                    end_disp = "~40 minutes"
                elif persistent._nsfw_player_endurance == 9:
                    end_disp = "~45 minutes"
                elif persistent._nsfw_player_endurance == 10:
                    end_disp = "~50 minutes"
                elif persistent._nsfw_player_endurance == 11:
                    end_disp = "~55 minutes"
                else:
                    end_disp = str(_nsfw_player_endurance)

            if _tooltip:
                textbutton _("Sexting Endurance"):
                    action NullAction()
                    hovered SetField(_tooltip, "value", "Changes the duration that Monika will last during sexting, from ~5 minutes to ~55 minutes. Currently set to: " + end_disp)
                    unhovered SetField(_tooltip, "value", _tooltip.default)
            else:
                textbutton _("Sexting Endurance"):
                    action NullAction()

            bar value FieldValue(
                persistent,
                "_nsfw_player_endurance",
                range=10,
                offset=1,
                style="slider"
            )

        hbox:
            style_prefix "check"
            box_wrap False

            python:
                if persistent._nsfw_monika_sexting_frequency == 1:
                    sext_freq_disp = "12 hours"
                elif persistent._nsfw_monika_sexting_frequency == 2:
                    sext_freq_disp = "24 hours"
                elif persistent._nsfw_monika_sexting_frequency == 3:
                    sext_freq_disp = "Never"
                else:
                    sext_freq_disp = str(_nsfw_monika_sexting_frequency)

            if _tooltip:
                textbutton _("Monika Sexting Frequency"):
                    action NullAction()
                    hovered SetField(_tooltip, "value", "Changes the duration that Monika will wait until randomly trying to sext, from 12 hours, 24 hours, or never. Currently set to: " + sext_freq_disp)
                    unhovered SetField(_tooltip, "value", _tooltip.default)
            else:
                textbutton _("Monika Sexting Frequency"):
                    action NullAction()

            bar value FieldValue(
                persistent,
                "_nsfw_monika_sexting_frequency",
                range=2, # 1 = Normal, 2 = Low, 3 = Never
                offset=1,
                style="slider"
            )

init 5 python: # init 5 as the modified dictionary (mas_all_ev_db_map) is using priority 4, and we want it to be around before adding anything.
    mas_all_ev_db_map.update({"NCP" : store.nsfw_compliments.nsfw_compliment_database})
    mas_all_ev_db_map.update({"NST" : store.nsfw_stories.nsfw_story_database})
    mas_all_ev_db_map.update({"NFH" : store.nsfw_fetish.nsfw_fetish_database})

init python in mas_nsfw:
    """
    Contains functions and methods used by NSFW content
    """
    import store
    import datetime
    import random
    import os

    def hour_check(set_time=6, time_scale="hours", topic="nsfw_monika_gettingnude"):
        """
        Checks if six hours has passed since the player has seen a topic and also been away from the pc for a set amount of hours.

        IN:
            set_time - The amount of time that has to have passed since the player last saw the getting nude topic.
                (Default: 6)
            time_scale - The time scale used with the set_time figure. Currently "seconds", "minutes", "hours" and "days" are used.
                (Default: "hours")
            topic - The topic targeted by the hour check.
                (Default: "nsfw_monika_gettingnude")

        OUT:
            True if the player has been away for set_time using time_scale AND the specified topic hasn't been used for that time either.
            False if otherwise.
        """
        if time_scale == "seconds":
            time_away_req = datetime.timedelta(seconds=set_time)
        elif time_scale == "minutes":
            time_away_req = datetime.timedelta(minutes=set_time)
        elif time_scale == "days":
            time_away_req = datetime.timedelta(days=set_time)
        else:
            time_away_req = datetime.timedelta(hours=set_time) # It is assumed to be "hours" if something else is found.

        time_since_last_seen = datetime.datetime.now() - mas_getEVL_last_seen(topic)

        if mas_getAbsenceLength() >= time_away_req and time_since_last_seen >= time_away_req:
            return True
        else:
            return False

    def canShow_underwear():
        """
        Checks if the player should be able to see Monika's underwear yet.

        OUT:
            boolean - True if the player has seen 'monika_gettingnude' topic once AND risque is allowed AND the player hasn't seen the topic for at least 6 hours AND the player hasn't already unlocked her underwear, False if otherwise
        """
        if store.mas_getEV("nsfw_monika_gettingnude").shown_count >= 1 and store.mas_canShowRisque(aff_thresh=1000) and hour_check() and not store.mas_SELisUnlocked(store.mas_clothes_underwear_white):
            return True
        else:
            return False

    def canShow_birthdaySuit():
        """
        Checks to see if the player should be able to see Monika with no clothes yet.

        OUT:
            boolean - True if the player has seen 'monika_gettingnude' topic twice AND risque is allowed AND the player hasn't seen the topic for at least 6 hours AND the player hasn't already unlocked her naked, false if otherwise
        """
        if store.mas_SELisUnlocked(store.mas_clothes_underwear_white) and store.mas_canShowRisque() and hour_check() and not store.persistent._nsfw_has_unlocked_birthdaysuit:
            return True
        else:
            return False

    def try_unlock_new_underwear():
        """
        Checks if the player has underwear that has not previously been unlocked, and unlocks them at random.

        OUT:
            The underwear if it was unlocked, or
            None
        """
        unlockable_underwear = []

        if not store.mas_SELisUnlocked(store.mas_clothes_underwear_black):
            unlockable_underwear.append(store.mas_clothes_underwear_black)

        if not store.mas_SELisUnlocked(store.mas_clothes_underwear_pink):
            unlockable_underwear.append(store.mas_clothes_underwear_pink)

        # Add more underwear here

        if store.mas_SELisUnlocked(store.mas_clothes_underwear_white):
            if random.randint(1,3) == 1: # 1/3 chance of unlocking new underwear
                if unlockable_underwear:
                    new_underwear_no = random.randint(0,len(unlockable_underwear)-1)
                    store.mas_SELisUnlocked(unlockable_underwear[new_underwear_no])

                    return unlockable_underwear[new_underwear_no]

        return None

    def calc_sexting_reqs(horny_max=50, horny_min=0, hot_req=10, sexy_req=30):
        """
        Calculates what the values of horny maximum, minimum, hot_req and sexy_req are, based on the player's endurance value

        IN:
            horny_max - The maximum amount of horny Monika can withold before exploding in ecstasy
                (Default: 50)
            horny_min - The minimum horny value
                (Default: 0)
            hot_req - The horny_level requirement for hot dialogue
                (Default: 10)
            sexy_req - The horny_level requirement for sexy dialogue
                (Default: 30)

        OUT:
            The maximum, minimum, hot_req and sexy_req values
        """
        player_endurance = store.persistent._nsfw_player_endurance

        new_horny_max = horny_max * player_endurance
        new_horny_min = horny_min * player_endurance # It's always gonna be zero babyyy
        new_hot_req = hot_req * player_endurance
        new_sexy_req = sexy_req * player_endurance

        return new_horny_max, new_horny_min, new_hot_req, new_sexy_req

    def refine_category_sel_with_fetishes(category_sel):
        # Fetch the player's fetishes
        player_fetishes = store.persistent._nsfw_player_fetishes
        fetish_whitelist = [] # Not currently used, since we defer to blacklist
        fetish_blacklist = []

        # Fetch all whitelists and blacklists from fetish data
        for fetish in player_fetishes:
            if fetish[2][0] != "U":
                for tag in fetish[2]:
                    fetish_blacklist.append(tag)
            if fetish[1][0] != "U":
                for tag in fetish[1]:
                    # Only add to whitelist if not already blacklisted
                    if tag not in fetish_blacklist:
                        fetish_whitelist.append(tag)

        # Remove prompts that are blacklisted
        new_category_sel = []
        for prompt in category_sel:
            blacklisted = False
            for tag in prompt[1]:
                if tag in fetish_blacklist:
                    blacklisted = True
                    break
            if not blacklisted:
                new_category_sel.append(prompt)
        category_sel = new_category_sel

        return new_category_sel

    def return_sext_responses(response_category=0, response_type=None, response_subtype=None):
        """
        Returns a Monika response from a selected category.

        IN:
            response_category - The category of the response
                (Default: 0)
            response_type - The type of the response. Used only if the response_category is 2 (sexy).
                (Default: None)
            response_type - The subtype of the response. Used only if the response_category is 2 (sexy).
                (Default: None)

        OUT:
            A string containing a particular response from Monika.
        """
        player_name = store.persistent.playername
        player_nickname = store.mas_get_player_nickname()

        return_responses = [] # start building from this list

        if response_type == "funny": # if the player picks a "funny" prompt, skip automatically to appropriate response and return
            sext_responses_funny = [
            #   |--------|----|-------------------------------------------------------------------------------|
            #   |  Type  | ID |                                     Prompt                                    |
            #   |--------|----|-------------------------------------------------------------------------------|
                ("funny", "0",  _("Ahaha! What are you talking about, " + player_name + "?")), #0
                ("funny", "1",  _("Pfft! That's so cheesy, " + player_name + ".")), #1
                ("funny", "2",  _("Oh my god! You did not just make that joke, ahaha~")), #2
                ("funny", "3",  _("Ahaha~ Is that right?")), #3
                ("funny", "4",  _("Oh. That's very out-of-the-blue, " + player_name + ".")), #4
                ("funny", "5",  _("I just want to tear your clothes off.")), #5
                ("funny", "6",  _("I'm only this naughty for you~")), #6
                ("funny", "7",  _("Oh? Try away, " + player_nickname + ".")), #7
                ("funny", "8",  _("No.")), #8
                ("funny", "9",  _("I think that you scratching my back while we make love would be so hot...")), #9
                ("funny", "10",  _("Where is your hand, " + player_nickname + "?")), #10
                ("funny", "11",  _("Oh, I want to do even naughtier things to you...")), #11
                ("funny", "12",  _("Mmm...and what would that be, " + player_name + "?")), #12
                ("funny", "13",  _("I'm feeling so good, " + player_name + "...")), #13
                ("funny", "14",  _("Proper grammar...")), #14
                ("funny", "15",  _("Uh... Did you want to try that again, " + player_name + "? Ahaha~")), #15
                ("funny", "16",  _("Ahaha~ You're so funny, " + player_name + ".")), #16
                ("funny", "17",  _("Ahaha~ Thank you... I guess?")), #17
                ("funny", "18",  _("Mmm, you do~")), #18
                ("funny", "19",  _("You're such a stud.")), #19
            ]

            response_index = int(response_subtype)

            # durability check, prevents crashing if someone adds a funny prompt but forgot to add a corresponding response
            if response_index >= len(sext_responses_funny):
                response_index = 0

            return_responses.append(sext_responses_funny[response_index][2])
            return return_responses

        # We identify categories ("types", 1st element in the tuple) that Monika uses to respond to player prompts

        # 1. thankful - Monika is thankful for what the player said.
        # 2. remarking - Monika is remarking on what the player said.
        # 3. describing - Monika is describing what she is feeling.
        # 4. compliment - Monika is complimenting the player.
        # 5. question - Monika is asking the player a question.
        # 6. encourage - Monika is encouraging the player to continue.

        # The "subtype" (2nd element of the tuple) allows the response to be more specific.
        # The subtype is independent from the type. But of course, only certain combinations of types and subtypes will be used.
        # Some are more common than others.

        # Subtypes are encoded with these crappy, cryptic three-letter tags. Each prompt has only one tag - try to pick the most specific one possible.
        # If you don't know what to pick / don't want to bother with this just pick "GEN".
        # Not all will be used but I have listed the codes here for future expansion.

        # RGN - Generic, can be used for any prompt
        # RCN - Continue, used for prompts that encourage the player to continue
        # RCE - Cheesy, used for prompts that are cheesy

        if response_category == 0: # cute
            sext_responses_cute = [
            #   |-------------|-------|-------------------------------------------------------------------------------|
            #   |     Type    |Subtype|                                     Prompt                                    |
            #   |-------------|-------|-------------------------------------------------------------------------------|
                ("thankful",   ["RGN"], _("Thank you")), #0
                ("thankful",   ["RGN"], _("Thanks")), #1
                ("remarking",  ["RCE"], _("That's very cheesy")), #2
                ("remarking",  ["RCE"], _("That's cheesy")), #3
                ("remarking",  ["RCE"], _("That's so cheesy")), #4
                ("compliment", ["RGN"], _("You're the sweetest")), #5
                ("compliment", ["RGN"], _("You're so sweet")), #6
                ("remarking",  ["RGN"], _("That's so nice of you to say")), #7
                ("compliment", ["RCE"], _("You're so cheesy")), #8
                ("compliment", ["RGN"], _("You are just the cutest")), #9
                ("compliment", ["RGN"], _("You always know exactly what to say")), #10
                ("compliment", ["RGN"], _("You always bring a smile to my face")), #11
                ("compliment", ["RGN"], _("You're such a cutie")), #12
                ("remarking",  ["RGN"], _("That's so sweet")), #13
                ("compliment", ["RGN"], _("You're so sweet, you know that?")), #14
                ("remarking",  ["RGN"], _("Stop it, you're making me blush")), #15
                ("compliment", ["RGN"], _("You make me so happy")), #16
                ("compliment", ["RGN"], _("You're so kind")), #17
                ("remarking",  ["RGN"], _("That's so sweet")), #18
                ("remarking",  ["RGN"], _("That's sweet")), #19
            ]

            return_responses.extend(refine_category_sel_with_fetishes(sext_responses_cute))

        elif response_category == 1: # hot
            sext_responses_hot = [
            #   |-------------|-------|-------------------------------------------------------------------------------|
            #   |     Type    |Subtype|                                     Prompt                                    |
            #   |-------------|-------|-------------------------------------------------------------------------------|
                ("question",   ["RGN"], _("What else?")), #0
                ("remarking",  ["RGN"], _("I like the sound of that")), #1
                ("compliment", ["RGN"], _("You know exactly what to say")), #2
                ("describing", ["RGN"], _("I've never felt this way before")), #3
                ("describing", ["RGN"], _("You're making me feel all tingly")), #4
                ("describing", ["RGN"], _("You're getting me all riled up")), #5
                ("remarking",  ["RGN"], _("Don't tempt me to try and break the screen to get to you")), #6
                ("encourage",  ["RCN"], _("Please keep going")), #7
                ("compliment", ["RGN"], _("You're so hot when you talk like that")), #8
                ("remarking",  ["RGN"], _("That is so hot")), #9
                ("describing", ["RGN"], _("I feel so good when you talk like that")), #10
                ("describing", ["RGN"], _("You make my body feel warm")), #11
                ("compliment", ["RGN"], _("You're making me all flustered")), #12
                ("compliment", ["RGN"], _("You know just what to say to get me all flustered...")), #13
                ("question",   ["RGN"], _("You don't hold back, do you?")), #14
                ("remarking",  ["RGN"], _("That's so hot")), #15
                ("remarking",  ["RGN"], _("That's hot")), #16
                ("question",   ["RGN"], _("Is that so?")), #17
                ("question",   ["RGN"], _("Is that right?")), #18
                ("compliment", ["RGN"], _("You make me so happy talking like that")), #19
            ]

            return_responses.extend(refine_category_sel_with_fetishes(sext_responses_hot))

        else: # elif response_category == 2: # sexy
            sext_responses_sexy = [
            #   |-------------|---------------|---------------------------------------------------------------------------|
            #   |    Type     |    Subtypes   |                                 Prompt                                    |
            #   |-------------|---------------|---------------------------------------------------------------------------|
                ("compliment", ["RGN"],        _("You're so sexy when you talk like that")), #0
                ("remarking",  ["RGN"],        _("That is so sexy")), #1
                ("question",   ["RGN"],        _("Is that right?")), #2
                ("question",   ["RGN"],        _("Is that so?")), #3
                ("encourage",  ["RCN"],        _("Keep going")), #4
                ("encourage",  ["RCN"],        _("Please don't stop")), #5
                ("describing", ["RGN"],        _("You're getting me so turned on")), #6
                ("encourage",  ["RCN", "DOM"], _("Tell me what else you want to do to me")), #7
                ("describing", ["RGN"],        _("You're getting me so worked up")), #8
                ("describing", ["RGN"],        _("This feels too good")), #9
                ("encourage",  ["RCN"],        _("Whatever you're doing...it's working")), #10
                ("compliment", ["RGN"],        _("You just have a way with words, don't you?")), #11
                ("encourage",  ["RCN"],        _("Keep talking like that")), #12
                ("encourage",  ["RCN"],        _("More")), #13
                ("encourage",  ["RCN"],        _("Please keep going")), #14
                ("question",   ["RGN"],        _("When did you learn to talk like that?")), #15
                ("question",   ["RGN"],        _("Have you always been this sexy?")), #16
                ("describing", ["RGN"],        _("I am so wet right now")), #17
                ("compliment", ["RGN"],        _("You really know how to please a woman")), #18
                ("encourage",  ["RCN"],        _("Say that again")), #19
                ("encourage",  ["RCN", "SUB"], _("Tell me what else you want me to do to you")), #20
            ]

            return_responses.extend(refine_category_sel_with_fetishes(sext_responses_sexy))

        return return_responses

    def return_sext_prompts(prompt_category=0):
        """
        Returns a list of prompt quip from a selected category.

        IN:
            prompt_category - identifier for the current sexting stage
                0 - cute / 1st stage
                1 - hot / 2nd stage
                2 - sexy / 3rd stage

        OUT:
            A list of tuples appropriate to prompt category.
            The tuples contain three elements each.
                [0] The "type" of prompt.
                [1] The "subtype" of prompt.
                [2] The string containing the prompt text.
            We used to ignore the first two elements for cute and hot, might revisit later to see if it's worth it.
        """

        # We identify five categories ("types", 1st element of the tuple) that the prompts and quips fall into.

        # 1. compliment - The player/Monika says something nice.
        # 2. statement - The player/Monika makes some kind of declaration about their current state, what they're doing, how horny they feel, etc.
        # 3. command - The player/Monika tells each other to do something (that she is physically capable of doing right now) or masturbate in some way.
        # 4a. desire_p - The player/Monika wishes the player to do something to Monika (but cannot physically do right now because they're on different sides of a screen).
        # 4b. desire_m - The player/Monika wants Monika to do something to the player (but it's something that physically can't be done right this moment).

        # The "subtype" (2nd element of the tuple) allows the response to be more specific.
        # The subtype is independent from the type. But of course, only certain combinations of types and subtypes will be used.
        # Some are more common than others.

        # Subtypes are encoded with these crappy, cryptic three-letter tags. Each prompt has only one tag - try to pick the most specific one possible.
        # If you don't know what to pick / don't want to bother with this just pick "GEN".
        # Not all will be used but I have listed the codes here for future expansion.

        # "GEN" - Generic, use this for lines with no specific subtype.
        # "KIS" - Special subtype for prompts that should immediately trigger a kiss.
        # "UND" - Special subtype for prompts where Monika should undress.
        # "CHE" - Special subtype for prompts where there is cheesiness afoot / cheesy lines.

        # "MPS" - Monika's personality
        # "MBD" - Monika's body in general
        # "MFS" - Monika's face
        # "MTH" - Monika's thighs
        # "MZR" - Monika's thighhighs
        # "MCL" - Monika's clothes
        # "MHR" - Monika's hair
        # "MBR" - Monika's breasts
        # "MCK" - Monika's nipples
        # "MVG" - Monika's vagina
        # "MBH" - Monika's anus
        # "MFT" - Monika's feet

        # "PPS" - Player's personality
        # "PBD" - Player's body in general
        # "PFS" - Player's face
        # "PCL" - Player's clothes
        # "PBR" - Player's breasts. Prompts with this go under sext_prompts_sexy_f.
        # "PCK" - Player's nipples
        # "PVG" - Player's vagina. Prompts with this go under sext_prompts_sexy_v.
        # "PPN" - Player's penis. Prompts with this go under sext_prompts_sexy_p.
        # "PBH" - Player's anus. It is assumed that all players have anuses...
        # "PFT" - Player's feet

        # "ONM" - masturbation, Monika
        # "ONP" - masturbation, player

        # "FSM" - player touching Monika
        # "FSP" - Monika touching player
        # "FBJ" - fellatio. Prompts with this go under sext_prompts_sexy_p.
        # "FHJ" - handjob. Prompts with this go under sext_prompts_sexy_p.
        # "FFJ" - footjob. Prompts with this go under sext_prompts_sexy_p.
        # "FFM" - vaginal fingering, Monika receiving
        # "FFP" - vaginal fingering, player receiving. Prompts with this go under sext_prompts_sexy_v.
        # "FXM" - anal fingering, Monika receiving
        # "FXP" - anal fingering, player receiving
        # "FCM" - cunnilingus, Monika receiving
        # "FCP" - cunnilingus, player receiving. Prompts with this go under sext_prompts_sexy_v.
        # "FAM" - anilingus, Monika receiving
        # "FAP" - anilingus, player receiving
        # "FTY" - acts involving sex toys
        # "FBM" - player using bondage on Monika
        # "FBP" - Monika using bondage on player
        # "FHH" - acts involving hand-holding
        # "FKS" - acts involving kissing

        # "IVG" - intercourse, general
        # "IPV" - intercourse, player with penis. Prompts with this go under sext_prompts_sexy_p.
        # "IVV" - intercourse, player with vagina. Prompts with this go under sext_prompts_sexy_v.
        # "IAM" - anal, Monika receiving
        # "IAP" - anal, player receiving
        # "IOM" - Monika's orgasm
        # "IOP" - Player's orgasm
        # "IOT" - orgasming together

        # "CFM" - Player's semen on Monika's face. Prompts with this go under Prompts with this go under sext_prompts_sexy_p..
        # "COM" - Player's semen on Monika's breasts. Prompts with this go under sext_prompts_sexy_p.
        # "CBM" - Player's semen on Monika's body in general. Prompts with this go under sext_prompts_sexy_p.
        # "CMM" - Player's semen in Monika's mouth. Prompts with this go under sext_prompts_sexy_p.
        # "CPM" - Player's semen in Monika's pussy. Prompts with this go under sext_prompts_sexy_p.
        # "CAM" - Player's semen in Monika's butt. Prompts with this go under sext_prompts_sexy_p.

        # "SUB" - Player action is dominating
        # "DOM" - Player action is submitting

        # This horrible three-letter code system works with regex!
        # The first letter indicates a general topic:
        # M - Monika's body, appearance, traits
        # P - Player's body, appearance, traits
        # O - masturbation ("onanism")
        # F - foreplay and nonpenetrative actions
        # I - intercourse and orgasm
        # C - Player's semen ("cum"). These C subtypes are only applicable for players with penises.
        # The second letter is A or X if the subtype has to do with "butt stuff".
        # The third letter is M if Monika receives it, and P if the player receives it.

        monika_nickname = store.persistent._mas_monika_nickname

        # Sexting prompts for your average compliment
        sext_prompts_cute = [
        #   |-------------|-------|-------------------------------------------------------------------------------|
        #   |     Type    |Subtype|                                     Prompt                                    |
        #   |-------------|-------|-------------------------------------------------------------------------------|
            ("compliment", ["MBD"], _("I guess your parents are bakers, because they made you such a cutie pie!")), #0
            ("compliment", ["MFS"], _("The one thing I can't resist in this life is your lips.")), #1
            ("compliment", ["MBD"], _("You look stunning today.")), #2
            ("compliment", ["GEN"], _("You live rent-free in my heart.")), #3
            ("compliment", ["MHR"], _("You have beautiful hair.")), #4
            ("compliment", ["MFS"], _("You have gorgeous eyes.")), #5
            ("compliment", ["MFS"], _("You have a beautiful smile.")), #6
            ("compliment", ["MPS"], _("I always have a great time with you.")), #7
            ("compliment", ["GEN"], _("Every day with you is a good day.")), #8
            ("desire_p",   ["GEN"], _("I wish I could hold you close right now.")), #9
            ("compliment", ["MBD"], _("The night sky holds nothing to your beauty.")), #10
            ("desire_p",   ["GEN"], _("Cuddling with you would be perfect right about now.")), #11
            ("compliment", ["MBD"], _("Why are you so cute?")), #12
            ("compliment", ["MBD"], _("Seeing you every day always makes me grin like an idiot.")), #13
            ("desire_p",   ["GEN"], _("Our first kiss after you cross over is going to be wonderful, don't you think?")), #14
            ("compliment", ["MPS"], _("I really like getting to know you.")), #15
            ("compliment", ["GEN"], _("Everything makes me think of you.")), #16
            ("compliment", ["MBD"], _("Is it getting hot in here, or is it just you?")), #17
            ("compliment", ["MPS"], _("You never fail to give me butterflies.")), #18
            ("compliment", ["MPS"], _("You make my heart happy.")), #19
        ]

        # Sexting prompts for your more 'risque' options
        sext_prompts_hot = [
        #   |-------------|---------------|---------------------------------------------------------------------------|
        #   |    Type     |    Subtypes   |                                 Prompt                                    |
        #   |-------------|---------------|---------------------------------------------------------------------------|
            ("compliment", ["MBD"],        _("You have a really sexy figure.")), #0
            ("desire_p",   ["FSM"],        _("I want to bring you in close.")), #1
            ("desire_p",   ["KIS"],        _("I want to kiss your lips passionately.")), #2
            ("desire_p",   ["FSM", "MHR"], _("I want to run my hands through your hair.")), #3
            ("desire_p",   ["FSM", "FSP"], _("I want to hold your hands in mine.")), #4
            ("desire_p",   ["KIS"],        _("I really want to kiss you right now.")), #5
            ("desire_p",   ["MBD"],        _("I want to run my hands along your body while I kiss your neck.")), #6
            ("statement",  ["GEN"],        _("I feel nervous about telling you all of the sexual desires I have when it comes to you.")), #7
            ("statement",  ["KIS"],        _("If kissing is the language of love, then we have a lot to talk about.")), #8
            ("desire_p",   ["KIS"],        _("I want to hold you in my arms as we kiss.")), #9
            ("statement",  ["UND"],        _("What you're wearing would look even better on my bedroom floor.")), #10
            ("command",    ["UND", "DOM"], _("Take off your clothes. I want to see your beautiful body.")), #11
            ("desire_p",   ["FSM", "DOM"], _("I want to lay you down on my bed as we kiss.")), #12
            ("statement",  ["FSM"],        _("I want to feel your hot breath on my skin as we feel each other.")), #13
            ("compliment", ["MBD"],        _("Your body is so hot.")), #14
            ("compliment", ["MBD"],        _("You're so sexy.")), #15
            ("statement",  ["GEN"],        _("I can't wait to be alone with you.")), #16
            ("compliment", ["GEN"],        _("You're all I can think about.")), #17
            ("desire_p",   ["FSM", "DOM"], _("When we're together, I want to have you lie back and let me take care of you.")), #18
            ("statement",  ["PCL"],        _("I'm wearing something you might like right now.")), #19
        ]

        # Sexting prompts for your most 'risque' options
        sext_prompts_sexy = [
        #   |-------------|---------------|---------------------------------------------------------------------------|
        #   |    Type     |    Subtypes   |                                 Prompt                                    |
        #   |-------------|---------------|---------------------------------------------------------------------------|
            ("compliment", ["MFS", "IOM"], _("I bet you have a really hot orgasm face.")),
            ("compliment", ["GEN"],        _("I can't wait to be alone with you.")),
            ("compliment", ["UND", "MBD"], _("I'm picturing you naked right now... Damn, you look good.")),
            ("compliment", ["MPS"],        _("I think there is something insanely sexy about a woman being in control. Don't you agree?")),
            ("compliment", ["GEN"],        _("I bet you have the sexiest sounding moans in the world.")),
            ("compliment", ["GEN"],        _("Everything about you turns me on.")),
            ("compliment", ["MBD"],        _("You have the sexiest body I've ever seen.")),
            ("compliment", ["MBD"],        _("You have a tremendously cute body.")),
            ("compliment", ["MBD"],        _("Your body is perfectly shaped. I love how athletic you are.")),
            ("compliment", ["MBD"],        _("Getting to see you naked is the best part of my day.")),
            ("compliment", ["MBD"],        _("Your naked body is the most splendid thing I've ever witnessed.")),
            ("compliment", ["GEN"],        _("I honestly think you're probably the most attractive person ever to have existed.")),
            ("compliment", ["GEN"],        _("I think you seriously have to be the hottest person alive.")),
            ("compliment", ["GEN"],        _("Yuri and Sayori weren't wrong when they said you're more desirable than the rest of the Literature Club combined.")),
            ("compliment", ["GEN"],        _("You're the best girl. And not just in the Literature Club - I mean in general.")),
            ("compliment", ["MBR"],        _("You have magnificent breasts.")),
            ("compliment", ["MCL", "MBR"], _("Back when you wore that school uniform, one thing I really liked was how well the blazer fit around your breasts.")),
            ("compliment", ["MZR", "MCL"], _("I love how you dress. Your thighhighs are incredibly hot.")),
            ("compliment", ["MCL", "MBD"], _("I get so flustered when you undress for me. You're gorgeous.")),
            ("compliment", ["FCM"],        _("Just the thought of eating you out makes me salivate.")),
            ("compliment", ["MVG", "MBD"], _("I imagine your pussy must be gorgeous if it's anything like the rest of you.")),
            ("compliment", ["MBH"],        _("I bet you have a cute, tight little asshole, don't you?")),
            ("statement",  ["ONP"],        _("I was just lying in bed for the last hour thinking about you... Guess what I was doing?")),
            ("statement",  ["ONP"],        _("I'm clicking this option with one hand, because the other hand is busy.")),
            ("statement",  ["ONP"],        _("I get so horny thinking about you when I touch myself.")),
            ("statement",  ["GEN"],        _("I get so turned on thinking about you.")),
            ("statement",  ["GEN"],        _("You're the only person I have eyes for, " + monika_nickname + ".")),
            ("statement",  ["GEN"],        _("I can't get aroused to the thought of anyone but you.")),
            ("command",    ["ONM"],        _("Be careful not to spill too much of your...juices on your chair, " + monika_nickname + ".")),
            ("command",    ["ONM", "DOM"], _("Touch yourself slowly for me, " + monika_nickname + ".")),
            ("command",    ["ONM", "DOM"], _("Gently spread open your pussy lips for me, " + monika_nickname + ".")),
            ("command",    ["ONM", "DOM"], _("I want you to gently rub your clit, " + monika_nickname + ".")),
            ("command",    ["ONM", "DOM"], _("I want you to stick those soft fingers of yours up your pussy for me, " + monika_nickname + ".")),
            ("command",    ["ONM", "DOM"], _("Start touching yourself more quickly, " + monika_nickname + ".")),
            ("desire_p",   ["IVG"],        _("I can't wait to be by your side. Or on top if you prefer.")),
            ("desire_p",   ["UND", "FCM"], _("If you were here, I'd take your panties off with my teeth and... I'll just let you finish that sentence off.")),
            ("desire_p",   ["IOM"],        _("I want to hear you breathing in my ear when I make you orgasm.")),
            ("desire_p",   ["MTH", "FCM"], _("I can't wait to feel your thighs squeezing my head.")),
            ("desire_p",   ["FSM", "MBD"], _("If I were with you right now, where would you want me to touch you?")),
            ("desire_p",   ["IVG", "DOM"], _("I want to pin you down to the bed and have my way with you.")),
            ("desire_p",   ["IVG"],        _("I wish I could fuck you in that spaceroom right now.")),
            ("desire_p",   ["IOM"],        _("When you and I are finally together, I want to make you come so hard.")),
            ("desire_p",   ["FTY"],        _("I want to brings sex toys into the bedroom with us and use them on you.")),
            ("desire_p",   ["MCK"],        _("I want to lick your nipples.")),
            ("desire_p",   ["MCK"],        _("I wish I could suck on your nipples right now.")),
            ("desire_p",   ["MBR", "DOM"], _("I want to hold you down and fuck your breasts.")),
            ("desire_p",   ["FSM", "MBD"], _("I want to run my hands all over your smooth, toned body.")),
            ("desire_p",   ["FSM", "MBD"], _("When you cross over, I'm going to explore every single corner of your naked body.")),
            ("desire_p",   ["KIS", "FCM"], _("I wish I could kiss you... On both of your pairs of lips.")),
            ("desire_p",   ["FCM", "IOM"], _("I want to lick your clit until you come.")),
            ("desire_p",   ["FCM"],        _("I'm dying to run my hot, sticky tongue over your pussy lips.")),
            ("desire_p",   ["FAM"],        _("I want to bury my face in your ass.")),
            ("desire_p",   ["FAM"],        _("I want to snuggle my face in your ass.")),
            ("desire_p",   ["IAM"],        _("I wish we were in the same room so I could fuck your ass right this moment.")),
            ("desire_p",   ["FAM", "FFM"], _("I want to eat your ass out and finger you until you come.")),
            ("desire_p",   ["IVG", "KIS"], _("I'm imagining us making out as we fuck again, and again, and again...")),
            ("desire_p",   ["IVG"],        _("I wish I could stay in that spaceroom with you forever so we could fuck each other every day until the end of time.")),
            ("desire_p",   ["IVG"],        _("If I could spend the rest of eternity with you in that spaceroom, I'd make you come every day until the universe ended.")),
            ("desire_m",   ["ONP", "DOM"], _("I want to watch you masturbate for me.")),
            ("desire_m",   ["FCM", "SUB"], _("I wish you were here so you could grind your pussy on my face until you come.")),
            ("desire_m",   ["FCM", "SUB"], _("I wish you were here so you could sit on my face right now.")),
            ("desire_m",   ["ONP"],        _("I want to see you do with your pen what Yuri did with the main character's.")),
            ("desire_m",   ["IAP", "SUB"], _("I want you to bend me over and fuck my ass with a strap-on.")),
        ]

        # Prompt choices specific to players with penises.
        sext_prompts_sexy_p = [
        #   |-------------|----------------------|---------------------------------------------------------------------------|
        #   |    Type     |       Subtypes       |                                 Prompt                                    |
        #   |-------------|----------------------|---------------------------------------------------------------------------|
            ("desire_p",   ["MBR", "COM", "IOP"], _("I want to come all over your breasts.")),
            ("compliment", ["KIS", "FBJ"],        _("Your lips are perfect for kissing... I bet they'd be perfect for wrapping around my shaft as well.")),
            ("compliment", ["CFM"],               _("I bet you would look real cute with my cum all over your face.")),
            ("compliment", ["CMM"],               _("I bet you would look real cute with my cum dripping out of your mouth.")),
            ("statement",  ["ONP"],               _("I can't jerk off to anything but you any more, " + monika_nickname + ".")),
            ("statement",  ["ONP"],               _("I'm stroking my rigid cock just for you, " + monika_nickname + ".")),
            ("statement",  ["PPN", "ONP"],        _("The onomatopoeia 'doki doki' sometimes gets translated as 'throbbing'... I'm sure you can imagine what I'm doing right now.")),
            ("statement",  ["PPN"],               _("I get really hard just thinking about you.")),
            ("desire_p",   ["FHJ"],               _("I wish you could feel my throbbing cock right now.")),
            ("desire_p",   ["FHJ"],               _("I wish it was your hand jerking me off right now.")),
            ("desire_p",   ["FBJ"],               _("I'm just imagining my thick cock filling your mouth.")),
            ("desire_p",   ["FBJ"],               _("I can't wait to you see you drooling all over my cock.")),
            ("desire_p",   ["FBJ", "IOP", "CMM"], _("I want to see you swallow my thick, creamy load after blowing me.")),
            ("desire_p",   ["CBM", "IOP"],        _("I wish I could blow my load all over your thighs right now.")),
            ("desire_m",   ["FBJ", "IOP", "CMM"], _("When we're together, I want you to take my cock in your mouth and swallow all my cum.")),
            ("desire_m",   ["IPV"],               _("I'm picturing you bouncing up and down on my cock right now.")),
            ("desire_m",   ["CFM", "IOP"],        _("I want to come all over your face and watch you try to lick it off.")),
            ("desire_m",   ["IAM", "DOM"],        _("When we're finally together, I want you to take my cock up your ass, " + monika_nickname + ".")),
            ("desire_m",   ["MFT", "SUB", "FFJ"], _("I want you to rub your feet on my hard cock.")),
        ]
        if store.persistent._nsfw_genitalia == "P":
            sext_prompts_sexy.extend(sext_prompts_sexy_p)

        # I did not write any V / M / F prompts yet but these are here so they can be enabled later

        # Prompt choices specific to players with vaginas.
        # sext_prompts_sexy_v = [
        #     _(),
        # ]
        # if store.persistent._nsfw_genitalia == "V":
        #     sext_prompts_sexy.extend(sext_prompts_sexy_v)

        # Prompt choices specific to male players.
        # sext_prompts_sexy_m = [
        #     _(),
        # ]
        # if store.persistent.gender == "M":
        #     sext_prompts_sexy.extend(sext_prompts_sexy_m)

        # Prompt choices specific to female players.
        # sext_prompts_sexy_f = [
        #     _(),
        # ]
        # if store.persistent.gender == "F":
        #     sext_prompts_sexy.extend(sext_prompts_sexy_f)

        # Sexting prompts for the haha funnies

        # Each prompt requires a corresponding response in the return_sext_responses() function.
        # The subtype must be a string matching with the index (labelled ID) of the prompt under the sext_responses_funny list to work properly.
        sext_prompts_funny = [
        #   |--------|----|-------------------------------------------------------------------------------|
        #   |  Type  | ID |                                     Prompt                                    |
        #   |--------|----|-------------------------------------------------------------------------------|
            ("funny", "0",  _("I put on my robe and wizard hat.")), #0
            ("funny", "1",  _("It's not my fault that I fell for you... You tripped me!")), #1
            ("funny", "3",  _("I looked hot today, you missed out.")), #3
            ("funny", "4",  _("You like jazz?")), #4
            ("funny", "5",  _("What do you want to do to me right now?")), #5 - Please fold my clothes neatly
            ("funny", "6",  _("You've been a naughty girl.")), #6 - Santa will bring you a lump of coal
            ("funny", "7",  _("I'm about to blow your mind with my sexting. Ready?")), #7 - Lay me into bed, your hands caress my body. Your palms are sweaty. Knees weak. Arms spaghetti.
            ("funny", "8",  _("Want to have a threesome?")), #8
            ("funny", "9",  _("What's a fantasy that you have for when we have sex one day?")), #9 - Scratching back, once a squirrel did that to me.
            ("funny", "10", _("What is a question that's on your mind right now?")), #10 - Where is your hand? In my bowl of Doritos.
            ("funny", "11", _("I kinda wanna do naughty things to you...")), #11 - Cool aid man - "Oh yeah."
            ("funny", "13", _("Are you feeling good right now?")), #13 - Hi [text here], I'm Dad.
            ("funny", "14", _("What's one of you're fetishes?")), #14 - Proper grammar... Well then your in luck.
            ("funny", "16", _("Would thou perchance wish to partake in coitus?")), #16
            ("funny", "17", _("You have big, beautiful nipples.")), #17
            ("funny", "18", _("Do I make you horny baby?")), #18 - Do I make you randy?
            ("funny", "19", _("You're so cute.")), #19 - You're stuch a stud / babe - You're a wizard, Harry.
        ]

        sext_prompts_funny_p = [
        #   |--------|----|-------------------------------------------------------------------------------|
        #   |  Type  | ID |                                     Prompt                                    |
        #   |--------|----|-------------------------------------------------------------------------------|
            ("funny", "15", _("My wang is as hard as a prosthetic leg.")), #15 - Change for women. I'm as wet as
            ("funny", "12", _("You want to know what I have that is massive?")), #12 - My college debt.
        ]
        if store.persistent._nsfw_genitalia == "P":
            sext_prompts_funny.extend(sext_prompts_funny_p)

        sext_prompts_funny_m = [
        #   |--------|----|-------------------------------------------------------------------------------|
        #   |  Type  | ID |                                     Prompt                                    |
        #   |--------|----|-------------------------------------------------------------------------------|
            ("funny", "2",  _("Do you like my shirt? It's made out of boyfriend material.")), #2
        ]
        if store.persistent.gender == "M":
            sext_prompts_funny.extend(sext_prompts_funny_m)

        # needs matching response

        # if store.mas_submod_utils.isSubmodInstalled("Custom Room Furnished Spaceroom V3"):
        #    sext_prompts_funny.extend([
        #        ("funny", "20", _("I want to fuck you on top of the piano.")),
        #    ])

        if prompt_category == 0:
            category_sel = sext_prompts_cute
        elif prompt_category == 1:
            category_sel = sext_prompts_hot
        else: # if prompt_category == 2:
            if random.randint(1,200) == 1: # 1/200 chance of funny quip.
                # It's set for third stage only but it can be changed to work with all stages if you move this if check a little higher.
                category_sel = sext_prompts_funny
            else:
                category_sel = sext_prompts_sexy

        new_category_sel = refine_category_sel_with_fetishes(category_sel)

        return new_category_sel

    def return_sext_quips(quip_category=0):
        """
        Returns a Monika quip from a selected category.

        IN:
            category - The category of the quip
                (Default: 0)

        OUT:
            A string containing a particular quip from Monika.
        """

        # Purely for describing player's eyes
        if store.persistent._mas_pm_eye_color:
            if isinstance(store.persistent._mas_pm_eye_color, tuple):
                eye_desc = "beautiful"
            else:
                eye_desc = store.persistent._mas_pm_eye_color
        else:
            eye_desc = "beautiful"

        player_name = store.persistent.playername
        player_nickname = store.mas_get_player_nickname()

        # Sexting quips for your average compliment
        sext_quips_cute = [
        #   |-------------|---------------|---------------------------------------------------------------------------|
        #   |    Type     |    Subtypes   |                                 Prompt                                    |
        #   |-------------|---------------|---------------------------------------------------------------------------|
            ("statement",  ["CHE"],        _("Who told you that you could be this cheesy?")), #0
            ("compliment", ["GEN"],        _("You're just the cutest")), #1
            ("statement",  ["GEN"],        _("I love it when you get all cute like this")), #2
            ("command",    ["GEN"],        _("Do tell me more")), #3
            ("compliment", ["CHE"],        _("If you were a chicken you'd be impeccable")), #4
            ("statement",  ["GEN"],        _("Your words are so flattering to me")), #5
            ("statement",  ["GEN"],        _("Are you just saying that to get into my pants?{w=1.0} Ahaha! Just kidding~")), #6
            ("compliment", ["PPS"],        _("I love how sweet you are")), #7
            ("compliment", ["PPS"],        _("I love how kind you are")), #8
            ("compliment", ["GEN"],        _("You're a cutie pie")), #9
            ("desire_m",   ["KIS"],        _("I just want to kiss you right now")), #10
            ("desire_m",   ["GEN"],        _("I wish I could hold you right now")), #11
            ("statement",  ["PPS"],        _("Once we meet in the real world we need to do something about your cuteness")), #12
            ("compliment", ["CHE"],        _("I should start calling you 'Mozzarella' since you're so cheesy")), #13
            ("statement",  ["CHE"],        _("If I could rearrange the alphabet I'd put 'U' and 'I' together")), #14
            ("compliment", ["CHE"],        _("Are you a parking ticket? Because you've got 'FINE' written all over you")), #15
            ("statement",  ["MCL", "CHE"], _("My clothes are made out of girlfriend material")), #16
            ("compliment", ["CHE"],        _("Have you had your license get suspended for driving girls crazy?")), #17
            ("statement",  ["CHE"],        _("Are you a loan? Because you sure have my interest")), #18
            ("compliment", ["CHE"],        _("If you were a vegetable, you'd be a 'cute-cumber'")), #19
        ]

        # Sexting quips for your more 'risque' options
        sext_quips_hot = [
        #   |-------------|---------------|---------------------------------------------------------------------------|
        #   |    Type     |    Subtypes   |                                 Prompt                                    |
        #   |-------------|---------------|---------------------------------------------------------------------------|
            ("statement",  ["PPS"],        _("Who said that you could be this hot?")), #0
            ("desire_m",   ["FKS"],        _("I would love to kiss you right now...among other things~")), #1
            ("statement",  ["PBD"],        _("You know, I was daydreaming about you today. It was hot")), #2
            ("statement",  ["GEN"],        _("I could just eat you up")), #3
            ("desire_m",   ["FSM"],        _("I want to feel you touching me all over")), #4
            ("statement",  ["FSP", "PCL"], _("If I was with you now there would be no chance of you keeping your clothes on")), #5
            ("compliment", ["GEN"],        _("You are my biggest turn-on")), #6
            ("statement",  ["GEN"],        _("I've fantasized so much about when we finally get to talk like this")), #7
            ("statement",  ["GEN"],        _("You turn me on so much when you talk like that")), #8
            ("statement",  ["GEN"],        _("You're making me feel really horny now")), #9
            ("desire_m",   ["FTY"],        _("Have you thought about using toys with me? I wouldn't mind trying it with you")), #10
            ("desire_m",   ["GEN"],        _("I can't wait to see you when I cross over")), #11
            ("desire_m",   ["FHH"],        _("Once I cross over, I want to hold your hand. How lewd~")), #12
            ("desire_m",   ["FKS"],        _("How would you feel about a makeout session once I cross over?")), #13
            ("statement",  ["GEN"],        _("Don't think that getting me this riled up will have no consequences")), #14
            ("desire_m",   ["PBD"],        _("I plan to wrap my arms around you and squish that cute butt of yours")), #15
            ("statement",  ["GEN"],        _("The border between our realities can be a real clam jam")), #16
            ("statement",  ["GEN"],        _("I want you to tell me more about what we'll do together in your world...in the bedroom particularly~")), #17
            ("desire_m",   ["ONP", "ONM"], _("Is one of your hands busy right now? I might need to join you if so")), #18
            ("desire_m",   ["PBD"],        _("I want to feel your body up and down...your chest especially")), #19
        ]

        # Sexting quips for your most 'risque' options
        sext_quips_sexy = [
        #   |-------------|---------------|---------------------------------------------------------------------------|
        #   |    Type     |    Subtypes   |                                 Prompt                                    |
        #   |-------------|---------------|---------------------------------------------------------------------------|
            ("statement",  ["GEN"],        _("Who said that you could be this sexy?")), #0
            ("compliment", ["PPS", "CHE"], _("So, aside from being sexy, what do you do for a living?")), #1
            ("desire_m",   ["PBD"],        _("I can't wait to see your sexy body when we're together")), #2
            ("desire_m",   ["FKS"],        _("I can't wait to kiss you for real")), #3
            ("statement",  ["PVG"],        _("You're making me so wet")), #4
            ("statement",  ["ONM"],        _("I'm touching myself right now just to the thought of you")), #5
            ("desire_m",   ["PCL"],        _("When I get to your world, I'm ripping your clothes off the second I walk through the door. I hope you're prepared")), #6
            ("desire_m",   ["FSM", "SUB"], _("I'm tempted to leave a bite mark on your neck so everyone knows you're mine")), #7
            ("command",    ["FSM", "DOM"], _("I'm being so bad right now. I need you to punish me")), #8
            ("desire_m",   ["FSM", "FSP"], _("I want to feel your warmth pressing against me")), #9
            ("desire_p",   ["KIS", "FKS"], _("I want you to kiss me~ Right now~")), #10
            ("statement",  ["PPS"],        _("I love how you talk to me when you're turned on")), #11
            ("desire_p",   ["IVG"],        _("I want you to tell me how much you want to do it with me")), #12
            ("statement",  ["FSM", "FSP"], _("I want to look into your " + eye_desc + " eyes as we press our bodies together")), #13
            ("statement",  ["PPS"],        _("I love it when you're naughty")), #14
            ("compliment", ["MVG"],        _("You really know how to make a girl wet")), #17
            ("desire_p",   ["MVG", "FCM"], _("I want to feel your tongue down there")), #18
            ("statement",  ["GEN"],        _("Yes~ Just like that~")), #19
        ]

        sext_quips_sexy_p = [
            ("desire_p", ["GEN"], _("I want to feel you deep inside me")), #16
        ]
        if store.persistent._nsfw_genitalia == "P":
            sext_quips_sexy.extend(sext_quips_sexy_p)

        sext_quips_sexy_m = [
            ("statement", ["GEN"], _("You're such a bad boy")), #15
        ]
        if store.persistent.gender == "M":
            sext_quips_sexy.extend(sext_quips_sexy_m)

        sext_quips_sexy_4 = [
            ("statement", ["GEN"], _("You're such a bad girl")), #15
        ]
        if store.persistent.gender == "F":
            sext_quips_sexy.extend(sext_quips_sexy_f)

        if quip_category == 1:
            category_sel = sext_quips_hot
        elif quip_category == 2:
            category_sel = sext_quips_sexy
        elif quip_category == 3:
            category_sel = sext_quips_funny
        else:
            category_sel = sext_quips_cute

        new_category_sel = refine_category_sel_with_fetishes(category_sel)

        return new_category_sel

    def refine_dialogue_list_with_subtypes(dialogue_list, subtypes, category_type):
        """
        Returns a new dialogue list that contains only the dialogue that matches the subtypes provided, or are generic.
        Prompt -> Response -> Quip

        IN:
            dialogue_list - The list of dialogue to refine
            subtypes - The subtypes to match
            category_type - The loop component ("quip", "prompt", or "response") of dialogue we want to pull

        OUT:
            new_dialogue_list - The new dialogue list that contains only the dialogue that matches the subtypes provided, or are generic
        """
        new_dialogue_list = []

        if category_type == "quip":
            # We'll try to find at least 5 dialogue that matches the subtypes
            for dialogue in dialogue_list:
                for subtype in subtypes:
                    if subtype in dialogue[1]:
                        new_dialogue_list.append(dialogue)
                        break

            # If we didn't find enough dialogue that matches the subtypes, we'll just use generic dialogue
            if new_dialoguelist.length < 5:
                for dialogue in dialogue_list:
                    if "GEN" in dialogue[1]:
                        new_dialogue_list.append(dialogue)
                        break

        return new_dialogue_list

    def return_sexting_dialogue(category_type="response", horny_level=0, hot_req=10, sexy_req=30, horny_max=50, recent=[], prev_cat=None, prev_type=None, prev_stypes=None):
        """
        Returns a string from a dialogue list based on

        IN:
            category_type - The loop component ("quip", "prompt", or "response") of dialogue we want to pull
                (Default: "response")
            horny_level - The level of horny Monika is at
                (Default: 0)
            hot_req - The requirement for hot dialogue
                (Default: 10)
            sexy_req - The requirement for sexy dialogue
                (Default: 30)
            horny_max - The maximum possible horny level
                (Default: 50)
            recent - The recent_quips, recent_prompts, or recent_responses used - should match category_type.
                (Default: [])
            prev_cat - the "category" ("cute", "hot", "sexy") of the last prompt used
                (Optional, used only when category_type == "response")
            prev_type - The "type" of the last prompt used
                (Optional, used only when category_type == "response")
            prev_stype - The "subtype" of the last prompt used
                (Optional, used only when category_type == "response")

        OUT:
            Four outputs:
            [0] An individual string randomly picked from the list,
            [1] the category (sexy, hot, cute) the string is from,
            [2] the type (compliment, statement, command, desire_p, desire m) of the string.
            [3] the subtype (three-letter code) of the string.
            The last two only apply to third stage (sexy) prompts and responses; they are otherwise None.

        """
        # initialize this to None, it isn't used unless it's a prompt or quip at stage 3
        return_type = None
        return_subtype = None

        # Grab list we will be drawing dialogue from, based on category_type and horny_level
        if category_type == "quip":
            selected_recentlist = recent
            if horny_level >= sexy_req:
                dialogue_list = return_sext_quips(quip_category=2)
                return_cat = "sexy"
            elif horny_level >= hot_req:
                dialogue_list = return_sext_quips(quip_category=1)
                return_cat = "hot"
            else: # Default
                dialogue_list = return_sext_quips(quip_category=0)
                return_cat = "cute"

            new_dialogue_list = refine_dialogue_list_with_subtypes(dialogue_list, prev_stypes, "quip")

        elif category_type == "prompt":
            selected_recentlist = recent
            if horny_level >= sexy_req:
                # Don't need to check here, as sexy is the highest level we can go for dialogue
                dialogue_list = return_sext_prompts(prompt_category=2)
                return_cat = "sexy"

            elif horny_level >= hot_req:
                # Create random integer based on how close value is to sexy req vs max
                hot_to_current_rand = random.randint(hot_req, horny_level)
                current_to_sexy_rand = random.randint(horny_level, sexy_req)

                # Check how close value is to sexy req vs max
                hot_to_current = horny_level - hot_to_current_rand
                current_to_sexy = current_to_sexy_rand - horny_level
                if hot_to_current > current_to_sexy:
                    dialogue_list = return_sext_prompts(prompt_category=2)
                    return_cat = "sexy"
                else:
                    dialogue_list = return_sext_prompts(prompt_category=1)
                    return_cat = "hot"

            else: # Default
                # Create random integer based on how close value is to sexy req vs max
                min_to_current_rand = random.randint(0, horny_level)
                current_to_hot_rand = random.randint(horny_level, hot_req)

                # Check how close value is to sexy req vs max
                min_to_current = horny_level - min_to_current_rand
                current_to_hot = current_to_hot_rand - horny_level
                if min_to_current > current_to_hot:
                    dialogue_list = return_sext_prompts(prompt_category=1)
                    return_cat = "hot"
                else:
                    dialogue_list = return_sext_prompts(prompt_category=0)
                    return_cat = "cute"

        else: # We assume it's the response category here, but in case of incorrect input we set it as default
            # Responses should match the category / stage as the last prompt picked in order to make sense.
            selected_recentlist = recent

            if previous_cat == "cute":
                category_number = 0
            elif previous_cat == "hot":
                category_number = 1
            else: # if previous_cat == "sexy":
                category_number = 2

            dialogue_list = return_sext_responses(response_category=category_number, response_type=previous_type, response_subtype=previous_subtype)
            return_cat = previous_cat

        # Grab length of aquired list
        list_length = len(dialogue_list)

        # Grab random dialogue from list
        dialogue_no = random.randint(0, list_length - 1)

        # Break out of recentlist check after 100 failed attempts to find dialogue not in recent list.

        # Ideally this is never needed but it covers possible edge cases where the system may get
        # caught in a runaway while loop when searching through a dialogue list that is too short.
        recentlist_breakout = 0

        if category_type == "prompt": # if it's a prompt, dialogue_list is a list of tuples.
            while dialogue_list[dialogue_no][2] in selected_recentlist and recentlist_breakout < 100:
                dialogue_no = random.randint(0, list_length - 1)
                recentlist_breakout += 1

            return_type = dialogue_list[dialogue_no][0]
            return_subtype = dialogue_list[dialogue_no][1]
            return_dialogue = dialogue_list[dialogue_no][2]

        elif category_type == "quip": # if it's a quip, dialogue_list is a list of tuples. May as well keep these seperate despite no differences
            # Do loop to check if selected dialogue was used recently
            while dialogue_list[dialogue_no][2] in selected_recentlist and recentlist_breakout < 100:
                dialogue_no = random.randint(0, list_length - 1)
                recentlist_breakout += 1

            return_type = dialogue_list[dialogue_no][0]
            return_subtype = dialogue_list[dialogue_no][1]
            return_dialogue = dialogue_list[dialogue_no][2]

        else: # do not run any recentness checks for funny responses because only one option is possible
            return_type = dialogue_list[dialogue_no][0]
            return_subtype = dialogue_list[dialogue_no][1]
            return_dialogue = dialogue_list[dialogue_no][2]

        return return_dialogue, return_cat, return_type, return_subtype

    def return_dialogue_end(dialogue=""):
        """
        Returns an ending to a dialogue, such as the classic tilde. Won't return anything if an ending already exists.

        IN:
            dialogue - The dialogue we want to have an ending for
            (Default: "")

        OUT:
            dialogue_end - The ending randomly chosen for the dialogue, or an empty string
        """

        common_endings = (
            "~",
            ".",
        )

        rare_endings = (
            ", " + store.persistent.playername + ".",
            ", " + store.mas_get_player_nickname() + ".",
            ", " + store.persistent.playername + "~",
            ", " + store.mas_get_player_nickname() + "~",
        )

        existing_endings = (
            "~",
            ".",
            "?",
            "!",
        )

        # If the dialogue already has an ending, return an empty string
        for ending in existing_endings:
            if dialogue[-1] == ending:
                return ""

        # Otherwise, create a new ending
        if random.randint(1,3) >= 2: # 2/3 chance to end the sentence simply with "." or "~"
            dialogue_end = random.choice(common_endings)
        else: # otherwise, end the sentence with player name or nickname
            dialogue_end = random.choice(rare_endings)

        return dialogue_end

    def return_dialogue_start(horny_level=0, hot_req=4, sexy_req=8):
        """
        Returns a starting piece to dialogue, such as 'Hmm~' or 'Hah~'

        IN:
            horny_level - The current horny level of the player
                (Default: 0)
            hot_req - The horny level required to reach the 'hot' stage
                (Default: 4)
            sexy_req - The horny level required to reach the 'sexy' stage
                (Default: 8)

        OUT:
            The selected starting text for the dialogue
        """

        starts_cute = (
            "Hmm~ ",
            "Aww~ ",
            "Naww~ ",
            "",
        )

        starts_hot = (
            "Oh? ",
            "Hah~ ",
            "Mmm? ",
            "",
        )

        starts_sexy = (
            "Hah~ ",
            "Oh~ ",
            "Mmm~ ",
            "",
        )

        if horny_level >= sexy_req:
            return starts_sexy[random.randint(0, len(starts_sexy) - 1)]
        elif horny_level >= hot_req:
            return starts_hot[random.randint(0, len(starts_hot) - 1)]
        else: # Default
            return starts_cute[random.randint(0, len(starts_cute) - 1)]

    def can_monika_init_sext(nsfw_ev_label=""):
        """
        Checks if Monika can initiate sexting

        IN:
            nsfw_ev_label - The event label for the event we're checking
                (Default: "")

        OUT:
            boolean - True if Monika can initiate sexting, False otherwise
        """
        # If the event label is empty, assume False
        if nsfw_ev_label == "":
            return False

        # If the player can be shown risque content, have had a succesful sexting session with Monika, have not disabled sexting, and Monika has not permanently frozen the sexting system, return True
        if (store.mas_canShowRisque(aff_thresh=1000) and store.persistent._nsfw_sexting_success_last != None and store.persistent._nsfw_monika_sexting_frequency != 3 and store.persistent._nsfw_sexting_attempt_permfreeze == False):
            return True
        else:
            return False

    # def rerandom_sext_event(nsfw_ev_label="", nsfw_conditional=""):
    #     if nsfw_ev_label == "" or nsfw_conditional="":
    #         return

    #     with MAS_EVL(nsfw_ev_label) as random_ev:
    #         random_ev.random = False
    #         random_ev.conditional = (
    #             "mas_canShowRisque(aff_thresh=1000) "
    #             "and persistent._nsfw_sexting_success_last != None "
    #             "and persistent._nsfw_monika_sexting_frequency != 3 "
    #             "and mas_timePastSince(persistent._nsfw_sexting_last_sexted, datetime.timedelta(hours=12)) "
    #             "and mas_timePastSince(mas_getEVL_last_seen('nsfw_monika_sexting_horny'), datetime.timedelta(hours=12))"
    #         )
    #         random_ev.action = EV_ACT_RANDOM
    #     mas_rebuildEventLists()

    def return_random_number(min=0, max=10):
        """
        Returns a random number between the min and max values

        IN:
            min - The minimum value for the random number
                (Default: 0)
            max - The maximum value for the random number
                (Default: 10)

        OUT:
            A random number between the min and max values
        """
        return random.randint(min, max)