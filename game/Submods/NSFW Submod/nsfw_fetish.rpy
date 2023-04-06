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
# Also noting that the 'context' used here is intended to coincide with sexting, so the prompts are appropriate to the player


default persistent._nsfw_pm_bondage = False
default persistent._nsfw_pm_bondage_context = ["U"] # ["FBM"] for Giving, ["FBP"] for Receiving, ["FBM", "FBP"] for both, ["U"] for Undefined

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
    m 1eua "Okay, let's talk about bondage."
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
                    $ persistent._nsfw_pm_bondage_context = ["FBM"]
                    m 3eubld "Oh?"
                    m 3rubla "I haven't really done something like this before..."
                    m 1ekbla "But I trust you, and if this is something you want to try..."
                    m 5ekbla "I'll do my best to make sure you enjoy yourself."
                    m 5tublb "Who knows? Maybe I'll even enjoy it {i}too{/i} much~"

                "Recieving":
                    $ persistent._nsfw_pm_bondage_context = ["FBP"]
                    m 5tubla "Oh?"
                    m 5tublb "Then I guess I'd better start practicing my knots~"

                "Both":
                    $ persistent._nsfw_pm_bondage_context = ["FBM", "FBP"]
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

default persistent._nsfw_pm_anal = False
default persistent._nsfw_pm_anal_context = ["U"] # ["IAM", "MBH", "MXM", "FAM"] for Giving, ["IAP", "PBH", "FXP", "FAP"] for Recieving, ["IAM", "MBH", "MXM", "FAM", "IAP", "PBH", "FXP", "FAP"] for both, ["U"] for Undefined

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
    m 2eud "Anal..."
    m 2rua "It's a pretty common fetish, and I'm sure you've heard of it before."
    m 3eubla "But in case you aren't aware, anal refers to the sexual stimulation of the anus."
    m 3eublb "It's interesting to learn, but the human prostate has a very interesting property."
    m 3wubld "It's been said that stimulating it during sex can lead to a more intense orgasm."
    m 4eubld "Some people say they prefer anal sex because of the feeling that it gives."
    m 3eubla "But, in any case..."
    m 1ekblb "Is anal something you are into?"
    $ _history_list.pop()
    menu:
        m "Is anal something you are into?{fast}"

        "Yes":
            $ persistent._nsfw_pm_anal = True
            m 3hublb "That's great!"
            m 3hubla "I feel like I'm getting to know more about you every day!"
            m 3eubla "Would you prefer giving, recieving, or both?"
            $ _history_list.pop()
            menu:
                m "Would you prefer giving, recieving, or both?{fast}"
                "Giving":
                    $ persistent._nsfw_pm_anal_context = ["IAM", "MBH", "MXM", "FAM"]
                    m 1tubla "Oh?"
                    m 2tublb "You want to get a good view back there, do you?"
                    m 1hublb "Ahaha~ Just teasing you, [player]."

                "Recieving":
                    $ persistent._nsfw_pm_anal_context = ["IAP", "PBH", "FXP", "FAP"]
                    m 1wubld "Really?"
                    if persistent._nsfw_genitalia = "P":
                        m 1rubld "I'm surprised."
                        m 1wubso "Not in a bad way or anything."
                        m 2rubsd "I just...didn't expect that from you."
                        m 2rkbsc "I don't know if I'm going to be able to do it right..."
                        m 1ekbsa "But if it will make you happy, I'll do my best."
                    elif persistent._nsfw_genitalia = "V":
                        m 1hubla "I suppose I wouldn't mind giving it a try."
                        m 3tkblb "I'll make sure you feel good~"
                    else:
                        m 1eubla "Well, I guess I'll have to try it out."
                        m 3tkblb "I want to make sure you feel good, [player]."

                "Both":
                    $ persistent._nsfw_pm_anal_context = ["IAM", "MBH", "MXM", "FAM", "IAP", "PBH", "FXP", "FAP"]
                    m 1tubla "Both, hey?"
                    m 1tublb "A giver, and a receiver..."
                    m 1tubsa "I'm happy to hear that, [player]."
                    m 3tkbsb "We can each take turns to satisfy one another~"

        "No":
            m 1hubla "Alright, [player]."

    m 3rubla "As for me, I'm willing to experiment."
    m 2ekbla "I've only just begun to explore my sexuality thanks to you, so I'm not sure what I'm into yet."
    m 2ekblb "You've helped me discover a lot of things about myself, and I'm sure there's more to come."
    m 5ekblb "I love you, and I'm willing to try anything with you, [player]."

    return "love"

