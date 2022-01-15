# ---- WORK IN PROGRESS ----

# label nsfw_sexting_main:
#     python:
#         sext_start_time = datetime.datetime.now()
#         sext_stop = False

#     m 1eua "Let's get sexting, [player]!" #temp

#     m 1eua "So...{w=0.3} What do you want to do to me?"
#     $ _history_list.pop()
#     menu:
#         m "So...{w=0.3} What do you want to do to me?{fast}"

#         "I want to take you out to dinner.":
#             m 1eua "Ooooh, that's hot!"

#         "Flirt 2":
#             m 1eua "I love it when you talk dirty."

#         "Flirt 3":
#             m 1eua "You're so funny!"

#         "Stop.":
#             m 1eua "Okay, stopping now."
#             $ sext_stop = True

#     while sext_stop == False:
#         m 1eua "So...{w=0.3} What do you want to do to me?"
#         $ _history_list.pop()
#         menu:
#             m "So...{w=0.3} What do you want to do to me?{fast}"
#             "I want to take you out to dinner.":
#                 m 1eua "Ooooh, that's hot!"

#             "Flirt 2":
#                 m 1eua "I love it when you talk dirty."

#             "Stop.":
#                 m 1eua "Okay, stopping now."
#                 $ sext_stop = True

#     if datetime.datetime.now() - sext_start_time < datetime.timedelta(seconds=30):
#         m 1eua "That was pretty quick, [player]."
#         m 1eua "Don't tell me you're a 'one-pump chump'!"
#     else:
#         m 1eua "That was nice, [player]."

#     return

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