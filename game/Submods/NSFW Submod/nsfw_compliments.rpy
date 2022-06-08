# Template used from script-compliments.rpy as of 8th June, 2022

# dict of tples containing the stories event data
default persistent._nsfw_compliments_database = dict()

# store containing compliment-related things
init 3 python in nsfw_compliments:

    nsfw_compliment_database = dict()

init 22 python in nsfw_compliments:
    import store

    # Need to set some nsfw thanking quips here.
    nsfw_thanking_quips = [
        _("You're so sweet, [player]."),
        _("Thanks for saying that again, [player]!"),
        _("Thanks for telling me that again, [mas_get_player_nickname()]!"),
        _("You always make me feel special, [mas_get_player_nickname()]."),
        _("Aww, [player]~"),
        _("Thanks, [mas_get_player_nickname()]!"),
        _("You always flatter me, [player].")
    ]

    # set this here in case of a crash mid-compliment
    thanks_quip = renpy.substitute(renpy.random.choice(nsfw_thanking_quips))

    def nsfw_compliment_delegate_callback():
        """
        A callback for the compliments delegate label
        """
        global thanks_quip

        thanks_quip = renpy.substitute(renpy.random.choice(nsfw_thanking_quips))
        store.mas_gainAffection()

# entry point for compliments flow
init 6 python: # Use init 6 since the dictionary entry to store our entries is added in 5, and we want it around
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_compliments",
            category=['sex'],
            prompt="I want to tell you something lewd...",
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_compliments:
    python:
        # Unlock any compliments that need to be unlocked
        Event.checkEvents(nsfw_compliments.nsfw_compliment_database)

        # build menu list
        nsfw_compliments_menu_items = [
            (ev.prompt, ev_label, not seen_event(ev_label), False)
            for ev_label, ev in nsfw_compliments.nsfw_compliment_database.iteritems()
            if (
                Event._filterEvent(ev, unlocked=True, aff=mas_curr_affection, flag_ban=EV_FLAG_HFM)
                and ev.checkConditional()
            )
        ]

        # also sort this list
        nsfw_compliments_menu_items.sort()

        # final quit item
        final_item = ("Oh nevermind.", False, False, False, 20)

    # move Monika to the left
    show monika at t21

    # call scrollable pane
    call screen mas_gen_scrollable_menu(nsfw_compliments_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    # return value? then push
    if _return:
        $ nsfw_compliments.nsfw_compliment_delegate_callback()
        $ pushEvent(_return)
        # move her back to center
        show monika at t11

    else:
        return "prompt"

    return

# NSFW compliments start here
init 6 python:
    addEvent(
        Event(
            persistent._nsfw_compliments_database,
            eventlabel="nsfw_compliment_thighs",
            prompt="I love your thighs!",
            unlocked=True
        ),
        code="NCP"
    )

label nsfw_compliment_thighs:
    if not renpy.seen_label("nsfw_compliment_thighs_2"):
        call nsfw_compliment_thighs_2
    else:
        call nsfw_compliment_thighs_3
    return

label nsfw_compliment_thighs_2:
    m 1eua "Oh..."
    m 1eua "I wasn't expecting you to compliment my body like that. Ahaha~"
    m 1eua "Y-You don't get many chances to see them nowadays in this position though..."
    m 1eua "..."
    m 1eua "You can probably tell, but you've made me a little flustered..."
    m 1eua "I'm not sure why some guys like thighs so much..."
    m 1eua "I mean...there are bunch of sexier things on a girl to look at, aren't there?"
    m 1eua "But...thank you, [player]~"
    menu:
        "I'd love to bury my face between them.":
            $ mas_gainAffection(5,bypass=True)
            m 1eua "H-Hey~"
            m 1eua "[player]...you're getting a little {i}too{/i} naughty there. Ahaha~"
            m 1eua "Not that I mind..."
            m 1eua "I'm sure I would enjoy it if you did that~"

        "You always had the best thighs in the club.":
            $ mas_gainAffection(2,bypass=True)
            m 1eua "Ahaha~"
            m 1eua "That means you were looking at Yuri, Sayori, and Natsuki's thighs too, huh?"
            m 1eua "Well..."
            m 1eua "I mean, Natsuki didn't have much..."
            m 1eua "But you get the point!"
            m 1eua "..."
            m 1eua "Ahaha~"
            m 1eua "Don't worry. It's okay to look, just don't touch{nw}"
            m "Don't worry. It's okay to look,{fast} as long as you think mine are the best~"

        "They kind of remind me of Yuri's.":
            $ mas_loseAffection() # Rule 1 of dating a woman: Don't compare them to another woman, you nuff nuff.
            m 1eua "Uh..."
            m 1eua "Are they, now?"
            m 1eua "..."
            m 1eua "Well, if you liked her body so much, maybe you should have brought {i}her{/i} back into existence instead..."
    return

label nsfw_compliment_thighs_3:
    python:
        thighs_quips = [
            _("I'm glad you enjoy my thighs so much."),
            _("Remember to give some love to the rest of my body too, okay~?"),
            _("I wish you could rest your head on my lap."),
        ]
        thighs_quip = random.choice(thighs_quips)
    m 1eua "Ehehe~"
    m 1eua "[nsfw_compliments.thanks_quip]"
    show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 1eua "[thighs_quip]"
    return
