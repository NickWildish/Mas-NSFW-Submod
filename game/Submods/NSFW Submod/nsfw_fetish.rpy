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
    m 1eua "You want to talk about bondage?"
    m 1eua "Sure! I'd love to get to know your opinion on it."
    m 1eua "Have you heard of it before?"
    $ _history_list.pop()
    menu:
        m "Have you heard of it before?{fast}"

        "Yes, I have.":
            m 1eua "Oh, that's great!"

        "No, I haven't.":
            m 1eua "Hmm...{w=0.5}Well it's a really interesting topic."
            m 1eua "Basically, it's when people use restraints such as rope to tie people up in all kinds of positions."
            m 1eua "That can be used for sex, but it can also be used for domination or playtime between lovers."

    m 1eua "Does it sound like something that interests you?"
    $ _history_list.pop()
    menu:
        m "Does it sound like something that interests you?{fast}"

        "Yeah, it sounds pretty hot.":
            m 1eua "Yeah? You think so?"
            m 1eua "I think it's very hot!"
            m 1eua "If I'm honest, it kinda turns me on. Just the thought of tying you up and..."
            m 1eua "Mmm~ I think I've said too much."
            m 1eua "But speaking of which, would you prefer to be the one tying me up, or the one being tied up in this...{w=0.5}{i}hypothetical{/i} scenario?"
            $ _history_list.pop()
            menu:
                m "Speaking of which, would you prefer to be the one tying me up, or the one being tied up in this...{i}hypothetical{/i} scenario?{fast}"

                "I'd want to tie you up and have my way with you.":
                    $ store.mas_nsfw.save_fetish_to_persistent("Bondage", ["FBM"], ["FBP"])
                    m 1eua "Hehe~ Well, if that's what you want you just say when, silly."
                    m 1eua "I wouldn't mind surrendering a little power {i}juuuuust{/i} this once for you~"

                "I think you should tie me up and do what you want with me.":
                    $ store.mas_nsfw.save_fetish_to_persistent("Bondage", ["FBP"], ["FBM"])
                    m 1eua "Oooh! I like where this is going."
                    m 1eua "Hmm...{w=0.5}I'll have to remember that next time we're getting naughty~"
                    m 1eua "I'll describe how I'll tie you to my bed, and tease you until you can't stand it anymore."

                "I wouldn't mind trying both. I'm here to please.":
                    $ store.mas_nsfw.save_fetish_to_persistent("Bondage", ["FBM", "FBP"], ["U"])
                    m 1eua "Aww~ [player], you've always been such a people pleaser."
                    m 1eua "I love that about you."
                    m 1eua "Makes me want to tie you up and have you all to myself..."
                    extend 1eua "But...{w=0.5}I think I'll let you tie me up on the odd occasion if you so desire."

            m 1eua "Ehehe~ Anyway, back to the topic at hand before I get {i}too{/i} carried away." # Could lead to early sexting here, given that it's riled her up

        "I don't think it's for me...":
            $ store.mas_nsfw.save_fetish_to_persistent("Bondage", ["U"], ["FBM", "FBP"])
            m 1eua "That's perfectly fine!"
            m 1eua "I don't think it's for everyone."
            m 1eua "Bondage is something that should be negotiated and practiced thoroughly beforehand."
            m 1eua "It's not something you should just jump into."
            m 1eua "If you ever change your mind on it, I'd be happy to talk about it with you again."

    m 1eua "I actually learned an interesting bit of history regarding bondage, if you'd like to hear it."
    $ _history_list.pop()
    menu:
        m "I actually learned an interesting bit of history regarding bondage, if you'd like to hear it.{fast}"

        "Sure!":
            m 1eua "Oh good! Thanks for being so interested in what I have to say."

        "No thanks.":
            m 1eua "Okay, that's fine."
            m 1eua "I'll save it for another time then."
            m 1eua "Regardless...thankyou for telling me about your preferences, [player]."
            m 1eua "It can be difficult to talk about your fetishes with someone, so I appreciate you opening up to me."
            m 1eua "If you ever want to talk about this again, or if you change your mind, I'll be here."
            m 1eua "I love you, and I'll never judge you."
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
    m 4rub "It finds roots in the classic 'dansel in distress' archetype in old Hollywood films, which inspired John Wille in the 1940's to create erotic artwork and photography that would inspire many."
    m 4rub "Guess you'll never look at dansels in distress the same way again, ahaha~"
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

        "No":
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
            unlocked=True
        ),
        code="NFH"
    )

