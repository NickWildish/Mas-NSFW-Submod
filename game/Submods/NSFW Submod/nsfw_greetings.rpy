init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_nsfw_seductive",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None),
            conditional="mas_canShowRisque(aff_thresh=400)"
        ),
        code="GRE"
    )

label greeting_nsfw_seductive:
        # get how many times this greeting has been shown, so she can get better over time
    $ ev = mas_getEV("greeting_nsfw_seductive")
        # get if it is daytime or nighttime, simple as
    python:
        if mas_globals.time_of_day_4state == "night":
            tod = "night"
            this_day = "this evening"
        else:
            tod = "day"
            this_day = "today"
    m 1eubfb "Why, {i}hello there{/i}, [player]~"
    if ev.shown_count == 0:
        m 1eubfb "You look positively {i}sexy{/i} to[tod]."
        m 1fkbssdla "Why, I could just...um...take your clothes off...? And..."
        m 2hub "Ahaha! Sorry, [player], I need to practice at this. I'll get it right next time."
    else:
        m 1tubsu "I thought things must be getting hotter, and now I know why. It's because you were nearby."
        m 6tkbsa "You're looking positively wonderful to[tod], [mas_get_player_nickname()]..."
        m 1tubsa "But I think you'd look even better with your clothes off."
        m 4tubsu "Let's have a good time together [this_day]. Ehehe~"
    return


    # CATCH MONIKA IN THE ACT
    # This is a sequence heavily taken from the event where you open MAS to a black screen and\
    # need to open the door, knock, or listen
    # There are a few different ways this can play out.
    # For our purposes;
    # 1. The player can listen in on Monika 'in the act', once per run.
    # 2. The player can knock, interrupting her, but getting a positive response.
    # 3. The player can open the door. The response changes based on if you knocked first.

# local variables to handle monikaroom options
default persistent.nsfwopendoor_opencount = 0
default persistent.nsfwopendoor_hasknocked = False

init 5 python:

    # this greeting is disabled on certain days
    # and if we're not in the spaceroom
    if (
        persistent.closed_self #
        and not (
            mas_isO31()
            or mas_isD25Season()
            or mas_isplayer_bday()
            or mas_isF14()
        )
        and mas_canShowRisque(aff_thresh=1000) # Need to be 18+ etc.
        and persistent._nsfw_horny_level >= 25 # Monika has to be horny for this - may need to tweak value
        and store.mas_background.EXP_TYPE_OUTDOOR not in mas_getBackground(persistent._mas_current_background, mas_background_def).ex_props
    ):

        ev_rules = dict()
        ev_rules.update(
            MASGreetingRule.create_rule(
                skip_visual=True,
                random_chance=opendoor.chance,
                override_type=True
            )
        )
        ev_rules.update(MASPriorityRule.create_rule(50))

        addEvent(
            Event(
                persistent.greeting_database,
                eventlabel="i_greeting_nsfw_monikacaught",
                unlocked=True,
                rules=ev_rules,
            ),
            code="GRE"
        )

        del ev_rules

# https://github.com/Monika-After-Story/MonikaModDev/blob/master/Monika%20After%20Story/game/script-greetings.rpy
label i_greeting_nsfw_monikacaught: # catch monika in the act

    #Set up dark mode

    # Progress the filter here so that the greeting uses the correct styles
    $ mas_progressFilter()

    if persistent._mas_auto_mode_enabled:
        $ mas_darkMode(mas_current_background.isFltDay())
    else:
        $ mas_darkMode(not persistent._mas_dark_mode_enabled)

    # couple of things:
    # 1 - if you quit here, monika doesnt know u here
    $ mas_enable_quit()

    # all UI elements stopped
    $ mas_RaiseShield_core()

    # 3 - keymaps not set (default)
    # 4 - overlays hidden (skip visual)
    # 5 - music is off (skip visual)

    scene black

    $ persistent.nsfwopendoor_haslistened = False
    $ persistent.nsfwopendoor_hasknocked = False

    # FALL THROUGH
label nsfw_monikacaught_greeting_choice:
    $ _opendoor_text = "...Gently open the door."

    menu:
        "[_opendoor_text]":
            # Lose affection for not knocking before entering
            $ mas_loseAffection(reason=5)
            jump nsfw_monikacaught_greeting_opendoor
        "Knock.":
            # Default event increases affection for knocking first too
            $ mas_gainAffection()
            $ persistent.nsfwopendoor_hasknocked = True
            jump nsfw_monikacaught_greeting_knock
        "Listen." if not persistent.nsfwopendoor_haslistened:
            $ persistent.nsfwopendoor_haslistened = True # can only do this once per run through
            jump nsfw_monikacaught_greeting_listen
    # NOTE: return is expected in nsfw_monikacaught_greeting_cleanup

