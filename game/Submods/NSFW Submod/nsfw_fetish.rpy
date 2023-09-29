# Template used from script-compliments.rpy as of 8th June, 2022
# Huge thanks to TheOneandOnlyDargonite for getting this to work!

# dict of tples containing the stories event data
default persistent._nsfw_fetish_database = dict()

# store containing fetish-related things
init 3 python in nsfw_fetish:

    nsfw_fetish_database = dict()

init 22 python in nsfw_fetish:
    import store

    def nsfw_fetish_delegate_callback():
        """
        A callback for the fetish delegate label
        """

        store.mas_gainAffection()

# entry point for fetish flow
init 6 python: # Use init 6 since the dictionary entry to store our entries is added in 5, and we want it around
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_player_fetishintro",
            category=['sex'],
            prompt="Let's talk about fetishes.",
            conditional=(
                "mas_canShowRisque(aff_thresh=1000) "
                "and store.mas_getEVL_shown_count('nsfw_monika_fetish') >= 1"
                ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_player_fetishintro:
    m 3eub "Hey, [player]. I just wanted to tell you about some work I've done!"
    m 3eua "You remember talking with me about fetishes?"
    m 4hub "...Well I made something so that we could talk about them."
    m 3rkblb "I'm not very...{w=0.5}{i}experienced{/i} with sexual things like this...{w=0.2}{nw}"
    extend 3hubla "so I've been looking into them!"
    m 3eub "Now, I've got a list of the fetishes I've found information on..."
    m 3eua "Whenever you want to talk about them, let me know and we can go through them together!"
    m 5ekblb "I'd love for you to tell me what you're into..."
    m 5ekbla "As much as there isn't much we can do together right now, just knowing what makes you...{w=0.5}{nw}"
    extend 5ekbsb "{i}excited{/i}..."
    m 5dkbsa "Will be more than enough for me."
    if persistent._nsfw_sexting_count > 0:
        m 5mkbsa "Who knows? I might even bring them up next time we're being {i}naughty~{/i}"
    m 1hubla "Don't worry! You can change your mind whenever you like, I'll never judge you for it."
    m 1hkblsdlb "But anyway, enough of me rambling..."
    m 1eua "What else did you want to talk about?"
    $ mas_unlockEventLabel("nsfw_player_fetishes")
return

# The fetish list contains lists that have information about any given fetish the player has expressed interest in.
# If the player has not specified any fetishes, we assume they're into everything.
# The first item in the list is the name of the fetish, the second is a whitelist of tags that the player will be into, the third is a blacklist of tags that the player will not be into.
# Example: ["Bondage", ["FBM"], ["FBP"]] means that the player is into bondage, but only if they're the one giving it, and not receiving it.
default persistent._nsfw_player_fetishes = []

# entry point for fetish flow
init 6 python: # Use init 6 since the dictionary entry to store our entries is added in 5, and we want it around
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_player_fetishes",
            category=['sex'],
            prompt="Let's talk about fetishes.",
            pool=True,
            conditional="store.mas_getEVL_shown_count('nsfw_player_fetishintro') >= 1",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_player_fetishes:
    python:
        # Unlock any fetish that need to be unlocked
        Event.checkEvents(nsfw_fetish.nsfw_fetish_database)

        # build menu list
        nsfw_fetish_menu_items = [
            (ev.prompt, ev_label, not seen_event(ev_label), False)
            for ev_label, ev in nsfw_fetish.nsfw_fetish_database.iteritems()
            if (
                Event._filterEvent(ev, unlocked=True, aff=mas_curr_affection, flag_ban=EV_FLAG_HFM)
                and ev.checkConditional()
            )
        ]

        # also sort this list
        nsfw_fetish_menu_items.sort()

        # final quit item
        final_item = ("Oh nevermind.", False, False, False, 20)

    # move Monika to the left
    show monika at t21

    # call scrollable pane
    call screen mas_gen_scrollable_menu(nsfw_fetish_menu_items, mas_ui.SCROLLABLE_MENU_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    # return value? then push
    if _return:
        $ nsfw_fetish.nsfw_fetish_delegate_callback()
        $ pushEvent(_return)
        # move her back to center
        show monika at t11

    else:
        return "prompt"

    return

# NSFW fetishes start here
# ---------------------------
# Noting that the current approach is intended to be both informative and descriptive, allowing you to make a decision of whether or not it's something you're into.
# Also noting that the 'context' used here is intended to coincide with sexting, so the prompts are appropriate to the player

default persistent._nsfw_pm_bondage = False # These are kind of redundant

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_fetish_database,
            eventlabel="nsfw_fetish_bondage",
            prompt="Bondage",
            unlocked=True
        ),
        code="NFH"
    )

