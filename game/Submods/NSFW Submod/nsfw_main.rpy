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
            _("You're cute."), #0
            _("You're cute."), #1
            _("You're cute."), #2
            _("You're cute."), #3
            _("You're cute."), #4
            _("You're cute."), #5
            _("You're cute."), #6
            _("You're cute."), #7
            _("You're cute."), #8
            _("You're cute."), #9
            _("You're cute."), #10
            _("You're cute."), #11
            _("You're cute."), #12
            _("You're cute."), #13
            _("You're cute."), #14
            _("You're cute."), #15
            _("You're cute."), #16
            _("You're cute."), #17
            _("You're cute."), #18
            _("You're cute."), #19
        )

        # Sexting quips for the more 'risque' options
        sext_quips_hot = (
            _("You're hot."), #0
            _("You're hot."), #1
            _("You're hot."), #2
            _("You're hot."), #3
            _("You're hot."), #4
            _("You're hot."), #5
            _("You're hot."), #6
            _("You're hot."), #7
            _("You're hot."), #8
            _("You're hot."), #9
            _("You're hot."), #10
            _("You're hot."), #11
            _("You're hot."), #12
            _("You're hot."), #13
            _("You're hot."), #14
            _("You're hot."), #15
            _("You're hot."), #16
            _("You're hot."), #17
            _("You're hot."), #18
            _("You're hot."), #19
        )

        # Sexting quips for the most 'risque' options
        sext_quips_hot = (
            _("You're sexy."), #0
            _("You're sexy."), #1
            _("You're sexy."), #2
            _("You're sexy."), #3
            _("You're sexy."), #4
            _("You're sexy."), #5
            _("You're sexy."), #6
            _("You're sexy."), #7
            _("You're sexy."), #8
            _("You're sexy."), #9
            _("You're sexy."), #10
            _("You're sexy."), #11
            _("You're sexy."), #12
            _("You're sexy."), #13
            _("You're sexy."), #14
            _("You're sexy."), #15
            _("You're sexy."), #16
            _("You're sexy."), #17
            _("You're sexy."), #18
            _("You're sexy."), #19
        )

        # Sexting quips for the haha funnies
        sext_quips_funny = (
            _("Haha! What are you talking about, [player]?"), #0
            _("You're funny."), #1
            _("You're funny."), #2
            _("You're funny."), #3
            _("You're funny."), #4
            _("You're funny."), #5
            _("You're funny."), #6
            _("You're funny."), #7
            _("You're funny."), #8
            _("You're funny."), #9
            _("You're funny."), #10
            _("You're funny."), #11
            _("You're funny."), #12
            _("You're funny."), #13
            _("You're funny."), #14
            _("You're funny."), #15
            _("You're funny."), #16
            _("You're funny."), #17
            _("You're funny."), #18
            _("You're funny."), #19
        )
        return

    def return_sext_prompt(category=0):
        # Sexting prompts for your average compliment
        sext_prompts_cute = (
            _("I guess your parents are bakers, because they made you such a cutie pie!"), #0
            _("The one thing I can't resist in this life is your lips."), #1
            _("You look stunning today."), #2
            _("You live rent-free in my heart."), #3
            _("You have beautiful hair."), #4
            _("You have gorgeous eyes."), #5
            _("You have a beautiful smile."), #6
            _("I always have a great time with you."), #7
            _("Every day with you is a good day."), #8
            _("I wish I could hold you close right now."), #9
            _("The night sky holds nothing to your beauty."), #10
            _("Cuddling with you would be perfect right about now."), #11
            _("Why are you so cute?"), #12
            _("Seeing you every day always makes me grin like an idiot."), #13
            _("Our first kiss is going to be epic, don't you think?"), #14
            _("I really like getting to know you."), #15
            _("Everything makes me think of you."), #16
            _("You're pretty much my dream girl."), #17
            _("You never fail to give me butterflies."), #18
            _("You make my heart happy."), #19
        )
        
        # Sexting prompts for your more 'risque' options
        sext_prompts_hot = (
            _("Is it geting hot in here, or is it just you?"), #0
            _("I want to bring you in close."), #1
            _("I want to kiss your lips passionately."), #2
            _("I want to run my hands through your hair."), #3
            _("I want to hold your hands in mine."), #4
            _("I really want to kiss you right now."), #5
            _("I want to run my hands along your body while I kiss your neck."), #6
            _("I feel nervous about telling you all of the sexual desires I have when it comes to you."), #7
            _("If kissing is the language of love, then we have alot to talk about."), #8
            _("I want to hold you in my arms as we kiss."), #9
            _("What you're wearing would look even better on my bedroom floor."), #10
            _("Take off your clothes. I want to see your beautiful body."), #11
            _("I want to lay you down on my bed as we kiss."), #12
            _("I want to feel your hot breath on my skin as we feel each other."), #13
            _("Your body is so hot."), #14
            _("You're so sexy."), #15
            _("I can't wait to be alone with you."), #16
            _("You're all I can think about."), #17
            _("I'm hot."), #18
            _("I'm hot."), #19
        )

        # Sexting prompts for your most 'risque' options
        sext_prompts_sexy = (
            _("I bet you have a really hot orgasm face."), #0
            _("I can't wait to be alone with you."), #1
            _("I can't wait to be by your side. Or on top if you prefer."), #2
            _("If you were here, I'd take your panties off with my teeth and... I'll just let you finish that sentence off."), #3
            _("I'm picturing you naked right now... damn you look good."), #4
            _("I think there is something insanely sexy about a woman being in control. Don't you agree?"), #5
            _("I want to hear you breathing in my ear when I make you reach orgasm."), #6
            _("I can't wait to feel your thighs squeezing my head."), #7
            _("I bet you have the sexiest sounding moans in the world."), #8
            _("I was just lying in bed for the last hour thinking about you... guess what I was doing!"), #9
            _("If I were with you right now, where would you want me to touch you?"), #10
            _("What is your secret fetish? You must have one, come on."), #11
            _("Everything about you turns me on."), #12
            _("I'm clicking this option with one hand, because the other hand is busy."), #13
            _("I wish I could fuck you in that spaceroom right now."), #14
            _("I get so horny thinking about you when I touch myself."), #15
            _("I get so turned on thinking about you."), #16
            _("When you and I are finally together, I want to make you cum so hard."), #17
            _("I wanna brings sex toys into the bedroom with us and use them on you."), #18
            _("I want to watch you masurbate for me."), #19
        )

        # Sexting prompts for the haha funnies
        sext_prompts_funny = (
            _("I put on my robe and wizard hat."), #0
            _("It's not my fault that I fell for you... You tripped me!"), #1 
            _("Do you like my shirt? It's made out of boyfriend material."), #2
            _("I looked hot today, you missed out."), #3
            _("I'm funny."), #4
            _("I'm funny."), #5
            _("I'm funny."), #6
            _("I'm funny."), #7
            _("I'm funny."), #8
            _("I'm funny."), #9
            _("I'm funny."), #10
            _("I'm funny."), #11
            _("I'm funny."), #12
            _("I'm funny."), #13
            _("I'm funny."), #14
            _("I'm funny."), #15
            _("I'm funny."), #16
            _("I'm funny."), #17
            _("I'm funny."), #18
            _("I'm funny."), #19
        )
        return