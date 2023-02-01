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

label nsfw_player_fetishintro: #TODo: Finish adding expressions
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


default persistent.nsfw_pm_bondage = False
default persistent.nsfw_pm_bondage_context = "U" #G for Giving, R for Recieving, B for both, U for Undefined

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
    m 1eua "Bondage is essentially at it's core, a matter of restraint through various means. Whether that's ribbon, rope, or even handcuffs."
    m 1eua "As far as I know, it was initially developed in the early 1900's, and in paralell in two different locations - bringing us the styles we have today: western and eastern, but that's slightly different."
    m 1eua "They each have different ideas at their core, but are superficially the same and have even taken inspiration from one another. I can explain more about the history later if you want."
    m 1eua "There are a variety of reasons someone might be into it, ranging from the sense of security it brings, the change in power dynamic, how it looks, or even the sense of trust needed to do it with another."

    m 1eua "Though with that well and done, what do you think, [player]? Do you think you'd like to try it out?"
    $ _history_list.pop()
    menu:
        m "Though with that well and done, what do you think, [player]? Do you think you'd like to try it out?{fast}"
        "Yes":
            $ persistent._nsfw_pm_bondage = True
            m 2tkbsb "Okay!"

            m 1eua "Would you prefer giving, recieving, or both?"
            $ _history_list.pop()
            menu:
                    m "Would you prefer giving, recieving, or both?{fast}"
                    "Giving":
                        $ persistent._nsfw_pm_bondage_context = "G"
                        m 1eua "Okay!"
                        m 1eua "While I'd love to respond in an appropriate manner, the Dev can't think of anything good right now."
                        m 1eua "Maybe another time."

                    "Recieving":
                        $ persistent._nsfw_pm_bondage_context = "R"
                        m 1eua "Oh?"
                        m 1eua "Then I guess I'd better start practicing my knots~"

                    "Both":
                        $ persistent._nsfw_pm_bondage_context = "B"
                        m 1eua "Guess we'd better start practicing our knots in the meantime, huh?"
        "No":
            $ persistent._nsfw_pm_bondage = False
            m 1hubsb "Alright, [player]."
            m 1eua "Guess I'll put away these handcuffs for now." #Smirk
    m 1eua "Ahaha~"
    m 1eua "You look so cute when you're flustered."

    m 1eua "Would you like to hear more about it? "
    extend "Though I don't mind if you say no, it's a lot to go through." #Big ol' smile.
    $ _history_list.pop()
    menu:
        m "Would you like to hear more about it? Though I don't mind if you say no, it's a lot to go through.{fast}"
        "Yes":
            m 1eua "I'm glad!"
            m 1eua "Now, there are three main styles of rope bondage in very broad categories: western and eastern. There are further styles beyond this, but I don't want to get too much into it."
            m 1eua "What we know as rope bondage today got its start in the early 1900's, with western and eastern developing in paralell into the 2000's."
            m 1eua "Now that's not to say people weren't doing something similar in the past, but not enough records of this have been found to trace it back further so we can't say for sure."
            m 1eua "There isn't any particular line of seperation here - especially since each style has gradually been hybridized as they're exposed to greater and greater degrees."
            m 1eua "But there are a few points that can be broadly contributed to one side or the other."
            m 1eua "Western bondage usually ties people up so that things can be {i}done{/i} to them. It finds roots in the classic 'dansel in distress' archetype in old Hollywood films, which inspired John Wille in the 1940's to create erotic artwork and photography that would inspire many."
            m 1eua "Guess you'll never look at dansels in distress the same way again, ahaha~"
            m 1eua "But anways, the style is generally designed to deal with restraint and handling a strugle, since the bonds are merely a means to an end. It commonly involves armbinders, gags, or furniture."
            m 1eua "In comparison, Eastern bondage usually focuses on the act of being being tied up {i}is{/i} what's happening to them. It finds roots in the work of Seiu Ito, an artist who incorporated rope bondage into his erotic work in the 20th century, and many attribute it to the importance of rope in important traditions, including the restraint of suspected criminals with rope."
            m 1eua "It's usually concerned with beauty, symbolism, and or the pleasure of the experience. The arms being folded behind the back is common, as is partial or full suspension."
            m 1eua "There's a bunch beyond this, like decorative styles based around aesthetics, the blended style seen in pornography, and even for performance!"
            m 1eua "It's actually rather nice to see so many people embrace what they like!"
            m 1eua "But that's all for now. Thanks for listening~"

        "No":
            m 1eua "That's okay. Let me know if you change your mind."
    return

default persistant.nsfw_pm_hand_holding = False

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

label nsfw_fetish_hand_holding: #TODO: Finish adding expressions
    m 1eua "Alright!"
    m 1eua "Hand holding is essentially one of the more...out there fetishes."
    m 1eua "It's when two people {i}clasp their hands around one another{/i}."
    m 1eua "Pretty lewd, right?"

    m 1eua "Though I gotta ask, are you into something like that?"
    $ _history_list.pop()
    menu:
        m "Though I gotta ask, are you into something like that?{fast}"
        "Yes":
            $ persistent._nsfw_pm_hand_holding = True
            m 2tkbsb "It's a pretty big jump...but I suppose I'm okay with it as long as it's with you."

        "No":
            $ persistent._nsfw_pm_hand_holding = False
            m 1hubsb "I completely agree, [player]. {nw}"
            extend 1eua "How could I even consider such a heinous act!"

    m 1eua "Ahaha~"
    m 1eua "This whole thing was a reference to a meme I've seen spreading in the internet for a while now."
    m 1eua "Though in all seriousness some people {i}do{/i} have a fetish for hands."
    m 1eua "Could be palm, fingers, or anything else."
    m 1eua "I'd usually unlock the option to go into further detail at this point, but that one's a work in progress for now. Sorry!"
    m 1eua "Though if you {i}are{/i} into hand holding, I wouldn't mind [player]~"
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
    m 1hkblsdlb "AnalTest"
    $ _history_list.pop()
    menu:
        m "AnalTest{fast}"
        "Yes":
            $ persistent._nsfw_pm_anal = True

            m 2tkbsb "YesConfirm"
            $ _history_list.pop()
            menu:
                m "YesConfirm"
                "Giving":
                    $ persistent._nsfw_pm_anal_context = "G"

                "Recieving":
                    $ persistent._nsfw_pm_anal_context = "R"

                "Both":
                    $ persistent._nsfw_pm_anal_context = "B"

        "No":
            m 1hubsb "NoConfirm"
    return

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
    m 1hkblsdlb "DominanceTest"
    $ _history_list.pop()
    menu:
        m "DominanceTest{fast}"
        "Dominance":
            $ persistent._nsfw_pm_dominance = "D"
            m 2tkbsb "DomConfirm"

        "Submission":
            $ persistent._nsfw_pm_dominance = "S"
            m 1hubsb "SubConfirm"

        "Both":
            $ persistent._nsfw_pm_dominance = "B"
            m 1hubsb "SwitchConfirm"

    m "As for me?"
    m "Well...I suppose I wouldn't mind being either." #As a way to explain Monika being accepting of every option.
    return
