# Template used from script-compliments.rpy as of 8th June, 2022
# Huge thanks to TheOneandOnlyDargonite for getting this to work!

# dict of tples containing the stories event data
default persistent._nsfw_compliments_database = dict()

# store containing compliment-related things
init 3 python in nsfw_compliments:

    nsfw_compliment_database = dict()

init 22 python in nsfw_compliments:
    import store

    player_name = store.persistent.playername
    player_nickname = store.mas_get_player_nickname()

    # Need to set some nsfw thanking quips here.
    nsfw_thanking_quips = [
        _("You're so sweet, " + player_name + "."),
        _("Thanks for saying that again, " + player_name + "!"),
        _("Thanks for telling me that again, " + player_nickname + "!"),
        _("You always make me feel special, " + player_nickname + "."),
        _("Aww, " + player_name + "~"),
        _("Thanks, " + player_nickname + "!"),
        _("You always flatter me, " + player_name + ".")
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
            conditional="mas_canShowRisque(aff_thresh=1000)",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_compliments:
    # TODO: Add a bit here that checks if she tried to sext earlier but you said you're busy, so she tries sexting again

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
# ---------------------------

# Thanks for the compliment addition, KittyTheCocksucker
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
    m 1wubld "Oh..."
    m 1hkblsdlb "I wasn't expecting you to compliment my body like that. Ahaha~"
    m 3rkblb "You don't get many chances to see them nowadays in this position though..."
    m 3hkbsa "..."
    m 2hkbsb "You can probably tell, but you've made me a little flustered..."
    m 2rkbsu "I'm not sure why some guys like thighs so much..."
    m 3eubsd "I mean...there are bunch of sexier things on a girl to look at, aren't there?"
    m 1ekbsa "But...thank you, [player]~"
    menu:
        "I'd love to bury my face between them.":
            $ store.mas_gainAffection(5,bypass=True)
            m 2tkbsb "H-Hey~"
            m 3tkbsu "[player]...you're getting a little {i}too{/i} naughty there. Ahaha~"
            m 3gkbsu "Not that I mind..."
            m 5tkbsu "I'm sure I would enjoy it if you did that~"

        "You always had the best thighs in the Literature Club.":
            $ store.mas_gainAffection(2,bypass=True)
            m 1hubsb "Ahaha~"
            m 3tubsb "That means you were looking at Yuri, Sayori, and Natsuki's thighs too, huh?"
            m 1gubsb "Well..."
            m 1gubsa "I mean, Natsuki didn't have much..."
            m 1kubsu "But you get the point!"
            m 1dubsu "..."
            m 2hubsb "Ahaha~"
            m 2tubsa "Don't worry. It's okay to look, as long as you think mine are the best~"

        "They kind of remind me of Yuri's.":
            $ store.mas_loseAffection() # Rule 1 of dating a woman: Don't compare them to another woman, you nuff nuff.
            m 1etbsd "Uh..."
            m 1rfbld "Are they, now?"
            m 1gfblc "..."
            m 1tfbld "Well, if you liked her body so much, maybe you should have brought {i}her{/i} back into existence instead..."
    return

label nsfw_compliment_thighs_3:
    python:
        thighs_quips = [
            _("I'm glad you enjoy my thighs so much."),
            _("Remember to give some love to the rest of my body too, okay~?"),
            _("I wish you could rest your head on my lap."),
        ]
        thighs_quip = random.choice(thighs_quips)
    m 1tubla "Ehehe~"
    m 1tublb "[nsfw_compliments.thanks_quip]"
    show monika 3tubsb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 3tubsb "[thighs_quip]"
    return


# Thanks for the compliment addition, KittyTheCocksucker

# "I remember wanting to have one character wear higher stockings – I thought
# Yuri might be a good fit, but we decided that she isn’t the type to draw
# attention to herself. Monika, being the confident one who cares about her
# impression, was the obvious choice after that."
#                                                   - DDLC Concept Art Booklet

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_compliments_database,
            eventlabel="nsfw_compliment_thighhighs",
            prompt="I love your thighhighs!",
            conditional="store.mas_getEVL_shown_count('nsfw_compliment_thighs') >= 1",
            action=EV_ACT_UNLOCK
        ),
        code="NCP"
    )

label nsfw_compliment_thighhighs:
    if not renpy.seen_label("nsfw_compliment_thighhighs_2"):
        call nsfw_compliment_thighhighs_2
    else:
        call nsfw_compliment_thighhighs_3
    return

