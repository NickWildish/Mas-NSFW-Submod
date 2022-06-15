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
