init -990 python in mas_submod_utils:
    Submod(
        author="NickWildish",
        name="NSFW Submod",
        description="A submod that is 'not safe for work'.",
        version="0.0.3",
        dependencies={},
        settings_pane=None,
        version_updates={}
    )

screen nsfw_submod_screen():
    python:
        submods_screen = store.renpy.get_screen("submods", "screens")

        if submods_screen:
            _tooltip = submods_screen.scope.get("tooltip", None)
        else:
            _tooltip = None
    
    vbox:
        box_wrap False
        xfill True
        xmaximum 1000
        
        hbox:
            style_prefix "check"
            box_wrap False

            if _tooltip:
                textbutton _("NSFW dud setting #1"):
                    action NullAction()
                    hovered SetField(_tooltip, "value", "This is an NSFW submod button which is inactive")
                    unhovered SetField(_tooltip, "value", _tooltip.default())

            else:
                textbutton _("NSFW dud setting #1"):
                    action NullAction()

init python in mas_nsfw:
    import store
    import datetime

    def six_hour_check():
    #RETURNS
    #    - True if the player has been away for six hours AND the topic hasn't been used for six hours
    #    - False if the player has not been away for six hours OR the topic hasn't been used for six hours
        time_away = store.mas_getAbsenceLength()
        time_away_in_hours = divmod(time_away.total_seconds(), 3600)

        return time_away_in_hours >= 6 and mas_getEVL_last_seen("monika_getnude") >= 6

    def canShow_underwear():
    #RETURNS:
    #    - True if the player has seen 'monika_getnude' topic AND risque is allowed
    #    - False if the player has not seen 'monika_getnude' topic OR risque is not allowed
        return mas_getEV("monika_getnude").shown_count >= 1 and mas_canShowRisque()

    def canShow_birthdaySuit():
    #RETURNS:
    #    - True if the player has seen 'monika_getnude' topic twice AND risque is allowed
    #    - False if the player has not seen 'monika_getnude' topic twice OR risque is not allowed
        return mas_SELisUnlocked(mas_clothes_underwear) and mas_canShowRisque()