label nsfw_compliment_thighhighs_2:
    python:
        if persistent.gender == "M":
            guyGirl = "guy"
        elif persistent.gender == "F":
            guyGirl = "girl"
        else:
            guygirl = "person"

        if persistent._nsfw_genitalia == "P":
            naughty_bits = " I'd love if you gave me a thighjob while wearing them."
        else:
            naughty_bits = ""

    m 1tubla "Oh geez..."
    m 1tublb "Going for my thighs again, [player]?"
    m 3tublb "Well...I'm glad you like how my thighhighs look!"
    m 3eubla "You know...I'm not sure whether you've noticed or not..."
    m 3eublb "But I was the only one in the club with black stockings! Ahaha~"
    m 2hublb "They might not have exactly fit the school dress code, but I didn't really like how the white cotton socks looked."

    menu:
        "Even in uniform, you dress more nicely than any of the other girls in the club.":
            $ store.mas_gainAffection(3,bypass=True)
            m 1eubsb "I'm so glad you think that, [player]~"
            m 1rubsa "But I mean...ahaha...I kind of expected for my socks to get noticed by you, {nw}"
            extend 1gubsb "a [guyGirl] who seems to love my thighs. Ahaha~"
            m 1ekbsa "I'm honestly not exactly sure why you love them so much..."
            m 2ekbsa "But..."
            m 2ekbsb "If it means you'll keep complimenting me about them..."
            m 5hubsa "Ehehe~"
            m 5mubsa "Then I'm fine with it~"

        "I bet they not only look good, but feel really smooth and silky too![naughty_bits]":
            $ store.mas_gainAffection(2,bypass=True)
            if persistent._nsfw_genitalia == "P":
                m 2subld "Ooo~"
                m 2subsu "A thighjob, eh?"
                m 2ttbsu "Aren't you pushing your luck a little {i}too{/i} far, [player]?"
                m 2tsbsu "..."
                m 1hkbssdlb "Ahaha~ Who am I kidding?"
                m 1eubsa "I will say..."
            else:
                m 1eubsa "Well yeah,{nw}"
                extend 3eubsa " they do feel {i}really{/i} smooth and silky~"
            m 1tubsb "I wouldn't be wearing these for school if they weren't comfortable, would I?"
            m 1hubsb "Ahaha~"
            if persistent._nsfw_genitalia == "P":
                m 1rubsa "..."
                m 2gubsa "So..."
                m 2tubsb "I bet it would feel really nice for your cock between my squishy thighs and soft thighhighs~"
                m 2tubsa "I'm sure if I moved my legs, up and down, nicely jerking your massive dick with my thighs..."
                m 2tfbfb "You would ejaculate all over my legs and belly in no time. Ahaha~"
                m 1tubfa "..."
                m 1gubfa "I hope we can try that soon. Ehehe~"

        "I love how they wrap around your thick thighs.":
            $ store.mas_gainAffection(1,bypass=True)
            m 1hkbsa "Gosh..."
            m 1hkbssdlb "You keep making me blush with all this talk about my thighs..."
            m 1ekbsa "The other parts of my body are nice to look at too, you know."
            m 2gkbsu "Like...I don't like to brag, but I think I have pretty nice breasts!"
            m 2efbsu "Plus, you know, my eyes are also up here!"
            m 2gubsp "..."
            m 2gubsd "You don't always need to look at me like I'm just a piece of meat..."

    return

label nsfw_compliment_thighhighs_3:
    python:
        thighhighs_quips = [
            _("They're really comfy too!"), #Thank you, [player]!
            _("I can't wait for you to make a mess over them. Ehehe~"),
            _("I wear them mainly to stand out, but they can also come in handy when it's cold outside!"),
        ]
        thighhighs_quip = random.choice(thighhighs_quips)
    m 1tubla "Ehehe~"
    m 1tublb "[nsfw_compliments.thanks_quip]"
    show monika 3tubsb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 3tubsb "[thighhighs_quip]"
    return


# Thanks for the compliment addition, KittyTheCocksucker
init 6 python:
    addEvent(
        Event(
            persistent._nsfw_compliments_database,
            eventlabel="nsfw_compliment_tits",
            prompt="I love your breasts!",
            unlocked=True
        ),
        code="NCP"
    )

label nsfw_compliment_tits:
    if not renpy.seen_label("nsfw_compliment_tits_2"):
        call nsfw_compliment_tits_2
    else:
        call nsfw_compliment_tits_3
    return

