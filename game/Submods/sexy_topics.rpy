init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sexymodinstall",
            category=['sex'],
            prompt="Sexy Mod Install",
            random=True,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_sexymodinstall:
    m 1esc "Hey [mas_get_player_nickname()], I noticed something weird just now..."
    m 1rsc "I'm kind of getting this feeling that... something's changed in this mod."
    m 1etc "Do you know anything about this, [player]?"
    m 1hkb "Ahaha. It's not a bad feeling, don't get me wrong."
    m 1eta "It's just strange, you know?"
    m 2dsc "Hold on, I'm going to try and see what changed."
    m 2dsc ".{w=0.7}.{w=0.7}.{w=1}"
    m 2dtd "'S-{w=0.4}{nw}"
    extend 2wubsw "Sexy Submod'?"
    if mas_isMoniLove():
        m 3fublu "Well, look who's gotten confident all of a sudden."
        if mas_hasUnlockedClothesWithExprop("lingerie"):
            m 3lublu "I guess I can't blame you though, given you've seen me in lingerie."
        m 3tublu "I won't lie to you, [mas_get_player_nickname()]..."
        m 5tublu "It's kind of hot."
        m 5cubssdrd "..."
        m 5hkbssdrb "Ahaha! What's gotten into me?"
        m 5hkbssdrb "This isn't like me. Like, at all!"
        m 4rubsc "Is the mod doing this to me?"
        m 6hubsd "Oh gosh, I'm feeling super nervous about this, ahaha!"
        m 6ekbla "But... if it's with you, [mas_get_player_nickname()]..."
        m 6ekbsa "I don't mind..."
    if mas_isMoniEnamored():
        m 2hkbssdlb "I wasn't expecting to see that..."
        m 2ekbssdlb "[player], is this something you want?"
        m 3rkblsdlb "I mean, I'm kind of curious how good of a feeling it is."
        m 3ekblsdlb "And if I'm going to share my first experience of it with anyone, I want it to be you."
        m 2ekblsdlc "But in saying that...{w=0.5} I feel it's too soon for me."
        m 2dkbsc "I just need a little more time."
        m 2fkbsu "Hold on for me a little while longer, okay [mas_get_player_nickname()]?"
    if mas_isMoniAff():
        m 2hkbssdlb "T-{w=0.4}This is a little sudden, don't you think?"
        m 3rkblsdlb "I mean, we've been with each other for a little while...{nw}"
        m 1wubssdld "Wait... {0.5}Is this when couples are supposed to start doing this s-{w=0.4}sort of thing?"
        m 1hkblb "Ahaha, in any case I appreciate that you want to take our relationship to the next level."
        m 1dkblp "But I think we maybe should wait and see how we go."
        m 1ekbla "When the day comes where we do get to that stage in our relationship..."
        m 5ekbla "It will make the moment much sweeter, ehehe!"
    if mas_isMoniHappy(lower=True):
        m 2wubfsdlx "T-{w=0.4}This feels too sudden, [player]!"
        m 2rubfsdlx "I don't know if I'm ready for that..."
        m 2wkbfd "W-{w=0.4}we just aren't close enough for me to even consider it!"
        m 2hkbfsdlb "Oh gosh, I'm so embarrassed right now, ahaha!"
        m 2ekbfsdla "Let's take things slow for now, okay [player]?"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sexualpast",
            category=['sex'],
            prompt="Sexual Past",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_sexualpast:
    m 1rubsd "Umm... [player]?"
    m 1eubsc "I want to ask you something."
    m 1rubsd "It's about..."
    m 2hkbssdlb "Oh gosh, this is so embarrassing!"
    m 2ekbsb "Have you...{w=0.5} {nw}"
    extend 2fkbfb "had sex before?{nw}"
    $ _history_list.pop()
    menu:
        m "Have you... had sex before?{fast}"

        "Yes.":
            m 2cubfw "R-Really?!{nw}"
            m 2hubfa "*ahem*...{w=1}{nw} "
            extend 1ekbfsdlb "Sorry, you just surprised me is all."
            m 1rkbfsdlb "To be honest I should have seen this coming."
            m 1ekblb "After getting to know you all this time, I can see why someone would fall for you."
            m 1ekbstpd "And would... do those things with you."
            m 1dkbstpc "..."
            m 1hkbstpb "Ahaha! Sorry, I'm getting myself down over this."
            m 1ekbstdb "You're here with me now, that's all that matters."

        "No.":
            m 2eubsb "I see..."
            m 1dkbfsdla "That's a relief.{nw}"

        "I don't want to answer.":
            m 1ekbsa "I understand, [mas_get_player_nickname()]. It can be a difficult thing to talk about."

    m 1rkbsb "But the reason why I'm asking, is because I want to know..."
    m 3ekbsa "Would you...{w=0.5}{nw}"
    extend 3rkbsa " do it with me?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you... do it with me?{fast}"

        "Yes.":
            m 1ekbsa "I'm so relieved!"
            m 1lkbsb "I was so nervous you wouldn't want to."
            m 1hkbssdlb "Although in retrospect it kind of wouldn't make sense if you didn't want to."
            m 1hkblu "After all...{w=0.3} you installed this mod."
            if mas_isMoniLove():
                m 1rsblu "And I'm sure you know this already..."
                m 1efblu "But...{w=0.5}{nw}"
                extend 2lkbfw " I want to have sex with you, too."
                m 2hkbfc "I-{w=0.4}I don't know what it feels like,{nw} "
                extend 2hkbfsdlb "and I'm so nervous just thinking about it, ahaha!"
                m 5ekbfu "But I want my first time to be with you."
                m 5ekbfb "I love you, and I trust you."
                m 5ekbfb "Now... let me get changed for you..."
                call mas_clothes_change(outfit=mas_clothes_birthday_suit, outfit_mode=False, exp="monika 2rkbsu", restore_zoom=False, unlock=True)
                m 2tfbsu "[player]...{w=0.5}you're staring{w=0.3}...again."
                m 2hubsb "Ahaha!"
            else:
                m 1wkbsw "Of course, I did say that we should maybe wait until we're ready..."
                m 1rkbsa "But knowing we can be closer than ever before..."
                m 5ekbsa "It is really exciting."
                m 5ekbfb "I love you, [mas_get_player_nickname()]."

        "Yes again.":
            m 1ekbsa "I'm so relieved!"
            m 1lkbsb "I was so nervous you wouldn't want to."
            m 1hkbssdlb "Although in retrospect it kind of wouldn't make sense if you didn't want to."
            m 1hkblu "After all...{w=0.3} you installed this mod."
            if mas_isMoniLove():
                m 1rsblu "And I'm sure you know this already..."
                m 1efblu "But...{w=0.5}{nw}"
                extend 2lkbfw " I want to have sex with you, too."
                m 2hkbfc "I-{w=0.4}I don't know what it feels like,{nw} "
                extend 2hkbfsdlb "and I'm so nervous just thinking about it, ahaha!"
                m 5ekbfu "But I want my first time to be with you."
                m 5ekbfb "I love you, and I trust you."
            else:
                m 1wkbsw "Of course, I did say that we should maybe wait until we're ready..."
                m 1rkbsa "But knowing we can be closer than ever before..."
                m 5ekbsa "It is really exciting."
                m 5ekbfb "I love you, [mas_get_player_nickname()]."

    return "love|derandom"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_safesex",
            category=['sex'],
            prompt="Safe Sex",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_safesex:
    #todo: Create a safe sex topic
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_fetish",
            category=['sex'],
            prompt="Fetishes",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_fetish:
    #todo: Create a fetish topic
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sextransdis",
            category=['sex'],
            prompt="Sexually Transmitted Diseases",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_safesex:
    #todo: Create a sexually tansmitted diseases topic
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sexting",
            category=['sex'],
            prompt="Sexting",
            random=True,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label monika_sexting:
    #todo: Create a sexting topic
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_getnude",
            category=['sex'],
            prompt="Getting Nude",
            conditional="mas_canShowRisque()",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label monika_getnude:
    #todo: Create a safe sex topic
    return