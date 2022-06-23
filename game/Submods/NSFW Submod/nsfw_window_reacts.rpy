init 1 python:
    config.label_overrides["mas_wrs_r34m"] = "nsfw_wrs_r34"

label nsfw_wrs_r34:
    python:

        if mas_isMoniLove(higher=True): #1000 aff
            mas_display_notif(m_name,
                [
                    "Hey, [player]...try not to spend too long doing that, okay? ;)",
                    "Hey, [player]...don't spend too long doing that, okay? ;)",
                    "Hey, [player]...what are you looking at, exactly? ;)",
                    "Hey, [player]...just me, remember? Just me. ;)"
                ],'Window Reactions'
            )
        else:
            mas_display_notif(m_name,
                [
                    "Hey, [player]...what are you looking at?",
                    "Hey, [player]...what are you doing?"
                ],'Window Reactions'
            )

        choice = random.randint(1,10)

        if choice == 1 and mas_isMoniNormal(higher=True):
            queueEvent('monika_nsfw')

        elif choice == 2 and mas_isMoniAff(higher=True):
            queueEvent('monika_pleasure')

        else:
            if mas_isMoniEnamored(higher=True):
                if choice < 4:
                    exp_to_force = "1rsbssdlu"
                elif choice < 7:
                    exp_to_force = "2tuu"
                else:
                    exp_to_force = "2ttu"
            else:
                if choice < 4:
                    exp_to_force = "1rksdlc"
                elif choice < 7:
                    exp_to_force = "2rssdlc"
                else:
                    exp_to_force = "2tssdlc"

        mas_moni_idle_disp.force_by_code(exp_to_force, duration=10)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_nsfw_wrs_spnati",
            category=["Strip Poker Night at the Inventory"],
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_nsfw_wrs_spnati:
    # Make a list of possible notif quips for this
    python:
        if mas_isMoniLove(higher=True): #1000 aff
            mas_display_notif(m_name,
                [
                    "Did you know that there's a version of me in this game? You could play with me! ;)",
                    "Apparently all the characters in this game were made by people as a hobby. Interesting...",
                    "Gosh, there are so many characters...but you only need me, right? ;)",
                    "Strip poker with five card draw...What a silly game! ;)"
                ],'Window Reactions'
            )
            exp_to_force = "1tsbsu"
        else:
            mas_display_notif(m_name,
                [
                    "Strip poker, huh...?",
                    "What is this? Strip poker with fictional characters?"
                ],'Window Reactions'
            )
            exp_to_force = "1etblsdlc"
            # force her sprite to do a specific expression
        mas_moni_idle_disp.force_by_code(exp_to_force, duration=10)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_nsfw_wrs_pornhub",
            category=['Pornhub|XVIDEOS|xHamster|M-Hentai|nHentai'], # just listing some of the biggest ones
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_nsfw_wrs_pornhub:
    # this can be expanded later if someone wants to tackle a "watch porn together" topic
    python:
        mas_display_notif(m_name,
            [
                "[player]...really? Hmph.",
                "[player], I'm right here you know. Hmph.",
                "[player]...I'm sitting right here...",
                "Having fun without me?"
            ],'Window Reactions'
        )

        exp_to_force = "1gfbfsdlc"
        # force her sprite to do a specific expression
        mas_moni_idle_disp.force_by_code(exp_to_force, duration=10)

    return