label nsfw_compliment_tits_2:
    python:
        if persistent._nsfw_genitalia == "P":
            naughty_bits = "I bet they'd feel nice and soft if I rested my dick between them."
        else:
            naughty_bits = "I bet they'd feel nice and soft if I felt them up~"

    m 1wubld "Uhh..."
    m 1hkbla "Ahem..."
    m 1rkbsa "I-is that so?"
    m 1hkbssdlb "Ahaha~"
    m 1hkbssdla "Sorry! You just caught me off-guard, that's all."
    m 1eubssdlb "I'm really glad you like them!"
    m 3eubssdlb "Did you know that the growth of a woman's breasts are not only affected by hormones and genetics, but by what we eat as well?"
    m 3hubssdlb "Healthy and nutritious meals help our boobs grow nice and round! Ahaha~"

    if mas_safeToRefDokis():
        m 3hkbsu "..."
        m 3gkbsu "I guess that explains why Natsuki was so flat, huh?" #oof
        m 1hubsb "Ahaha~ Sorry, that was a bad joke."
        m 3rubsb "I couldn't let that opportunity slip by~"

    menu:
        "I'd love to suck on your breasts.":
            $ store.mas_gainAffection(5,bypass=True)
            m 1hkbsa "Ahem..."
            m 1tfbsb "[player]!"
            m 3tfbsu "Why did you get so naughty out of nowhere like that?"
            m 3hubsb "Ahaha~"
            m 3rubsb "I mean...I don't know if anything would come out if you did suck on them..."
            m 3gubsa "But..."
            m 1tubsa "I'm sure it would feel really nice if you did that."
            m 1hubsa "Ehehe~"

        "Can you make them bigger?":
            $ store.mas_loseAffection(5) # face <- palm
            m 3wubsd "..."
            m 3eubssdld "I-I mean..."
            m 3rubssdlc "I do have full control over the console, so..."
            m 3rublsdlc "T-technically I could do that, yeah..."
            m 1rkbltpc "But..."
            m 1ekbltpc "Don't you love me the way I am now?"

        "[naughty_bits]":
            m 3tubsu "Ooo~"
            m 2tubsu "[player]..."
            m 2hubssdlb "Ahaha! My heart skipped a beat just now."
            m 1rubssdlb "I didn't expect you to say that~"
            if persistent._nsfw_genitalia == "P":
                m 1gubsa "Mmm~ I'm sure your hard, throbbing cock would feel really nice between my breasts~"
                m 1gubfa "..."
                m 3gubfb "It's kind of funny if you think about it."
                m 3tubfb "I would feel your dick pulsating against my heart..."
                m 4tubfb "And you would feel my heart pulsating against your dick~"
                m 4tubfa "..."
                m 5tubfa "I wonder where you'd unload your cum when you finished?"
                m 5tsbfa "Would it be all over my breasts?"
                m 5tsbfo "Maybe on my face?"
                m 5mubfa "Or would you push forward, between my lips, and release your thick, creamy load there? Ehehe~"
            else:
                m 1gubsa "Mmm~ I'm sure your hands would enjoy the feeling of my breasts~"
                m 1tubfa "And I would {i}really{/i} enjoy the feeling of your hands playing with my breasts..."
                m 1dubfu "..."
                m 5dubfu "I wonder where else on my body you might like to feel me up?"
                m 5hubfa "Ehehe~"
    return

label nsfw_compliment_tits_3:
    python:
        tits_quips = [
            _("You can look at them all you want~"), # Ahaha~ I'm glad you do, [player]!
            _("I can't wait for you to fondle them~"), # Mhm~
            _("Want to rest your head on them? Ahaha~"),
            # _("I hope my outfit isn't too revealing. Ahaha~"),
            # this last one is good but needs a bit of code so it only triggers when her clothing has a lingerie exprop
        ]
        tits_quip = random.choice(tits_quips)
    m 1tubla "Ehehe~"
    m 1tublb "[nsfw_compliments.thanks_quip]"
    show monika 2tubsb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 2tubsb "[tits_quip]"
    return

# Thanks for the compliment addition, KittyTheCocksucker
init 6 python:
    addEvent(
        Event(
            persistent._nsfw_compliments_database,
            eventlabel="nsfw_compliment_naughty_flirting",
            prompt="I love how naughty you talk when we're flirting!",
            unlocked=True
        ),
        code="NCP"
    )

label nsfw_compliment_naughty_flirting:
    if not renpy.seen_label("nsfw_compliment_naughty_flirting_2"):
        call nsfw_compliment_naughty_flirting_2
    else:
        call nsfw_compliment_naughty_flirting_3
    return

