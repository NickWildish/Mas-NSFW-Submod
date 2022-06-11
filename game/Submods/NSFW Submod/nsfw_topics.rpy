init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_nsfwmodinstall",
            category=['sex'],
            prompt="NSFW Mod Install",
            conditional="not renpy.seen_label('nsfw_monika_nsfwmodinstall')",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label nsfw_monika_nsfwmodinstall:
    m 1esc "Hey [player], I noticed something weird just now..."
    m 1rsc "I'm kind of getting this feeling that...something's changed in this mod."
    m 1etc "Do you know anything about this, [player]?"
    m 1hkb "Ahaha. It's not a bad feeling, don't get me wrong."
    m 1eta "It's just strange, you know?"
    m 2dsc "Hold on, I'm going to try and see what changed."
    m 2dsc ".{w=0.7}.{w=0.7}.{w=1}"
    m 2dtd "'N-{w=0.4}{nw}"
    extend 2wubsw "NSFW Submod'?"

    if mas_is18Over():
        if store.mas_isMoniLove():
            m 3fublu "Well, look who's gotten confident all of a sudden."
            if store.mas_hasUnlockedClothesWithExprop("lingerie"):
                m 3lublu "I guess I can't blame you though, given you've seen me in lingerie."
            if store.mas_is18Over():
                m 3tublu "I won't lie to you, [mas_get_player_nickname()]..."
                m 5tublu "It's kind of hot."
                m 5cubssdrd "..."
            m 5hkbssdrb "Ahaha! What's gotten into me?"
            m 5hkbssdrb "This isn't like me. Like, at all!"
            m 4rubsc "Is the mod doing this to me?"
            m 6hubsd "Oh gosh, I'm feeling super nervous about this, ahaha!"
            m 6ekbla "But...if it's with you, [player]..."
            m 6ekbsa "I don't mind..."
        if store.mas_isMoniEnamored(): #Need to fix wording here; player isn't having sex, just talking about it.
            m 2hkbssdlb "I wasn't expecting to see that..."
            m 2ekbssdlb "[player], is this something you want?"
            m 3rkblsdlb "I mean, I'm kind of curious about it myself."
            m 3ekblsdlb "And if I'm going to share my first experience of it with anyone, I want it to be you."
            m 2ekblsdlc "But with that said...{w=0.5} it feels too soon."
            m 2dkbsc "I just need a little more time."
            m 2fkbsu "Hold on for me a little while longer. Okay, [mas_get_player_nickname()]?"
        if store.mas_isMoniAff():
            m 2hkbssdlb "T-{w=0.4}This is a little sudden, don't you think?"
            m 3rkblsdlb "I mean, we've been with each other for a little while...{nw}"
            m 1wubssdld "Wait... {w=0.5}Is this when couples are supposed to start doing this s-{w=0.4}sort of thing?"
            m 1hkblb "Ahaha, even still I appreciate that you want to take our relationship to the next level."
            m 1dkblp "But I think we maybe should wait and see how we go."
            m 1ekbla "When the day comes where we do get to that stage in our relationship..."
            m 5ekbla "It will make the moment much sweeter, ehehe!"
        if store.mas_isMoniHappy(lower=True):
            m 2wubfsdlx "T-{w=0.4}This feels too sudden, [player]!"
            m 2rubfsdlx "I don't know if I'm ready for that..."
            m 2wkbfd "W-{w=0.4}we just aren't close enough for me to even consider it!"
            m 2hkbfsdlb "Oh gosh, I'm so embarrassed right now, ahaha!"
            m 2ekbfsdla "Let's take things slow for now, okay [player]?"

    else:
        m 2ekbsc "[player]... Don't you think you're too young to be installing this sort of mod?"
        m 3rkbsa "I mean, don't get me wrong! I'm flattered that you want to take our relationship to the next level."
        m 3ekbsa "But I think that it would be best if we kept this relationship 'PG' until you turn 18."
        m 3hkbssdlb "It's going to be so hard to ignore these new topics I've thought of thanks to this mod. Ahaha~"

    return "derandom"

