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

        mas_gainAffection()

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

label nsfw_player_fetishintro: #TODO: Finish adding expressions
    m 1eua "Hey, [player]. I just wanted to tell you about some work I've done!"
    m 1eua "You remember talking with me about fetishes?"
    m 1eua "...Well I made something so that we could talk about them."
    m 1eua "I'm not very...{i}experienced{/i} with sexual things like this, so I've been looking into them!"
    m 1eua "And at the end"
    extend 2eua "...you get to tell me if you're into it or not."
    m 1eua "Don't worry! You can change your mind whenever, I don't mind."
    m 1eua "I'd love to help you explore your fetishes, [player]. Ahaha~"
    $ mas_unlockEventLabel("nsfw_player_fetishes")
return

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


default persistent._nsfw_pm_bondage = False
default persistent._nsfw_pm_bondage_context = "U" #G for Giving, R for Recieving, B for both, U for Undefined

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

label nsfw_fetish_bondage: #TODO: Finish adding expressions
    m 3eub "Bondage is essentially at it's core, a matter of restraint through various means. Whether that's with a ribbon, rope, or even handcuffs."
    m 3eua "As far as I know, it was initially developed in the early 1900's, and in paralell in two different locations - bringing us the styles we have today: western and eastern, but they're slightly different."
    m 4eua "They each have different ideas at their core, but are superficially the same and have even taken inspiration from one another. I can explain more about the history later if you want."
    m 4eub "There are a variety of reasons someone might be into it, ranging from the sense of security it brings, the change in power dynamic, how it looks, or even the sense of trust needed to do it with another."
    m 7ekbla "Though with that being said, what do you think, [player]? Do you think you'd like to try it out?"
    $ _history_list.pop()
    menu:
        m "Though with that being said, what do you think, [player]? Do you think you'd like to try it out?{fast}"
        "Yes":
            $ persistent._nsfw_pm_bondage = True
            m 3hublb "That's great!"
            m 3hubla "I feel like I'm getting to know more about you every day!"
            m 3eubla "From what I've said, would you prefer giving, recieving, or both?"
            $ _history_list.pop()
            menu:
                m "Would you prefer giving, recieving, or both?{fast}"

                "Giving":
                    $ persistent._nsfw_pm_bondage_context = "G"
                    m 3eubld "Oh?"
                    m 3rubla "I haven't really done something like this before..."
                    m 1ekbla "But I trust you, and if this is something you want to try..."
                    m 5ekbla "I'll do my best to make sure you enjoy yourself."
                    m 5tublb "Who knows? Maybe I'll even enjoy it {i}too{/i} much~"

                "Recieving":
                    $ persistent._nsfw_pm_bondage_context = "R"
                    m 5tubla "Oh?"
                    m 5tublb "Then I guess I'd better start practicing my knots~"

                "Both":
                    $ persistent._nsfw_pm_bondage_context = "B"
                    m 5tubla "Oh?"
                    m 5tublb "Guess we'd better start practicing our knots in the meantime, huh?"

        "No":
            $ persistent._nsfw_pm_bondage = False
            m 1hubla "Alright, [player]."
            m 5tublb "Guess I'll put away these handcuffs for now." #Smirk

    m 5hublb "Ahaha~"
    m 1hublb "You look so cute when you're flustered."
    m 3eubla "Would you like to hear more about it? "
    extend 3ekbla "Though I don't mind if you say no, it's a lot to go through." #Big ol' smile.

    $ _history_list.pop()
    menu:
        m "Would you like to hear more about it? Though I don't mind if you say no, it's a lot to go through.{fast}"
        "Yes":
            m 1hua "I'm glad!"
            m 1eub "Now, there are three main styles of rope bondage in very broad categories: western and eastern.{w=0.5}{nw}"
            extend 3rkb "There are further styles beyond this, but I don't want to get too much into it."
            m 3eua "What we know as rope bondage today got its start in the early 1900's, with western and eastern developing in paralell into the 2000's."
            m 4rkb "Now that's not to say people weren't doing something similar in the past, but not enough records of this have been found to trace it back further so we can't say for sure."
            m 7eub "There isn't any particular line of seperation here - especially since each style has gradually been hybridized as they're exposed to greater and greater degrees."
            m 7eua "But there are a few points that can be broadly contributed to one side or the other."
            m 4eub "Western bondage usually ties people up so that things can be {i}done{/i} to them."
            m 4rub "It finds roots in the classic 'dansel in distress' archetype in old Hollywood films, which inspired John Wille in the 1940's to create erotic artwork and photography that would inspire many."
            m 4rub "Guess you'll never look at dansels in distress the same way again, ahaha~"
            m 1eua "But anways, the style is generally designed to deal with restraint and handling a strugle, since the bonds are merely a means to an end. It commonly involves armbinders, gags, or furniture."
            m 3eua "In comparison, Eastern bondage usually focuses on the act of being being tied up {i}is{/i} what's happening to them."
            m 3eub "It finds roots in the work of Seiu Ito, an artist who incorporated rope bondage into his erotic work in the 20th century, and many attribute it to the importance of rope in important traditions, including the restraint of suspected criminals with rope."
            m 4eub "It's usually concerned with beauty, symbolism, and or the pleasure of the experience. The arms being folded behind the back is common, as is partial or full suspension."
            m 4eua "There's a bunch beyond this, like decorative styles based around aesthetics, the blended style seen in pornography, and even for performance!"
            m 4hua "It's actually rather nice to see so many people embrace what they like!"
            m 3hua "But that's all for now. Thanks for listening~"

        "No":
            m 3hua "That's okay. Let me know if you change your mind."
    return