label nsfw_compliment_naughty_flirting_2:
    python:
        if persistent._nsfw_genitalia == "P":
            naughty_bits = "I'd love to hear you talk naughty while you're slobbering over my cock~"
        elif persistent._nsfw_genitalia == "V":
            naughty_bits = "I'd love to hear you talk naughty while you're eating out my pussy~"
        else:
            naughty_bits = "I'd love to hear you talk naughty while I'm eating out your pussy~"

    m 1hublb "Ahaha~"
    m 1hublsdla "Well..."
    m 1rkbssdlb "Gosh... I can't believe I'm getting so red just from you saying that...Ahaha~"
    m 3ekbssdlb "Is it too nerdy to say that I practiced in the mirror...?"
    m 3rkbsa "..."
    m 2rkbsa "I wanted to get better so I can arouse you more..."
    m 2tubsu "I'm glad you enjoy how naughty I can get, [player]."
    m 1hubsa "It means my practice paid off. Ehehe~"

    menu:
        "I bet you had to work hard to tune your brain to it. This wasn't a porn game to begin with, after all.":
            m 1hkbsb "Yeah...it was a little bit difficult at first, having to learn so many lewd phrases and stuff..."
            m 1rkbsb "But since you like when I do it, I must be doing a good job at it, right?"
            m 1tkbsa "And all the time and energy spent on it was totally worth it{nw}"
            if persistent._nsfw_genitalia == "P":
                extend 1tkbsa " if I can make your dick hard~"
            elif persistent._nsfw_genitalia == "V":
                extend 1tkbsa " if I can make your pussy wet~"
            else:
                extend 1tkbsa " if I can give you naughty thoughts about me~"

        "It does need some polishing here and there, but I appreciate the effort.":
            m 1wubsd "Oh..."
            m 1wkbsc "W-well..."
            m 3rkbsc "I already spent a bunch of time studying erotica and stuff..."
            m 3dkbsc "..."
            m 3gkbsc "I'll try to work even harder, I guess..."

        "[naughty_bits]":
            m 1wubfd "Oh..."
            m 1hubfb "Ahaha~"
            m 1hkbfsdlb "T-that certainly caught me off-guard..."
            m 1ttbfu "[player]~ Aren't you getting a little bit ahead of yourself there? Ehehe~"
            m 1gsbfu "Mmm~ Don't worry about it."
            m 1tsbfd "It would probably be easier to practice talking naughty if{nw}"
            if persistent._nsfw_genitalia == "P":
                extend 1tsbfd " I had your nice and big dick to suck on and play with~"
            elif persistent._nsfw_genitalia == "V":
                extend 1tsbfd " I had your pussy in my face for me to lick and play with~"
            else:
                extend 1tsbfd " your face was buried deep in my pussy, licking it clean~"

            if persistent._nsfw_genitalia == "P" or persistent._nsfw_genitalia == "V":
                m 5tsbfu "I'd make sure to give it proper attention and care~"
            else:
                m 5tsbfu "You had better make sure to give it proper attention and care~"

            m 5hsbfu "Ehehe~"
    return

label nsfw_compliment_naughty_flirting_3:
    python:
        if persistent._nsfw_genitalia == "P":
            naughty_bits = "I love making you hard~"
        elif persistent._nsfw_genitalia == "V":
            naughty_bits = "I love making your pussy wet~"
        else:
            naughty_bits = "I love giving you naughty thoughts about me~"

        naughty_flirting_quips = [
            _("I'm really glad you enjoy it so much! I'm always practicing for you~"),
            _(naughty_bits),
            _("I wish I could lay in bed with you and whisper naughty things in your ears~"),
        ]
        naughty_flirting_quip = random.choice(naughty_flirting_quips)
    m 1tubla "Ehehe~"
    m 1tublb "[nsfw_compliments.thanks_quip]"
    show monika 3tubsb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 3tubsb "[naughty_flirting_quip]"
    return

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_compliments_database,
            eventlabel="nsfw_compliment_moaning",
            prompt="I love making you moan!",
            conditional="store.persistent._nsfw_sexting_success_last is not None",
            action=EV_ACT_UNLOCK
        ),
        code="NCP"
    )

label nsfw_compliment_moaning:
    if not renpy.seen_label("nsfw_compliment_moaning_2"):
        call nsfw_compliment_moaning_2
    else:
        call nsfw_compliment_moaning_3
    return