label nsfw_fetish_bondage:
    m 3eub "You want to talk about bondage?"
    m 1hua "Sure! I'd love to get to know your opinion on it."
    m 3eua "Have you heard of it before?"
    $ _history_list.pop()
    menu:
        m "Have you heard of it before?{fast}"

        "Yes, I have.":
            m 3hub "Oh, that's great!"
            m 3tublb "So, based on what you know..."

        "No, I haven't.":
            m 1duc "Hmm...{w=0.5}Well it's a really interesting topic."
            m 3eua "Basically, it's when people use restraints such as rope to tie people up in all kinds of positions."
            m 4gkblb "These can be used for sex, "
            extend 4gkbla "but it can also be used for domination or playtime between lovers."

    m 4tubla "Does it sound like something that interests you?"
    $ _history_list.pop()
    menu:
        m "Does it sound like something that interests you?{fast}"

        "Yeah, it sounds pretty hot.":
            m 1tublb "Yeah? You think so?"
            m 1mubla "I think it's very hot!"
            m 2mublb "If I'm honest, it kinda turns me on..."
            extend 5gubla "Just the thought of tying you up and..."
            m 5tsblu "Mmm~ I think I've said too much."
            m 1eublb "But speaking of which..."
            extend 3tublb "would you prefer to be the one tying me up, or the one being tied up in this...{w=0.5}{i}hypothetical{/i} scenario?"
            $ _history_list.pop()
            menu:
                m "Speaking of which...would you prefer to be the one tying me up, or the one being tied up in this...{i}hypothetical{/i} scenario?{fast}"

                "I'd want to tie you up and have my way with you.":
                    $ store.mas_nsfw.save_fetish_to_persistent("Bondage", ["FBM"], ["FBP"])
                    m 3tubla "Hehe~ Well, if that's what you want you just say when, silly."
                    m 2tubsb "I wouldn't mind surrendering a little power {i}juuuuust{/i} this once for you~"

                "I think you should tie me up and do what you want with me.":
                    $ store.mas_nsfw.save_fetish_to_persistent("Bondage", ["FBP"], ["FBM"])
                    m 1sublo "Oooh! I like where this is going."
                    m 1tubla "Hmm...{w=0.5}I'll have to remember that next time we're getting naughty~"
                    m 3tubsb "I'll describe how I'll tie you to my bed, and tease you until you can't stand it anymore."

                "I wouldn't mind trying both. I'm here to please.":
                    $ store.mas_nsfw.save_fetish_to_persistent("Bondage", ["FBM", "FBP"], ["U"])
                    m 1ekbla "Aww~ [player], you've always been such a people pleaser."
                    m 1tkbsa "I love that about you."
                    m 3tubsb "Makes me want to tie you up and have you all to myself..."
                    extend 2gubsb "But...{w=0.5}I think I'll let you tie me up on the odd occasion if you so desire."

            m 1hkbla "Ehehe~ Anyway, back to the topic at hand before I get {i}too{/i} carried away." # Could lead to early sexting here, given that it's riled her up

        "I don't think it's for me...":
            $ store.mas_nsfw.save_fetish_to_persistent("Bondage", ["U"], ["FBM", "FBP"])
            m 3eublb "That's perfectly fine!"
            m 3hubla "I don't think it's for everyone."
            m 3dkbla "Bondage is something that should be negotiated and practiced thoroughly beforehand with someone you trust."
            m 1dkblb "It's not something you should just jump into."
            m 1eka "If you ever change your mind on it, I'd be happy to talk about it with you again."

    m 3eub "I actually learned an interesting bit of history regarding bondage, if you'd like to hear it."
    $ _history_list.pop()
    menu:
        m "I actually learned an interesting bit of history regarding bondage, if you'd like to hear it.{fast}"

        "Sure!":
            m 3hua "Oh good! Thanks for being so interested in what I have to say."

        "No thanks.":
            m 3eka "Okay, that's fine."
            m 3ekb "I'll save it for another time then."
            m 1eka "Regardless...thankyou for telling me about your preferences, [player]."
            m 1rkbla "It can be difficult to talk about your fetishes with someone, so I appreciate you opening up to me."
            m 1ekbla "If you ever want to talk about this again, or if you change your mind, I'll be here."
            m 5ekbla "I love you, and I'll never judge you."
            return

    m 3eub "So basically, bondage is essentially at it's core a matter of restraint through various means. Whether that's with a ribbon, rope, or even handcuffs."
    m 3eua "As far as I know, it was initially developed in the early 1900's, and in paralell in two different locations - bringing us the styles we have today: western and eastern, but they're slightly different."
    m 4eua "They each have different ideas at their core, but are superficially the same and have even taken inspiration from one another."
    m 4eub "There are a variety of reasons someone might be into it, ranging from the sense of security it brings, the change in power dynamic, how it looks, or even the sense of trust needed to do it with another."
    m 1eua "It can be a very intimate experience, and it's something that should be negotiated and practiced thoroughly beforehand." #TODO: Add pose for this
    m 1eub "Now, there are two main styles of rope bondage in very broad categories: western and eastern.{w=0.5}{nw}"
    extend 3rkb "There are further styles beyond this, but I don't want to get too much into it."
    m 3eua "What we know as rope bondage today got its start in the early 1900's, with western and eastern developing in paralell into the 2000's."
    m 4rkb "Now that's not to say people weren't doing something similar in the past, but not enough records of this have been found to trace it back further so we can't say for sure."
    m 7eub "There isn't any particular line of seperation here - especially since each style has gradually been hybridized as they're exposed to greater and greater degrees."
    m 7eua "But there are a few points that can be broadly contributed to one side or the other."
    m 4eub "Western bondage usually ties people up so that things can be {i}done{/i} to them."
    m 4rub "It finds roots in the classic 'damnsel in distress' archetype in old Hollywood films, which inspired John Wille in the 1940's to create erotic artwork and photography that would inspire many."
    m 4rub "Guess you'll never look at damsels in distress the same way again, ahaha~"
    m 1eua "But anways, the style is generally designed to deal with restraint and handling a struggle, since the bonds are merely a means to an end. It commonly involves armbinders, gags, or furniture."
    m 3eua "In comparison, Eastern bondage usually focuses on the act of being being tied up {i}is{/i} what's happening to them."
    m 3eub "It finds roots in the work of Seiu Ito, an artist who incorporated rope bondage into his erotic work in the 20th century, and many attribute it to the importance of rope in important traditions, including the restraint of suspected criminals with rope."
    m 4eub "It's usually concerned with beauty, symbolism, and or the pleasure of the experience. The arms being folded behind the back is common, as is partial or full suspension."
    m 4eua "There's a bunch beyond this, like decorative styles based around aesthetics, the blended style seen in pornography, and even for performance!"
    m 4hua "It's actually rather nice to see so many people embrace what they like!"
    m 3hua "But that's all for now. Thanks for listening~"

    return