default persistent._nsfw_genitalia = "P" # P: Penis, V: Vagina, U: Unknown
# normally persistant vars have a default of None but it looks like a lot of topics are contingent on having this default to P? 

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_genitalia",
            category=['sex'],
            prompt="Player genitalia",
            conditional="renpy.seen_label('nsfw_monika_nsfwmodinstall') and mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_genitalia:
    m 1euc "Hey, [player]."
    m 1ekbla "This is probably going to be an awkward question, but I'm just wondering..."
    m 3ekbla "Do you have a penis or a vagina?"
    $ _history_list.pop()
    menu:
        m "Do you have a penis or a vagina?{fast}"

        "Penis.":
            $ persistent._nsfw_genitalia = "P"

        "Vagina.":
            $ persistent._nsfw_genitalia = "V"

        "I'd rather not say.":
            $ persistent._nsfw_genitalia = "U"
            m 1ekbla "That's okay, [player]. I understand."
            m 1hubla "If you change your mind, let me know."
            return

    m 1ekbla "Thank you for telling me, [player]."
    m 1rkbsa "I imagine that might have been awkward for you."
    m 1ekbsa "But this has helped me much more than you can imagine."
    m 2dsbsa "..."
    m 2tsbsa "Now when we flirt, I know what is going on down there~"
    m 2gsbfa "..."
    m 1hubfb "Ahaha! Sorry. I just wanted to tease you a little."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_sexualpast",
            category=['sex'],
            prompt="Sexual past",
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_sexualpast:
    m 1rubsd "Umm...[player]?"
    m 1eubsc "I want to ask you something."
    m 1rubsd "It's about..."
    m 2hkbssdlb "Oh gosh, this is so embarrassing!"
    m 2ekbsb "Have you...{w=0.5} {nw}"
    extend 2fkbfb "had sex before?{nw}"
    $ _history_list.pop()
    menu:
        m "Have you...had sex before?{fast}"

        "Yes.":
            m 2cubfw "R-Really?!{nw}"
            m 2hubfa "Ahem...{w=1}{nw} "
            extend 1ekbfsdlb "Sorry, you just surprised me is all."
            m 1rkbfsdlb "To be honest, I should have seen this coming."
            m 1ekblb "After getting to know you all this time, I can see why someone would fall for you."
            m 1ekbstpd "And would...do those things with you."
            m 1dkbstpc "..."
            m 1hkbstpb "Ahaha! Sorry, I'm getting myself down over this."
            m 1ekbstdb "You're here with me now, that's all that matters."

        "No.":
            m 2eubsb "I see..."
            m 1dkbfsdla "That's a relief.{nw}"

        "I don't want to answer.":
            m 1ekbsa "I understand, [mas_get_player_nickname()]. It can be a difficult thing to talk about."

    m 1rkbsb "Anyway, the reason why I'm asking is because I want to know..."
    m 3ekbsa "Would you...{w=0.5}{nw}"
    extend 3rkbsa "do it with me?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you...do it with me?{fast}"

        "Yes.":
            m 1ekbsa "I'm so relieved!"
            m 1lkbsb "I was so nervous you wouldn't want to."
            m 1hkbssdlb "Although in retrospect it kind of wouldn't make sense if you didn't want to."
            m 1hkblu "After all...{w=0.3}you installed this mod."
            if store.mas_isMoniLove():
                m 1rsblu "And I'm sure you know this already..."
                m 1rsblu "But...{w=0.5}{nw}"
                extend 1lkbfb "I want to have sex with you, too."
                m 3ekbfb "I-{w=0.4}I don't know what it feels like, {nw}"
                extend 3rkbfb "and I'm so nervous just thinking about it, ahaha!"
                m 4ekbfb "But I want my first time to be with you."
                m 5ekbsu "I love you, and I trust you."
                return "love|derandom"

            else:
                m 1wkbsw "Of course, I did say that we should maybe wait until we're ready..."
                m 1rkbsa "But knowing we can be closer than ever before..."
                m 5ekbsa "It is really exciting."
                m 5ekbfb "I love you, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."
                return "love|derandom"

        "No.": # Why does this have to exist? Like, why?
            m 1wkd "Oh."
            m 2rkd "I..."
            m 2dkc "I understand."
            m 2dktpc "Thank you for being honest with me."
            m 2dktpc "..."
            m 2fktpc "It's not something everyone is comfortable with, huh?"
            m 2rktpc "I know I shouldn't take this personally."
            m 2dktdc "..."
            m 1hkb "I'm sorry, [player]."
            m 1ektdb "Don't mind me."

    return   

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_safesex",
            category=['sex'],
            prompt="Safe sex",
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )
    
