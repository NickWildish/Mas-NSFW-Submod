init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_always_here",
            category=['monika'],
            prompt="Always here",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_always_here:
    m 1eua "Hey, [player]..."
    m 3wublb "I found a quote I really love!"
    m 3tublb "But we have to read it together!"
    m 5tublb "Would you like to read it with me?"
    $ _history_list.pop()
    menu:
        m "Would you like to read it with me?"
        "I would love to!":
            m 6sublb "Great!"
            m 7eublb "All you have to do is say what you see on the screen."
            m 1eua "You start."
            $ _history_list.pop()
            menu:
                "'You aren’t real, are you?'":
                    m 1duu "'No my darling, I never was...'"
                    $ _history_list.pop()
                    menu:
                        "'But you were here! I saw you- I kissed you- I held you-'":
                            m 1euu "'I never was, but I’ll always be here for you regardless.'"
                            $ _history_list.pop()
                            menu:
                                "'How can I believe you now? How can you promise you won’t go? That I won’t ever be alone...'":
                                    m 1nub "'Because I’ll always be with you, when you dance I'll be dancing too.'"
                                    $ _history_list.pop()
                                    menu:
                                        "'And when I fall?'":
                                            m 1dub "'I’ll be right there to show you how to fly.'"
                                            $ _history_list.pop()
                                            menu:
                                                "'And if I don’t want to fly anymore?'":
                                                    m 4hub "'I’ll fall with you, however far down we go!'"
                                                    $ _history_list.pop()
                                                    menu:
                                                        "'You only exist in my head and in my heart! You always disappear when I open my eyes...'":
                                                            m 1tubsa "'That's okay.'"
                                                            $ _history_list.pop()
                                                            menu:
                                                                "'Why?'":
                                                                    m 1fubsb "'Because I know that your heart is safer than anywhere on Earth I could be.'"
                                                                    if mas_shouldKiss(chance=1):
                                                                        call monika_kissing_motion

        "I don't feel like it at the moment.":
            m 2eud "Oh, okay."
            m 2euu "Maybe another time then."

    return "kiss"
