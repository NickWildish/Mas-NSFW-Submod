label nickwildish_nsfw_submod_v1_0_1(version="v_1_0_1"):
    return

label nickwildish_nsfw_submod_v1_0_2(version="v_1_0_2"):
    return

label nickwildish_nsfw_submod_v1_0_3(version="v_1_0_3"):
    return

label nickwildish_nsfw_submod_v1_1_0(version="v_1_1_0"):
    python:
        store.mas_setEVLPropValues(
            "nsfw_monika_sexualpast",
            prompt = "[player]'s sexual past",
            conditional="mas_canShowRisque(aff_thresh=400)"
        )
        store.mas_setEVLPropValues(
            "nsfw_monika_safesex",
            random=False,
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM
        )
        store.mas_setEVLPropValues(
            "nsfw_monika_fetish",
            random=False,
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM
        )
        store.mas_setEVLPropValues(
            "nsfw_monika_sexting",
            random=False,
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM
        )
        store.mas_setEVLPropValues(
            "nsfw_monika_gettingnude",
            random=False,
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM
        )
        store.mas_setEVLPropValues(
            "nsfw_monika_shaving",
            random=False,
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM
        )
        store.mas_setEVLPropValues(
            "nsfw_monika_judging_sexual_desires",
            random=False,
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM
        )
        store.mas_setEVLPropValues(
            "nsfw_player_sextingsession",
            pool=False,
            conditional="mas_canShowRisque(aff_thresh=1000) and store.mas_getEVL_shown_count('nsfw_monika_sexting') >= 1",
            action=EV_ACT_POOL,
        )
    return

label nickwildish_nsfw_submod_v1_1_1(version="v_1_1_1"):
    python:
        store.mas_setEVLPropValues(
            "monika_brb_nsfw_masturbate",
            eventlabel = "nsfw_monika_brb_masturbate"
        )

        store.mas_setEVLPropValues(
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
    python:
        store.mas_setEVLPropValues(
            "nsfw_player_sextingsession",
            pool=True,
            unlocked=False,
            conditional=(
            "mas_canShowRisque(aff_thresh=1000) "
            "and store.mas_getEVL_shown_count('nsfw_monika_sexting') >= 1"
            ),
            action=EV_ACT_UNLOCK
        )

        store.mas_setEVLPropValues(
            "nsfw_monika_sexualpast",
            random=False,
            conditional=(
                "mas_canShowRisque(aff_thresh=400) "
                "and renpy.seen_label('nsfw_monika_safesex')"
            ),
            action=EV_ACT_RANDOM
        )

        store.mas_setEVLPropValues(
            "nsfw_monika_favorite_position",
            random=False,
            conditional=(
                "mas_canShowRisque(aff_thresh=400) "
                "and persistent._nsfw_genitalia == 'P' "
                "and renpy.seen_label('nsfw_monika_sexualpast')"
            ),
            action=EV_ACT_RANDOM
        )
    return

label nickwildish_nsfw_submod_v1_3_1(version="v_1_3_1"):
    return

label nickwildish_nsfw_submod_v1_3_2(version="v_1_3_2"):
    python:
        store.mas_setEVLPropValues(
            "nsfw_player_monika_initiate_sext",
            unlocked=False,
            rules={"no_unlock": None},
            conditional=(
            "persistent._nsfw_sexting_attempt_permfreeze == True"
            ),
            action=EV_ACT_UNLOCK
        )
    return

label nickwildish_nsfw_submod_v1_3_3(version="v_1_3_3"):
    return

label nickwildish_nsfw_submod_v1_3_4(version="v_1_3_4"):
    python:
        store.mas_setEVLPropValues(
            "nsfw_player_monika_initiate_sext",
            unlocked=False,
            conditional="persistent._nsfw_sexting_attempt_permfreeze == True",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock": None}
        )
    return

label nickwildish_nsfw_submod_v1_3_5(version="v_1_3_5"):
    return