default persistent._nsfw_pm_dominance = ["U"] # ["command", "FSM"] for Dom, ["FSP"] for Sub, ["command", "FSM", "FSP"] for Switch, ["U"] for Undefined

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
    m 3eub "On the one side, you have the dominant."
    m 3tub "They are the ones who take control."
    m 5eua "And on the other side, is the submissive."
    m 5eub "They are the ones who give up control."
    m 3rua "A switch is someone who can be either."
    m 3eua "They can be the dominant one moment, and the submissive the next."
    m 1eua "Which would you say you are, [player]?"
    m 1eka "If you're not sure, I can describe each one to you."
    m 1ekblb "Would you like that?"
    $ _history_list.pop()
    menu:
        m "Would you like that?{fast}"
        "Yes.":
            m 1hubla "Okay!"
            m 3eublb "The best way to think of a dom-sub relationship is like a consesual, eroticized exchange of power." # Cynthia Slater's words
            m 3rua "The dominant is the one who takes control."
            m 4gua "They are the assertive ones, with their role being to lead, guide, and protect."
            m 4eubla "It's basically their job to lead how the sex plays out, and that their partner is safe while doing so."
            m 5eubla "The submissive is the one who gives control."
            m 5eublb "They are required to surrender themselves to the dominant, and to trust them to lead."
            m 5rublb "Think of them like they are giving in to the dominant's will."
            m 5eubla "Sometimes a person can also be either."
            m 1eublb "One moment they like being the dominant one, and the next they are wanting to surrender themselves to their partner."
            m 1eubla "This can even be done in the same session, if they so choose."
            m 3eubla "They are probably the most adaptive to any given lover, since they can take on the role of either."
            m 3tubla "So, based on what I've just told you..."

        "No.":
            m 1hubla "Okay, [player]."
            m 3tubla "So then..."

    m 3tublb "Are you a dominant, a submissive, or both?"
    $ _history_list.pop()
    menu:
        m "Are you a dominant, a submissive, or both?{fast}"
        "Dominant":
            $ persistent._nsfw_pm_dominance = ["FSM"]
            m 3tubla "A dominant, huh?"
            m 3gubla "I can see it."
            m 5tubla "You seem like the sort of person who likes to take charge."
            m 5tublb "And I'm all here for it~"

        "Submissive":
            $ persistent._nsfw_pm_dominance = ["FSP"]
            m 3tubla "A submissive, huh?"
            m 3gubla "I can see it."
            m 1kubla "You seem like the sort of person who likes to be told what to do."
            m 1ekbla "It's cute~"
            m 5tublb "Makes me want to take care of you..."
            m 5tubla "Ehehe~"

        "Both":
            $ persistent._nsfw_pm_dominance = ["FSM", "FSP"]
            m 3tubla "A switch, huh?"
            m 3gubla "I can see it."
            m 1ekbla "You strike me as a cooperative person."
            m 1ekblb "Wanting to please your partner, and being willing to do whatever they want."
            m 5eublb "That is something I love about you~"

    m 5gublu "As for me?"
    m 5rublb "Well...I suppose I wouldn't mind being either." #As a way to explain Monika being accepting of every option.
    if persistent._nsfw_pm_dominance == "B":
        m 5hubla "Guess we are the same in that regard."
        m 5hublb "We both like to please our partners."
        m 1dublb "And we both like to be pleased."
    else:
        m 5rkbla "I'm willing to try anything, but I'm not sure what I prefer."
        m 5tkbla "I guess I'll have to experiment with you."
        m 1tkbla "Not that I mind~"

    m 1eublb "In any case..."
    m 3ekbla "Regardless of what you prefer, I will always love you, [player]."

    return "love"