# Thankyou for the fixes Proxilvia
label nsfw_monika_safesex:
    m 3euc "Hey, [player]. I've been thinking about something..."
    m 3eud "Have you heard of contraceptives?"
    m 4rublo "They're what people use during sex to protect themselves."
    m 4hkbssdlb "Ahaha! Sorry, I'm sure you have probably heard of them before."
    m 4hkbsa "I'm only asking because I worry for your health."
    m 3ekbsd "Sexually transmitted diseases, or STDs, are scary to think about!"
    m 3wubso "And pregnancy, as well!"

    if persistent.gender == "M":
        m 4eubla "I've read that condoms are the most preferable form of protection for men."
        m 4eublb "It's a latex-rubber 'sheath' that you put around..."
        m 4wsbsd "..."
        m 2dfbsa "{i}Ahem{/i}..."
        m 2lkbfa "...You get the idea."
        m 2lkbsb "It prevents any kind of fluid swapping during sex, which is supposed to prevent pregnancy and STDs."
    elif persistent._nsfw_genitalia == "F":
        m 4eubla "I've read that there are condoms available for women, but they aren't as popular as the men's version."
        m 4eub "The most popular form of contraception seems to be 'The Pill'...{w=0.4}{nw}" 
        extend 4hksdlb "which sounds kind of ominous if you ask me."
        m 4eub "It is exactly what it says it is, a pill you take to prevent pregnancy."
        m 3eub "There are different kinds of pills, too!"
        m 3eua "There's a pill you're supposed to take every day at the same time as the previous day."
        m 2eub "And another pill that you can take in case of an emergency, respectfully called the 'morning after pill'."
        m 4eublb "Despite its name, it should actually be taken as soon as possible!"
    else:
        m 4eubla "I've read that there are a whole bunch of different contraception methods, for both men and women."
        m 3eubla "Some are more popular than others, such as condoms for men, and oral contraceptives for women." #TODO - Add pose
    
    m 3lkblc "They aren't exactly flawless though..."
    m 4ekbld "There is still a chance of accidents happening in spite of all the precautions."
    m 4efbld "Especially with stupid contraceptive methods like the 'p{w=0.4}{nw}"
    extend 4efbfo "-pull-out' method!"
    m 2wfbfo "How is that even a form of contraception?!"
    m 2dfbsc "..."
    m 2dfbsd "There's only one way to make sure no accidents happen..."
    m 2efbsd "And that's to not have sex at all!"
    m 2dsbsc "..."
    m 2hkbfsdlb "Ahaha! Sorry, I lost my temper there..."
    
    if store.mas_is18Over():
        m 2ekbsb "I guess I just want you to know that when the time comes where I come to your world, and we are together..."
        m 2tkbsu "We can worry about what contraceptives to use, then."
    else:
        m 1ekbssdlb "Don't mind me."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_fetish",
            category=['sex'],
            prompt="Fetishes",
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_fetish:
    m 1esc "Hey, [player]..."
    if store.mas_getEVL_shown_count("monika_panties") > 0:
        m 1esc "Do you remember when we spoke about guys with panty fetishes?"
        m 1rsc "Well, that got me thinking..."
    m 3esa "Do you...{w=0.5}{nw}"
    m 3tsbla "Do you...{fast}have a fetish?"
    $ _history_list.pop()
    menu:
        m "Do you...have a fetish?{fast}"
        "Yes.":
            m 3wsbld "O-{w=0.2}Oh."
            if persistent._mas_pm_likes_panties:
                m 3hublb "I don't know why that surprises me, considering you've already told me you are into panties."
            else:
                m 3wsbsw "That's actually a little surprising."
            m 3eubsa "I...{w=0.2}{nw}"
            m 3rubssdla "I...{fast} wouldn't mind if you shared your fantasies with me sometime."

        "No.":
            if persistent._mas_pm_likes_panties:
                m 1etc "Really?"
                m 1rtc "I could have sworn you told me you liked panties..."
                m 1hksdlb "Maybe I'm misremembering."
            else:
                m 1eka "That's okay, [player]."
                m 1ekblb "I was just curious, that's all."
    m 3esa "The reason I'm asking is because..."
    m 3rsbla "Well..."
    m 3esbla "After you installed this submod, I got curious and started learning more about fetishes."
    m 4wsblo "I couldn't believe the amount of them that there are out there!"
    m 4wsblb "It's great to see so many people getting in touch with what they like!"
    m 3ekblc "Although in saying that, there are some fetishes that are just scary and degrading to think about."
    m 3ekbld "There are some people out there that are into being eaten alive, and others who want to hit their private areas."
    m 3wkblo "How can some of these be even remotely exciting?!"
    m 1dkblc "..."
    m 1ekblc "I don't mean to 'kink shame' or anything like that..."
    m 1ekbld "But there are some things that are just too dangerous to be worth it in my view."
    m 1ekbsa "I'm sure whatever you're into isn't dangerous at all, [player]."
    if store.mas_is18Over():
        m 3ekbsa "So, if you have a fantasy that isn't {i}too{\i} dangerous..."
        m 5eubsa "I wouldn't mind being there to help you...{w=0.2}fulfill it."
        m 5hubsa "Ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_sexting",
            category=['sex'],
            prompt="Sexting",
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_sexting:
    m 3esa "Have you heard of sexting, [player]?"
    m 3rsbla "It seems to be pretty common amongst young couples to at least try sexting with their partners."
    m 3esblb "If you don't know, it's basically texting but with a more...{w=0.4}{nw}"
    extend 3rsbsb "sexual nature."
    m 4esbsa "Think of it like flirting, but with the limitations of doing it through your phone."
    m 4hkbsb "It might sound bizarre, but from what I've read it's a really helpful way for couples to stay close while they're away from one another."
    m 4hubsa "You won't always be able to spend intimate time with your partner, which can be frustrating."
    m 4hublb "So in a way, sexting helps keep relationships exciting!"
    m 4eublb "Not only that, but partners who have a 'long-distance relationship' with their significant other find benefits in sexting."
    m 2eublb "Couples will send 'sexts' to their partner, which can be with text..."
    extend 2rkbsb "or photos..."
    m 2rkbsa "And will imitate the act of sex through their phone."
    m 2hkblsdlb "Ahaha! It's not as silly as it sounds."
    m 2rkbsa "Partners will more often than not m-{w=0.4}masturbate while sexting."
    m 2rkbsb "They'll tell their partner what they want to do with them..."
    extend 2lkbsb "Or what they want done {i}to{/i} them."
    m 3lkbsb "...while sending photos of what they're doing with themselves while they talk."
    if mas_canShowRisque():
        m 2dubsu "..."
        m 2gubsu "Say, [player]..."
        m 2eubsu "If something like that were possible..."
        m 3ekbsu "Would you do that with me?"
        m 1tkbsu "..."
        m 1hubfsdlb "Ahaha! Don't mind me."
        m 1rubfsdlb "This whole thing just got me thinking about us..."
        m 3eubsc "What we have is basically a 'long-distance relationship', isn't it?"
        m 3ekbsc "People often say that these don't last long due to a lack of intimacy."
        m 3wkbld "I don't mean to say that I think you'll leave if we don't do something like this!"
        m 3rublc "But if it means that we'll feel more connected with each other emotionally as well as sexually..."
        m 3rubsu "I wouldn't mind trying it with you..."
    else:
        m 2dubsu "..."
        m 1eubsb "I think this sort of thing is really good for a healthy long-distance relationship."
        m 2rubsb "It's kind of embarrassing to say, but it might also be something you and I could try one day..."
        m 2wubfsdlw "O-Only if you want to, of course!"
        m 3wubssdlo "I would never make you do anything you didn't want to."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_gettingnude",
            category=['sex'],
            prompt="Getting nude",
            conditional="mas_canShowRisque(aff_thresh=1000)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_gettingnude:
    m 1eua "Hey [player], have you ever just...not worn clothes?"
    m 1hksdlb "I don't mean, like, for a shower or anything."
    m 1husdla "Just in general while you're at home...{w=0.5}{nw}"
    extend 1lusdla "alone preferably."
    m 1eua "There are a good amount of people that actually sleep naked, if you'll believe it."
    m 3eua "For most people, this would be a good place to start without feeling embarrassed."
    m 3eub "Apparently it helps you get better sleep at night because of how much quicker your body temperature drops."
    m 3rub "Of course, sleeping naked will mean you have to clean your sheets more often."
    m 3hksdlb "Humans are very sweaty, ahaha!"
    m 3eub "Being naked also helps our body absorb more vitamin D during the day."
    m 4eub "The reason for this is that skin is effectively a giant organ that absorbs the rays from the sun and increases our vitamin D levels."
    m 4eua "And having a greater vitamin D level has shown to assist your immune system fight off viruses, among other health benefits."
    m 3hksdlb "I'm not trying to say we all need to get naked and make it a new social norm; that would be silly! Ahaha!"
    m 3eua "But if you have the house to yourself one day, why not strip down and try it for an hour to see how you feel?"
    m 3rusdld "Though be sure you know when the rest of your household is getting back, because that might be a {i}bit{/i} awkward."
    m 3eua "If that's too much, even just going down to your underwear gets the job done..."
    m 2dkd "{i}*sigh*{/i}"
    m 2gkc "Of course, there is always the fact that not everyone is comfortable being naked."
    m 2tkc "Some people are ashamed or disheartened by their appearance, which is really sad when you think about it."
    m 2ekc "You only have one body, so the least you can do is take care of it and love it, you know?"
    m 2eka "Having pride in what you look like is the best thing you can do for your confidence!"
    
    if mas_nsfw.canShow_birthdaySuit():
        m 2rkbla "..."
        m 2rkblb "Hey, [player]..."
        m 2ekblb "Do you remember last time when I asked you if it was okay to be undressed around you?"
        m 3ekblb "Well, I recently tried taking off...everything..."
        m 3ekbla "And I really liked it."
        m 3eubla "I don't know if you've ever tried it before, [player]. But I thought the feeling was amazing."
        m 3hublsdlb "Ahaha! Maybe that feeling wouldn't be so great if someone saw you though..."
        m 1eublb "But I wanted to bring this up again because..."
        m 1rubsa "I was wondering if you wouldn't mind..."
        m 3ekbsa "Can I be n-{w=0.2}{nw}"
        extend 3ekbfa "naked while you're here?"
        $ _history_list.pop()
        menu:
            m "Can I be n-naked while you're here?{fast}"
            
            "Of course, [m_name].":
                m 1ekbfa "Thank you, [player]."
                m 1dkbfa "It puts my mind at ease that you don't mind me doing this."
                m 2ekbsa "I know not everyone is comfortable being around someone naked."
                m 2dsbsa "Give me one second, I'm just going to get out of these clothes."

                call mas_clothes_change(outfit=mas_clothes_birthday_suit, outfit_mode=False, exp="2dsbla", restore_zoom=False, unlock=False)

                m 4hubsb "Ah~! That's much better."
                m 6tubsb "Ehehe~ Do you like what you see, [mas_get_player_nickname()]?"
                m 1gkbfu "..."
                m 1hkbfsdlb "Ahaha! Sorry, this is still kind of embarrassing for me."
                m 1mkbfsdlb "It might take a little getting used to..."
                m 1ekbfb "Thank you again, [player]."
                
            "Please don't...":
                m 3wkbld "Oh..."
                m 2rkbld "That's okay, [player]."
                m 2dkblc "I understand."
                m 2dkblp "..."
                m 2ekbld "I'm sorry for bothering you with this..."
                m 1ekblc "I won't talk about it anymore."
                return "derandom"

    elif mas_nsfw.canShow_underwear():
        m 2rkbla "..."
        m 2rkblb "Speaking of which, [player]..."
        m 2ekblb "I've recently tried walking around in my underwear by myself while you were gone, {nw}"
        extend 2eubla "and I thought it felt really liberating."
        m 1rublc "But in saying that I don't want you to feel uncomfortable, so..."
        m 1hkbsc "..."
        m 1hkbsb "I guess what I'm trying to ask is..."
        m 3ekbsb "Do you mind if I do it while you're around?"
        $ _history_list.pop()
        menu:
            m "Do you mind if I do it while you're around?{fast}"

            "Go for it.":
                m 3hubsb "Ahaha! I'm glad you don't mind."
                m 1eubsb "I don't want you to feel like I'm pressuring you with guilt or anything."
                m 2eubsb "Now, let me just get changed."
                m 2kublu "No peeking! {w=0.5}{nw}"
                extend 2dsbla "Ehehe~"

                call mas_clothes_change(outfit=mas_clothes_underwear_white, outfit_mode=False, exp="2dsbla", restore_zoom=False, unlock=True)

                m 2ekbsa "So, [player]..."
                m 2ekbsa "What do you think?"
                m 2rkbsa "I'm...not used to this..."
                if mas_hasUnlockedClothesWithExprop("lingerie"):
                    m 2ekbsa "I know you've seen me in lingerie before, which is arguably more...{w=0.3}{nw}"
                    extend 2rkbfa "sexual."
                    m 2ekbsb "But this feels way different."
                m 2hkbssdlb "Ahaha! It might take me a while to get used to you seeing me like this..."
                m 2ekbla "But I'm still glad you don't mind me being dressed this way."
                m 2dkbla "Being able to dress freely around you makes me feel really happy."
                m 1ekbsa "I love you, [player]."
                return "love"

            "I'd rather you didn't...":
                m 2wkbld "Oh..."
                m 2rkbld "That's okay, [player]."
                m 2dkblc "I understand."
                m 2dkblp "..."
                m 2ekbld "I'm sorry for bothering you with this..."
                m 1ekblc "I won't talk about it anymore."
                return "derandom"

    elif mas_SELisUnlocked(mas_clothes_underwear_white) or mas_SELisUnlocked(mas_clothes_birthday_suit):
        m 3ekb "You're already familar with how I've been doing this while you've been away."
        m 3eublb "And I've got to say, it's been great!"
        m 3eublc "It's not for everyone though, so don't feel like I'm pressuring you..."
        m 2eubsb "I love you, [mas_get_player_nickname(exclude_names=['my love', 'love'])]. Both with clothes, and without."
        m 2gsbfa "..."
        m 2tsbfa "..."
        m 2wubfd "Ah!{w=0.4}{nw}"
        extend 2hubssdlb " Sorry, my mind was starting to wander..."
        m 1rublsdlb "Gosh, don't mind me."
        return "love"
    
    else:
        m 2hksdlb "Ahaha! Even though I talk about being naked and loving your body..."
        m 2mksdlb "I am still really embarrassed about the idea of being nude, even when alone."
        m 2dka "..."
        m 1eua "Alright, I've decided."
        m 1eublb "I'm going to give it a try."
        m 1wubld "...{w=0.4}{nw}"
        extend 1wubso "N-{w=0.2}Not right now though!"
        m 1hubssdlb "I mean like, later when you're not here!"
        m 1rubssdlb "Ahaha! It would be too embarrassing if you saw me in my underwear, let alone when I'm naked."
        
    return