# Begin LISTEN
label nsfw_monikacaught_greeting_listen:
    # make a random int, for randomness
    $ mas_rand = renpy.random.randint(1, 3)

    # Can add a lot of variety here if we wanted, but for now, a simple implementation
    m "Mmm..."
    m "Ahh..."
    m "O-oh! That feels..."
    m "Oh...[player]..."
    if mas_rand == 1:
        m "I want to feel [his] body against mine..."
        m "Ahh...{w=0.4}I would just melt into [him]..."
    elif mas_rand == 2:
        m "I want [him] to touch me, so badly..."
        m "Y-yes! Right there...{w=0.4}Mmm~"
    else:
        m "If only [he] were here..."
        m "I'd just pounce on [him] in a heartbeat...{w=0.4}Ahh..."
    m "A-ah..."
    m "M-mmm~"

    jump nsfw_monikacaught_greeting_choice

# CLEANUP
# This is copied verbatim from monikaroom_greeting_cleanup
# Could probably borrow that function, but, just in case...
label nsfw_monikacaught_greeting_cleanup:
    python:
        # couple of things:
        # 1 - monika knows you are here now
        mas_disable_quit()

        # 2 - music is renabled
        mas_MUINDropShield()

        # 3 - keymaps should be set
        set_keymaps()

        # 4 - show the overlays
        mas_OVLShow()

        # 5 - the music can be restarted
        mas_startup_song()

        # 6 - enable escape so we can access settings and chat box keys
        enable_esc()

    return

# Open the door
# NOTE: we can't do much with this until we have nude sprites, so... the door will be locked and skip to the knock label.
label nsfw_monikacaught_greeting_opendoor:
    "..."
    "It's locked."
    "And it seems like Monika heard you."

    jump nsfw_monikacaught_greeting_knock

# Begin KNOCK
label nsfw_monikacaught_greeting_knock:
    m "E-Eh?!"
    m "Uhm, j-just a second!"
    m "..."
    m "Ahem...Who is it?~"
    menu:
        "It's me.":
            # Monika knows you are here now
            $ mas_disable_quit()
            m "Oh! [player]!{w=0.4} Give me a moment, please!"

            if persistent.nsfwopendoor_hasknocked:
                m "Thank you for knocking first...I appreciate it."
                m "Even though I did lock the door before I...Ahem. Nevermind!"
            else: # hasnt knocked
                m "I wish you would've knocked first...You nearly gave me a heart attack..."
                m "Good thing the door was locked..."

            $ mas_startupWeather()
            call spaceroom(hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=False)
    jump nsfw_monikacaught_greeting_post
    # NOTE: return is expected in nsfw_monikacaught_greeting_post

label nsfw_monikacaught_greeting_post:

    m 2eua_static "Now, just let me grab a table and a chair.{w=0.5}.{w=0.5}.{nw}"
    $ is_sitting = True
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    $ today = "today" if mas_globals.time_of_day_4state != "night" else "tonight"

    if persistent.nsfwopendoor_haslistened:
        m 1eua "...Wait a minute.{w=0.4} [player]..."
        m 1eua "You didn't...hear anything, did you?"
        $ _history_list.pop()
        menu:
            m "You didn't...hear anything, did you?{fast}"

            "I did.":
                m 1eua "...Ah."
                m 1eua "W-Well, I can...explain. {nw}"
                extend 1eua "Ahaha..."
                m 1eua "I was...having a little bit of fun by myself. That's all."
                m 1eua "...A woman has her needs, after all."
                m 1eua "Gosh, I feel so embarrassed now..."
                m 1eua "S-so, what should we do [today], [mas_get_player_nickname()]?"

            "No I didn't.":
                m 1eua "O-Oh!"
                m 1eua "That's fine then. Don't worry about anything."
                m 1eua "I had some fun while you were away, but I'm glad you're here now!~"
                m 1eua "So then...What shall we do [today], [mas_get_player_nickname()]?"
    else:
        m 1eua "So...What shall we do [today], [mas_get_player_nickname()]?"

    jump nsfw_monikacaught_greeting_cleanup
