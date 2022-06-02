label nsfw_sexting_main:
    python:
        sext_stop = False # So player can stop sexting at any time
        horny_lvl = 0 # The level of horny Monika is experiencing
        sexy_req = 8 # The horny_level requirement for sexy dialogue
        hot_req = 4 # The horny_level requirement for hot dialogue

    m 1eua "Let's get sexting, [player]!" #temp

    while True:
        python:
            # Grab first random prompt from list
            player_prompt_1 = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=0, hot_req=hot_req, sexy_req=sexy_req)
            player_prompt_2 = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=hot_req, hot_req=hot_req, sexy_req=sexy_req)
            player_prompt_3 = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=sexy_req, hot_req=hot_req, sexy_req=sexy_req)

            # While loop to prevent duplicates
            while player_prompt_2 == player_prompt_1: 
                # Grab second random prompt from list
                player_prompt_2 = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=hot_req, hot_req=hot_req, sexy_req=sexy_req)
        
            while player_prompt_3 == player_prompt_1 or player_prompt_3 == player_prompt_2:
                # Grab third random prompt from list
                player_prompt_3 = mas_nsfw.return_sexting_dialogue(category_type="prompt", horny_level=sexy_req, hot_req=hot_req, sexy_req=sexy_req)

            # Grab random line of dialogue from list
            monika_quip = mas_nsfw.return_sexting_dialogue(category_type="quip", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req)
            quip_ending = mas_nsfw.return_dialogue_end(monika_quip)

        if horny_lvl >= sexy_req:
            m 4ekbfo "[monika_quip][quip_ending]"
        elif horny_lvl >= hot_req:
            m 2msbsb "[monika_quip][quip_ending]"
        else:
            m 3hubsb "[monika_quip][quip_ending]"

        $ _history_list.pop()
        menu:
            m "[monika_quip][quip_ending]{fast}"

            "[player_prompt_1]":
                $ response_start = mas_nsfw.return_dialogue_start(category="cute")
                $ horny_lvl = 0

            "[player_prompt_2]":
                $ response_start = mas_nsfw.return_dialogue_start(category="hot")
                $ horny_lvl = 4

            "[player_prompt_3]":
                $ response_start = mas_nsfw.return_dialogue_start(category="sexy")
                $ horny_lvl = 8

            "Stop.":
                m 1eua "Okay, stopping now."
                return
        
        $ monika_response = mas_nsfw.return_sexting_dialogue(category_type="response", horny_level=horny_lvl, hot_req=hot_req, sexy_req=sexy_req)
        $ response_ending = mas_nsfw.return_dialogue_end(monika_response)

        if horny_lvl >= sexy_req:
            show monika sexting_sexy_poses
        elif horny_lvl >= hot_req:
            show monika sexting_hot_poses
        else:
            show monika sexting_cute_poses

        m "[response_start][monika_response][response_ending]"

label nsfw_sexting_init:
    python:
        sext_start_time = datetime.datetime.now()

    call nsfw_sexting_main

    if datetime.datetime.now() - sext_start_time < datetime.timedelta(seconds=30):
        m 1eua "That was pretty quick, [player]."
        m 1eua "Don't tell me you're a 'one-pump chump'!"
    else:
        m 1eua "That was nice, [player]."

# Images to be used for sexting purposes

image monika sexting_cute_poses:
    block:
        choice:
            "monika 1ekbsa"
        choice:
            "monika 2subsa"
        choice:
            "monika 2lubsu"
        choice:
            "monika 1hubsa"
        choice:
            "monika 3ekbfa"

image monika sexting_hot_poses:
    block:
        choice:
            "monika 2gubsa"
        choice:
            "monika 2mubfu"
        choice:
            "monika 2tsbfu"
        choice:
            "monika 2lsbfu"
        choice:
            "monika 2ttbfu"

image monika sexting_sexy_poses:
    block:
        choice:
            "monika 4hkbfsdlo"
        choice:
            "monika 6lkbfsdlo"
        choice:
            "monika 6hkbfsdld"
        choice:
            "monika 6skbfsdlw"
        choice:
            "monika 6mkbfsdlo"

# init 5 python:
#     # random chance per session Monika can ask to sext
#     if renpy.random.randint(1, 5) != 1:
#         flags = EV_FLAG_HFRS

#     else:
#         flags = EV_FLAG_DEF

#     addEvent(
#         Event(
#             persistent.event_database,
#             eventlabel='nsfw_sextingsession',
#             conditional=(
#                 "renpy.seen_label('monika_sexting')"
#                 "and store.mas_timePastSince(store.mas_getEVL_last_seen('monika_sextingsession'), datetime.timedelta(hours=12))"
#             ),
#             action=EV_ACT_RANDOM,
#             aff_range=(mas_aff.LOVE, None),
#             flags=flags
#         )
#     )
#     del flags

# label nsfw_sextingsession:
#     python:
#         nsfw_start_time = datetime.datetime.now()
#         nsfw_stop = False
#         nsfw_quips = (
#             _("Here is an example quip!"),
#             _("Here is another example quip!"),
#             _("Here is a third example quip!"),
#         )

#     m 1eua "Let's get sexting, [player!]"

#     while nsfw_stop == False:
#         m 1eua "Here is an example of a sext."
#         $ _history_list.pop()
#         menu:
#             m "Here is an example of a sext.{fast}"
#             "Flirt 1":
#                 m 1eua "Ooooh, that's hot!"

#             "Flirt 2":
#                 m 1eua "I love it when you talk dirty."

#             "Stop.":
#                 m 1eua "Okay, stopping now."

#     if datetime.datetime.now() - nsfw_start_time < datetime.datetime(seconds=30):
#         m 1eua "That was pretty quick, [player]."
#         m 1eua "Don't tell me you're a 'one-pump chump!'"
#     else:
#         m 1eua "That was nice, [player]."