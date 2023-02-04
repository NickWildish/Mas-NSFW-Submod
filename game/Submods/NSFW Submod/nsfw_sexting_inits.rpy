# PLAYER

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_player_sextingsession",
            category=['sex'],
            prompt="Do you want to sext?",
            conditional=(
                "mas_canShowRisque(aff_thresh=1000) "
                "and store.mas_getEVL_shown_count('nsfw_monika_sexting') >= 1"
                ),
            action=EV_ACT_POOL,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_player_sextingsession:
    # Check when player's last succesful sexting session was
    if store.persistent._nsfw_sexting_success_last is not None:
        $ timedelta_of_last_success = datetime.datetime.now() - store.persistent._nsfw_sexting_success_last
        $ time_since_last_success = datetime.datetime.now() - timedelta_of_last_success
    else:
        $ time_since_last_success = datetime.datetime.today() - datetime.timedelta(days=1)

    # If the player's last succesful sexting session was less than three hours ago
    if time_since_last_success >= datetime.datetime.today() - datetime.timedelta(hours=3):
        m 1eka "I'm sorry [player], but I'm still tired from the last time we sexted."
        m 3eka "Could you give me a little more time, please?"
        m 3hub "I love you~"
        return "love"

    m 1hua "Sure!"

    call nsfw_sexting_init

    return

# MONIKA

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