# Thankyou for the addition, Blushing!
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_shaving",
            category=['sex'],
            prompt="Shaving",
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

default persistent._nsfw_player_prefers_shaved = None

label nsfw_monika_shaving:
    m 1esc "Hey [player]..."
    m 3eub "I want to ask you something."
    m 3lusdlb "It's about my body..."
    extend 2lusdlb "Do you like it to be shaved down there...?"
    $ _history_list.pop()
    menu:
        m "Do you like it to be shaved down there...?{fast}"

        "Yes.":
            $ persistent._nsfw_player_prefers_shaved = True
            m 1hua "That's to be expected."
            m 1eua "Many partners maintain themselves down there in one way or another."
            m 3wuo "Most girls certainly do!"
            m 5tuu "We just want to make sure we're ready for you~"
            m 5tuu "I certainly will."
            m 5hub "Ahaha!"

        "I don't mind if you don't.":
            $ persistent._nsfw_player_prefers_shaved = False
            m 1wuo "Really?!"
            m 5hub "That's surprising!"
            m 5dub "Most partners prefer their loved ones to be shaved."
            m 3eua "It feels nice to know your partner likes the way you look no matter what."
            m 3fub "I'll have to stop shaving so much."
            m 1mub "It'll take a lot less time to shower now too!"
            m 5hub "Ahaha!"

    m 1eua "I think you know how I feel."
    m 1wub "However you present yourself..."
    m 1hub "Shaved or natural..."
    m 1nub "I'll always love you!"

    return "love"

