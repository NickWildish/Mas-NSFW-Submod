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
            for tag in prompt[1]:
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

        # I did not write any V / M / F prompts yet but these are here so they can be enabled later

        # Prompt choices specific to players with vaginas.
        # sext_prompts_sexy_v = store.mas_nsfw_sexting_dialogue.sext_prompts_sexy_v
        # if store.persistent._nsfw_genitalia == "V":
        #     sext_prompts_sexy.extend(sext_prompts_sexy_v)

        # Prompt choices specific to male players.
        # sext_prompts_sexy_m = store.mas_nsfw_sexting_dialogue.sext_prompts_sexy_m
        # if store.persistent.gender == "M":
        #     sext_prompts_sexy.extend(sext_prompts_sexy_m)

        # Prompt choices specific to female players.
        # sext_prompts_sexy_f = store.mas_nsfw_sexting_dialogue.sext_prompts_sexy_f

        # Sexting prompts for the haha funnies
        sext_prompts_funny = store.mas_nsfw_sexting_dialogue.sext_prompts_funny

        # Sexting prompts for the haha funnies specific to players with penises
        sext_prompts_funny_p = store.mas_nsfw_sexting_dialogue.sext_prompts_funny_p
        if store.persistent._nsfw_genitalia == "P":
            sext_prompts_funny.extend(sext_prompts_funny_p)

        # Sexting prompts for the haha funnies specific to male players
        sext_prompts_funny_m = store.mas_nsfw_sexting_dialogue.sext_prompts_funny_m
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

        # sext_quips_sexy_f = store.mas_nsfw_sexting_dialogue.sext_quips_sexy_f
        # if store.persistent.gender == "F":
        #     sext_quips_sexy.extend(sext_quips_sexy_f)

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