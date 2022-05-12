init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_shaving",
            category=['sex'],
            prompt="Shaving",
            conditional="renpy.seen_label('monika_nsfwmodinstall')",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_shaving:
    m 1esc "Hey [player]..."
    m 3eub "I want to ask you something."
    m 3lusdlb "It's about my body.."
    extend 2lusdlb "Do you like it to be shaved down there?.."
    $ _history_list.pop()
    menu:
        m "Do you like it to be shaved down there?..{fast}"

        "Yes.":
            m 1hua "That's to be expected."
            m 1eua "Most partners maintain themselves down there in one way or another."
            m 3wuo "Most girls certainly do!"
            m 5tuu "We just want to make sure we're ready for you~"
            m 5tuu "I certainly will."
            m 5hub "Ahaha!.."

        "I don't mind.":
            m 1wuo "Really?!"
            m 5hub "That's surprising!"
            m 5dub "Most partners prefer their loved ones to be shaved."
            m 3eua "It feels nice to know your partner likes the way you look no matter what."
            m 3fub "I'll have to stop shaving so much."
            m 1mub "It'll take a lot less time to shower now too!"
            m 5hub "Ahaha!.."

    m 1eua "I think you know how I feel."
    m 1wub "However you present yourself.."
    m 1hub "Shaven or natural.."
    m 1nub "I'll always love you!"

    return love
