init -990 python in mas_submod_utils:
    Submod(
        author="NickWildish",
        name="NSFW Submod",
        description="A collection of NSFW topics and features for MAS.",
        version="0.9.0",
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

        OUT: 
            True if the player has been away for six hours AND the getting nude topic hasn't been used for six hours, False if otherwise
        """
        time_away_req = datetime.timedelta(hours=set_hours)
        time_since_last_seen = datetime.datetime.now() - store.mas_getEVL_last_seen("nsfw_monika_gettingnude")

        if store.mas_getAbsenceLength() >= time_away_req and time_since_last_seen >= time_away_req:
            return True
        else:
            return False

    def canShow_underwear():
        """
        Checks if the player should be able to see Monika's underwear yet.

        OUT:
            True if the player has seen 'monika_gettingnude' topic AND risque is allowed AND the player hasn't seen the topic for at least 6 hours AND the player hasn't already unlocked her underwear, False if otherwise
        """
        if store.mas_getEV("nsfw_monika_gettingnude").shown_count >= 1 and store.mas_canShowRisque() and hour_check(set_hours=6) and not store.mas_SELisUnlocked(store.mas_clothes_underwear_white):
            return True
        else:
            return False

    def canShow_birthdaySuit():
        """
        Checks to see if the player should be able to see Monika with no clothes yet.

        OUT: 
            True if the player has seen 'monika_gettingnude' topic twice AND risque is allowed AND the player hasn't seen the topic for at least 6 hours AND the player hasn't already unlocked her naked, false if otherwise
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

    def return_sext_response(category=0, response_no=0):
        """
        Returns a Monika quip from a selected category.

        IN:
            category - The category of the response
                (Default: 0)
            response_no - The location in the category of a response
                (Default: 0)

        OUT: 
            A string containing a particular response from Monika.
        """

        # Sexting responses for your average compliment
        sext_response_cute = (
            _("Thankyou"), #0
            _("Thanks"), #1
            _("That's very cheesy"), #2
            _("That's cheesy"), #3
            _("That's so cheesy"), #4
            _("You're the sweetest"), #5
            _("You're so sweet"), #6
            _("That's so nice of you to say"), #7
            _("You're so cheesy"), #8
            _("You are just the cutest"), #9
            _("You always know exactly what to say"), #10
            _("You always bring a smile to my face"), #11
            _("..."), #12
            _("That's so sweet"), #13
            _("You're so sweet, you know that?"), #14
            _("You know just what to say..."), #15
            _("You make me so happy"), #16
            _("You're so kind"), #17
            _("That's so sweet"), #18
            _("That's sweet"), #19
        )

        # Sexting responses for the more 'risque' options
        sext_quips_hot = (
            _("What else?"), #0
            _("I like the sound of that"), #1
            _("You know exactly what to say"), #2
            _("I've never felt this way before"), #3
            _("You're making me feel all tingly"), #4
            _("You're getting me all riled up"), #5
            _("Don't tempt me to try and break the screen to get to you"), #6
            _("Please keep going"), #7
            _("You're so hot when you talk like that"), #8
            _("That is so hot"), #9
            _("I feel so good when you talk like that"), #10
            _("..."), #11
            _("You're making me all flustered"), #12
            _("Stop it, you're making me blush"), #13
            _("You don't hold back, do you?"), #14
            _("You're hot."), #15
            _("You're hot."), #16
            _("You're hot."), #17
            _("You're hot."), #18
            _("You make me so happy talking like that"), #19
        )

        # Sexting responses for the most 'risque' options
        sext_quips_sexy = (
            _("You're so sexy when you talk like that"), #0
            _("That is so sexy"), #1
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

        # Sexting responses for the haha funnies
        sext_quips_funny = (
            _("Haha! What are you talking about, [player]?"), #0
            _("Pfft! That's so cheesy, [player]."), #1
            _("Oh my god! You did not just make that joke, haha~"), #2
            _("Haha~ Is that right?"), #3
            _("Oh. That's very out-of-the-blue, [player]."), #4
            _("I just want to tear your clothes off."), #5
            _("I'm only this naughty for you~."), #6
            _("Oh? Try away, [player]."), #7
            _("No."), #8
            _("I think that you scratching my back while we make love would be so hot..."), #9
            _("Where is your hand, [player]?"), #10
            _("Oh, I want to do even naughtier things to you..."), #11
            _("Mmm... and what would that be, [player]?"), #12
            _("I'm feeling so good, [player]..."), #13
            _("Proper grammar..."), #14
            _("Uh... Did you want to try that again, [player]? Haha~"), #15
            _("Ahaha~ You're so funny, [player]."), #16
            _("Ahaha~ Thankyou... I guess?"), #17
            _("Mmm, you do~"), #18
            _("You're such a stud."), #19
        )

        if category == 1:
            category_name = sext_quips_hot
        else if category == 2:
            category_name = sext_quips_sexy
        else if category == 3:
            category_name = sext_quips_funny
        else:
            category_name = sext_quips_cute

        return category_name[quip_no]

    def return_sext_prompt(category=0, prompt_no=0):
        """
        Returns a Monika quip from a selected category.

        IN:
            category - The category of the quip
                (Default: 0)
            prompt_no - The location in the category of a prompt
                (Default: 0)

        OUT: 
            A string containing a particular prompt for Monika.
        """

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
            _("When we're together, I want to have you lie back and let me take care of you."), #18
            _("I'm wearing something you might like right now."), #19
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
            _("I want to watch you masturbate for me."), #19
        )

        # Sexting prompts for the haha funnies
        sext_prompts_funny = (
            _("I put on my robe and wizard hat."), #0
            _("It's not my fault that I fell for you... You tripped me!"), #1 
            _("Do you like my shirt? It's made out of boyfriend material."), #2
            _("I looked hot today, you missed out."), #3
            _("You like jazz?"), #4
            _("What do you want to do to me right now?"), #5 - Please fold my clothes neatly
            _("You've been a naughty girl."), #6 - Santa will bring you a lump of coal
            _("I'm about to blow your mind with my sexting. Ready?"), #7 - Lay me into bed, your hands caress my body. Your palms are sweaty. Knees weak. Arms spaghetti.
            _("Wanna have a threesome?"), #8
            _("What's a fantasy that you have for when we have sex one day?"), #9 - Scratching back, once a squirrel did that to me.
            _("What is a question that's on your mind right now?"), #10 - Where is your hand? In my bowl of Doritos.
            _("I kinda wanna do naughty things to you..."), #11 - Cool aid man - "Oh yeah."
            _("You want to know what I have that is massive?"), #12 - My college debt.
            _("Are you feeling good right now?"), #13 - Hi [text here], I'm Dad.
            _("What's one of you're fetishes?"), #14 - Proper grammar... Well then your in luck.
            _("My wang is as hard as a prosthetic leg."), #15 - Change for women. I'm as wet as 
            _("Would thou perchance wish to partake in coitus?"), #16
            _("You have big, beautiful nipples."), #17
            _("Do I make you horny baby?"), #18 - Do I make you randy?
            _("You're so cute."), #19 - You're stuch a stud / babe - You're a wizard, Harry.
        )
        
        if category == 1:
            category_name = sext_prompts_hot
        else if category == 2:
            category_name = sext_prompts_sexy
        else if category == 3:
            category_name = sext_prompts_funny
        else:
            category_name = sext_prompts_cute

        return category_name[prompt_no]