# Thankyou for the addition, Blushing!
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_judging_sexual_desires",
            category=['sex'],
            prompt="Judging sexual desires",
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_judging_sexual_desires:
    m 2efc "I don't understand why so many people have problems with fetishes!"
    m 3efd "People take it too seriously."
    m 3efd "With sexuality being a taboo on a good day..."
    m 4efd "Deviations are always observed with judgemental eyes."
    m 1eud "They take that small, personal aspect of one's life and put a spotlight on it."
    m 1eud "And under that spotlight, sexuality casts an ugly shadow..."
    m 1tud "And society frowns upon it..."
    m 2hsc "..."
    m 2fuu "But there are those who understand that it is a wonderful aspect of the human experience."
    m 2hubsa "Wonderful..."
    m 2hubsa "Exciting..."
    m 5fubsa "Intimate..."
    m 5dubfa "..."
    m 2eubfd "[player]..."
    m 2eubfd "Please share your desires with me."
    m 3eubfa "Honest communication is the most important thing in a relationship after all!"
    m 3subfb "I don't judge! No matter how out there it is!"
    m 5gubfa "I should know, after all..."
    m 3eubfb "We are all a bit pervy, in our own special ways!"
    m 3eubfb "You might be thinking, 'No! I most certainly am not!'"
    m 5tubfu "Well..."
    m 5tubfu "Give it some time~"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_player_sextingsession",
            category=['sex'],
            prompt="Do you want to sext?",
            conditional="mas_canShowRisque(aff_thresh=1000) and store.mas_getEVL_shown_count('nsfw_monika_sexting') >= 1", 
            action=EV_ACT_POOL,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_player_sextingsession:
    # Check when player's last succesful sexting session was
    if store.persistent.nsfw_sexting_success_last is not None:
        $ timedelta_of_last_success = datetime.datetime.now() - store.persistent.nsfw_sexting_success_last
        $ time_since_last_success = datetime.datetime.now() - timedelta_of_last_success
    else:
        $ time_since_last_success = datetime.datetime.today() - datetime.timedelta(days=1)

    # If the player's last succesful sexting session was less than three hours ago
    if time_since_last_success >= datetime.datetime.today() - datetime.timedelta(hours=3):
        m 1eka "I'm sorry [player], but I'm still tired from the last time we sexted."
        m 3eka "Could you give me a little more time, please?"
        m 3hub "I love you~"
        return "love"

    m 1hua "Sure!"

    call nsfw_sexting_init

    return