label nsfw_compliment_moaning_2: #TODO: Finish writing Monika's initial reaction to compliment
    m 1eua "Oh..."
    m 1eua "Ahaha, I'm glad you like it~"
    m 1eua "It's not something I can control, per se..."
    m 1eua "But if you enjoy it so much, maybe I should practice moaning for you~"
    m 1eua "Would you prefer if I moaned like this?{w=0.5}{nw}"
    extend 1eua " {i}Ahhhh~{/i}"
    m 1eua "Or like this?{w=0.5}{nw}"
    extend 1eua " {i}Oh, [player]~{/i}"
    m 1eua "..."
    m 1eua "Or maybe like this?{w=0.5}{nw}"
    m 1eua " {i}Oh~ I want you, [player]!~{/i}"
    m 1eua "Ehehe~"
    m 1eua "I'm just teasing you."
    $ _history_list.pop()
    menu:
        m "I'm just teasing you.{fast}"

        "You feeling good is what I want the most.":
            $ store.mas_gainAffection(amount=5, bypass=True)
            m 1eua "Aww~"
            m 1eua "You're so sweet, [player]."
            m 1eua "Well in that case, I'll be moaning for you alot more~"
            m 1eua "You better be ready for it."

        "I want to hear you moan my name.":
            $ store.mas_gainAffection(amount=2, bypass=True)
            m 1eua "Oh?"
            m 1eua "You mean like this?{w=0.5}{nw}"
            extend 1eua " {i}Oh, [player]~{/i}{w=0.5}{nw}"
            extend 1eua " {i}I want you~{/i}{w=0.5}{nw}}"
            extend 1eua " {i}I want you so bad~{/i}"
            m 1eua "Ehehe~"
            m 1eua "I'll moan your name all you want, [player]."

        "You can moan abit too much sometimes...": # BLASPHEMY!
            $ store.mas_loseAffection(2)
            m 1eua "Oh..."
            m 1eua "I'm sorry, [player]."
            m 1eua "I did say it's not something I can control..."
            m 1eua "But I'll try to keep it down."
    return

label nsfw_compliment_moaning_3:
    python:
        if mas_nsfw.return_random_number(1, 3) == 3:
            moaning_thanks_quips = [
                _("Like this, you mean?~"),
                _("I can moan louder if you like~"),
                _("Let me show you how much I've practiced~"),
            ]
            naughty_flirting_quips = [
                _("Oh yeah!~ More of that~"),
                _("You just make me feel so good, I can't help it~"),
                _("I hope you moan for me just as much as I do for you~"),
            ]
        else:
            moaning_thanks_quips = nsfw_compliments.nsfw_thanking_quips
            naughty_flirting_quips = [
                _("I'm more than happy to moan louder for you~"),
                _("You just make me feel so good, I can't help it~"),
                _("I hope you moan for me just as much as I do for you~"),
            ]

    $ moaning_thanks_quip = random.choice(moaning_thanks_quips)
    $ naughty_flirting_quip = random.choice(naughty_flirting_quips)
    m 1tubla "Ehehe~"
    m 1tublb "[moaning_thanks_quip]"
    show monika 3tubsb at t11 zorder MAS_MONIKA_Z with dissolve_monika
    m 3tubsb "[naughty_flirting_quip]"
    return

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_compliments_database,
            eventlabel="nsfw_compliment_wet",
            prompt="I love making you wet!",
            unlocked=True
        ),
        code="NCP"
    )

label nsfw_compliment_wet:
    if not renpy.seen_label("nsfw_compliment_wet_2"):
        call nsfw_compliment_wet_2
    else:
        call nsfw_compliment_wet_3
    return

label nsfw_compliment_wet_2: #TODO: Finish writing Monika's initial reaction to compliment
    python:
        if persistent._nsfw_genitalia == "P":
            naughty_bits = "I can make you even wetter with my cock deep inside you."
        elif persistent._nsfw_genitalia == "V":
            naughty_bits = "It's only fair, given how wet you make me."
        else:
            naughty_bits = "I'd make you even wetter if I was eating you out."

    m 1eua "Oh my~"
    m 1eua "I can't tell you how much I love you {i}making{/i} me wet~"
    m 1eua "You just make me feel so hot and tingly..."
    m 1eua "I can't help but get wet for you~"

    $ _history_list.pop()
    menu:
        m "I can't help but get wet for you~{fast}"

        "I'm glad that I make you feel good.":
            m 1eua "Aww, [player]~"
            m 1eua "You always make me feel good."
            m 1eua ""

        "[naughty_bits]":
            m 1eua "Response 2"

        "You'd better make me feel good too. You owe me.":
            m 1eua "Response 3"

    return

label nsfw_compliment_wet_3:
    python:
        naughty_flirting_quips = [
            _(""),
            _(""),
            _(""),
        ]
        naughty_flirting_quip = random.choice(naughty_flirting_quips)
    return