init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fetishes",
            category=['sex'],
            prompt="Fetishes",
            conditional="renpy.seen_label('monika_nsfwmodinstall')",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_fetishes:
    m 2efc "I don't understand why so many people have problems with fetishes!"
    m 3efd "People take it too seriously."
    m 3efd "With sexuality being a taboo on a good day-"
    m 4efd "Deviations are always observed with judgemental eyes."
    m 1eud "They take that small, personal aspect of one's life and put a spotlight on it."
    m 1eud "and under that spotlight, sexuality casts an ugly shadow.."
    m 1tud "and society frowns upon it.."
    m 2hsc "..."
    m 2fuu "But there are those who understand that it is a wonderful aspect of the human experience."
    m 2hubsa "Wonderful.."
    m 2hubsa "Exciting.."
    m 5fubsa "Intimate.."
    m 5dubfa "..."
    m 2eubfd "[player]..."
    m 2eubfd "Please share your desires with me."
    m 3eubfa "Honest communication is the most important thing in a relationship after all!"
    m 3subfb "I don't judge! No matter how out there it is!"
    m 5gubfa "I should know after all.."
    m 3eubfb "We are all a bit pervy, in our own special ways!"
    m 3eubfb "You might be thinking.."
    m 6tfbfp "No! I most certainly am not!"
    m 5tubfu "Well.."
    m 5tubfu "Give it some time~"

    return