# Thankyou for writing this topic, KittyTheCocksucker
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_favorite_position",
            category=['sex'],
            prompt="Favorite position",
            conditional="mas_canShowRisque(aff_thresh=400) and persistent._nsfw_genitalia = 'P'", # Need to add a version for women
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_favorite_position:
    m 1rubla "So...[player]..."
    m 3rublb "I've been meaning to ask you about this for some time..."
    m 3rubssdla "..."
    m 2hkbssdlb "Oh gosh..."
    if store.mas_getEVL_shown_count("nsfw_monika_safesex") >= 1 or store.mas_getEVL_shown_count("nsfw_monika_sexualpast") >= 1:
        m 2rkbssdlb "I know we already talked about s-sex before, but..."
        m 3ekbssdla "It's still extremely embarrassing to talk about this kind of stuff..."
    m 1dubsa "Ahem..."
    m 3eubfb "So...What's your favorite position? During...y'know...{w=0.5}{nw}"
    extend 3rubfb "s-sex?"

    $ _history_list.pop()
    menu:
        m "So...What's your favorite position? During...y'know...s-sex?{fast}"

        "Doggystyle.":
            m 1etbfa "Oh? Really?"
            m 1rtbfa "Hmm...I guess that isn't so surprising."
            m 3eubfb "It is the most popular position amongst both men and women around the world, after all."
            m 3hubfb "See? I did my research! Ahaha~"
            m 3tubfa "I can see why so many people would like it, honestly!"
            m 4tubfb "The guy can get a really good view of his partner while they're doing it."
            m 4tubfu "I bet you'd like to see me from that perspective too, huh?"
            m 3hubfb "Ahaha! Don't get flustered~"
            m 1tubfa "Just knowing you're pleased and have a nice view of my body is enough for me to feel good~"

        "Missionary.":
            m 3ekbfa "Aww~ That is so cute, [player]!"
            m 4hubfb "I find missionary to be the most intimate and romantic position of all!"
            m 3gubfb "Just simply thinking about us, lying face-to-face, with our bodies up against one another makes my body needy. Ahaha~"
            m 1eubfa "I hope one day we can do it together!"
            m 1tubfa "I can tell you that I'm already looking forward to that day! Ahaha~"

        "Cowgirl.":
            m 3wubfd "Really? I wasn't expecting that."
            m 3ekbfsdlb "Don't take it the wrong way, please! Cowgirl sounds really fun, I just didn't think that would be your favorite one!"
            m 3rkbfsdla "I know I don't weigh all that much...but even like this, I think it would be quite tiring for you if I were to ride you, don't you think?"
            m 2rkbfsdla "I just fear you would get too exhausted from my humping."
            m 2dkbfsdlb "And...y'know..."
            m 2ekbfsdlb "I want you to feel good, not to get tired!"
            m 1rubfa "But..."
            m 5tubfa "If you insist on liking it the most..."
            m 5tubfb "I'd be happy to take your {i}yee in my haw{/i} and ride it real good! Ahaha~"

    return