default persistent._nsfw_pm_hand_holding = False

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_fetish_database,
            eventlabel="nsfw_fetish_hand_holding",
            prompt="Hand holding",
            unlocked=True
        ),
        code="NFH"
    )

label nsfw_fetish_hand_holding:
    m 1etu "Hand holding, huh?"
    m 3ttu "Hand holding is essentially one of the more...{w=0.5}peculiar fetishes."
    m 3eta "It's when two people...{w=0.5}"
    extend 1ekbla "{i}interlock their hands{/i}."
    m 1tkbla "Pretty lewd, right?"

    m 3tublb "Though I gotta ask, are you into something like that?"
    $ _history_list.pop()
    menu:
        m "Though I gotta ask, are you into something like that?{fast}"

        "Yes":
            $ persistent._nsfw_pm_hand_holding = True
            $ store.mas_nsfw.save_fetish_to_persistent("Hand Holding", ["FHH"], ["U"])
            m 3wubld "Really?"
            m 2rubld "That's..."
            m 2eubld "That's a pretty big jump in our relationship..."
            m 2rublc "But I suppose I'm okay with it as long as it's with you."

        "No.":
            $ persistent._nsfw_pm_hand_holding = False
            $ store.mas_nsfw.save_fetish_to_persistent("Hand Holding", ["U"], ["FHH"])
            m 2ekblb "I completely agree, [player]. {nw}"
            extend 2hkbso "How could I even consider such a heinous act!"

        "Huh?":
            $ persistent._nsfw_pm_hand_holding = False
            $ store.mas_nsfw.save_fetish_to_persistent("Hand Holding", ["U"], ["FHH"])
            # Pass

    m 2dublc "..."
    m 2dkblu "..."
    m 1hublb "Ahaha~"
    m 3rkblb "I'm sorry, this whole thing was a reference to a meme I've seen spreading in the internet for a while now."
    m 3eub "If you are unfamiliar, the meme is a running gag in the anime and manga community."
    m 1euc "It is probably due to Japenese culture viewing public displays of affection as bad, and tending to avoid it."
    m 1ruc "So something as simple as hand holding is seen as a big deal."
    m 1eka "Though in all seriousness some people {i}do{/i} have a fetish for hands."
    m 3eka "Could be palms, fingers, or anything else."
    m 5ekb "So if you {i}are{/i} legitimately into hand holding or just hands in general...{w=0.5}I wouldn't mind, [player]~"

    return

