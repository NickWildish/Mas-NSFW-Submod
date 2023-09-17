init -990 python in mas_submod_utils:
    Submod(
        author="NickWildish",
        name="NSFW Submod",
        version="1.3.0",
        description="A collection of NSFW topics and features for MAS.",
        settings_pane="nsfw_submod_screen",
        version_updates= {
            "nickwildish_nsfw_submod_v1_0_3": "nickwildish_nsfw_submod_v1_1_0",
            "nickwildish_nsfw_submod_v1_1_0": "nickwildish_nsfw_submod_v1_1_1",
            "nickwildish_nsfw_submod_v1_2_7": "nickwildish_nsfw_submod_v1_3_0"
        },
        coauthors=["mizuotana-nirera", "TreeWizard96"]
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

        time_since_last_seen = datetime.datetime.now() - store.mas_getEVL_last_seen(topic)

        if store.mas_getAbsenceLength() >= time_away_req and time_since_last_seen >= time_away_req:
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

    def calc_sexting_reqs(horny_min=0, hot_req=10, sexy_req=30, horny_max=50):
        """
        Calculates what the values of horny maximum, minimum, hot_req and sexy_req are, based on the player's endurance value

        IN:
            horny_min - The minimum horny value
                (Default: 0)
            hot_req - The horny_level requirement for hot dialogue
                (Default: 10)
            sexy_req - The horny_level requirement for sexy dialogue
                (Default: 30)
            horny_max - The maximum amount of horny Monika can withold before exploding in ecstasy
                (Default: 50)

        OUT:
            The maximum, minimum, hot_req and sexy_req values
        """
        player_endurance = store.persistent._nsfw_player_endurance

        new_horny_max = horny_max * player_endurance
        new_horny_min = horny_min * player_endurance # It's always gonna be zero babyyy
        new_hot_req = hot_req * player_endurance
        new_sexy_req = sexy_req * player_endurance

        return new_horny_min, new_hot_req, new_sexy_req, new_horny_max

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
            for i in range(2):
                # Check if any of the tags in the type or subtype of the prompt are blacklisted
                for tag in prompt[i]:
                    if tag in fetish_blacklist:
                        blacklisted = True
                        break
            if not blacklisted:
                new_category_sel.append(prompt)

        return new_category_sel

    def return_sext_responses(response_vars=[0, None, None], recent=[]):
        """
        Returns a Monika response from a selected category.

        IN:
            response_vars - A list of variables to be used in the response [category, type, subtype]
                (Default: [0, None, None])
            recent - A list of recent responses to prevent repeats
                (Default: [])

        OUT:
            A string containing a particular response from Monika.
        """
        player_name = store.persistent.playername
        player_nickname = store.mas_get_player_nickname()

        return_responses = [] # start building from this list

        if response_vars[1] == "funny": # if the player picks a "funny" prompt, skip automatically to appropriate response and return
            sext_responses_funny = store.mas_nsfw_sexting_dialogue.sext_responses_funny

            response_index = int(response_vars[2])

            # durability check, prevents crashing if someone adds a funny prompt but forgot to add a corresponding response
            if response_index >= len(sext_responses_funny):
                response_index = 0

            return_responses.append(sext_responses_funny[response_index][2])
            return return_responses

        if response_vars[0] == 0: # cute
            sext_responses_cute = store.mas_nsfw_sexting_dialogue.sext_responses_cute

            return_responses.extend(refine_category_sel_with_fetishes(sext_responses_cute))

        elif response_vars[0] == 1: # hot
            sext_responses_hot = store.mas_nsfw_sexting_dialogue.sext_responses_hot

            return_responses.extend(refine_category_sel_with_fetishes(sext_responses_hot))

        else: # elif response_category == 2: # sexy
            sext_responses_sexy = store.mas_nsfw_sexting_dialogue.sext_responses_sexy

            return_responses.extend(refine_category_sel_with_fetishes(sext_responses_sexy))

        new_return_responses = refine_dialogue_list_with_types(return_responses, response_vars[1], None, recent)

        return new_return_responses

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

        monika_nickname = store.persistent._mas_monika_nickname

        # Sexting prompts for your average compliment
        sext_prompts_cute = store.mas_nsfw_sexting_dialogue.sext_prompts_cute

        # Sexting prompts for your more 'risque' options
        sext_prompts_hot = store.mas_nsfw_sexting_dialogue.sext_prompts_hot

        # Sexting prompts for your most 'risque' options
        sext_prompts_sexy = store.mas_nsfw_sexting_dialogue.sext_prompts_sexy

        # Prompt choices specific to players with penises.
        sext_prompts_sexy_p = store.mas_nsfw_sexting_dialogue.sext_prompts_sexy_p
        if store.persistent._nsfw_genitalia == "P":
            sext_prompts_sexy.extend(sext_prompts_sexy_p)

        # Prompt choices specific to players with vaginas.
        sext_prompts_sexy_v = store.mas_nsfw_sexting_dialogue.sext_prompts_sexy_v
        if store.persistent._nsfw_genitalia == "V":
            sext_prompts_sexy.extend(sext_prompts_sexy_v)

        # Prompt choices specific to male players.
        sext_prompts_sexy_m = store.mas_nsfw_sexting_dialogue.sext_prompts_sexy_m
        if store.persistent.gender == "M":
            sext_prompts_sexy.extend(sext_prompts_sexy_m)

        # Prompt choices specific to female players.
        sext_prompts_sexy_f = store.mas_nsfw_sexting_dialogue.sext_prompts_sexy_f
        if store.persistent.gender == "F":
            sext_prompts_sexy.extend(sext_prompts_sexy_f)

        # Sexting prompts for the haha funnies
        # sext_prompts_funny = store.mas_nsfw_sexting_dialogue.sext_prompts_funny

        # Sexting prompts for the haha funnies specific to players with penises
        #sext_prompts_funny_p = store.mas_nsfw_sexting_dialogue.sext_prompts_funny_p
        #if store.persistent._nsfw_genitalia == "P":
        #    sext_prompts_funny.extend(sext_prompts_funny_p)

        # Sexting prompts for the haha funnies specific to male players
        #sext_prompts_funny_m = store.mas_nsfw_sexting_dialogue.sext_prompts_funny_m
        #if store.persistent.gender == "M":
        #    sext_prompts_funny.extend(sext_prompts_funny_m)

        # needs matching response

        # if store.mas_submod_utils.isSubmodInstalled("Custom Room Furnished Spaceroom V3"):
        #    sext_prompts_funny.extend([
        #        ("funny", "20", _("I want to fuck you on top of the piano.")),
        #    ])

        if prompt_category == 0:
            category_sel = sext_prompts_cute
        elif prompt_category == 1:
            category_sel = sext_prompts_hot
        else: # if prompt_category == 2: TODO: Add funny prompts back
            # if random.randint(1,200) == 1: # 1/200 chance of funny quip.
            #     # It's set for third stage only but it can be changed to work with all stages if you move this if check a little higher.
            #     category_sel = sext_prompts_funny
            # else:
            #     category_sel = sext_prompts_sexy
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

        # Sexting quips for the haha funnies TODO: Get funny quips working
        # sext_quips_funny = store.mas_nsfw_sexting_dialogue.sext_quips_funny

        # Sexting quips for your average compliment
        sext_quips_cute = store.mas_nsfw_sexting_dialogue.sext_quips_cute

        # Sexting quips for your more 'risque' options
        sext_quips_hot = store.mas_nsfw_sexting_dialogue.sext_quips_hot

        # Sexting quips for your most 'risque' options
        sext_quips_sexy = store.mas_nsfw_sexting_dialogue.sext_quips_sexy

        sext_quips_sexy_p = store.mas_nsfw_sexting_dialogue.sext_quips_sexy_p
        if store.persistent._nsfw_genitalia == "P":
            sext_quips_sexy.extend(sext_quips_sexy_p)

        sext_quips_sexy_m = store.mas_nsfw_sexting_dialogue.sext_quips_sexy_m
        if store.persistent.gender == "M":
            sext_quips_sexy.extend(sext_quips_sexy_m)

        sext_quips_sexy_f = store.mas_nsfw_sexting_dialogue.sext_quips_sexy_f
        if store.persistent.gender == "F":
            sext_quips_sexy.extend(sext_quips_sexy_f)

        if quip_category == 1:
            category_sel = sext_quips_hot
        elif quip_category == 2:
            category_sel = sext_quips_sexy
        # elif quip_category == 3:
        #     category_sel = sext_quips_funny
        else:
            category_sel = sext_quips_cute

        new_category_sel = refine_category_sel_with_fetishes(category_sel)

        return new_category_sel

    def dialogue_already_in_pool(dialogue, *pools):
        """
        Checks if the dialogue is already in the pool

        IN:
            dialogue - The dialogue to check
            pools - The pools to check

        OUT:
            True if the dialogue is already in the pool, False otherwise
        """
        return any(dialogue in pool for pool in pools)

    def refine_dialogue_list_with_types(dialogue_list, types=None, dialogue_pool=None, recent=[]):
        """
        Refines a dialogue list with a list of types. This is only to be used for responses.

        IN:
            dialogue_list - The dialogue list to be refined
            types - A list of types to be used in the refinement
                (Default: None)
            dialogue_pool - A list of dialogue to be used in the refinement
                (Default: None)
            recent - A list of dialogue that has been recently used
                (Default: [])

        OUT:
            A refined dialogue list
        """
        # Rare use cases
        if types == None:
            types = ["STM"]

        dp1, dp2, dp3 = [], [], [] # may use other 2 dialogue pools at a later date

        unique_tags = ["CMP", "CMD", "DES", "QUE", "ANS"] # Theses are the non-generic tags

        response_pairings = [
        #   |--------------|---------------------|
        #   |    Prompt    |      Response       |
        #   |--------------|---------------------|
            (["CMP"],       ["CMP", "THK"]),
            (["CMP"],       ["CMP", "CMP"]),
            (["CMP"],       ["CMP", "CRM"]),
            (["CMD"],       ["CMD", "CPL"]),
            (["DES", "PLY"],["DES", "LED"]),
            (["DES", "MON"],["DES", "LED"]),
            (["DES", "PLY"],["DES", "DRM"]),
            (["DES", "MON"],["DES", "DRM"]),
            (["DES", "PLY"],["DES", "DRM", "PLY"]),
            (["DES", "MON"],["DES", "DRM", "MON"]),
            (["QUE", "QSP"],["ANS", "ASP"]), # We search for integer in third column
            (["QUE", "QYS"],["ANS", "AYS"]),
            (["QUE", "QNO"],["ANS", "ANO"]),
            (["QUE", "QAG"],["ANS", "AAG"]),
            (["QUE", "QDG"],["ANS", "ADG"]),
            (["QUE", "QAT"],["ANS", "AAT"]),
            (["QUE", "QDT"],["ANS", "ADT"]),
            (["STM"],       ["DES", "LED"]),
        ]

        for dialogue in dialogue_list:
            if dialogue[2] in recent:
                continue

            dp_to_append = 3 # Default to 3, which means "no match" or "generic"
            for pair in response_pairings:
                if types == pair[0] and dialogue[0] == pair[1]:
                    dp_to_append = 1
                    break
                elif len(types) == 3 and types[:2] == pair[0] and dialogue[0][:2] == pair[1]:
                    if types[2] == dialogue[0][2]:
                        dp_to_append = 1
                    else:
                        dp_to_append = 3 if dp_to_append > 3 else None
                    break
                elif types[0] not in unique_tags:
                    dp_to_append = 2 if dp_to_append > 2 else None
                    break

            if not dialogue_already_in_pool(dialogue, dp1, dp2, dp3):
                if dp_to_append == 3:
                    renpy.say("System", "Type match not found: " + ", ".join(str(x) for x in types) + " does not work with " + ", ".join(str(x) for x in dialogue[0]) + ".") # DEBUG
                    dp3.append(dialogue)
                elif dp_to_append == 2:
                    renpy.say("System", "Type match semi-found: " + ", ".join(str(x) for x in types) + " somewhat works with " + ", ".join(str(x) for x in dialogue[0]) + ".") # DEBUG
                    dp2.append(dialogue)
                elif dp_to_append == 1:
                    renpy.say("System", "Type match found: " + ", ".join(str(x) for x in types) + " works with " + ", ".join(str(x) for x in dialogue[0]) + ".") # DEBUG
                    dp1.append(dialogue)

        if len(dp1) == 0: # DEBUG
            renpy.say("System", "No dialogue found for the given types. Using a less specific dialogue pool.")
            dp1 = dp2 if len(dp2) > 0 else dp3
            if len(dp2) > 0:
                renpy.say("System", "Dialogue pool 2 used.")
            else:
                renpy.say("System", "Dialogue pool 3 used.")

        return dp1

    def refine_dialogue_list_with_subtypes(dialogue_list, subtypes=None, dialogue_pool=None, recent=[]):
        """
        Returns a new dialogue list that contains only the dialogue that matches the subtypes provided, or are generic.

        IN:
            dialogue_list - The list of dialogue to refine
            subtypes - The subtypes to match
            dialogue_pool - The pool of dialogue to use. If none, return them all.
            recent - The list of recent dialogue

        OUT:
            new_dialogue_list - The new dialogue list that contains only the dialogue that matches the subtypes provided, or are generic
        """
        # Rare use cases
        if subtypes == None:
            subtypes = ["GEN"]

        # The dialogue list should have a variety, but we want it to apply to the correct subject.
        # Tags that start with P or M get prompts with both P-- or M-- tags, with -- representing other tags in their category
        # Any other tags get prompts with their first two characters, then their first character.
        # The rest are random.
        # Example: We receive a subtype of "PPS", so we find subtypes that have "PP-" and "MP-"
        # Example 2: We receive a subtype of "IAM", so we find subtypes that have "IA-" and "I--"

        special_tags = ["GEN", "KIS", "UND", "CHE"]

        # These are the pools we'll use to collect the dialogue types
        dp1, dp2, dp3 = [], [], []

        for i, subtype in enumerate(subtypes):
            for j, dialogue in enumerate(dialogue_list):
                pool_no = 4

                # If the dialogue has already been used recently, skip it
                if dialogue[2] in recent:
                    continue

                # If the subtype is in the special tags
                elif subtype in special_tags:
                    if subtype == "GEN":
                        target_pools = [2, 3]
                        pool_no = 1 if subtype in dialogue[1] else target_pools[(j - len(dp1)) % 2]
                    elif subtype == "KIS":
                        target_pools = [2, 3]
                        pool_no = 1 if "FKS" in dialogue[1] else target_pools[(j - len(dp1)) % 2]
                    elif subtype == "UND":
                        target_pools = [2, 3]
                        pool_no = 1 if "MCL" in dialogue[1] or "PCL" in dialogue[1] else target_pools[(j - len(dp1)) % 2]
                    elif subtype == "CHE":
                        target_pools = [2, 3]
                        pool_no = 1 if subtype in dialogue[1] else target_pools[(j - len(dp1)) % 2]
                    else: # Shouldn't activate, but here in case any get added
                        target_pools = [1, 2, 3]
                        pool_no = target_pools[(j - len(dp1)) % 3]

                # If there are multiple subtypes
                elif len(subtypes) > 1:
                    if subtype in dialogue[1]:
                        # we match subtype index to the pool index
                        pool_no = i + 1
                    else:
                        pool_no = 3 if len(subtypes) != 3 else 4

                # If the subtype has the letter "M" or "P" to start
                elif subtype[0] in "MP":
                    if subtype in dialogue[1]:
                        pool_no = 1
                    else:
                        for subs in dialogue[1]:
                            if subtype[0] != subs[0] and subtype[1:] == subs[1:]:
                                pool_no = 2
                                break
                            else:
                                pool_no = 3

                # If there is one subtype and no special tags
                else:
                    if subtype in dialogue[1]:
                        pool_no = 1
                    elif subtype[0] == dialogue[1][0]:
                        pool_no = 2
                    else:
                        pool_no = 3

                if pool_no == 1 and not dialogue_already_in_pool(dialogue, dp1, dp2, dp3):
                    dp1.append(dialogue)
                elif pool_no == 2 and not dialogue_already_in_pool(dialogue, dp1, dp2, dp3):
                    dp2.append(dialogue)
                elif pool_no == 3 and not dialogue_already_in_pool(dialogue, dp1, dp2, dp3):
                    dp3.append(dialogue)

        for i, pool in enumerate([dp1, dp2, dp3]):
            if len(pool) == 0:
                if i == 0: # Ensures if we only have 1 dialogue, it goes to the first pool (In the cases of specific types, like "QSP")
                    non_empty_pools = [p for p in [dp1, dp2, dp3] if len(p) >= 1 and p != pool]
                else: # Otherwise, we can choose any pool that isn't empty
                    non_empty_pools = [p for p in [dp1, dp2, dp3] if len(p) > 1 and p != pool]

                if non_empty_pools == [dp3]:
                    index = random.randint(0, len(dp3) - 1)
                    for j, dialogue in enumerate(dp3):
                        if "GEN" in dialogue[1]:
                            index = j
                    pool.append(dp3.pop(index))
                elif non_empty_pools:
                    if i == 2: # If we're on the last pool, choose the last non-empty pool
                        chosen_pool = non_empty_pools[len(non_empty_pools) - 1]
                    else: # Otherwise, choose the first non-empty pool
                        chosen_pool = non_empty_pools[0]
                    index = random.randint(0, len(chosen_pool) - 1)
                    pool.append(chosen_pool.pop(index))

        new_dialogue_list = [dp1, dp2, dp3] if dialogue_pool is None else [dp1, dp2, dp3][dialogue_pool]

        return new_dialogue_list

    def return_sexting_dialogue(category_type="response", horny_lvl=0, horny_reqs=[0, 10, 30, 50], recent=[], previous_vars=[], past_prompts=[None, None]):
        """
        Returns a string from a dialogue list based on

        IN:
            category_type - The loop component ("quip", "prompt", or "response") of dialogue we want to pull
                (Default: "response")
            horny_lvl - The level of horny Monika is at
                (Default: 0)
            horny_reqs - The horny requirements for each category [min, hot, sexy, max].
                (Default: [0, 10, 30, 50])
            recent - The recent_quips, recent_prompts, or recent_responses used - should match category_type.
                (Default: [])
            previous_vars - The previous dialogue's category, type and subtype [category, type, subtype].
                (Default: [])
            past_prompts - The past prompts used (only used when getting prompt).
                (Default: None)
        OUT:
            Four outputs:
            [0] An individual string randomly picked from the list,
            [1] the category (sexy, hot, cute) the string is from,
            [2] the type (CMP, STM, etc.) of the string.
            [3] the subtype (MBD, PCL, etc.) of the string.

        """
        # initialize this to None, it isn't used unless it's a prompt or quip at stage 3
        return_type = None
        return_subtype = None

        # Grab list we will be drawing dialogue from, based on category_type and horny level
        if category_type == "quip":
            selected_recentlist = recent
            if horny_lvl >= horny_reqs[2]:
                dialogue_list = return_sext_quips(quip_category=2)
                return_cat = "sexy"
            elif horny_lvl >= horny_reqs[1]:
                dialogue_list = return_sext_quips(quip_category=1)
                return_cat = "hot"
            else: # Default
                dialogue_list = return_sext_quips(quip_category=0)
                return_cat = "cute"

        elif category_type == "prompt":
            selected_recentlist = recent
            if horny_lvl >= horny_reqs[2]:
                # Don't need to check here, as sexy is the highest level we can go for dialogue
                dialogue_list = return_sext_prompts(prompt_category=2)
                if dialogue_list[0][0] == "funny":
                    return_cat = "funny"
                else:
                    return_cat = "sexy"

            elif horny_lvl >= horny_reqs[1]:
                # Create random integer based on how close value is to sexy req vs max
                hot_to_current_rand = random.randint(horny_reqs[1], horny_lvl)
                current_to_sexy_rand = random.randint(horny_lvl, horny_reqs[2])

                # Check how close value is to sexy req vs max
                hot_to_current = horny_lvl - hot_to_current_rand
                current_to_sexy = current_to_sexy_rand - horny_lvl
                if hot_to_current > current_to_sexy:
                    dialogue_list = return_sext_prompts(prompt_category=2)
                    return_cat = "sexy"
                else:
                    dialogue_list = return_sext_prompts(prompt_category=1)
                    return_cat = "hot"

            else: # Default
                # Create random integer based on how close value is to sexy req vs max
                min_to_current_rand = random.randint(0, horny_lvl)
                current_to_hot_rand = random.randint(horny_lvl, horny_reqs[1])

                # Check how close value is to sexy req vs max
                min_to_current = horny_lvl - min_to_current_rand
                current_to_hot = current_to_hot_rand - horny_lvl
                if min_to_current > current_to_hot:
                    dialogue_list = return_sext_prompts(prompt_category=1)
                    return_cat = "hot"
                else:
                    dialogue_list = return_sext_prompts(prompt_category=0)
                    return_cat = "cute"

        else: # We assume it's the response category here, but in case of incorrect input we set it as default
            # Responses should match the category / stage as the last prompt picked in order to make sense.
            selected_recentlist = recent

            if previous_vars[0] == "cute":
                category_number = 0
            elif previous_vars[0] == "hot":
                category_number = 1
            else: # if previous_vars[0] == "sexy":
                category_number = 2

            dialogue_list = return_sext_responses(response_vars=[category_number, previous_vars[1], previous_vars[2]], recent=selected_recentlist)
            return_cat = previous_vars[0]

        new_dialogue_list = refine_dialogue_list_with_subtypes(dialogue_list, previous_vars[2], None, selected_recentlist)

        # Grab length of acquired list
        list_length = len(new_dialogue_list)
        list_length_first = len(new_dialogue_list[0])
        list_length_second = len(new_dialogue_list[1])
        list_length_third = len(new_dialogue_list[2])

        # Grab random dialogue from list
        dialogue_no = random.randint(0, list_length - 1)

        if list_length_first is not 0:
            dialogue_no_first = random.randint(0, list_length_first - 1)
        else:
            dialogue_no_first = -1

        if list_length_second is not 0:
            dialogue_no_second = random.randint(0, list_length_second - 1)
        else:
            dialogue_no_second = -1

        # Should never happen, but just in case so we know where the issue is
        if list_length_third is not 0:
            dialogue_no_third = random.randint(0, list_length_third - 1)
        else:
            dialogue_no_third = -1

        # Ideally this is never needed but it covers possible edge cases where the system may get
        # caught in a runaway while loop when searching through a dialogue list that is too short.
        recentlist_breakout = 0

        if category_type == "prompt": # if it's a prompt, new_dialogue_list is a list of tuples.
            final_prompt_refinement = []

            # Create a prompt using the three pools
            # Use past prompts to verify which pool to use
            if past_prompts[0] is None and dialogue_no_first is not -1:
                # If there are no past prompts, this is using the first pool
                final_prompt_refinement = new_dialogue_list[0][dialogue_no_first]

                # Check if the dialogue is in the recent list, if so, grab a new one
                while final_prompt_refinement[2] in selected_recentlist and recentlist_breakout < 100:
                    dialogue_no_first = random.randint(0, list_length_first - 1)
                    final_prompt_refinement = new_dialogue_list[0][dialogue_no_first]
                    recentlist_breakout += 1

            elif past_prompts [1] is None and dialogue_no_second is not -1:
                # If there is only one past prompt, this is using the second pool
                final_prompt_refinement = new_dialogue_list[1][dialogue_no_second]

                # Check if the dialogue is in the recent list, if so, grab a new one
                while final_prompt_refinement[2] in selected_recentlist and recentlist_breakout < 100:
                    dialogue_no_first = random.randint(0, list_length_first - 1)
                    final_prompt_refinement = new_dialogue_list[1][dialogue_no_second]
                    recentlist_breakout += 1

            else:
                # If there are two past prompts, this is using the third pool
                final_prompt_refinement = new_dialogue_list[2][dialogue_no_third]

                # Check if the dialogue is in the recent list, if so, grab a new one
                while final_prompt_refinement[2] in selected_recentlist and recentlist_breakout < 100:
                    dialogue_no_first = random.randint(0, list_length_first - 1)
                    final_prompt_refinement = new_dialogue_list[2][dialogue_no_third]
                    recentlist_breakout += 1

            return_dialogue = final_prompt_refinement[2]
            return_type = final_prompt_refinement[0]
            return_subtype = final_prompt_refinement[1]

        elif category_type == "quip": # if it's a quip, dialogue_list is a list of tuples. May as well keep these seperate despite no differences
            final_prompt_refinement = new_dialogue_list[0][dialogue_no_first]

            # Do loop to check if selected dialogue was used recently
            while final_prompt_refinement[2] in selected_recentlist and recentlist_breakout < 100:
                dialogue_no_first = random.randint(0, list_length_first - 1)
                final_prompt_refinement = new_dialogue_list[0][dialogue_no_first]
                recentlist_breakout += 1

            return_dialogue = final_prompt_refinement[2]
            return_type = final_prompt_refinement[0]
            return_subtype = final_prompt_refinement[1]

        else: # do not run any recentness checks for funny responses because only one option is possible
            # renpy.say("DEV", "Here are my responses:")

            # if len(new_dialogue_list[0]) is not 0:
            #     for dialogue in new_dialogue_list[0]:
            #         renpy.say("DEV", "pool 1: " + dialogue[2])
            # else:
            #     renpy.say("DEV", "pool1: No responses found.")
            # if len(new_dialogue_list[1]) is not 0:
            #     for dialogue in new_dialogue_list[1]:
            #         renpy.say("DEV", "pool 2: " + dialogue[2])
            # else:
            #     renpy.say("DEV", "pool2: No responses found.")
            # if len(new_dialogue_list[2]) is not 0:
            #     for dialogue in new_dialogue_list[2]:
            #         renpy.say("DEV", "pool 3: " + dialogue[2])
            # else:
            #     renpy.say("DEV", "pool3: No responses found.")

            # renpy.say("DEV", "Here is my chosen response:")
            final_prompt_refinement = new_dialogue_list[0][dialogue_no_first]

            return_dialogue = final_prompt_refinement[2]
            return_type = final_prompt_refinement[0]
            return_subtype = final_prompt_refinement[1]

        sexting_dialogue = [return_dialogue, return_cat, return_type, return_subtype]

        return sexting_dialogue

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
        if random.randint(1,5) == 1: # 1/5 chance to end the sentence with player name or nickname
            dialogue_end = random.choice(rare_endings)
        else: # otherwise, end the sentence simply with "." or "~"
            dialogue_end = random.choice(common_endings)

        return dialogue_end

    def return_dialogue_start(horny_level=0, horny_reqs=[10, 30]):
        """
        Returns a starting piece to dialogue, such as 'Hmm~' or 'Hah~'

        IN:
            horny_level - The current horny level of the player
                (Default: 0)
            hot_req - The horny level required to reach the 'hot' stage
                (Default: 10)
            sexy_req - The horny level required to reach the 'sexy' stage
                (Default: 30)

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

        if horny_level >= horny_reqs[1]:
            return starts_sexy[random.randint(0, len(starts_sexy) - 1)]
        elif horny_level >= horny_reqs[0]:
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

    def create_sexting_prompts(horny_lvl=0, horny_reqs=[0, 10, 30, 50], previous_vars=[], recent_prompts=[]):
        """
        Creates sexting prompts for Monika to send to the player

        IN:
            horny_lvl - The current horny level of the player
                (Default: 0)
            horny_reqs - The horny level requirements for each stage of sexting
                (Default: [0, 10, 30, 50])
            previous_vars - The previous variables used in the sexting session
                (Default: [])
            recent_prompts - The recent prompts used in the sexting session
                (Default: [])

        OUT:
            new_player_prompts - The new prompts for the player to choose from
        """
        new_player_prompts = [["", "", "", ""], ["", "", "", ""], ["", "", "", ""]] # The prompts from which the player will choose from, and their respective category/type/subtype.

        if horny_lvl > horny_reqs[2]:
            sext_category = 2
            category_type = "sexy"
        elif horny_lvl > horny_reqs[1]:
            sext_category = 1
            category_type = "hot"
        else:
            sext_category = 0
            category_type = "cute"

        # # Check how many unique prompts we can create
        # # Only if greater than 10 do we enforce the while loop below
        # unique_prompts_1 = len(refine_dialogue_list_with_subtypes(return_sext_prompts(sext_category), previous_vars[2], dialogue_pool=0))
        # unique_prompts_2 = len(refine_dialogue_list_with_subtypes(return_sext_prompts(sext_category), previous_vars[2], dialogue_pool=1))
        # unique_prompts_3 = len(refine_dialogue_list_with_subtypes(return_sext_prompts(sext_category), previous_vars[2], dialogue_pool=2))

        # while len(recent_prompts) >= unique_prompts_1:
        #     recent_prompts.pop(0)

        # while len(recent_prompts) >= unique_prompts_2:
        #     recent_prompts.pop(0)

        # while len(recent_prompts) >= unique_prompts_3:
        #     recent_prompts.pop(0)

        past_prompts = [None, None]
        # Make 3 player prompts
        for x in range(3):
            new_player_prompts[x] = return_sexting_dialogue(
                category_type="prompt",
                horny_lvl=horny_lvl,
                horny_reqs=horny_reqs,
                recent=recent_prompts,
                previous_vars=previous_vars,
                past_prompts=past_prompts
            )

            if x < 2:
                past_prompts[x]=new_player_prompts[x]

        while new_player_prompts[1][0] == new_player_prompts[0][0]:
            past_prompts[1]=None

            # Check for duplicates with second prompt
            new_player_prompts[1] = return_sexting_dialogue(
                category_type="prompt",
                horny_lvl=horny_lvl,
                horny_reqs=horny_reqs,
                recent=recent_prompts,
                previous_vars=previous_vars,
                past_prompts=past_prompts
            )

            past_prompts[1]=new_player_prompts[1]

        while new_player_prompts[2][0] == new_player_prompts[0][0] or new_player_prompts[2][0] == new_player_prompts[1][0]:
            # Check for duplicates with third prompt
            new_player_prompts[2] = return_sexting_dialogue(
                category_type="prompt",
                horny_lvl=horny_lvl,
                horny_reqs=horny_reqs,
                recent=recent_prompts,
                previous_vars=previous_vars,
                past_prompts=past_prompts
            )

        return new_player_prompts

    def create_sexting_quips(horny_lvl=0, horny_reqs=[0, 10, 30, 50], previous_vars=[], recent_quips=[]):
        """
        Creates sexting quips for Monika to send to the player

        IN:
            horny_lvl - The current horny level of the player
                (Default: 0)
            horny_reqs - The horny level requirements for each stage of sexting
                (Default: [0, 10, 30, 50])
            previous_vars - The previous variables used in the sexting session
                (Default: [])
            recent_quips - The recent quips used in the sexting session
                (Default: [])

        OUT:
            new_monika_quip - The new quip for Monika to send to the player
        """
        # Set up variables
        new_monika_quip = [] # The quip Monika will say, the category/type/subtype of the quip, and the ending of the quip.

        if horny_lvl > horny_reqs[2]:
            sext_category = 2
            category_type = "sexy"
        elif horny_lvl > horny_reqs[1]:
            sext_category = 1
            category_type = "hot"
        else:
            sext_category = 0
            category_type = "cute"

        unique_quips = len(refine_dialogue_list_with_subtypes(return_sext_prompts(sext_category), previous_vars[2], dialogue_pool=0))

        while len(recent_quips) >= unique_quips:
            recent_quips.pop(0)

        # Set quip, noting the category/type/subtype
        new_monika_quip = return_sexting_dialogue(
            category_type="quip",
            horny_lvl=horny_lvl,
            horny_reqs=horny_reqs,
            recent=recent_quips,
            previous_vars=previous_vars
        )

        new_monika_quip.append("")

        # Set quip ending
        new_monika_quip[4] = return_dialogue_end(new_monika_quip[0])

        return new_monika_quip

    def create_sexting_response(horny_lvl=0, horny_reqs=[0, 10, 30, 50], previous_vars=[], recent_responses=[]):
        """
        Creates sexting responses for Monika to send to the player

        IN:
            horny_lvl - The current horny level of the player
                (Default: 0)
            horny_reqs - The horny level requirements for each stage of sexting
                (Default: [0, 10, 30, 50])
            previous_vars - The previous variables used in the sexting session
                (Default: [])
            recent_responses - The recent responses used in the sexting session
                (Default: [])

        OUT:
            new_monika_response - The new response for Monika to send to the player
        """
        # Set up variables
        new_monika_response = [] # The response Monika will say, the category/type/subtype of the quip, the beginning and the ending of the quip.

        # Set response, noting the category/type/subtype
        new_monika_response = return_sexting_dialogue(
            category_type="response",
            horny_lvl=horny_lvl,
            horny_reqs=horny_reqs,
            recent=recent_responses,
            previous_vars=previous_vars
        )

        new_monika_response.append("")
        new_monika_response.append("")

        # Set response ending
        new_monika_response[4] = return_dialogue_start(horny_level=horny_lvl, horny_reqs=[horny_reqs[1], horny_reqs[2]])
        new_monika_response[5] = return_dialogue_end(new_monika_response[0])

        return new_monika_response

    def save_fetish_to_persistent(fetish_name, fetish_whitelist, fetish_blacklist):
        # Force-update the fetish
        found_fetish = False
        for fetish in persistent._nsfw_player_fetishes:
            if fetish[0] == fetish_to_save:
                found_fetish = True
                fetish[1] = fetish_whitelist
                fetish[2] = fetish_blacklist
                break

        if not found_fetish:
            # If we get here, we didn't find the fetish
            persistent._nsfw_player_fetishes.append([fetish_to_save, fetish_whitelist, fetish_blacklist])