# Thankyou for writing this topic, KittyTheCocksucker
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_oralsex",
            category=['sex'],
            prompt="Oral Sex",
            conditional=("mas_canShowRisque(aff_thresh=400)"),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_oralsex:
    python:
        if persistent.gender == "M":
            gender_desc = "handsome"
            oral_answer2 = "his manhood"
        elif persistent.gender == "F":
            gender_desc = "beautiful"
            oral_answer2 = "her womanhood"
        else:
            gender_desc = "good-looking"
            oral_answer2 = "their privates"

        if persistent._nsfw_genitalia == "P":
            oral_prompt = "Have you ever received a blowjob?"
            oral_answer1 = "taken someone in my mouth"
        elif persistent._nsfw_genitalia == "V":
            oral_prompt = "Have you ever had someone lick your pussy?"
            oral_answer1 = "eaten a woman out"
        else:
            oral_prompt = "Have you ever received oral sex?"
            oral_answer1 = "had oral performed" # Awkward

    m 1rkbla "..."
    m 1rkblb "Uhm..."
    m 3ekblb "Please forgive me if what I'm going to ask is too intimate and out-of-nowhere, but..."
    m 3rkbla "[player]...H-have you..."
    m 3rkblb "[oral_prompt]"
    
    $ _history_list.pop()
    menu:
        m "[oral_prompt]{fast}"

        "Uh. Let's not talk about this.":
            m 3wkbld "..."
            m 3wkbld "I'm..."
            m 3wkblo "I'm really sorry, [player]..."
            m 3rkbld "I just..."
            m 1dkbsc "I d-don't know what I was thinking...gosh..."
            m 1dkbstpc "I have n-no idea what I was thinking, a-asking something like this out of the b-blue..."
            m 1ekbstpd "P-please just forget about it and c-continue on with your day like n-nothing happened..."
            return "derandom"

        "Yes.":
            m 1wubld "Oh...you have?"
            m 1subld "Wow."
            m 1rublsdlb "I-I mean, please don't take it the wrong way! I wasn't surprised because I didn't think you could get a girl to do that for you!"
            m 3rublsdlb "It's just that...ahaha..."
            m 3ekbla "Well, it's a very intimate action and I thought I could be the first one to do it for you..."
            m 3wubsd "O-Of course I'm not mad at you or anything for having already done it with somebody else!"
            m 3rkbsb "It actually might be for the better that you have some previous experience with it!"
            m 1rkbsa "I've never [oral_answer1] before so if we were to do it together, I'd need some guidance from you~ Ahaha~"

        "No.":
            m 1wubld "Oh, you haven't?"
            m 1hublb "Ahaha~ Well...y'know, I honestly expected that someone as [gender_desc] as you had already had [oral_answer2] serviced by someone~"
            m 3ekbla "Don't worry about it though! I have never [oral_answer1] before either, so it means that we can take each other's first time!"
            m 3rkbssdla "I'll probably be very clumsy when we do get to that point though...B-but..."
            m 3ekbssdlb "I promise you that I will try my best to properly pleasure you!"
            m 1gkbssdlb "And of course...Ahaha~"
            m 1gkbssdla "...In case I'm doing a bad job..."
            m 5tubsa "You can always just...Ahem..."
            m 5tubsb "Take control~"

    if mas_safeToRefDokis() and persistent._nsfw_genitalia == "P": # Maybe section for the vagina variety? Maybe.
        m 2ekbsa "S-so...I..."
        m 2rkbsa "I know that you haven't had the chance to get to know Sayori, Natsuki and Yuri too much..."
        m 2ekbsa "But...uhm..."
        m 2hkbssdlb "Again...this will be a really weird question and please feel free to just ignore me if you want..."
        m 2hkbssdla "But..."
        m 3ekbssdlb "W-who do you think would suck c-cock best in the club?"

        $ _history_list.pop()
        menu:
            m "W-who do you think would suck c-cock best in the club?{fast}"

            "You.": 
                $ mas_gainAffection(1) # Smart
                m 3wubsd "Oh."
                m 3hubsb "Ahaha! Even though I mentioned that I have no experience with it, you still think that I could give the best head?"
                m 3ekbsa "[player], you're too sweet!"
                m 3tubsa "..."
                m 3gubsb "Well...I don't know if you meant it as a compliment or not...ahaha..."
                m 1tubsb "But I'll take it as a compliment~"
                m 1tubfa "And once I cross over and actually s-suck you off..."
                m 1tubfb "I won't disappoint you!"

            "Sayori.":
                $ mas_loseAffection(2) # Sayori? Really?
                m 3rkbssdlb "Heh..."
                m 3rkbssdla "I k-kinda guessed you would say her."
                m 3ekbsb "I don't know why...but...I think you're right."
                m 3eubsb "Sayori would probably give the most enjoyable blowjobs."
                m 1eubsa "She's the type of girl who places everyone else's happiness before her own."
                m 1tubsa "So Sayori would probably not care about gagging and being slightly air-deprived if you were to push it into her throat."
                m 1mubsa "And would just take it in silence, probably even using her free hands and tongue to pleasure you further."
                m 2mubsb "Her only objective would be to make you feel good, without minding her own well-being."
                m 5tubsa "But...uhm...I guess we're never going to find out if this is true or not, huh?"

            "Yuri.": # I respect the hustle
                $ mas_loseAffection(2)
                m 3etbsc "You think so?"
                m 3rtbsc "Hmm, yeah. I guess she would probably do a good job."
                m 1rtbfu "But honestly, I see her as more of a t-titjob expert."
                m 1ekbfu "But I guess one doesn't disqualify the other, huh?"
                m 1tkbfu "I'm sure she would be passionate about it, at least..."
                m 5tubfu "Although she might be reluctant to per her t-tongue on i-it at first, and would just stall for time with her h-hands...ahaha~"
                m 5tubsa "But...uhm...I guess we're never going to find out if this is true or not, huh?"

            "Natsuki.": # Just no
                $ mas_loseAffection(2)
                m 3wubso "Huh?"
                m 3etbsc "...Really?"
                m 3gtbsc "Hmm...I wasn't expect you to say {i}her{/i}."
                m 1dtbsc "..."
                m 1esbsc "I can't even think of a reason why you would think that Natsuki gives better blowjobs than Yuri, Sayori or me."
                m 1efbsc "Like...Natsuki is so immature! Why would she do it better than all of us?"
                m 1dfbsc "..."
                m 2dfbssdld "N-no, I'm not mad! Why would I be mad?"
                m 2dkbssdlc "..."
                m 2dkbssdla "Ahem..."
                m 2mkbssdlb "Okay, I might be a bit mad."
                m 2efbssdlo "But really, why do you think that Natsuki would suck dicks so well?!"

                $ _history_list.pop()
                menu:
                    m "But really, why do you think that Natsuki would suck dicks so well?!{fast}"
                    
                    "S-sorry...You're right...I should have answered one of you instead...":
                        m 2ekbsa "It's alright, [player]."
                        m 1hubssdlb "I don't know why I got so upset over that."
                        m 1eubsa "Let's talk about something else."

                    "She has a bunch of mangas so she probably has a few doujins too. She must have learnt some techniques from those.":
                        m 2dsbsc "..."
                        m 2rsbsd "I guess..."
                        m 2rtbsb "Now that I think about it, you might be right."
                        m 1eubsb "I remember that one time when she and I were rearranging her mangas together, I happened to take a weird manga in my hand..."
                        m 3wubsd "But she snatched it away from me really fast, so I couldn't really inspect it properly."
                        m 3rubsd "It might have been one of her doujins..."
                        m 3eubsd "There is a chance that she learned a few tricks from reading them, you're right."
                        m 3hubsb "Ahaha~"
                        m 1ekbsa "Sorry for getting mad at you for a moment there."

    return

