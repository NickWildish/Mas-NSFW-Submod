# BRB - Going to masturbate
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_brb_masturbate",
            prompt="I'm going to masturbate",
            category=['be right back'],
            conditional="mas_is18Over()",
            pool=True,
            unlocked=True
        ),
        markSeen = True
    )

label nsfw_monika_brb_masturbate:
    # make a random int, for randomness
    $ mas_rand = renpy.random.randint(1, 3)

    # Expansion - add in Affectionate variation, possibly with call to Sexting etc.
    if mas_isMoniEnamored(higher=True): # Enamored (400-999+)
    # Room for expansion - more random responses? More topics unlocked?
        if mas_rand == 1:
        # Response 1
            m 1tublb "Oh? My, [player], how bold of you~"
            m 1tubla "Admitting to your girlfriend that you're going to go masturbate?"
            m 1hubla "Ahaha~"
            m 1mublb "Well, I hope you think of me while you do it, [mas_get_player_nickname()]..."
            m 2tublb "I'd be...flattered, if you did."
            m 3kublu "I'll be waiting for you to be finished~"
        elif mas_rand == 2:
            m 1tublb "[player]... How very forward of you~"
            m 1tubla "It's almost like you want me to give you permission... Is that it?"
            m 1hubla "Ehehe~"
            m 1mublb "If that's the case...you have my permission to go masturbate, [mas_get_player_nickname()]."
            m 6tubfb "Masturbate while thinking of me, [player]."
            m 3kublu "I'll be here when you're done~"
        else:
            m 6wubfsdlo "Oh! Oh my, [player], I wasn't expecting {i}that!{/i}"
            m 6ekbfa "That caught me off guard a little..."
            m 1hubla "Ehehe~"
            m 1mublb "Well, it's nice to know that's what you're up to..."
            m 4ksbfa "Just make sure to think of your girlfriend, Monika, while you do it!"
            m 2ksbfa "That'd make me really happy."
            m 3kublu "I'll be here when you're all finished up~"
    # other affection values - Don't know why you'd try this is if you have low affection
    else: # Anything less than 400 affection
        m 2tsbsc "..."
        m 2tsbsd "I'm going to pretend I didn't hear that."
        m 2ekbssdlb "Just tell me when you're done."

    # the callback label
    $ mas_idle_mailbox.send_idle_cb("monika_brb_nsfw_masturbate_callback")
    # The idle data
    $ persistent._mas_idle_data["nsfw_monika_brb_masturbate"] = True
    # unlock masturbation random topics
        # $ mas_unlockEventLabel("nsfw_monika_masturbation_benefits")
    $ mas_showEVL("nsfw_monika_masturbation_benefits", "EVE", _random=True)
    # and exit
    return "idle"

label monika_brb_nsfw_masturbate_callback:
    $ wb_quip = mas_brbs.get_wb_quip()

    # Expansion - add in choices for added interaction, e.g. "I came" "I didnt get off" etc
    if mas_isMoniEnamored(higher=True):
        if mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=30), "nsfw_monika_brb_masturbate"):
            m 2eubfb "There you are, [player]!"
            m 2eubfa "You had been gone for a little while."
            m 1hubfb "Were you able to...you know...get off? I hope so. Ahaha~"
            m 2eua "Anyway..."
            m 1eua "[wb_quip]"
        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=15), "nsfw_monika_brb_masturbate"):
            m 1hubfb "Welcome back, [player]. Took you long enough!"
            m 1eubfb "I'm guessing you had plenty of time to...do the deed?"
            m 1eubfb "I hope it didn't take you too long to get into it...{w=0.5}or to clean up, ehehe~"
            m 1eua "[wb_quip]"
        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=5), "nsfw_monika_brb_masturbate"):
            m 1hubfb "Welcome back, [player]. Ehehe~"
            m 1eubfb "I'm guessing you had enough time to...do the deed?"
            m 1eubfb "I hope you had a bit of {i}fun{/i} by yourself there..."
            m 1eua "[wb_quip]"
        elif mas_brbs.was_idle_for_at_least(datetime.timedelta(minutes=1), "nsfw_monika_brb_masturbate"):
            m 1hubfb "Welcome back, [player]."
            m 2hubfb "That was fast! Ehehe~"
            m 2eub "I hope you didn't strain yourself..."
            m 1eua "[wb_quip]"
        else:
            m 1hubfb "Oh? Welcome back, [player]."
            m 2eua "Did you change your mind?"
            m 2eua "[wb_quip]"

    elif mas_isMoniNormal(higher=True):
        m 1hubfb "Welcome back, [player]."
        m 6euafb "Now that you're done with...{i}that{/i}..."
        m 1eua "[wb_quip]"

    else:
        call mas_brb_generic_low_aff_callback

    return
