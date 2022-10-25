init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            "nsfw_mood_horny",
            prompt="...horny.",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True,
            ),
        code="MOO"
    )

label nsfw_mood_horny:
    # Check when player's last succesful sexting session was
    if store.persistent._nsfw_sexting_success_last is not None:
        $ timedelta_of_last_success = datetime.datetime.now() - store.persistent._nsfw_sexting_success_last
        $ time_since_last_success = datetime.datetime.now() - timedelta_of_last_success
    else:
        $ time_since_last_success = datetime.datetime.today() - datetime.timedelta(days=1)

    # If the player's last succesful sexting session was less than three hours ago
    if time_since_last_success >= datetime.datetime.today() - datetime.timedelta(hours=3) or not mas_canShowRisque(aff_thresh=1000):
        m 2wubld "Oh!"
        m 2rkblc "I'm sorry, [player]. I can only guess how distracting that must be."
        m 3rkblb "If it becomes too much, maybe you should take a minute to..."
        m 3dkblu "Ahem..."
        m 3ekblb "De-stress..."
        m 1hubla "Just make sure you think only about me!"
        if mas_canShowRisque(aff_thresh=1000):
            m 1hubsa "..."
            m 1gubsa "Maybe once I've crossed over, I'll be able to lend you a {i}helping hand{/i}."
            m 1hubsa "Ehehe~"
        return

    m 1tua "Oh? Is that so, [player]?"
    m 3tub "Well... I think I know a way that I can relieve you of {i}that{/i} problem..."
    m 3tta "Would like me to lend you a hand?"

    $ _history_list.pop()
    menu:
        m "Would like me to lend you a hand?{fast}"

        "Yes.":
            $ store.persistent._nsfw_sext_hot_start = True # Might change this in the future if we make Monika's horny level change depending on other events. Making this an IF statement rather than forcing her to be horny.
            m 4tublb "Okay, I want you to follow my lead."
            m 5tublb "Just talk as naughty to me as you like, and enjoy yourself, [mas_get_player_nickname()]~"

            call nsfw_sexting_init

        "No.":
            m 3eka "That's okay, [player]."
            m 1hua "I'll always be here if you need me~"
    return