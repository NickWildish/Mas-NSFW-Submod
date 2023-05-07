label nickwildish_nsfw_submod_v1_0_1(version="v_1_0_1"):
    return

label nickwildish_nsfw_submod_v1_0_2(version="v_1_0_2"):
    return

label nickwildish_nsfw_submod_v1_0_3(version="v_1_0_3"):
    return

label nickwildish_nsfw_submod_v1_1_0(version="v_1_1_0"):
    mas_setEVLPropValues(
        "nsfw_monika_sexualpast",
        prompt = "[player]'s sexual past",
        conditional="mas_canShowRisque(aff_thresh=400)"
    )
    mas_setEVLPropValues(
        "nsfw_monika_safesex",
        random=False,
        conditional="mas_canShowRisque(aff_thresh=400)",
        action=EV_ACT_RANDOM
    )
    mas_setEVLPropValues(
        "nsfw_monika_fetish",
        random=False,
        conditional="mas_canShowRisque(aff_thresh=400)",
        action=EV_ACT_RANDOM
    )
    mas_setEVLPropValues(
        "nsfw_monika_sexting",
        random=False,
        conditional="mas_canShowRisque(aff_thresh=400)",
        action=EV_ACT_RANDOM
    )
    mas_setEVLPropValues(
        "nsfw_monika_gettingnude",
        random=False,
        conditional="mas_canShowRisque(aff_thresh=400)",
        action=EV_ACT_RANDOM
    )
    mas_setEVLPropValues(
        "nsfw_monika_shaving",
        random=False,
        conditional="mas_canShowRisque(aff_thresh=400)",
        action=EV_ACT_RANDOM
    )
    mas_setEVLPropValues(
        "nsfw_monika_judging_sexual_desires",
        random=False,
        conditional="mas_canShowRisque(aff_thresh=400)",
        action=EV_ACT_RANDOM
    )
    mas_setEVLPropValues(
        "nsfw_player_sextingsession",
        pool=False,
        conditional="mas_canShowRisque(aff_thresh=1000) and store.mas_getEVL_shown_count('nsfw_monika_sexting') >= 1",
        action=EV_ACT_POOL,
    )
    return

label nickwildish_nsfw_submod_v1_1_1(version="v_1_1_1"):
    mas_setEVLPropValues(
        "monika_brb_nsfw_masturbate",
        eventlabel = "nsfw_monika_brb_masturbate"
    )

    mas_setEVLPropValues(
        "nsfw_monika_masturbation_benefits",
        conditional="mas_canShowRisque(aff_thresh=400) and store.mas_getEVL_shown_count('nsfw_monika_brb_masturbate')"
    )
    return

label nickwildish_nsfw_submod_v1_1_2(version="v_1_1_2"):
    return

label nickwildish_nsfw_submod_v1_2_0(version="v_1_2_0"):
    return

label nickwildish_nsfw_submod_v1_2_2(version="v_1_2_2"):
    return

label nickwildish_nsfw_submod_v1_2_3(version="v_1_2_3"):
    return

label nickwildish_nsfw_submod_v1_2_4(version="v_1_2_4"):
    return

label nickwildish_nsfw_submod_v1_2_5(version="v_1_2_5"):
    return

label nickwildish_nsfw_submod_v1_2_6(version="v_1_2_6"):
    return

label nickwildish_nsfw_submod_v1_2_7(version="v_1_2_7"):
    return

label nickwildish_nsfw_submod_v1_3_0(version="v_1_3_0"):
    mas_setEVLPropValues(
        "nsfw_player_sextingsession",
        pool=True,
        unlocked=False,
        conditional=(
        "mas_canShowRisque(aff_thresh=1000) "
        "and store.mas_getEVL_shown_count('nsfw_monika_sexting') >= 1"
        ),
        action=EV_ACT_UNLOCK
    )
    return