default persistant._nsfw_pm_hand_holding = False
# Could maybe add hands as a legit fetish alongside handholding

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
            m 3wubld "Really?"
            m 2rubld "That's..."
            m 2eubld "That's a pretty big jump in our relationship..."
            m 2rublc "but I suppose I'm okay with it as long as it's with you."

        "No":
            $ persistent._nsfw_pm_hand_holding = False
            m 2ekblb "I completely agree, [player]. {nw}"
            extend 2hkbso "How could I even consider such a heinous act!"

        "Huh?":
            $ persistent._nsfw_pm_hand_holding = False
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

default persistent.nsfw_pm_anal = False
default persistent.nsfw_pm_anal_context = "U" #G for Giving, R for Recieving, B for both, U for Undefined

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

label nsfw_fetish_anal: #TODO: Finish adding expressions
    m 1eua "Anal, huh?"
    m 1eua "It's a pretty common fetish, and I'm sure you've heard of it before."
    m 1eua "But in case you aren't aware, anal refers to the sexual stimulation of the anus."
    m 1eua "Whilst the reasoning people give for choosing anal sex over vaginal sex varies, many can see it as simply a personal preference."
    m 1eua "With that being said, is anal something you are into?"
    $ _history_list.pop()
    menu:
        m "With that being said, is anal something you are into?{fast}"

        "Yes":
            $ persistent._nsfw_pm_anal = True
            m 3hublb "That's great!"
            m 3hubla "I feel like I'm getting to know more about you every day!"
            m 3eubla "From what I've said, would you prefer giving, recieving, or both?"
            $ _history_list.pop()
            menu:
                m "From what I've said, would you prefer giving, recieving, or both?{fast}"
                "Giving":
                    $ persistent._nsfw_pm_anal_context = "G"
                    m 1eua "Oh?"
                    m 1eua "You want to get a good view back there, do you?"
                    m 1eua "Ahaha~ Just teasing you, [player]."

                "Recieving":
                    $ persistent._nsfw_pm_anal_context = "R"
                    m 1eua "Really?"
                    if persistent._nsfw_genitalia = "P":
                        m 1eua "I'm surprised."
                        m 1eua "Not in a bad way or anything."
                        m 1eua "I don't know if I'm going to be able to do it right..."
                        m 1eua "But if it will make you happy, I'll do my best."
                    elif persistent._nsfw_genitalia = "V":
                        m 1eua "I suppose I wouldn't mind giving it a try."
                        m 1eua "I'll make sure you feel good~"
                    else:
                        m 1eua "Well, I guess I'll have to try it out."
                        m 1eua "I want to make sure you feel good, [player]."

                "Both":
                    $ persistent._nsfw_pm_anal_context = "B"
                    m 1eua "Both, hey?"
                    m 1eua "A giver, and a receiver..."
                    m 1eua "I'm happy to hear that, [player]."
                    m 1eua "We can each take turns to satisfy one another~"

        "No":
            m 1hubla "Alright, [player]."

    m 1eua "As for me, I'm willing to experiment."
    m 1eua "I've only begun to explore my sexuality, so I'm not sure what I'm into yet."
    m 1eua "You've helped me discover a lot of things about myself, and I'm sure there's more to come."
    m 1eua "I love you, and I'm willing to try anything with you, [player]."
    return "love"