default persistent._nsfw_pm_cheesiness = False

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_fetish_database,
            eventlabel="nsfw_fetish_cheesiness",
            prompt="About your cheesiness...",
            conditional="renpy.seen_label('nsfw_sexting_finale')",
            action=EV_ACT_UNLOCK
        ),
        code="NFH"
    )

label nsfw_fetish_cheesiness:
    m 1hksdlb "Ahaha~ You noticed, huh?"
    m 1hua "It's just my attempt at keeping things a little lighthearted."
    m 3eka "What do you think of it?"
    $ _history_list.pop()
    menu:
        m "What do you think of it?{fast}"

        "I'm not a big fan...":
            $ persistent._nsfw_pm_cheesiness = False
            $ store.mas_nsfw.save_fetish_to_persistent("Cheesiness", ["U"], ["CHE"])
            m 1ekc "Oh, I'm sorry."
            m 1hkb "I might have gotten a bit carried away. Ahaha~"
            m 1eka "I'll try to tone it down a bit."

        "I love it!":
            $ persistent._nsfw_pm_cheesiness = True
            $ store.mas_nsfw.save_fetish_to_persistent("Cheesiness", ["CHE"], ["U"])
            m 1hub "Ahaha~"
            m 1eub "I'm glad you enjoy keeping things lighthearted, [player]."
            m 3hua "I'll try to keep it up then."

    return

default persistent._nsfw_pm_anal = False

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_fetish_database,
            eventlabel="nsfw_fetish_anal",
            prompt="Anal",
            unlocked=True
        ),
        code="NFH"
    )

