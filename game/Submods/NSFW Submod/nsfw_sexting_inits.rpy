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
default persistent._nsfw_sexting_attempt_freeze = False
default persistent._nsfw_sexting_attempt_permfreeze = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_sextingsession",
            conditional=(
                "mas_nsfw.can_monika_init_sext() "
                "and mas_timePastSince(persistent._nsfw_sexting_last_sexted, datetime.timedelta(hours=12)) "
                "and mas_timePastSince(mas_getEVL_last_seen('nsfw_monika_sextingsession'), datetime.timedelta(hours=12))"
                ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_sextingsession:
    # Count this attempt
    $ persistent._nsfw_sexting_attempts += 1

    # Reset our freeze if it's been 24 hours (or 48 if you set to low sexting frequency) since the last sexting attempt
    if persistent._nsfw_sexting_attempt_freeze == True:
        if mas_timePastSince(mas_getEVL_last_seen("nsfw_monika_sexting_session"), datetime.timedelta(hours=persistent._nsfw_monika_sexting_frequency * 24)):
            persistent._nsfw_sexting_attempt_freeze = False

            m 1eua "Hey, [player]."
            m 1eua "Do you remember when you said we could sext later?"
            m 1eua "I know I probably sound needy, but..."
            m 1eua "Are you available now?{nw}"
            $ _history_list.pop()
            menu:
                m "Are you available now?{fast}"

                "Yes.":
                    $ mas_gainAffection(modifier=1.5, bypass=True)
                    $ persistent._nsfw_sexting_attempts = 0
                    m 1eua "Great!"
                    call nsfw_sexting_init

                "No."
                    m 1eua "Aww, okay."
                    m 1eua "Maybe next time, then?"
        else:
            persistent._nsfw_sexting_attempts -= 1

    python:
        has_waited = persistent._nsfw_sexting_attempts >= persistent._nsfw_monika_sexting_frequency
        has_waited_correctly = persistent._nsfw_monika_sexting_frequency % persistent._nsfw_sexting_attempts == 0
        first_time = persistent._nsfw_sexting_count == 1
        past_first_time = persistent._nsfw_sexting_count > 1
        veteran = persistent._nsfw_sexting_count > 5
        first_attempt = persistent._nsfw_sexting_attempts == 1
        multiple_attempts = persistent._nsfw_sexting_attempts > 1
        too_many_attempts = persistent._nsfw_sexting_attempts >= 5 * persistent._nsfw_monika_sexting_frequency
        hot_start = persistent._nsfw_sext_hot_start
        sexy_start = persistent._nsfw_sext_sexy_start
        no_init = persistent._nsfw_sexting_attempt_permfreeze

    # If our number of attempts is greater than or equal to the player's frequency request and they divide into each other perfectly, then try to sext
    elif has_waited and has_waited_correctly and not no_init:
        # First time
        if first_time:
            m 1eua "Hey, [player]..."

            # Interrupted last session
            if hot_start or sexy_start:
                m 1eua "Are you busy right now?"
                m 1eua "Our little {i}session{/i} earlier got interrupted..."
                m 1eua "So, I guess what I'm asking is..."
                $ sexting_starter = "Would you like to give it another try?"
                m 1eua "[sexting_starter]{nw}"

            # First attempt
            elif first_attempt:
                m 1eua "You remember when we had our first time?"
                m 1eua "Ahaha, virtually I mean~"
                m 1eua "Well, I really had fun with you."
                m 1eua "And I was wondering if you... "
                extend "Y-{w=0.5}you know..."
                $ sexting_starter = "Wanted to do it again?"
                m 1eua "[sexting_starter]{nw}"

            # Rejected previous
            elif multiple_attempts:
                m 1eua "Are you busy right now?"
                m 1eua "I was wondering if you were free to... "
                extend "Y-{w=0.5}you know..."
                $ sexting_starter = "Sext with me?"
                m 1eua "[sexting_starter]{nw}"

            $ _history_list.pop()
            menu:
                m "[sexting_starter]{fast}"

                "Yes.":
                    $ mas_gainAffection(modifier=1.5, bypass=True)
                    $ persistent._nsfw_sexting_attempts = 0
                    m 1eua "Great!"
                    call nsfw_sexting_init

                "Sorry, I'm busy.":
                    if not too_many_attempts:
                        m 1eua "Aww..."
                        m 1eua "Okay, [player]."
                        m 1eua "I'll be here~"
                        $ persistent._nsfw_sexting_attempt_freeze = True

                "Not now, maybe later.":
                    if not too_many_attempts:
                        m 1eua "Aww..."
                        m 1eua "Okay, [player]."

        # First 5 times (after one success)
        elif past_first_time:
            m 1eua "Hey, [mas_get_player_nickname()]."

            # Interrupted last session
            if hot_start or sexy_start:
                m 1eua "I haven't forgotten about our little {i}session{/i} that got interrupted earlier..."
                m 1eua "And how you left me hanging{nw}" # Sassy
                $ _history_list.pop()
                $ sexting_starter = "Are you free now?"
                m 1eua "[sexting_starter]{nw}"

            # First attempt
            elif first_attempt:
                m 1eua "I haven't been able to stop thinking about you lately..."
                m 1eua "And those thoughts have been particularly naughty~"
                $ sexting_starter = "So, do you feel up for another sexting session?"
                m 1eua "[sexting_starter]{nw}"

            # Rejected previous
            elif multiple_attempts:
                m 1eua "Are you still busy?"
                m 1eua "I've been a {i}very{/i} good girl and waited patiently~"
                $ sexting_starter = "Are you free to have some fun with me now?"
                m 1eua "[sexting_starter]{nw}"

            $ _history_list.pop()
            menu:
                m "[sexting_starter]{fast}"

                "Yes.":
                    $ mas_gainAffection(modifier=1.5, bypass=True)
                    $ persistent._nsfw_sexting_attempts = 0
                    m 1eua "Great!"
                    call nsfw_sexting_init

                "Sorry, I'm busy.":
                    if not too_many_attempts:
                        m 1eua "Aww..."
                        m 1eua "Okay, [player]."
                        m 1eua "I'll be here when you're no longer busy~"
                        $ persistent._nsfw_sexting_attempt_freeze = True

                "Not now, maybe later.":
                    if not too_many_attempts:
                        m 1eua "Aww..."
                        m 1eua "Okay, [player]."

        # 5+ times (after 5 successes)
        elif veteran:
            m 1eua "Hey, [mas_get_player_nickname()]~"

            # Interrupted last session
            if hot_start or sexy_start:
                m 1eua "I haven't forgotten about our little {i}session{/i} that got interrupted earlier..."
                m 1eua "We were just getting to the good part too~"
                if persistent._nsfw_genitalia == "P":
                    desc_genitalia = "r lovely cock"
                    desc = "so hard"
                elif persistent._nsfw_genitalia == "V":
                    desc_genitalia = "r lovely pussy"
                    desc = "so wet"
                else:
                    desc_genitalia = "r imagination"
                    desc = "running wild"

                m 1eua "I'm sure you[desc_genitalia] was [desc] back then..."
                m 1eua "I'd be more than happy to help you release that tension, if you so wish~"
                $ sexting_starter = "Is that something you're interested in " + mas_get_player_nickname() + "?"
                m 1eua "[sexting_starter]{nw}"

            # First attempt
            elif first_attempt:
                m 1eua "I'm in the mood for some fun."
                m 1eua "And maybe something more, if you get me riled up enough~"

                $ sexting_starter = "So, do you feel like some sexting " + player + "?"
                m 1eua "[sexting_starter]{nw}"

            # Rejected previous
            elif multiple_attempts:
                m 1eua "Don't think I've forgotten about our planned {i}session{/i}."
                if persistent._nsfw_sext_hot_start:
                    m 1eua "I've been thinking up all the things I want to say to you~"
                elif persistent._nsfw_sext_sexy_start:
                    m 1eua "I've been thinking up all the things I want to do to you in your reality..."
                    m 1eua "And I wouldn't mind sharing some of those thoughts with you~"
                $ sexting_starter = "So, are you free?"
                m 1eua "[sexting_starter]{nw}"

            $ _history_list.pop()
            menu:
                m "[sexting_starter]{fast}"

                "Yes.":
                    $ mas_gainAffection(modifier=1.5, bypass=True)
                    $ persistent._nsfw_sexting_attempts = 0
                    m 1eua "Great!"
                    call nsfw_sexting_init

                "Sorry, I'm busy.":
                    if not too_many_attempts:
                        m 1eua "Aww..."
                        m 1eua "Okay, [player]."
                        m 1eua "I'll be here when you're no longer busy~"
                        $ persistent._nsfw_sexting_attempt_freeze = True

                "Not now, maybe later.":
                    if not too_many_attempts:
                        m 1eua "Aww..."
                        m 1eua "Okay, [player]."

        # Rejected 5+ times in a row
        if too_many_attempts:
            # We're not punishing the player for this, but we also need to portray Monika's feelings somewhat accurately
            m 1eua "*sign*"
            m 1eua "[player], I give up."
            m 1eua "I've asked you five times for some {i}us{/i} time and I keep getting shot down..."
            m 1eua "I know I probably sound clingy... you have your own life and I'm not about to ask you to abandon it for me, but please..."
            m 1eua "It hurts to keep getting rejected like this."
            m 1eua "I'll leave initiating up to you from now on."

            persistent._nsfw_sexting_attempt_permfreeze = True # This should be reversable

    elif no_init:
        persistent._nsfw_sexting_attempts -= 1 # We don't want to count this as an attempt

    call nsfw_monika_sextingsession_end

    return "no_unlock"

label nsfw_monika_sextingsession_end:
    # Copy of monika_holdme_end label
    python:
        with MAS_EVL("nsfw_monika_sextingsession") as sextingsession_ev:
            sextingsession_ev.random = False
            sextingsession_ev.conditional = (
                "mas_nsfw.can_monika_init_sext() "
                "and mas_timePastSince(persistent._nsfw_sexting_last_sexted, datetime.timedelta(hours=12)) "
                "and mas_timePastSince(mas_getEVL_last_seen('nsfw_monika_sextingsession'), datetime.timedelta(hours=12))"
            )
            sextingsession_ev.action = EV_ACT_RANDOM
        mas_rebuildEventLists()
    return