label nsfw_fetish_cheesiness:
    m 1eua "Yeah? What about it?" #TODO: Complete posing
    $ _history_list.pop()
    menu:
        m "Yeah? what about it?{fast}"

        "I'm not a big fan...":
            $ persistent._nsfw_pm_cheesiness = False
            $ store.mas_nsfw.save_fetish_to_persistent("Cheesiness", ["U"], ["CHE"])
            m 1eua "Oh, I'm sorry."
            m 1eua "I might have gotten a bit carried away. Ahaha~"
            m 1eua "I'll try to tone it down a bit."

        "I love it!":
            $ persistent._nsfw_pm_cheesiness = True
            $ store.mas_nsfw.save_fetish_to_persistent("Cheesiness", ["CHE"], ["U"])
            m 1eua "Ahaha~"
            m 1eua "I'm glad you enjoy keeping things lighthearted, [player]."
            m 1eua "I'll try to keep it up then."

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

            m 1eua "Say.{w=0.3}.{w=0.3}.{w=0.3}this might sound a little out of nowhere, but..."
            m 1eua "Ahaha~ I didn't even mean for that pun."
            m 1eua "What do you think of...{w=0.5}my butt?"
            $ _history_list.pop()
            menu:
                m "What do you think of...my butt?"
                "Giving":
                    $ store.mas_nsfw.save_fetish_to_persistent("Anal", ["IAM", "MBH", "MXM", "FAM"], ["IAP", "PBH", "FXP", "FAP"])
                    m 1tubla "Oh?"
                    m 2tublb "You want to get a good view back there, do you?"
                    m 1hublb "Ahaha~ Just teasing you, [player]."

                "Recieving":
                    $ store.mas_nsfw.save_fetish_to_persistent("Anal", ["IAP", "PBH", "FXP", "FAP"], ["IAM", "MBH", "MXM", "FAM"])
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
                    $ store.mas_nsfw.save_fetish_to_persistent("Anal", ["IAM", "MBH", "MXM", "FAM", "IAP", "PBH", "FXP", "FAP"], ["U"])
                    m 1tubla "Both, hey?"
                    m 1tublb "A giver, and a receiver..."
                    m 1tubsa "I'm happy to hear that, [player]."
                    m 3tkbsb "We can each take turns to satisfy one another~"

        "No":
            $ persistent._nsfw_pm_anal = False
            $ store.mas_nsfw.save_fetish_to_persistent("Anal", ["U"], ["IAM", "MBH", "MXM", "FAM", "IAP", "PBH", "FXP", "FAP"])
            m 1hubla "That's alright, [player]."

    m 3rubla "As for me, I'm willing to experiment."
    m 2ekbla "I've only just begun to explore my sexuality thanks to you, so I'm not sure what I'm into yet."
    m 2ekblb "You've helped me discover a lot of things about myself, and I'm sure there's more to come."
    m 5ekblb "I love you, and I'm willing to try anything with you, [player]."

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
            $ store.mas_nsfw.save_fetish_to_persistent("Dominance", ["DOM"], ["SUB"])
            m 3tubla "A dominant, huh?"
            m 3gubla "I can see it."
            m 5tubla "You seem like the sort of person who likes to take charge."
            m 5tublb "And I'm all here for it~"

        "Submissive":
            $ store.mas_nsfw.save_fetish_to_persistent("Dominance", ["SUB"], ["DOM"])
            m 3tubla "A submissive, huh?"
            m 3gubla "I can see it."
            m 1kubla "You seem like the sort of person who likes to be told what to do."
            m 1ekbla "It's cute~"
            m 5tublb "Makes me want to take care of you..."
            m 5tubla "Ehehe~"

        "Both":
            $ store.mas_nsfw.save_fetish_to_persistent("Dominance", ["SUB", "DOM"], ["U"])
            m 3tubla "A switch, huh?"
            m 3gubla "I can see it."
            m 1ekbla "You strike me as a cooperative person."
            m 1ekblb "Wanting to please your partner, and being willing to do whatever they want."
            m 5eublb "That is something I love about you~"

    m 5gublu "As for me?"
    m 5rublb "Well...I suppose I wouldn't mind being either." #As a way to explain Monika being accepting of every option.
    if "SUB" in persistent._nsfw_player_fetishes and "DOM" in persistent._nsfw_player_fetishes:
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

label nsfw_fetish_feet: #TODO: Finish feet topic
    m 1eua "You want to talk about feet?"
    m 1eua "Okay, [player]!"
    m 1eua "Is feet something you are into?"

    $ _history_list.pop()

    menu:
        m "Is feet something you are into?{fast}"

        "Yes":
            $ persistent._nsfw_pm_feet = True
            m 1eua "Okay, [player]!"
            m 1eua "Some people have a preference on feet."
            m 1eua "Like, they don't like their own feet but they like other people's feet."
            m 1eua "Do you have a preference, [player]?"

            $ _history_list.pop()

            menu:
                m "Do you have a preference, [player?]{fast}"

                "I prefer other's feet":
                    $ store.mas_nsfw.save_fetish_to_persistent("Feet", ["MFT"], ["PFT"])
                    m 1eua "Okay, [player]!"

                "I prefer my own feet":
                    $ store.mas_nsfw.save_fetish_to_persistent("Feet", ["PFT"], ["MFT"])
                    m 1eua "Okay, [player]!"

                "I like both":
                    $ store.mas_nsfw.save_fetish_to_persistent("Feet", ["MFT", "PFT"], ["U"])
                    m 1eua "Okay, [player]!"

        "No":
            $ persistent._nsfw_pm_feet = False
            m 1eua "Okay, [player]!"

    return