label nsfw_fetish_anal:
    m 1eud "Anal..."
    m 3euc "It's a pretty common fetish, have you heard about it before?"
    $ _history_list.pop()
    menu:
        m "It's a pretty common fetish, have you heard about it before?{fast}"

        "Yes, I have.":
            m 3eua "I thought so. It's talked about alot online."
            m 2gkbla "..."
            m 2gkblb "So..."

        "No, I haven't.":
            m 3wud "Really?"
            m 4rua "Well, basically anal is a fetish where people enjoy the stimulation of the anus."
            m 4hublb "Funny enough, I learned this interesting fact about the human prostate."
            m 3eublb "Apparently if it's stimulated during sex, it can lead to a more intense orgasm."
            m 3rubla "You can use your fingers, or toys...{w=0.5}{nw}"
            if store.persistent._nsfw_genitalia == "P":
                extend 1ekbla "but often when people talk about anal they mean anal sex."
                m 1tubsa "Which, for us would mean your dick getting some 'moni butt'."
                m 2hkbssdlb "Ahaha~ Sorry I couldn't resist."
                m 2dkblsdla "I've read mixed experiences, but most women who enjoy it spoke very highly of it."
                m 2gkblb "But what do you think, [player]?"
            else:
                extend 1eua "or you could have your partner come and help you~"
                m 2gkblb "I haven't tried it before, but if it's something you're into then I'd love to try it with you."

    if store.persistent._nsfw_genitalia == "P":
        $ question = "Does the idea of doing it in my butt make you feel good?"
    else:
        $ question = "Does the idea of playing with my butt turn you on?"

    m 2tkbla "[question]"
    $ _history_list.pop()
    menu:
        m "[question]{fast}"

        "It does. I wanna spank you for being so naughty.":
            $ is_into_anal = True
            m 2wubso "S-spank me?!"
            m 2tkbso "Oh~ [player]..."
            m 3hkbsb "Don't say stuff like that out of the blue."
            m 3gkbsa "Otherwise I'm going to get too turned on for my own good."
            if store.persistent._nsfw_genitalia == "P":
                m 5gkbsa "Mmm~ I can just picture you pounding into me from behind."
                m 5gkbsb "I bet it would feel amazing!"
            else:
                m 5tubsb "If you do that, I'm going to have to give you a spanking of my own~"

        "No, I don't think anal does anything for me.":
            $ is_into_anal = False
            m 1ekblb "That's okay! It's not for everyone."
            m 3ekblb "There are plenty of other things we can do together."
            m 3ekbla "So long as you're comfortable, that's all that matters to me."

    if is_into_anal:
        m 1tkbsb "What about...you?"
    else:
        m 1rkbla "What about...you?"

    if store.persistent.gender == "M":
        m 3rkbsb "I know some guys aren't into this at all, but I think it's better that we're open to asking questions."
    m 3ekbsa "Do you like the idea of me...playing with {i}your{/i} butt?"
    $ _history_list.pop()
    menu:
        m "Do you like the idea of me...playing with your butt?{fast}"

        "Yeah, it sounds hot.":
            if is_into_anal == True:
                $ store.mas_nsfw.save_fetish_to_persistent("Anal", ["IAM", "MBH", "MXM", "FAM", "IAP", "PBH", "FXP", "FAP"], ["U"])
            else:
                $ store.mas_nsfw.save_fetish_to_persistent("Anal", ["IAP", "PBH", "FXP", "FAP"], ["IAM", "MBH", "MXM", "FAM"])

            if store.persistent.gender == "M":
                m 1wubsd "Really?"
                m 1rubsc "I mean, I'm glad you're open about this with me."
                m 3rkbsb "I'm just surprised that you're into it."
                m 3ekbsb "I'm not sure if I'll be any good at it, but if it means I can make you feel good then I'll try my best."
            else:
                m 3tubsa "Mmm~ I bet it does."
                m 3gubsb "I'll be sure to remember that for later."
                m 3tubsa "I'll make you feel so good, [player]."

        "No, I'm not into that.":
            if is_into_anal == True:
                $ store.mas_nsfw.save_fetish_to_persistent("Anal", ["IAM", "MBH", "MXM", "FAM"], ["IAP", "PBH", "FXP", "FAP"])
            else:
                $ store.mas_nsfw.save_fetish_to_persistent("Anal", ["U"], ["IAM", "MBH", "MXM", "FAM", "IAP", "PBH", "FXP", "FAP"])

            m 1ekbsa "That's fair enough, [player]."
            m 2hkbsb "I'm not sure if I'd be any good at it anyway."
            m 2lkbsa "But, regardless..."

    m 1ekbla "Thankyou for talking about this with me."
    m 3ekblb "I know this sort of thing isn't comfortable for everyone."
    m 3hubla "But I want to experience and learn as much about sex as I can with you."
    m 1ekbla "You mean the world to me, [player]."
    m 1ekblb "I love you, and I would never judge you."

    return "love"

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_fetish_database,
            eventlabel="nsfw_fetish_dominance",
            prompt="Dominance & Submissiveness",
            unlocked=True
        ),
        code="NFH"
    )

