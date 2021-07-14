init -1 python:
    import store
    ### BIRTHDAY SUIT (NAKED)
    ## birthdaysuit
    # Monika naked
    # thanks u/DABnoREGRET
    mas_clothes_birthday_suit = MASClothes(
        "birthdaysuit",
        "birthdaysuit",
        MASPoseMap(
            default=True,
            user_reg_for_1=True,
        ),
        stay_on_start=False,
        pose_arms=MASPoseArms({}, def_base=False)
    )
    store.mas_sprites.init_clothes(mas_clothes_birthday_suit)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_birthday_suit,
        "Birthday Suit",
        "birthdaysuit",
        "clothes",
        visible_when_locked=True,
        select_dlg=[
            "AH! Where have my clothes gone?!"
        ]
    )