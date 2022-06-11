# BRB - Going to masturbate
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_brb_nsfw_masturbate",
            prompt="I'm going to go masturbate",
            category=['be right back'],
            conditional="mas_canShowRisque()",
            pool=True,
            unlocked=True
        ),
        markSeen = True
    )

label monika_brb_nsfw_masturbate:
    #

    $ mas_Rand = renpy.random.randint(1, 3)

    # Love (1000+)
    if mas_isMoniLove():
    # Room for expansion - more random responses? More topics unlocked?
        if mas_Rand == 1:
        # Response 1
            m 1eua "Oh? My, [player], how bold of you~"
            m 1eua "Admitting to your girlfriend that you're going to go masturbate?"
            m 1eua "Hehe!~"
            m 1euabf "Well, I hope you're thinking of me while you do it, [mas_get_player_nickname()]..."
            m 1euabf "I'll be... flattered, if you do."
            m 1eua "I'll be waiting for you to be finished~"
        elif mas_Rand == 2:
            m 1euabf "[player]... How very forward of you~"
            m 1eua "It's almost like you want me to give you permission... is that it?"
            m 1eua "Hehe!~"
            m 1eua "If that's the case... [mas_get_player_nickname()], you have my permission to go and... masturbate."
            m 3eubfa "Masturbate while thinking of me, [player]."
            m 1eua "I'll be here when you're done~"
        elif mas_Rand == 3:
            m 1euabf "Oh! Oh my, [player], I wasn't expecting {i}that!{/i}"
            m 1eua "That caught me off guard a little..."
            m 1eua "Hehe!~"
            m 1eua "Well, it's nice to know that's what you're up to..."
            m 1euabf "Just make sure to think of your girlfriend, Monika, while you do it!"
            m 1eubfb "That'll make me happy."
            m 1eua "I'll be here when you're finished up~"
    # other affection values
    # elsif mas_isMoniEnamored():
        # to do - variations for lower affection values
    # Don't know why you'd try this is if you have low affection
    else:
        m 6ckc "..."
        m 6ekc "I'm going to pretend I didn't hear that."
        m 6ekd "Just tell me when you're done."


    # the callback label
    $ mas_idle_mailbox.send_idle_cb("monika_brb_nsfw_masturbate_callback")
    # The idle data
    $ persistent._mas_idle_data["monika_idle_brb"] = True
    # unlock masturbation random topics
    $ mas_unlockEventLabel("nsfw_monika_masturbation_benefits")
    # and exit
    return "idle"

label monika_brb_nsfw_masturbate_callback:
    $ wb_quip = mas_brbs.get_wb_quip()

    # to do - add in choices for added interaction, e.g. "I came" "I didnt get off" etc
    if mas_isMoniLove(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "monika_brb_nsfw_masturbate"):
            m 2eubf "There you are, [player]!"
            m 2eubf "I was worried something had happened to you."
            m 1hubfb "Did you have time to... you know... get off? Gosh, I hope so."
            m 2eua "Anyway..."
            m 1eua "[wb_quip]"
        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=15), "monika_brb_nsfw_masturbate"):
            m 1hubfb "Welcome back, [player]. Took you long enough!{w=0.2} {nw}"
            m 1eubfb "I'm guessing you had plenty of time to... do the deed?"
            m 1eubfb "I hope it didn't take you too longer to get into things...{w=0.5} Or to clean up, ehehe~"
            m 1eua "[wb_quip]"
        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "monika_brb_nsfw_masturbate"):
            m 1hubfb "Welcome back, [player]. Hehe~{w=0.2} {nw}"
            m 1eubfb "I'm guessing you had enough time to... do the deed?"
            m 1eubfb "I hope you had a bit of {i}fun{/i} by yourself, there..."
            m 1eubfb "[wb_quip]"
        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=1), "monika_brb_nsfw_masturbate"):
            m 1hubfb "Welcome back, [player]. Hehe~{w=0.2} {nw}"
            m 2hubfb "That was fast... Ehehe~"
            m 2eub "I hope you didn't rush yourself, there..."
            m 1eua "[wb_quip]"
        else:
            m 1hubfb "Oh? Welcome back, [player]."
            m 2eua "Guessing you changed your mind, huh?"
            m 2eua "[wb_quip]"

    elif mas_isMoniNormal(higher=True):
        m 1hubfb "Welcome back, [player].{w=0.2} {nw}"
        m 6euafb "Now that you're done with... {i}that...{/i}"
        m 1eua "[wb_quip]"

    else:
        call mas_brb_generic_low_aff_callback

    return