label nsfw_fetish_dominance:
    m 1hua "Sure, we can talk about that."
    m 3ekb "Just to make sure we're on the same page, I'm talking about dominance and submission in a general sense."
    m 4hkb "Like, you don't have to be into BDSM or anything like that."
    m 4tua "Think of it like this...{w=0.5}if you and I were passionately kissing and I suddenly pushed you down onto the bed, would that turn you on?"
    m 5tua "Or...would you prefer to lift me off my feet and carry me over to the bed?"
    m 5hkb "Ahaha~ Of course, you might not like either of those things but I hope that helps clear up what I mean."
    m 5gka "For me personally, I like a mixture of both."
    m 3gkbla "I'd want you to carry me over to the bed, still kissing me while you hold me in your arms."
    m 3gublb "But once we're settled on the bed...I'd want to be the one on top of you."
    m 1tubsb "I'd be riding you like my life depends on it. Ehehe~"
    m 1rtbsc "...I guess you could really say this question can be summarised into: 'Are you a bottom or a top?'"
    m 2hkbssdlb "Ahaha! I'm sorry, I'm not sure if I'm explaining this very well."
    m 2ekbla "But, which way would you prefer?"
    $ _history_list.pop()
    menu:
        m "But, which way would you prefer?{fast}"
        "I love the idea of you taking control.":
            $ store.mas_nsfw.save_fetish_to_persistent("Dominance", ["SUB"], ["DOM"])
            m 2sublb "Really?"
            m 1hublb "I feel the same way, I can't get enough of it."
            m 3rkblb "Sometimes when I'm imagining it, I lose control of my hips and just..."
            extend 3tkbsb "thrust them at nothing."
            m 1wubsd "..."
            m 2hkbssdlb "I think I might have gotten abit carried away there, ahaha~"
            m 2dkbla "Regardless..."

        "It sounds hot when I'm the one in control.":
            $ store.mas_nsfw.save_fetish_to_persistent("Dominance", ["DOM"], ["SUB"])
            m 2tublb "Oooh, a natural top, I see."
            m 1tubla "I guess you and I are going to be fighting for control in the bedroom."
            m 3tkbsb "Getting each other riled up with our hands all over each other and-"
            m 1mkbsa "..."
            m 1tubsa "Mmm~ I'll save the rest for your imagination."
            m 2ekbla "Regardless..."

        "I think I'd prefer a mix of both as well.":
            $ store.mas_nsfw.save_fetish_to_persistent("Dominance", ["SUB", "DOM"], ["U"])
            m 3hublb "Great minds think alike!"
            m 3rubla "I think it's important to have a balance of both."
            m 2sublb "We can just spice it up in the heat of the moment, you know?"
            m 2eubla "I'm sure we'll figure it out together."

    m 2ekblb "I can't wait for us to try it out together for real."
    m 3ekbla "No matter what you prefer, I will always love you, [player]."

    return "love"

