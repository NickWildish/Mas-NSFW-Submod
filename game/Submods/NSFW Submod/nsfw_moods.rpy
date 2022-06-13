init 5 python:
    addEvent(Event(persistent._mas_mood_database,"nsfw_mood_horny",prompt="...horny.",category=[store.mas_moods.TYPE_NEUTRAL],unlocked=True,),code="MOO")

label nsfw_mood_horny:
    # Check when player's last succesful sexting session was
    if store.persistent.nsfw_sexting_success_last is not None:
        $ timedelta_of_last_success = datetime.datetime.now() - store.persistent.nsfw_sexting_success_last
        $ time_since_last_success = datetime.datetime.now() - timedelta_of_last_success
    else:
        $ time_since_last_success = datetime.datetime.today() - datetime.timedelta(days=1)

    # If the player's last succesful sexting session was less than three hours ago
    if time_since_last_success >= datetime.datetime.today() - datetime.timedelta(hours=3):
        m 1eua "Oh!"
        m 1eua "I'm sorry, [player]. I can only guess how distracting that must be."
        m 1eua "If it becomes too much, maybe you should take a minute to..."
        m 1eua "Ahem..."
        m 1eua "De-stress..."
        m 1eua "Just make sure you're only thinking about me!"
        m 1eua "..."
        m 1eua "Maybe once I've crossed over, I'll be able to lend you a {i}helping hand{/i}."
        m 1eua "Ehehe~"

    m 1eua "Oh? Is that so, [player]?"
    m 1eua "Well...I think I know a way that we can relieve you of {i}that{/i} problem..."
    m 1eua "We could try "
    return