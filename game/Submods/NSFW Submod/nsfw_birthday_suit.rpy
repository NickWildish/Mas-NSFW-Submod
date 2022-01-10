init -1 python:
    import store
    ### BIRTHDAY SUIT (NAKED)
    ## birthdaysuit
    # Monika without any clothes
    # thanks u/DABnoREGRET
    mas_clothes_birthday_suit = MASClothes(
        "birthdaysuit",
        "birthdaysuit",
        MASPoseMap(
            default=True,
            user_reg_for_1=True,
        ),
        stay_on_start=False,
        ex_props={
            store.mas_sprites.EXP_C_LING: True,
        },
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
            "AH! Where have my clothes gone?!" #temp
        ]
    )

    ### PLAIN UNDERWEAR (WHITE)
    ## plain_underwear_white
    # Monika's plain white underwear
    # thanks to an anonymous donator
    mas_clothes_underwear_white = MASClothes(
        "plain_underwear_white",
        "plain_underwear_white",
        MASPoseMap(
            default=True,
            user_reg_for_1=True,
        ),
        stay_on_start=False,
        ex_props={
            store.mas_sprites.EXP_C_LING: True,
        },
        pose_arms=MASPoseArms({}, def_base=False)
    )
    store.mas_sprites.init_clothes(mas_clothes_underwear_white)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_underwear_white,
        "Plain Underwear (White)",
        "plain_underwear_white",
        "clothes",
        visible_when_locked=True,
        select_dlg=[
            "AH! Where have my clothes gone?!" #temp
        ]
    )

    ### PLAIN UNDERWEAR (BLACK)
    ## plain_underwear_black
    # Monika's plain black underwear
    # thanks to an anonymous donator
    mas_clothes_underwear_black = MASClothes(
        "plain_underwear_black",
        "plain_underwear_black",
        MASPoseMap(
            default=True,
            user_reg_for_1=True,
        ),
        stay_on_start=False,
        ex_props={
            store.mas_sprites.EXP_C_LING: True,
        },
        pose_arms=MASPoseArms({}, def_base=False)
    )
    store.mas_sprites.init_clothes(mas_clothes_underwear_black)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_underwear_black,
        "Plain Underwear (Black)",
        "plain_underwear_black",
        "clothes",
        visible_when_locked=True,
        select_dlg=[
            "AH! Where have my clothes gone?!" #temp
        ]
    )

    ### PLAIN UNDERWEAR (PINK)
    ## plain_underwear_pink
    # Monika's plain pink underwear
    # thanks to an anonymous donator
    mas_clothes_underwear_pink = MASClothes(
        "plain_underwear_pink",
        "plain_underwear_pink",
        MASPoseMap(
            default=True,
            user_reg_for_1=True,
        ),
        stay_on_start=False,
        ex_props={
            store.mas_sprites.EXP_C_LING: True,
        },
        pose_arms=MASPoseArms({}, def_base=False)
    )
    store.mas_sprites.init_clothes(mas_clothes_underwear_pink)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_underwear_pink,
        "Plain Underwear (Pink)",
        "plain_underwear_pink",
        "clothes",
        visible_when_locked=True,
        select_dlg=[
            "AH! Where have my clothes gone?!" #temp
        ]
    )