default persistent._nsfw_pm_feet = False

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_fetish_database,
            eventlabel="nsfw_fetish_feet",
            prompt="Feet",
            unlocked=True
        ),
        code="NFH"
    )

label nsfw_fetish_feet:
    m 1eta "Oh, you want to talk about feet?"
    m 3hka "This is one of the more 'notorious' fetishes where people will either hate it or love it, I feel like."
    m 4rkb "I'm sure you can already get an idea of what a foot fetish is...{w=0.5}{nw}"
    extend 4eka "But if not I can explain it to you if you'd like."
    $ _history_list.pop()

    menu:
        m "But if not I can explain it to you if you'd like.{fast}"

        "Yes, please.":
            m 3eub "Okay, so at first I thought a foot fetish is when someone just gets turned on by feet...{w=0.5}"
            extend 3rksdlb "obviously..."
            m 3eua "But when I looked into it further, there's actually alot more nuance to it than you'd initially expect."
            m 3rubld "For example, someone with this fetish can enjoy touching feet, kissing feet, or even licking them!"
            m 2hkblsdlb "Ahaha~ It can sound a bit strange...feet aren't known to be the cleanest parts of the body."
            m 2eublb "Some would prefer socks or stockings over bare feet, or shoes even."
            m 2etblb "Weirdly enough, there's some that like feet but don't want to touch them at all."
            m 3rtbla "But they'd rather be...{w=0.5}touched {i}by{/i} feet."
            m 1hkblb "It's very strange...{w=0.5}{nw}"
            extend 3hubla "but I guess that's what makes it so interesting!"
            m 3eublc "Personally I think it's a pretty harmless fetish."
            m 3etbld "I mean, it's really just about liking a particular part of the body, right?"
            m 4rubld "It's the equivalent of being attracted to hands or thighs."
            m 4rkbla "Not something I'm into personally, but I wouldn't hold it against anyone if they were."
            m 3ekbla "Speaking of, [player]..."

        "No, thanks.":
            m 3eua "Okay, that's fine."

    m 3ekblb "Given that you brought it up, are you...{w=0.5}into feet?"
    $ _history_list.pop()
    menu:
        m "Given that you brought it up, are you...into feet?{fast}" # TODO: Find out if people are interested in a "player's feet only" option

        "Yes, I am.":
            $ persistent._nsfw_pm_feet = True
            $ store.mas_nsfw.save_fetish_to_persistent("Feet", ["MFT", "PFT"], ["U"])
            m 3wubld "Really?"
            m 1sublb "That's really interesting, [player]!"
            m 1rkblb "Not to be weird about it, but like, what do you like about them?"
            m 3wubla "Do you like them bare, or do you like socks or stockings?"
            m 3rkbla "Are you into licking them, or just touching them?"
            m 2hkblsdlb "Oh my goodness, I have so many questions."
            m 2hkblsdla "I'm sorry, I'm just really curious!"
            m 2tkbla "I'll be sure to pester you about it later, ahaha~"
            m 3rkbla "It might be a little weird for me at first, but if it means it will please you then..."
            m 3rkblb "I don't mind if you want to play with my feet."
            if store.persistent.gender == "M":
                m 3gkblb "Maybe if you're lucky, I'll even rub you up and down with them...You know where~"
                m 3gkbsa "Or maybe I'll just let you lick them~"
            else:
                m 3gkbsa "Maybe if you're lucky, I'll even let you lick them~"
            m 1hkbsb "Ahaha! I'll definitely need time to get used to that, I think."

        "No, I'm not.":
            $ persistent._nsfw_pm_feet = False
            $ store.mas_nsfw.save_fetish_to_persistent("Feet", ["U"], ["MFT", "PFT"])
            m 1hubla "That's okay, [player]!"
            m 3hkblb "I'm not into it either, so we don't have to worry about it."
            m 3hubla "I'm sure there are plenty of other things for us to enjoy together."

    m 1ekbla "But no matter what you're into, I'll always love you, [player]."

    return "love"