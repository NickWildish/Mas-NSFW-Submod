default persistent._nsfw_sexting_attempts = 0

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_sexting_horny",
            conditional=(
                "mas_nsfw.can_monika_init_sext() "
                "and mas_timePastSince(persistent._nsfw_sexting_last_sexted, datetime.timedelta(hours=12)) "
                "and mas_timePastSince(mas_getEVL_last_seen('nsfw_monika_sexting_horny'), datetime.timedelta(hours=12))"
                ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_sexting_horny:
    # Count this attempt, but only if less than the frequency requested.
    if persistent._nsfw_sexting_attempts >= persistent._nsfw_monika_sexting_frequency:
        $ persistent._nsfw_sexting_attempts = persistent._nsfw_monika_sexting_frequency
    else:
        $ persistent._nsfw_sexting_attempts += 1

    # If our number of attempts matches the player's frequency request, then try to sext
    if persistent._nsfw_sexting_attempts == persistent._nsfw_monika_sexting_frequency:
        m 1eua "Hey, [player]." # TODO: Make proper dialogue for this bit
        m 1eua "I wanna sext with you."
        m 1eua "Are you up for it?"
        $ _history_list.pop()
        menu:
            m "Are you up for it?{fast}"

            "Yes.":
                $ persistent._nsfw_sexting_attempts = 0
                m 1eua "Great!"
                call nsfw_sexting_init

            "No.":
                m 1eua "Aww..."
                m 1eua "Okay, [player]."

    $ mas_flagEVL("nsfw_monika_sexting_horny", "EVE", EV_FLAG_HFRS)

    call nsfw_monika_sexting_horny_end

    return "no_unlock"

label nsfw_monika_sexting_horny_end:
    # Copy of monika_holdme_end label
    python:
        with MAS_EVL("nsfw_monika_sexting_horny") as sexting_horny_ev:
            sexting_horny_ev.random = False
            sexting_horny_ev.conditional = (
                "mas_nsfw.can_monika_init_sext() "
                "and mas_timePastSince(persistent._nsfw_sexting_last_sexted, datetime.timedelta(hours=12)) "
                "and mas_timePastSince(mas_getEVL_last_seen('nsfw_monika_sexting_horny'), datetime.timedelta(hours=12))"
            )
            sexting_horny_ev.action = EV_ACT_RANDOM
        mas_rebuildEventLists()
    return