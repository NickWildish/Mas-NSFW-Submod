init 5 python:
    addEvent(Event(persistent._mas_mood_database,"nsfw_mood_horny",prompt="...horny.",category=[store.mas_moods.TYPE_GOOD],unlocked=True),code="MOO")

label mas_mood_horny:
    m 1eua "Oh? Is that so, [player]?"
    m 1eua "Oh...wait..."
    m 1eua "Sorry [player], it looks like the developer is getting tired and wants to get some sleep."
    m 1eua "Guess we're going to have to wait and see what he has planned for this topic, huh?"
    m 1eua "Ehehe~" # Sorry, I have a really good idea and don't want to wait
    return