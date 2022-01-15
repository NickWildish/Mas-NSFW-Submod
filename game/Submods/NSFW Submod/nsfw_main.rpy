init -990 python in mas_submod_utils:
    Submod(
        author="NickWildish",
        name="NSFW Submod",
        description="A collection of NSFW topics and features for MAS.",
        version="0.1.0",
        dependencies={},
        settings_pane=None,
        version_updates={}
    )

screen nsfw_submod_screen():
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")

        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None
    
    vbox:
        box_wrap False
        xfill True
        xmaximum 1000
        
        hbox:
            style_prefix "check"
            box_wrap False

            if _tooltip:
                textbutton _("NSFW dud setting #1"):
                    action NullAction()
                    hovered SetField(_tooltip, "value", "This is an NSFW submod button which is inactive")
                    unhovered SetField(_tooltip, "value", _tooltip.default())

            else:
                textbutton _("NSFW dud setting #1"):
                    action NullAction()

init python in mas_nsfw:
    import store
    import datetime

    def hour_check(set_hours=6):
        """
        Checks if six hours has passed since the player has seen the getting nude topic and also been away from the pc for at least six hours.

        RETURNS: True if the player has been away for six hours AND the getting nude topic hasn't been used for six hours, False if otherwise
        """
        time_away_req = datetime.timedelta(hours=set_hours)
        time_since_last_seen = datetime.datetime.now() - store.mas_getEVL_last_seen("monika_gettingnude")

        if store.mas_getAbsenceLength() >= time_away_req and time_since_last_seen >= time_away_req:
            return True
        else:
            return False

    def canShow_underwear():
        """
        Checks if the player should be able to see Monika's underwear yet.

        RETURNS: True if the player has seen 'monika_gettingnude' topic AND risque is allowed AND the player hasn't seen the topic for at least 6 hours AND the player hasn't already unlocked her underwear, False if otherwise
        """
        if store.mas_getEV("monika_gettingnude").shown_count >= 1 and store.mas_canShowRisque() and hour_check(set_hours=6) and not store.mas_SELisUnlocked(store.mas_clothes_underwear_white):
            return True
        else:
            return False

    def canShow_birthdaySuit():
        """
        Checks to see if the player should be able to see Monika with no clothes yet.

        RETURNS: True if the player has seen 'monika_gettingnude' topic twice AND risque is allowed AND the player hasn't seen the topic for at least 6 hours AND the player hasn't already unlocked her naked, false if otherwise
        """
        if store.mas_SELisUnlocked(store.mas_clothes_underwear_white) and store.mas_canShowRisque() and hour_check(set_hours=6) and not store.mas_SELisUnlocked(store.mas_clothes_birthday_suit):
            return True
        else:
            return False
    
    # def has_sexted_today():
    #     """
    #     Checks if the sexting event has run today.

    #     RETURNS: True if the player has run the sexting event today, False if otherwise.
    #     """
    #     # NOTE: Code used from Multimokia's Auto Hair Change submod. Didn't want to create a dependency, but figured
    #     # it couldn't hurt to borrow this.
        
    #     #NOTE: This try/except is for use of this function in event conditionals
    #     #Since mas_getEV doesn't exist until init 6
    #     try:
    #         ev = store.mas_getEV("nsfw_sextingsession")
    #     except:
    #         ev = None

    #     #If the event doesn't exist, return None to note it
    #     if not ev:
    #         return None

    #     #No last seen means we know it wasn't seen on the date
    #     elif not ev.last_seen:
    #         return False

    #     #Otherwise let's check
    #     return ev.last_seen.date() == datetime.date.today()

    def return_sext_quip(category=0):
        # Sexting quips for your average compliment
        sext_quips_cute = (
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
            _("You're cute."),
        )

        # Sexting quips for the more 'risque' options
        sext_quips_hot = (
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
            _("You're hot."),
        )

        # Sexting quips for the most 'risque' options
        sext_quips_hot = (
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
            _("You're sexy."),
        )

        # Sexting quips for the haha funnies
        sext_quips_funny = (
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
            _("You're funny."),
        )
        return

    def return_sext_prompt(category=0):
        # Sexting prompts for your average compliment
        sext_prompts_cute = (
            _("I bring you in close and hold you in my arms."),
            _("I kiss your lips passionately."),
            _("I run my hands through your hair."),
            _("I hold your hands in mine."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
            _("I'm cute."),
        )
        
        # Sexting prompts for your more 'risque' options
        sext_prompts_hot = (
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
            _("I'm hot."),
        )

        # Sexting prompts for your most 'risque' options
        sext_prompts_sexy = (
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
            _("I'm sexy."),
        )

        # Sexting prompts for the haha funnies
        sext_prompts_funny = (
            _("I put on my robe and wizard hat."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
            _("I'm funny."),
        )
        return