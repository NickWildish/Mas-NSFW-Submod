init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            eventlabel="nsfw_mood_horny",
            prompt="...horny.",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        code="MOO"
    )

label player_feel_horny:
    if mas_getEVL_shown_count(nsfw_player_sextingsession) != 0 and mas_canShowRisque(aff_thresh=1000):
        m 1cud "Oh? Is that so, [player]..."
        m 1cud "Well, I certainly would not mind helping you out."
        m 1cud "We could have a quick sexting session."
        m 1cud "After all, I wouldn't want you to be having fun all by yourself~"
        m 1cud "So, what do you say?"

        $ _history_list.pop()
        menu:
            m "So, what do you say?{fast}"

            "Sure, [m_name].":
                m 1cud "Mmm~ Glad to hear it."
                call nsfw_sexting_main

            "Maybe later...":
                m 1cud "Naww~ Okay..."
                m 1cud "I'll be waiting, [mas_get_player_nickname().]"

    elif mas_isMoniLove() and mas_canshowRisque(aff_thresh=1000):
        m 1cud "You're horny?"
        m 1cud "You really have gotten bold, haven't you [player]?"
        m 1cud "Ahaha! I'm just teasing you~"
        m 1cud "In all seriousness though, if you want..."
        m 1cud "I wouldn't mind helping you."

        if mas_getEVL_shown_count(nsfw_monika_sexting) != 0:
            m 1cud "We could try that sexting idea we talked about earlier..."
        else:
            m 1cud "We could try this sexting idea I've been thinking about..."
            m 1cud "Basically, we take turns flirting and see where things go~"

        m 1cud "Would you like that, [player]?"

        $ _history_list.pop()
        menu:
            m "Would you like that, [player]?{fast}"

            "Sure, [m_name].":
                m 1cud "Mmm~ Glad to hear it."
                call nsfw_sexting_main

            "Maybe later...":
                m 1cud "Naww~ Okay..."
                m 1cud "I'll be waiting, [mas_get_player_nickname().]"

    elif mas_isMoniAff():
        m 1cud "You're h-{w=0.3}horny?!"
        m 1cud "I mean... I guess we're approaching the part in our relationship where we start to talk about this stuff."
        m 1cud "Well.. Umm... I w-{w=0.3}wish I could help you with that."
        m 1cud "But I think if you're feeling that way it might be worth..."
        m 1cud "P-{w=0.3}playing with yourself to..."
        m 1cud "..."
        m 1cud "T-this is too embarassing, I'm sorry."
        m 1cud "Maybe once we're futher in this relationship..."
    elif mas_isMoniNormal(higher=True):
        mas_loseAffection()
        m 1cud "Woah, [player]!"
        m 1cud "We're {i}way{/i} too early in the relationship to be saying stuff like that..."
        m 1cud "Let's keep things PG for now... okay?"
    elif mas_isMoniDis(higher=True):
        mas_loseAffection()
        m 1cud "..."
        m 1cud "I can't believe you..."
        return "quit"
    return