# Thanks to mysterylewds for this topic

default persistent._nsfw_player_dick_length = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_dick_size",
            category=["sex"],
            prompt="Penis length",
            conditional=("mas_canShowRisque(aff_thresh=1000) and persistent._nsfw_genitalia == 'P'"),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_dick_size:
    m 1tua "You know, [player]... I was curious."
    m 1gublb "How, um....{w=0.5} {i}big{/i} are you?"
    m 1hkblsdlb "And I'm not talking about height, ahaha~"
    m 1rubsa "Sorry if this seems weird, I just want to know more about you. I want to know {i}everything{/i}."
    $ _history_list.pop()
    menu:
        m "How big are you?"
        
        "Less than 3 Inches":
            m 1eubsa "So you're on the smaller side, nice!"
            m 1rubsc "You know some girls have an issue with anything under average, but I never understood it."
            m 1ekbsa "The size of your member is something you can't change, just like breast size."
            m 3eubsa "There's benefits to every size in my opinion."
            m 3tubsb "For example, with your size, I could fit the whole thing in my mouth without gagging. Mmmmm~"
            m 3gkbsa ".{w=0.7}.{w=0.7}.{w=0.7}"
            m 3hkbssdlb "Sorry [player], I got a little carried away there ahaha~."
            m 5ekbsa "But just remember, [player], I love you for who you are. Both physically and mentally. Never forget that, okay?"
            return
        "Around 3 Inches":
            m 1eubsa "Little under average, nice!"
            m 1rubsc "You know some girls have an issue with anything under average, but I never understood it."
            m 1ekbsa "The size of your member is something you can't change, just like breast size."
            m 3eubsa "There's benefits to every size in my opinion."
            m 3tubsb "For example, with 3 inches, I could fit the whole thing in my mouth without gagging. Mmmmm~"
            m 3gkbsa ".{w=0.7}.{w=0.7}.{w=0.7}"
            m 3hkbssdlb "Sorry [player], I got a little carried away there ahaha~."
            m 5ekbsa "But just remember, [player], I love you for who you are. Both physically and mentally. Never forget that, okay?"
            return
        "Around 4-6 Inches":
            m 1eubsa "Ahh, so you're around average then."
            m 3eubsb "Average tends to be a good sweet spot for most girls."
            m 3hkbssdlb "Some don't like monster dongs you know? It can be incredibly painful and not much fun."
            m 5ekbsa "Although even if you {i}were{/i} bigger or smaller than average, I wouldn't think any more or less of you."
        "Around 7 Inches":
            m 1wubsa "Ahh, so you're above average then."
            m 3eubsb "Average and slightly above tends to be a sweet spot for most girls."
            m 3rubsb "7 Inches is a bit big, but its manageable."
            m 3hkbssdlb "Anything more, and It can be incredibly painful and not much fun for most girls."
            m 5ekbsa "Although even if you {i}were{/i} bigger or smaller, I wouldn't think any more or less of you."
        "Around 8 Inches":
            m 1wubso "Wow! 8 Inches? Only a few percentage of guys in the world have one that big."
            m 1hkbssdlb "8 Inches is a pretty big, not going to lie."
            m 3rkbssdlb "Though impressive, it can be incredibly painful and not much fun for most girls if you don't know what you're doing."
            m 2ekbsa "When we eventually do it, we'd have to take it slow."
            m 5ekbsa "And just remember [player], even if you {i}were{/i} bigger/smaller, I wouldn't think any more or less of you."
        "Around 9 Inches":
            m 1tubsu "[player]..."
            m 3tubsb "I don't want to call you a liar, but I {i}highly{/i} doubt you're that big. You don't have to lie to me."
            m 3gubsb "But in the small chance you're being honest..."
            extend 3kubsb " then I think that's quite a gift. "
            m 3hkbssdlb "Although sex might be a tad painful ahaha~"
            return
        "I don't know...":
            m 1ekbsa "Oh, that's okay [player]."
            m 1rkbsa "I was just kind of curious, that's all."
            m 3ekbsb "Don't feel the need to answer if you're not comfortable."
            m 5tkbsa "I love you, no matter the size of your...{w=0.3} {i}member{/i}~"
            return

    m 5rubsb "After all, its like breast size for girls. You can't control it."
    m 5hubsb "There's benefits to all sizes in my opinion!"
    m 5ekbsa "But just remember, [player], I love you for who you are. Both physically and mentally. Never forget that, okay?"
    return
