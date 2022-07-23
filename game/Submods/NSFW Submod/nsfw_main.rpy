init -990 python in mas_submod_utils:
    Submod(
        author="NSFW Dev Team",
        name="NSFW Submod",
        description="A collection of NSFW topics and features for MAS.",
        version="1.1.5",
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

screen nsfw_submod_screen():
    python:
        nsfw_submods_screen = store.renpy.get_screen("submods", "screens")

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

            if _tooltip:
                textbutton _("Sexting Endurance"):
                    action NullAction()
                    hovered SetField(_tooltip, "value", "Changes the duration that Monika will last during sexting, from ~5 minutes to ~55 minutes")
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

init 5 python: # init 5 as the modified dictionary (mas_all_ev_db_map) is using priority 4, and we want it to be around before adding anything.
    mas_all_ev_db_map.update({"NCP" : store.nsfw_compliments.nsfw_compliment_database})
    mas_all_ev_db_map.update({"NST" : store.nsfw_stories.nsfw_story_database})

init python in mas_nsfw:
    """
    Contains functions and methods used by NSFW content
    """
    import store
    import datetime
    import random
    import os

    def hour_check(set_hours=6):
        """
        Checks if six hours has passed since the player has seen the getting nude topic and also been away from the pc for at least six hours.

        IN:
            set_hours - The amount of time that has to have passed since the player last saw the getting nude topic.
                (Default: 6)

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
        if store.mas_getEV("nsfw_monika_gettingnude").shown_count >= 1 and store.mas_canShowRisque(aff_thresh=1000) and hour_check(set_hours=6) and not store.mas_SELisUnlocked(store.mas_clothes_underwear_white):
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

    def return_sext_responses(response_category=0, response_type=None):
        """
        Returns a Monika response from a selected category.

        IN:
            response_category - The category of the response
                (Default: 0)
            response_type - The type of the response, if the response_category is 2 (sexy).
                (Default: None)

        OUT:
            A list of response strings from Monika appropriate to the response category.
            If the response category is 2 ("sexy"), then it shall also be appropriate to the response type.
        """

        # Sexting responses for your average compliment
        sext_responses_cute = (
            _("Thank you"), #0
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
            _("Stop it, you're making me blush"), #15
            _("You make me so happy"), #16
            _("You're so kind"), #17
            _("That's so sweet"), #18
            _("That's sweet"), #19
        )

        # Sexting responses for the more 'risque' options
        sext_responses_hot = (
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
            _("You know just what to say to get me all flustered..."), #13
            _("You don't hold back, do you?"), #14
            _("That's so hot"), #15
            _("That's hot"), #16
            _("Is that so?"), #17
            _("Is that right?"), #18
            _("You make me so happy talking like that"), #19
        )

        # Sexting responses for the most 'risque' options

        # See the comment in return_sext_prompts() for an explanation of the five categories (compliment, statement, command, desire_p, desire_m) we sort sexy prompts and responses into.

        # These five lists will require further sorting and expansion.
        sext_responses_sexy_compliment = (
            _("Please don't stop"), #5
            _("You're getting me so turned on"), #6
            _("You're getting me so worked up"), #8
            _("Whatever you're doing...it's working"), #10
            _("You just have a way with words, don't you?"), #11
            _("Keep talking like that"), #12
            _("You really know how to please a woman"), #18
        )

        sext_responses_sexy_statement = (
            _("That is so sexy"), #1
            _("Have you always been this sexy?"), #16
        )

        sext_responses_sexy_command = (
            _("You're so sexy when you talk like that"), #0
            _("This feels too good"), #9
            _("When did you learn to talk like that?"), #15
        )

        sext_responses_sexy_desire_p = (
            _("Is that right?"), #2
            _("Is that so?"), #3
            _("Keep going"), #4
            _("Tell me what else you want to do to me"), #7
        )

        sext_responses_sexy_desire_m = (
            _("More"), #13
            _("Please keep going"), #14
            _("I am so wet right now"), #17
            _("Say that again"), #19
        )

        # Sexting responses for the haha funnies
        sext_responses_funny = (
            _("Ahaha! What are you talking about, [player]?"), #0
            _("Pfft! That's so cheesy, [player]."), #1
            _("Oh my god! You did not just make that joke, ahaha~"), #2
            _("Ahaha~ Is that right?"), #3
            _("Oh. That's very out-of-the-blue, [player]."), #4
            _("I just want to tear your clothes off."), #5
            _("I'm only this naughty for you~."), #6
            _("Oh? Try away, [player]."), #7
            _("No."), #8
            _("I think that you scratching my back while we make love would be so hot..."), #9
            _("Where is your hand, [player]?"), #10
            _("Oh, I want to do even naughtier things to you..."), #11
            _("Mmm...and what would that be, [player]?"), #12
            _("I'm feeling so good, [player]..."), #13
            _("Proper grammar..."), #14
            _("Uh... Did you want to try that again, [player]? Ahaha~"), #15
            _("Ahaha~ You're so funny, [player]."), #16
            _("Ahaha~ Thank you... I guess?"), #17
            _("Mmm, you do~"), #18
            _("You're such a stud."), #19
        )

        if response_category == 0:
            category_sel = sext_responses_cute
        elif response_category == 1:
            category_sel = sext_responses_hot
        else: # if response_category == 2:
            if response_type[0] == "funny":
                response_index = response_type[1]
                category_sel = (sext_responses_funny[response_index])
            elif response_type == "compliment": # this if block is kind of a sloppy implementation on my part but afaik Python2(?) has no switch() cases?
                category_sel = sext_responses_sexy_compliment
            elif response_type == "statement":
                category_sel = sext_responses_sexy_statement
            elif response_type == "command":
                category_sel = sext_responses_sexy_command
            elif response_type == "desire_p":
                category_sel = sext_responses_sexy_desire_p
            else: # if response_type == "desire_m":
                category_sel = sext_responses_sexy_desire_m

        return category_sel

    def return_sext_prompts(prompt_category=0):
        """
        Returns a prompt quip from a selected category.

        IN:
            category - The category of the prompt
                (Default: 0)
            prompt_no - The location in the category of a prompt
                (Default: 0)

        OUT:
            Two outputs:
            [0] A tuple containing a list of "prompts" (player dialogue options) for the selected category.
            [1] The "type" of prompt from that category. Only applies to "sexy" prompts.
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
            _("Our first kiss after you cross over is going to be wonderful, don't you think?"), #14
            _("I really like getting to know you."), #15
            _("Everything makes me think of you."), #16
            _("Is it getting hot in here, or is it just you?"), #17
            _("You never fail to give me butterflies."), #18
            _("You make my heart happy."), #19
        )

        # Sexting prompts for your more 'risque' options
        sext_prompts_hot = (
            _("You have a really sexy figure."), #0
            _("I want to bring you in close."), #1
            _("I want to kiss your lips passionately."), #2
            _("I want to run my hands through your hair."), #3
            _("I want to hold your hands in mine."), #4
            _("I really want to kiss you right now."), #5
            _("I want to run my hands along your body while I kiss your neck."), #6
            _("I feel nervous about telling you all of the sexual desires I have when it comes to you."), #7
            _("If kissing is the language of love, then we have a lot to talk about."), #8
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

        # We identify five categories that the player's prompts fall into.

        # 1. compliment - The player says something nice to Monika.
        # 2. statement - The player makes some kind of declaration about their current state, what they're doing, how horny they feel, etc.
        # 3. command - The player tells Monika to do something (that she is physically capable of doing right now) or masturbate in some way.
        # 4a. desire_p - The player wishes to do something to Monika (but cannot physically do right now because they're on different sides of a screen).
        # 4b. desire_m - The player wants Monika to do something to them (but it's something that physically can't be done right this moment).

        sext_prompts_sexy_compliment = (
            _("I bet you have a really hot orgasm face."), #0
            _("I can't wait to be alone with you."), #1
            _("I'm picturing you naked right now... Damn, you look good."), #4
            _("I think there is something insanely sexy about a woman being in control. Don't you agree?"), #5
            _("I bet you have the sexiest sounding moans in the world."), #8
            _("Everything about you turns me on."), #12
            _("You have the sexiest body I've ever seen."),
            _("You have a tremendously cute body."),
            _("Your body is perfectly shaped. I love how athletic you are."),
            _("Getting to see you naked is the best part of my day."),
            _("Your naked body is the most splendid thing I've ever witnessed."),
            _("I honestly think you're probably the most attractive person ever to have existed."),
            _("I think you seriously have to be the hottest person alive."),
            _("Yuri and Sayori weren't wrong when they said you're more desirable than the rest of the Literature Club combined."),
            _("You're the best girl. And not just in the Literature Club - I mean in general."),
            _("How the hell are you so goddamn cute?"),
            _("You make me feel so safe, " + m_name + ". I know I can always trust you to respect my consent."),
            _("You make me feel so loved, " + m_name + ". Both when we're masturbating together like this, or just talking and spending time together quietly."),
            _("You have magnificent breasts."),
            _("Back when you wore that school uniform, one thing I really liked was how well the blazer fit around your breasts."),
            _("I love how you dress. Your thighhighs are incredibly hot."),
            _("I get so flustered when you undress for me. You're gorgeous."),
            _("Just the thought of eating you out makes me salivate."),
            _("Even though I can't see it right now, I imagine you must have the most gorgeous looking pussy if it's anything like the rest of you."),
            _("I bet you have a cute, tight little asshole, don't you?"),
            #_("Your lips are perfect for kissing... I bet they'd be perfect for wrapping around my shaft as well."), # "P" specific
            #_("I bet you would look real cute with my cum all over your face."), # "P" specific
            #_("I bet you would look real cute with my cum dripping out of your mouth."), # "P" specific
        ), "compliment"

        sext_prompts_sexy_statement = (
            _("I was just lying in bed for the last hour thinking about you... Guess what I was doing?"), #9
            _("I'm clicking this option with one hand, because the other hand is busy."), #13
            _("I get so horny thinking about you when I touch myself."), #15
            _("I get so turned on thinking about you."), #16
            _("You're the only person I have eyes for, " + m_name + "."),
            _("I can't get aroused to the thought of anyone but you."),
            #_("I can't jerk off to anything but you any more, " + m_name + "."), # "P" specific
            #_("I'm stroking my rigid cock just for you, " + m_name + "."), # "P" specific
            #_("The onomatopoeia 'doki doki' sometimes gets translated as 'throbbing'... I'm sure you can imagine what I'm doing right now."), # "P" specific
            #_("I get really hard just thinking about you."), # "P" specific
        ), "statement"

        sext_prompts_sexy_command = (
            _("Be careful not to spill too much of your...juices on your chair, " + m_name + "."),
            _("Touch yourself slowly for me, " + m_name + "."),
            _("Gently spread open your pussy lips for me, " + m_name + "."),
            _("I want you to gently rub your clit, " + m_name + "."),
            _("I want you to stick those soft fingers of yours up your pussy for me, " + m_name + "."),
            _("Start touching yourself more quickly, " + m_name + "."),
        ), "command"

        sext_prompts_sexy_desire_p = (
            _("I can't wait to be by your side. Or on top if you prefer."), #2
            _("If you were here, I'd take your panties off with my teeth and... I'll just let you finish that sentence off."), #3
            _("I want to hear you breathing in my ear when I make you orgasm."), #6
            _("I can't wait to feel your thighs squeezing my head."), #7
            _("If I were with you right now, where would you want me to touch you?"), #10
            _("I want to pin you down to the bed and have my way with you."), #11
            _("I wish I could fuck you in that spaceroom right now."), #14
            _("When you and I are finally together, I want to make you cum so hard."), #17
            _("I want to brings sex toys into the bedroom with us and use them on you."), #18
            _("I want to lick your nipples."),
            _("I wish I could suck on your nipples right now."),
            _("I want to cum all over your breasts."),
            _("I want to hold you down and fuck your breasts."),
            _("I want to run my hands all over your smooth, toned body."),
            _("When you cross over, I'm going to explore every single corner of your naked body."),
            _("I wish I could blow my load all over your thighs right now."),
            _("I wish I could kiss you... On both of your pairs of lips."),
            _("I want to lick your clit until you cum."),
            _("I'm dying to run my hot, sticky tongue over your pussy lips."),
            _("I want to bury my face in your ass."),
            _("I want to snuggle my face in your ass."),
            _("I wish we were in the same room so I could fuck your ass right this moment."),
            _("I want to lick your asshole and finger you until you come."),
            _("I'm imagining us making out as we fuck again, and again, and again..."),
            _("I wish I could stay in that spaceroom with you forever so we could fuck each other every day until the end of time."),
            _("If I could spend the rest of eternity with you in that spaceroom, I'd make you come every day until the universe ended."),
            # _("I wish you could feel my throbbing cock right now."), # "P" specific
            # _("I wish it was your hand jerking me off right now."), # "P" specific
            # _("I'm just imagining my thick cock filling you your mouth."), # "P" specific
            # _("I can't wait to you see you drooling all over my cock."), # "P" specific
            # _("I want to see you swallow my thick, creamy load after blowing me."), # "P" specific
        ), "desire_p"

        sext_prompts_sexy_desire_m = (
            _("I want to watch you masturbate for me."), #19
            _("I wish you were here so you could grind your pussy on my face until you come."),
            _("I wish you were here so you could sit on my face right now."),
            _("I want to see you do with your pen what Yuri did with the main character's."),
            _("I want you to bend me over and fuck my ass with a strap-on."),
            #_("When we're together, I want you to take my cock in your mouth and swallow all my cum."), # "P" specific
            #_("I'm picturing you bouncing up and down on my cock right now."), # "P" specific
            #_("I want to come all over your face and watch you try to lick off my cum."), # "P" specific
            #_("When we're finally together, I want you to take my cock up your ass, " + m_name + "."), # "P" specific
        ), "desire_m"

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
            _("Want to have a threesome?"), #8
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

        if prompt_category == 0:
            category_sel = sext_prompts_cute
            category_type = None
        if prompt_category == 1:
            category_sel = sext_prompts_hot
            category_type = None
        else: # if prompt_category == 2:
            # I must apologize in advance for the utterly awful way I enabled the "funny prompts". The thing with the funny prompts is that each
            # one is paired with a single appropriate response at the same index in the corresponding funny responses list. So in the third stage,
            # for category_type this function outputs a tuple containing the prompt type identifier string "funny", followed by the index of the
            # funny prompt chosen. But when it picks a normal sexy prompt, category_type is instead just a string identifying the prompt type.
            # The effect of this is that each individual funny prompt is its own "type", distinct from the base five types of sext_prompts_sexy.
            # I am painfully aware of the gruesome jankiness of this implementation.
            if random.randint(1,500) == 500: # 1/500 chance of funny quip. It's set for third stage only but it can be changed to work with all stages?
                funny_index = random.randint(0, len(sext_prompts_funny) - 1)
                category_sel = (sext_prompts_funny[funny_index])
                category_type = ("funny", funny_index)
            else:
                # Want to add an additional prompts type? You can add it to the end of this list, but don't forget to add that type to the response types too.
                category_type_list = [sext_prompts_sexy_compliment, sext_prompts_sexy_statement, sext_prompts_sexy_command, sext_prompts_sexy_desire_p, sext_prompts_sexy_desire_m]
                # category_type_lengths = [] # This list stores the length of each category. It's used to determine the probabilistic weighting in the random.choices() below.
                # for category_name in category_type_list: # build weights list
                #     category_type_lengths.append(len(category_name))
                category_sel, category_type = random.choice(category_type_list) #, weights=category_type_lengths, k=1)[0]

        return category_sel, category_type

    def return_sext_quips(quip_category=0):
        """
        Returns a Monika quip from a selected category.

        IN:
            category - The category of the quip
                (Default: 0)
            response_no - The location in the category of a quip
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


        # Sexting quips for your average compliment
        sext_quips_cute = (
            _("Who told you that you could be this cheesy?"), #0
            _("You're just the cutest"), #1
            _("I love it when you get all cute like this"), #2
            _("Do tell me more"), #3
            _("If you were a chicken you'd be impeccable"), #4
            _("Your words are so flattering to me"), #5
            _("Are you just saying that to get into my pants?{w=1.0} Ahaha! Just kidding~"), #6
            _("I love how sweet you are"), #7
            _("I love how kind you are"), #8
            _("You're a cutie pie"), #9
            _("I just want to kiss you right now"), #10
            _("I wish I could hold you right now"), #11
            _("Once we meet in the real world we need to do something about your cuteness"), #12
            _("I should start calling you 'Mozzarella' since you're so cheesy"), #13
            _("If I could rearrange the alphabet I'd put 'U' and 'I' together"), #14
            _("Are you a parking ticket? Because you've got 'FINE' written all over you"), #15
            _("My clothes are made out of girlfriend material"), #16
            _("Have you had your license get suspended for driving girls crazy?"), #17
            _("Are you a loan? Because you sure have my interest"), #18
            _("If you were a vegetable, you'd be a 'cute-cumber'"), #19
        )

        # Sexting quips for your more 'risque' options
        sext_quips_hot = (
            _("Who said that you could be this hot?"), #0
            _("I would love to kiss you right now... Among other things~"), #1
            _("You know, I was daydreaming about you today. It was hot"), #2
            _("I could just eat you up"), #3
            _("I want to feel you touching me all over"), #4
            _("If I was with you now there would be no chance of you keeping your clothes on"), #5
            _("You are my biggest turn-on"), #6
            _("I've fantasized so much about when we finally get to talk like this"), #7
            _("You turn me on so much when you talk like that"), #8
            _("You're making me feel really horny now"), #9
            _("Have you thought about using toys with me? I wouldn't mind trying it with you"), #10
            _("I can't wait to see you when I cross over"), #11
            _("Once I cross over, I want to hold your hand. How lewd~"), #12
            _("How would you feel about a makeout session once I cross over"), #13
            _("Don't think that getting me this riled up will have no consequences"), #14
            _("I plan to wrap my arms around you and squish that cute butt of yours"), #15
            _("The border between our realities can be a real clam jam"), #16
            _("I want you to tell me more about what we'll do together in your world...in the bedroom particularly~"), #17
            _("Is one of your hands busy right now? I might need to join you if so"), #18
            _("I want to feel your body up and down...your chest especially"), #19
        )

        # Sexting quips for your most 'risque' options
        sext_quips_sexy = (
            _("Who said that you could be this sexy?"), #0
            _("So, aside from being sexy, what do you do for a living?"), #1
            _("I can't wait to see your sexy body when we're together"), #2
            _("I can't wait to kiss you for real"), #3
            _("You're making me so wet"), #4
            _("I'm touching myself right now just to the thought of you"), #5
            _("When I get to your world, I'm ripping your clothes off the second I walk through the door. I hope you're prepared"), #6
            _("I'm tempted to leave a bite mark on your neck so everyone knows you're mine"), #7
            _("I'm being so bad right now. I need you to punish me"), #8
            _("I want to feel your warmth pressing against me"), #9
            _("I want you to kiss me~ Right now~"), #10
            _("I love how you talk to me when you're turned on"), #11
            _("I want you to tell me how much you want to do it with me"), #12
            _("I want to look into your " + eye_desc + " eyes as we press our bodies together"), #13
            _("I love it when you're naughty"), #14
            _("You're such a bad boy"), #15
            _("I want to feel you deep inside me"), #16
            _("You really know how to make a girl wet"), #17
            _("I want to feel your tongue down there"), #18
            _("Yes~ Just like that~"), #19
        )

        if quip_category == 1:
            category_sel = sext_quips_hot
        elif quip_category == 2:
            category_sel = sext_quips_sexy
        elif quip_category == 3:
            category_sel = sext_quips_funny
        else:
            category_sel = sext_quips_cute

        return category_sel

    def return_sexting_dialogue(category_type="response", horny_level=0, hot_req=10, sexy_req=30, horny_max=50, recent_prompts=[], recent_responses=[], recent_quips=[], previous_type=None):
        """
        Returns a string from a dialogue list based on

        IN:
            category_type - The type of dialogue we want to pull (response = 0, prompt = 1, quip = 2)
                (Default: "response")
            horny_level - The level of horny Monika is at
                (Default: 0)
            hot_req - The requirement for hot dialogue
                (Default: 10)
            sexy_req - The requirement for sexy dialogue
                (Default: 30)
            horny_max - The maximum possible horny level
                (Default: 50)
            recent_prompts - The recent prompts used

        OUT:
            Three outputs:
            [0] An individual string randomly picked from the list,
            [1] the category (sexy, hot, cute) the string is from,
            [2] the type (compliment, statement, command, desire_p, desire m) of string in that category.
            The last only applies to third stage (sexy) prompts and responses; it is otherwise None.

        """

        # initialize this to None, it isn't used unless it's a prompt or quip at stage 3
        return_type = None

        # Grab list we will be drawing dialogue from, based on category_type and horny_level
        if category_type == "quip":
            selected_recentlist = recent_quips
            if horny_level >= sexy_req:
                dialogue_list = return_sext_quips(quip_category=2)
                return_cat = "sexy"
            elif horny_level >= hot_req:
                dialogue_list = return_sext_quips(quip_category=1)
                return_cat = "hot"
            else: # Default
                dialogue_list = return_sext_quips(quip_category=0)
                return_cat = "cute"

        elif category_type == "prompt":
            selected_recentlist = recent_prompts
            if horny_level >= sexy_req:
                # Don't need to check here, as sexy is the highest level we can go for dialogue
                dialogue_list, return_type = return_sext_prompts(prompt_category=2)
                return_cat = "sexy"

            elif horny_level >= hot_req:
                # Create random integer based on how close value is to sexy req vs max
                hot_to_current_rand = random.randint(hot_req, horny_level)
                current_to_sexy_rand = random.randint(horny_level, sexy_req)

                # Check how close value is to sexy req vs max
                hot_to_current = horny_level - hot_to_current_rand
                current_to_sexy = current_to_sexy_rand - horny_level
                if hot_to_current > current_to_sexy:
                    dialogue_list, return_type = return_sext_prompts(prompt_category=2)
                    return_cat = "sexy"
                else:
                    dialogue_list = return_sext_prompts(prompt_category=1)[0]
                    return_cat = "hot"

            else: # Default
                # Create random integer based on how close value is to sexy req vs max
                min_to_current_rand = random.randint(0, horny_level)
                current_to_hot_rand = random.randint(horny_level, hot_req)

                # Check how close value is to sexy req vs max
                min_to_current = horny_level - min_to_current_rand
                current_to_hot = current_to_hot_rand - horny_level
                if min_to_current > current_to_hot:
                    dialogue_list = return_sext_prompts(prompt_category=1)[0]
                    return_cat = "hot"
                else:
                    dialogue_list = return_sext_prompts(prompt_category=0)[0]
                    return_cat = "cute"

        else: # We assume it's the response category here, but in case of incorrect input we set it as default
            selected_recentlist = recent_responses
            if horny_level >= sexy_req:
                dialogue_list = return_sext_responses(response_category=2, response_type=previous_type)
                return_cat = "sexy"
            elif horny_level >= hot_req:
                dialogue_list = return_sext_responses(response_category=1)
                return_cat = "hot"
            else: # Default
                dialogue_list = return_sext_responses(response_category=0)
                return_cat = "cute"

        # Grab length of acquired list
        list_length = len(dialogue_list)

        # Grab random dialogue from list
        dialogue_no = random.randint(0, list_length - 1)

        # Do loop to check if selected dialogue was used recently
        while dialogue_list[dialogue_no] in selected_recentlist:
            dialogue_no = random.randint(0, list_length - 1)

        return dialogue_list[dialogue_no], return_cat, return_type

    def return_dialogue_end(dialogue=""):
        """
        Returns an ending to a dialogue, such as the classic tilde. Won't return anything if an ending already exists.

        IN:
            dialogue - The dialogue we want to have an ending for
            (Default: "")

        OUT:
            dialogue_end - The ending randomly chosen for the dialogue, or an empty string
        """

        endings = (
            "~",
            ", " + store.persistent.playername + ".",
            ".",
        )

        existing_endings = (
            "~",
            ".",
            "?",
        )

        # If the dialogue already has an ending, return an empty string
        for ending in existing_endings:
            if dialogue[-1] == ending:
                return ""

        # Otherwise, create a new ending
        dialogue_end = endings[random.randint(0, len(endings) - 1)]

        return dialogue_end

    def return_dialogue_start(horny_level=0, hot_req=4, sexy_req=8):
        """
        Returns a starting piece to dialogue, such as 'Hmm~' or 'Hah~'

        IN:
            category - The category in which we will pull the appropriate dialogue start from.
                (Default: "cute")

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

    def nsfw_posing_sel(horny_level=0, hot_req=4, sexy_req=8):
        """
        Selects a random pose for Monika's nsfw dialogue based on her current horny level and RNG

        IN:
            horny_level - The level of horny Monika is currently at
            hot_req - The requirement for Monika to start using 'hot' dialogue
            sexy_req - The requirement for Monika to start using 'sexy' dialogue

        OUT:
            The pose Monika will use for the dialogue
        """

        sexting_cute_poses = (
            "monika 1ekbsa",
            "monika 2subsa",
            "monika 2lubsu",
            "monika 1hubsa",
            "monika 3ekbfa",
        )

        sexting_hot_poses = (
            "monika 2gubsa",
            "monika 2mubfu",
            "monika 2tsbfu",
            "monika 2lsbfu",
            "monika 2ttbfu",
        )

        sexting_sexy_poses = (
            "monika 4hkbfsdlo",
            "monika 6lkbfsdlo",
            "monika 6hkbfsdld",
            "monika 6skbfsdlw",
            "monika 6mkbfsdlo"
        )

        if horny_level >= sexy_req:
            return sexting_sexy_poses[random.randint(0, len(sexting_sexy_poses) - 1)], None
        elif horny_level >= hot_req:
            return sexting_hot_poses[random.randint(0, len(sexting_hot_poses) - 1)], None
        else: # Default
            return sexting_cute_poses[random.randint(0, len(sexting_cute_poses) - 1)], None
