init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_nsfw_seductive",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None),
            conditional="mas_canShowRisque()"
        ),
        code="GRE"
    )

label greeting_nsfw_seductive:
        # get how many times this greeting has been shown, so she can get better over time
    $ ev = mas_getEV("greeting_nsfw_seductive")
        # get if it is daytime or nighttime, simple as
    $ tod = "day" if mas_globals.time_of_day_4state != "night" else "night"
    m 1eubfb "Why, {i}hello there{/i}, [player]~"
    if ev.shown_count ==0:
        m 1eubfb "You look positively {i}sexy{/i} to[tod]."
        m 1fkbssdla "Why, I could just... Uhm... Take your clothes off...? And..."
        m 2hub "Ahaha! Sorry, [player], I need to practice at this. I'll get it right next time."
    else:
        m 1tubsu "I thought things must be getting hotter, and now I know why. It's because you were nearby."
        m 6tkbsa "You're looking positively wonderful to[tod], [mas_get_player_nickname()]..."
        m 1tubsa "But I think you'd look even better with your clothes off."
        m 4tubsu "Let's have a good time together. Ehehe~"
    return