default persistent.nsfw_pm_dominance = "U" #D for Dom, S for Sub, B for Switch, U for Undefined

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_fetish_database,
            eventlabel="nsfw_fetish_dominance",
            prompt="Dominance",
            unlocked=True
        ),
        code="NFH"
    )

label nsfw_fetish_dominance: #TODO: Finish adding expressions
    m 1eua "Dominance, huh?"
    m 1eua "I guess people's sexual preferences can be categorised into three main groups."
    m 1eua "The first is the dominant, and the second is the submissive."
    m 1eua "The dominant is the one who takes control, and the submissive is the one who gives control."
    m 1eua "I suppose by the same logic, a switch is someone who can be either."
    m 1eua "Which would you say you are, [player]?"
    m 1eua "If you're not sure, I can describe each one to you."
    m 1eua "Would you like me to explain?"
    $ _history_list.pop()
    menu:
        m "Would you like me to explain?{fast}"
        "Yes."
            m 1eua "Okay!"
            m 1eua "The dominant is the one who takes control."
            m 1eua "They are the one who decides what happens, and when."
            m 1eua "And they are often the ones to initiate."
            m 1eua "You could say they like being the boss, ahaha~"
            m 1eua "Anyway, the submissive is the one who gives control."
            m 1eua "They are the one who is told what to do, and when."
            m 1eua "And they are often the ones to be initiated upon."
            m 1eua "This is not always the case, however."
            m 1eua "Sometimes the submissive one can be the one to inititate, but during the act the dominant one takes control."
            m 1eua "A switch is someone who can be either."
            m 1eua "They can be the dominant one moment, and the submissive the next."
            m 1eua "They can be the one to initiate, and the one to be initiated upon."
            m 1eua "It can even happen mid-act!"
            m 1eua "They are probably the most adaptive to any given lover, since they can take on the role of either."
            m 1eua "So, based on what I've just told you..."

        "No."
        m 1eua "Okay, [player]."
        m 1eua "So then..."

    m 1eua "Are you a dominant, a submissive, or a switch?"
    $ _history_list.pop()
    menu:
        m "DominanceTest{fast}"
        "Dominance":
            $ persistent._nsfw_pm_dominance = "D"
            m 1eua "A dominant, huh?"
            m 1eua "I can see it."
            m 1eua "You seem like the sort of person who likes to take charge."
            m 1eua "And I'm all here for it~"

        "Submission":
            $ persistent._nsfw_pm_dominance = "S"
            m 1eua "A submissive, huh?"
            m 1eua "I can see it."
            m 1eua "You seem like the sort of person who likes to be told what to do."
            m 1eua "It's cute~"
            m 1eua "Makes me want to take care of you...."
            m 1eua "Ehehe~"

        "Both":
            $ persistent._nsfw_pm_dominance = "B"
            m 1eua "A switch, huh?"
            m 1eua "I can see it."
            m 1eua "You strike me as a cooperative person."
            m 1eua "Wanting to please your partner, and being willing to do whatever they want."
            m 1eua "That is something I love about you~"

    m 1eua "As for me?"
    m 1eua "Well...I suppose I wouldn't mind being either." #As a way to explain Monika being accepting of every option.
    if persistent._nsfw_pm_dominance == "B":
        m 1eua "Guess we are the same in that regard."
        m 1eua "We both like to please our partners."
        m 1eua "And we both like to be pleased."
    else:
        m 1eua "I'm willing to try anything, but I'm not sure what I prefer."
        m 1eua "I guess I'll have to experiment with you."
        m 1eua "Not that I mind~"

    m 1eua "Regardless of what you prefer, I will always love you, [player]."
    return "love"
