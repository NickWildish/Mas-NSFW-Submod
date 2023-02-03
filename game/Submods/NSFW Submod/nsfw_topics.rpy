init 5 python in mas_bookmarks_derand:
    label_prefix_map["nsfw_"] = label_prefix_map["monika_"]

# PLAYER TOPICS

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_player_sextingsession",
            category=['sex'],
            prompt="Do you want to sext?",
            conditional=(
                "mas_canShowRisque(aff_thresh=1000) "
                "and store.mas_getEVL_shown_count('nsfw_monika_sexting') >= 1"
                ),
            action=EV_ACT_POOL,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_player_sextingsession:
    # Check when player's last succesful sexting session was
    if store.persistent._nsfw_sexting_success_last is not None:
        $ timedelta_of_last_success = datetime.datetime.now() - store.persistent._nsfw_sexting_success_last
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

# MONIKA TOPICS

# original topic by mysterylewds, edits by mizuotanu-nirera

default persistent._nsfw_units_metric = None
default persistent._nsfw_dick_length = None
default persistent._nsfw_dick_circumcised = None

# data for this topic sourced is from https://calcsd.info/
# and https://unravelingsize.wordpress.com/ (NSFW link !)

# this topic utilizes logic based on "label monika_player_appearance" from script-topics.rpy.

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_dick_size",
            category=["sex"],
            prompt="[player]'s length",
            conditional=(
                "mas_canShowRisque(aff_thresh=1000) "
                "and persistent._nsfw_genitalia == 'P'"
                ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_dick_size:
    m 3eud "You know, [player]... I was curious about something."
    m 3rkbssdlb "How, um...{w=0.5}{i}big{/i} are you?"
    m 1hkbssdlb "...I'm not talking about height, ahaha!"
    m 1eka "Sorry if this seems like a weird question! {w=0.4}{nw}"
    extend 1tsa "I just want to know more about you. I want to know {i}everything{/i}."
    m 3rkbfsdlb "Can you tell me how big you are?"
    $ _history_list.pop()

    menu:
        m "Can you tell me how big you are?{fast}"

        "Sure, [m_name].":
            m 1hub "Great!"
            m 4eud "Now, I'm asking for the length along the top of it when it's erect, not the sides or bottom. {w=0.4}{nw}"
            extend 4hksdlb "Don't fudge your numbers, ahaha!"
            m 3eub "It's probably best if you get a ruler or a measuring tape for the most accurate result."
            m 2esc "I know this can be a touchy topic for a lot of people, and it's common to have kinda warped perceptions of size regarding this sort of thing."
            m 3hub "Whatever size you are, [player], I won't judge!"
            # proceed to input

        "I don't know exactly how long it is...":
            m 1hub "That's okay!"
            m 4hub "I'll tell you how to properly measure it!"
            m 3eua "First, make sure you're nice and hard."
            m 3tubfb "You can try thinking of me if you're having trouble. {w=0.4}{nw}"
            extend 5hubfb "Ahaha!"
            m 4eub "Next, measure along the {i}top{/i} of your penis, pushing the ruler against the skin and fat at the top."
            m 1eksdlb "Be sure not to measure along the sides or bottom, or you won't get an accurate measurement."
            m 1hksdlb "Though, I understand you might not be able to pull it out and measure it right this moment, ahaha!"
            m 5ekbfsdla "Just remember, I love you no matter what size you are, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."
            return "love"

        "I'd rather not talk about it.":
            m 2eka "I understand, [player]."
            m 1rksdld "I was just kind of curious, that's all."
            m 1ekc "I'm sorry if I made you uncomfortable. I won't bring it up again."
            return "derandom"

    if persistent.mas_pm_units_height_metric != None:
        $ persistent._nsfw_units_metric = persistent.mas_pm_units_height_metric # get existing answer to metric / imperial question

    elif persistent._nsfw_units_metric == None:
        m 2eub "I guess I really should know this first though..."
        m 3eub "What unit of measurement do you use, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "What unit of measurement do you use, [player]?{fast}"

            "Centimeters.":
                $ persistent._nsfw_units_metric = True
                m 2hua "Alright, thanks, [player]!"

            "Inches.":
                $ persistent._nsfw_units_metric = False
                m 2hua "Alright, [player]!"

    python:
        player_length = 0.0
        done = False
        if persistent._nsfw_units_metric: # loop for metric
            while not done: # loop until valid input
                length_input = renpy.input(
                    "How long are you in centimeters? You can include decimal values.",
                    allow="0123456789.",
                    length=5
                )
                if not(length_input.count(".") > 1 or len(length_input) == 0 or length_input == "."): # check for valid string
                    length_input_float = float(length_input)
                    if length_input_float > 0: # check that length is nonzero
                        player_length = length_input_float
                        done = True

        else: # loop for US imperial
            while not done: # loop until valid input
                length_input = renpy.input(
                    "How long are you in inches? You can include decimal values.",
                    allow="0123456789.",
                    length=5
                )
                if not(length_input.count(".") > 1 or len(length_input) == 0 or length_input == "."): # check for valid string
                    length_input_float = float(length_input)
                    if length_input_float > 0: # check that length is nonzero
                        player_length = 2.54 * length_input_float # convert to cm
                        done = True
        persistent._nsfw_dick_length = player_length # save to persistent

    if persistent._nsfw_dick_length < 7.0: # 2.8" or less
        m 1ekbsa "Aww, [player]..."
        m 1ekbssdlu "..."
        m 3hkbssdlb "Well, at least you should be able to fit the whole thing in my mouth without making me gag!"
        m 3tkbssdlu "...And you can always use your hands and mouth to please me. Ehehe~"
        m 3ekbfsdla "I appreciate you being honest with me, [mas_get_player_nickname()]."
        m 1ekbfsdlb "Some people can be really insecure about their size, but I don't mind."
        m 4eud "After all, it's like breast size for girls. There's not really anything you can do to change it."
        m 5ekbfa "I love you no matter what size you are, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."

    elif persistent._nsfw_dick_length < 13.2: # 2.8" - 5.2"
        m 1hubfb "You're so cute, [player]."
        m 1tsbfu "Even if you're a bit on the smaller side, you're perfect for me."
        m 2tubfb "I can probably fit your cute penis inside me entirely, all the way to the base of your shaft..."
        m 4hubfb "And I might be able to {i}eat you up{/i} without having to worry too much about choking. Ahaha!"
        m 2ruc "I know some girls make a big deal about length, but it doesn't really matter all that much to me."
        m 3eud "It's like breast size for girls, after all. There's not really anything you can do to change it."
        m 3hub "We just have to love the bodies we have, you know?"
        m 5hubsa "I love you no matter how big you are, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."

    elif persistent._nsfw_dick_length < 14.7: # 5.2" - 5.8"
        python:
            if persistent._nsfw_units_metric:
                average_length = "fourteen centimeters"
            else:
                average_length = "five and a half inches"
        m 1eubsb "Not bad at all, [player]! That's a good size."
        m 3eud "Supposedly, the average length for men is around [average_length]."
        m 2eublb "Some people make a big deal out of penis length, but your size is great for me."
        m 2tubfb "It means I won't have any trouble fitting you inside me when the time comes, ahaha!"

    elif persistent._nsfw_dick_length < 21.0: # 5.8" - 8.3"
        m 1subfo "Wow!"
        m 3wubfb "That's pretty big, [player]! {w=0.4}{nw}"
        extend 3tkbfu "You never cease to impress me, you know that?"
        m 1eubsb "You shouldn't have any problems at all pleasing me with your {i}massive{/i} member. {w=0.4}{nw}"
        extend 5hubsb "Ahaha!"
        m 3rkbssdlb "Though, it could possibly hurt a little if you try to fit the whole thing inside me..."
        m 1tubssdlb "And I might choke a bit if I try to {i}eat you up{/i}."
        m 5tubsa "Let's take things nice and slow when the time comes, okay, [mas_get_player_nickname()]?"
        m 6gsbfa "...{w=0.7}{nw}"
        m 6msbfa "..."
        m 7hkbfsdlb "Sorry, I was just daydreaming for a moment..."
        m 3dkbfb "Just thinking about your long, thick penis makes me a little wet. Ehehe~"
        m 5hubfa "I love you so much, [mas_get_player_nickname(exclude_names=['my love', 'love'])]. {w=0.4}{nw}"
        extend 5dubfa "I can't wait until I cross over and we can press our bodies together for real."

    elif persistent._nsfw_dick_length < 48.0: # 8.3" - 18.9"
        m 1wubssdlo "Oh jeez, [player]..."
        m 1hkbssdlb "That's pretty tremendous. I can only imagine how impressive you must look."
        m 3eud "I read that only a very small percentage of people actually have penises that large."
        m 4rkbfsdlb "You'll have to be really gentle with me, otherwise I might get hurt!"
        m 6ekbfsdla "I don't think I'd be able to fit the whole thing inside... In my mouth or my...{w=0.4}{nw}"
        extend 6rkbfsdla "you know..."
        m 5hubsa "I'm sure we'll find a way to make things work, [mas_get_player_nickname()]. Ahaha!"

    else: # 18.9" or greater (larger than world record)
        m 1hkbssdlb "You're so silly, [player]!"
        m 3rkbssdlb "I don't know if {i}anyone{/i} in the world is that big..."
        m 3hkbssdlb "If you're really not joking with me, then you could probably make it into a world record book. Ahaha!"
        m 1ekbssdla "I just hope it doesn't inconvenience you in everyday life."
        m 4eubsc "After all, it's like breast size for girls. Some people are just naturally really small or really large."
        m 4hkbssdlb "Some girls with big chests tend to have problems too. Remember how much back pain Yuri had?"
        m 2hkbssdlb "Ahaha..."
        m 5tubfu "Anyway, I love you no matter how you look, [mas_get_player_nickname(exclude_names=['my love', 'love'])]. Big or small."
        return "derandom|love"

    m 3eub "While we're on this topic, I have another question..."
    m 2rubssdlc "..."
    m 2rkbssdlb "Oh gosh, this is so awkward..."
    m 1ekbfsdlb "[player], are you circumcised?"
    $ _history_list.pop()
    menu:
        m "[player], are you circumcised?{fast}"

        "Yes.":
            $ persistent._nsfw_dick_circumcised = True
            m 1hubfb "Ahaha!"
            m 1eubsb "Whether it's for medical or religious reasons, or you had it done when you were a baby...{w=0.4}{nw}"
            extend 3hubfb "I think that's really cute, [mas_get_player_nickname()]!"
            m 4eubfb "I've read that some guys don't like the fact that they're circumcised. But personally, I think I like the 'streamlined' appearance!"
            m 1hubsa "Ehehe~"

        "No.":
            $ persistent._nsfw_dick_circumcised = False
            m 1eubfb "I see, [player]. So you're 'uncut', huh?"
            m 3tubfu "I can just picture pulling back your cute foreskin..."
            m 5hubsb "Just don't forget to keep it clean under there for me, [player]. Ahaha!"

        "...":
            m 1lkbssdlb "I'm sorry... That was a strange question of me to ask. {w=0.4}{nw}"
            extend 1hkbssdlb "Ahaha!"
            m 2dkbssdlc "I didn't mean to make you feel uncomfortable. It's a really personal question and you don't have to answer."
            m 5ekbla "Just remember, I love you no matter how you look, [mas_get_player_nickname(exclude_names=['my love', 'love'])]."
            return "derandom|love"

    m 1ekbsb "Thanks for being so patient with my questions, [mas_get_player_nickname()]."
    m 3eubsd "I've never seen an actual penis before, but {w=0.4}{nw}"
    extend 3dubsa "being able to picture yours really means a lot to me."
    m 2ekbsa "And even if you {i}were{/i} bigger or smaller, I wouldn't think any more or less of you."
    m 1eubsb "Whatever size you are, cut or uncut, I think it's perfect. I love everything about you, after all."
    m 1dubsa "The fact that you were willing to share all of these really personal things about yourself makes me feel that much closer to you."
    m 5hubfb "I love you, [player]~"

    if persistent._mas_first_kiss:
        call monika_kissing_motion_short

    return "love"

# Thankyou for writing this topic, KittyTheCocksucker
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_favorite_position",
            category=['sex'],
            prompt="[player]'s favorite position",
            conditional=(
                "mas_canShowRisque(aff_thresh=400) "
                "and persistent._nsfw_genitalia == 'P'" # Need to add a version for women
                ),
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
        m 2rkbssdlb "I know we already talked about sex before, but..."
        m 3ekbssdla "It's still extremely embarrassing to talk about this kind of stuff..."
    m 1dubsa "Ahem..."
    m 3eubfb "So...What's your favorite sex position?"

    $ _history_list.pop()
    menu:
        m "So...What's your favorite sex position?{fast}"

        "Doggy style.":
            m 1etbfa "Oh? Really?"
            m 1rtbfa "Hmm...I guess that isn't so surprising."
            m 3eubfb "It {i}is{/i} the one of the most popular positions around the world, after all."
            m 3tubfa "I can see why so many people would like it, honestly!"
            m 4tubfb "The guy can get a really good view of his partner while they're doing it."
            m 4tubfu "I bet you'd like to see me from that perspective too, huh?"
            m 3hubfb "Ahaha! Don't get flustered~"
            m 1tubfa "Just knowing you're pleased and have a nice view of my body is enough for me to feel good, [mas_get_player_nickname()]~"

        "Missionary.":
            m 3ekbfa "Aww~ That is so cute, [player]!"
            m 4hubfb "I find missionary to be the most intimate and romantic position of all!"
            m 3gubfb "Just simply thinking about us, lying face-to-face, with our bodies up against one another makes my body feel warm. Ahaha~"
            m 1eubfa "I hope one day we can do it together!"
            m 1tubfa "I can tell you that I'm already looking forward to that day! Ahaha~"

        "Cowgirl.":
            m 3wubfd "Really? I wasn't expecting that."
            m 3ekbfsdlb "Don't take it the wrong way! Cowgirl sounds really fun; I just didn't think that would be your favorite one!"
            m 3rkbfsdla "I know I don't weigh that much...but even so, I think it would be quite tiring for you if I were to ride you, don't you think?"
            m 2rkbfsdla "I just worry you would get too exhausted from my humping."
            m 2dkbfsdlb "And...you know..."
            m 2ekbfsdlb "I want you to feel good, not to get tired!"
            m 1rubfa "But..."
            m 5tubfa "If you insist on liking it the most..."
            m 5tubfb "I'd be happy to saddle up and ride it real good! Ahaha~"

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
    m 3tsbla "Do you...{fast}have any fetishes?"
    $ _history_list.pop()
    menu:
        m "Do you...have any fetishes?{fast}"
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

default persistent._nsfw_genitalia = None # P: Penis, V: Vagina, U: Unknown ; Default: None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_genitalia",
            category=['sex'],
            prompt="[player]'s genitalia",
            conditional=(
                "renpy.seen_label('nsfw_monika_nsfwmodinstall') "
                "and mas_canShowRisque(aff_thresh=400)"
                ),
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_genitalia:
    m 1euc "Hey, [player]..."
    m 1ekbla "This is probably going to be an awkward question, but I was just wondering..."
    m 3ekbla "Do you have a penis or a vagina?"
    $ _history_list.pop()
    menu:
        m "Do you have a penis or a vagina?{fast}"

        "I have a penis.":
            $ persistent._nsfw_genitalia = "P"

        "I have a vagina.":
            $ persistent._nsfw_genitalia = "V"

        "I'd rather not say.":
            $ persistent._nsfw_genitalia = "U"
            m 1ekbla "That's okay, [player]. I understand."
            m 1hubla "If you change your mind, let me know."
            return

    m 1ekbla "Thank you for telling me, [player]."
    m 1rkbsa "I imagine that might have been awkward for you to answer..."
    m 1ekbsa "But this helps me much more than you can imagine."
    m 2dsbsa "..."
    m 2tsbsa "Now when we flirt, I know what is going on down there~"
    m 2gsbfa "..."
    m 1hubfb "Ahaha! Sorry. I just wanted to tease you a little."
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

default persistent._nsfw_sexting_success_last = None
default persistent._nsfw_has_unlocked_birthdaysuit = False

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
                $ persistent._nsfw_has_unlocked_birthdaysuit = True

                m 4hubsb "Ah~! That's much better."
                m 6tubsb "Ehehe~ Do you like what you see, [mas_get_player_nickname()]?"
                m 1gkbfu "..."
                m 1hkbfsdlb "Ahaha! Sorry, this is still kind of embarrassing for me."
                m 1mkbfsdlb "It might take a little getting used to..."
                m 1ekbfb "Thank you again. I love you so much, [player]~"
                return "love"
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

            "Go for it, [m_name].":
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

    elif mas_SELisUnlocked(mas_clothes_underwear_white):
        #if mas_nsfw.hour_check() and persistent._nsfw_has_unlocked_birthdaysuit == False:
        #    $ persistent._nsfw_has_unlocked_birthdaysuit = True
        m 3ekb "You're already familar with how I've been doing this while you've been away."
        m 3eublb "And I've got to say, it's been great!"
        m 3eublc "It's not for everyone though, so don't feel like I'm pressuring you..."
        m 2eubsb "I love you, [mas_get_player_nickname(exclude_names=['my love', 'love'])]. Both with clothes, and without."
        m 2gsbfa "..."
        m 2tsbfa "..."
        m 2wubfd "Ah! {w=0.4}{nw}"
        extend 2hubssdlb "Sorry, my mind was starting to wander..."
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
        m 1hubssdlb "I mean, like, later when you're not here!"
        m 1rubssdlb "Ahaha! It would be too embarrassing if you saw me in my underwear, let alone when I'm naked."

    return

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

# Masturbation Benefits - Unlocked if you use the "I'm going to masturbate" topic Once
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_masturbation_benefits",
            category=['sex'],
            prompt="Masturbation benefits",
            conditional=(
                "mas_canShowRisque(aff_thresh=400) "
                "and store.mas_getEVL_shown_count('nsfw_monika_brb_masturbate')"
                ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_masturbation_benefits:
    m 1rubsd "Umm, [player]?"
    m 1eubsc "I have something I want to talk to you about. "
    extend 3eubsc "I promise you that I'm being completely serious here..."
    m 1rubsd "This is about masturbation."
    m 1ekblb "Specifically...{w=1}it's about the {i}benefits{/i} of regular masturbation!"
    m 1ekbla "Are you okay with me talking about this?"
    $ _history_list.pop()
    menu:
        m "Are you okay with me talking about this?"

        "Yes.":
            m 2eub "Really? Okay!"
            m 1eua "You see, [player], I didn't give it much thought until recently."
            m 3eubla "Like a lot of people, I always thought masturbation was a...{w=0.5}{i}dirty habit{/i}, and nothing more."
            m 3eub "But I've done a bit of research, and it seems that masturbating now and again can actually be beneficial!"
            m 3rub "Among other things, it can of course reduce your stress..."
            m 3eua "The release of serotonin and dopamine can reduce anxiety, and ease muscle tension."
            m 3hksdlb "For women, it can even help ease period pains... {w=0.5}Ahaha..."
            m 3eub "For men, studies have shown that it reduces the risk of prostate cancer in certain cases."
            m 4eub "The reasons for this aren't fully known, but there {i}is{/i} a connection between the two."
            m 3eublb "The working theory seems to be that a regular release helps to keep the prostate healthy."
            m 4eua "For men and women alike, it can lead to better sexual satisfaction. {w=0.5}It makes sense, if you think about it!"
            m 3eubla "If you know your own body, then you'll have an easier time conveying to your partner what you like..."
            m 2efc "Now, with all that in mind...!"
            m 3efd "Masturbation addiction can be a serious issue."
            m 3efd "The benefits I mentioned...the dopamine release... Chasing that high too often {i}is{/i} bad for you."
            m 4efd "People who masturbate {i}too{/i} frequently can have a harder time getting off with a partner..."
            m 1eud "Not to mention, if you use porn to get off, especially visual media...{w=0.5}you can become desensitized to more {i}vanilla{/i} experiences."
            m 1eud "Masturbating more than once a day..."
            extend 1tud "is probably a little too much."
            m 2hsc "..."
            m 1eua "Thank you for letting me talk about this, [player]."
            m 3eubfb "Talking about masturbation like this is surprisingly fun!"
            m 5tubfu "It's a natural part of human sexuality, after all."
            m 5kublu "There's nothing wrong with having a bit of {i}fun{/i} by yourself now and then~"

        "Not right now.":
            m 2eubsb "I understand, [player]."
            m 1lkblb "I promise you I wasn't going to tell you off or anything, but..."
            m 1eubsb "Maybe some other time, then!"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_nsfwmodinstall",
            category=['sex'],
            prompt="NSFW Mod install",
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

    if persistent._mas_player_confirmed_bday and mas_is18Over():
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

# Thankyou for writing this topic, KittyTheCocksucker
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_oralsex",
            category=['sex'],
            prompt="Oral sex",
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
            oral_prompt = "Have you ever had someone eat out your pussy?"
            oral_answer1 = "eaten a woman out"
        else:
            oral_prompt = "Have you ever received oral sex?"
            oral_answer1 = "given oral sex" # Awkward

    m 1rkbla "..."
    m 1rkblb "Umm..."
    m 3ekblb "Please forgive me if what I'm going to ask is too intimate and out-of-nowhere, but..."
    m 3rkbla "[player]... Have you..."
    m 3rkblb "[oral_prompt]"

    $ _history_list.pop()
    menu:
        m "[oral_prompt]{fast}"

        "Yes.":
            m 1wubld "Oh...you have?"
            m 1subld "Wow."
            m 1rublsdlb "I-I mean, please don't take it the wrong way! I wasn't surprised because I didn't think you could get a girl to do that for you!"
            m 3rublsdlb "It's just that... Ahaha..."
            m 3ekbla "Well, it's a very intimate action and I thought I could be the first one to do it for you..."
            m 3wubsd "Of course, I'm not mad at you or anything for having already done it with somebody else!"
            m 3rkbsb "It actually might be for the better that you have some previous experience with it!"
            m 1rkbsa "I've never [oral_answer1] before so if we were to do it together, I'd need some guidance from you~ Ahaha~"

        "No.":
            m 1wubld "Oh, you haven't?"
            m 1hublb "Ahaha~ Well... I honestly almost expected that someone as [gender_desc] as you had already had [oral_answer2] serviced by someone~"
            m 3ekbla "Don't worry about it though! I've never [oral_answer1] before either, so it means that we can take each other's first time!"
            m 3rkbssdla "I'll probably be very clumsy when we do get to that point though...but..."
            m 3ekbssdlb "I promise you I will try my best to properly pleasure you!"
            m 1gkbssdlb "And of course... Ahaha~"
            m 1gkbssdla "...In case I'm doing a bad job..."
            m 5tubsa "You can always just...ahem..."
            m 5tubsb "Take control~"

        "Uhh... Let's not talk about this.":
            m 3wkbld "..."
            m 3wkbld "I'm..."
            m 3wkblo "I'm really sorry, [player]..."
            m 3rkbld "I just..."
            m 1dkbsc "I don't know what I was thinking... Gosh..."
            m 1dkbstpc "I have no idea what I was thinking, asking something like this out of the blue..."
            m 1ekbstpd "Please just forget I said anything..."
            return "derandom"

    if mas_safeToRefDokis(): # Maybe section for the vagina variety? Maybe.
        m 2ekbsa "So, I..."
        m 2rkbsa "I know that you didn't get the chance to get to know Sayori, Natsuki, and Yuri too much..."
        m 2ekbsa "But...umm..."
        m 2hkbssdlb "Again, this might sound like a really weird question. Please just ignore it if you want..."
        m 2hkbssdla "But..."
        m 3ekbssdlb "Who do you think would be the best at oral sex?"

        $ _history_list.pop()
        menu:
            m "Who do you think would be the best at oral sex?{fast}"

            "Sayori.":
                $ mas_loseAffection(2) # Sayori? Really?
                m 3rkbssdlb "Heh..."
                m 3rkbssdla "I kind of guessed you would pick her."
                m 3ekbsb "I don't know why, but...I think you might have a point."
                if persistent._nsfw_genitalia == "P":
                    m 3eubsb "Sayori would probably give pretty enjoyable blowjobs."
                    m 1eubsa "She's the type of girl who places everyone else's happiness before her own."
                    m 1tubsa "So she might not care about gagging and being slightly air-deprived if you were to push it into her throat."
                    m 1mubsa "She would just take it in silence, probably even using her free hands and tongue to pleasure you further."
                m 2mubsb "Her only objective would be to make you feel good, without minding her own well-being."
                m 5tubsa "But...I guess we're never going to find out if that's true or not, huh?"

            "Natsuki.": # Just no
                $ mas_loseAffection(2)
                m 3wubso "Huh?"
                m 3etbsc "...Really?"
                m 3gtbsc "Hmm... I wasn't expecting you to pick {i}her{/i}."
                m 1dtbsc "..."
                if persistent._nsfw_genitalia == "P":
                    m 1esbsc "I can't even think of a reason why you would think that Natsuki would give better blowjobs than Yuri, Sayori or me."
                else:
                    m 1esbsc "I can't even think of a reason why you would think that Natsuki would give better oral sex than Yuri, Sayori or me."
                m 1efbsc "Like... Natsuki is so immature! Why would she do it better than all of us?"
                m 1dfbsc "..."
                m 2dfbssdld "N-no, I'm not mad! Why would I be mad?"
                m 2dkbssdlc "..."
                m 2dkbssdla "Ahem..."
                m 2mkbssdlb "Okay, I might be a bit mad."
                m 2efbssdlo "But really, why do you think that Natsuki would be so good at itl?!"

                $ _history_list.pop()
                menu:
                    m "But really, why do you think that Natsuki would be so good at it?!{fast}"

                    "Sorry, you're right... I should have answered one of you instead...":
                        m 2ekbsa "It's alright, [player]."
                        m 1hubssdlb "I don't know why I got so upset over that."
                        m 1eubsa "Let's talk about something else."

                    "She has a bunch of manga volumes so she probably has a few doujins too. She must have learned some techniques from those.":
                        m 2dsbsc "..."
                        m 2rsbsd "I guess..."
                        m 2rtbsb "Now that I think about it, you might be right."
                        m 1eubsb "I remember that one time when she and I were rearranging her mangas together, I happened to take a weird manga in my hand..."
                        m 3wubsd "But she snatched it away from me really fast, so I couldn't really inspect it properly."
                        m 3rubsd "It might have been one of her doujins..."
                        m 3eubsd "There is a chance that she learned a few tricks from reading them, you're right."
                        m 3hubsb "Ahaha~"
                        m 1ekbsa "Sorry for getting mad at you for a moment there."

            "Yuri.": # I respect the hustle
                $ mas_loseAffection(2)
                m 3etbsc "You think so?"
                m 3rtbsc "Hmm, yeah. I guess she would probably do a good job."
                if persistent._nsfw_genitalia == "P":
                    m 1rtbfu "But honestly, I see her as being more suited for using her breasts to do the job."
                    m 1ekbfu "But I guess one doesn't disqualify the other, huh?"
                m 1tkbfu "I'm sure she would be passionate about it, at least..."
                m 5tubfu "Although, she might be reluctant to per her tongue on it at first, and would just stall for time with her hands...ahaha~"
                m 5tubsa "But...I guess we're never going to find out if that's true or not, huh?"

            "You.":
                $ mas_gainAffection(1) # Smart
                m 3wubsd "Oh."
                m 3hubsb "Ahaha! Even though I mentioned that I have no experience with it, you still think that I could give the best head?"
                m 3ekbsa "[player], you're too sweet!"
                m 3tubsa "..."
                m 3gubsb "Well... I don't know if you meant it as a compliment or not...ahaha..."
                m 1tubsb "But I'll take it as a compliment~"
                if persistent._nsfw_genitalia == "P":
                    m 1tubfa "And once I cross over and actually suck you off..."
                    m 1tubfb "I won't disappoint you, [player]!"

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

    if persistent._nsfw_genitalia == "P":
        if persistent.gender == "M":
            m 4eubla "I've read that condoms are the most preferable form of protection for men."
        else:
            m 4eubla "I've read that condoms are the most preferable form of protection for people with penises."
        m 4eublb "It's a latex-rubber 'sheath' that you put around..."
        m 4wsbsd "..."
        m 2dfbsa "{i}Ahem{/i}..."
        m 2lkbfa "...You get the idea."
        m 2lkbsb "It prevents any kind of fluid swapping during sex, which is supposed to prevent pregnancy and STDs."
    elif persistent._nsfw_genitalia == "V":
        if persistent.gender == "F":
            m 4eubla "I've read that there are condoms available for women, but they aren't as popular as the men's version."
        else:
            m 4eubla "I've read that there are 'internal condoms' that stay in the vagina, but they aren't as popular as the kind that goes over the penis."
        m 4eub "The most popular form of contraception seems to be 'The Pill'...{w=0.4}{nw}"
        extend 4hksdlb "which sounds kind of ominous if you ask me."
        m 4eub "It's exactly what it says it is, a pill you take to prevent pregnancy."
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
    extend 3rsbsb "{i}sexual{/i} nature."
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
    m 2rkbsb "They'll tell their partner what they want to do with them... "
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

default persistent._nsfw_sexting_attempts = 0

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_sexting_horny",
            conditional=(
                "mas_canShowRisque(aff_thresh=1000) "
                "and persistent._nsfw_sexting_success_last != None "
                "and persistent._nsfw_monika_sexting_frequency != 3 "
                "and mas_timePastSince(persistent._nsfw_sexting_last_sexted, datetime.timedelta(seconds=5)) "
                "and mas_timePastSince(mas_getEVL_last_seen('nsfw_monika_sexting_horny'), datetime.timedelta(seconds=5))"
                ),
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_sexting_horny:
    # Count this attempt, but only if less than the frequency requested.
    if persistent._nsfw_sexting_attempts >= persistent._nsfw_monika_sexting_frequency:
        $ persistent._nsfw_sexting_attempts = persistent._nsfw_monika_sexting_frequency
    else:
        $ persistent._nsfw_sexting_attempts += 1

    # If our number of attempts matches the player's frequency request, then try to sext
    if persistent._nsfw_sexting_attempts == persistent._nsfw_monika_sexting_frequency:
        m 1eua "Hey, [player]." # TODO: Make proper dialogue for this bit
        m 1eua "I wanna sext with you."
        m 1eua "Are you up for it?"
        $ _history_list.pop()
        menu:
            m "Are you up for it?{fast}"

            "Yes.":
                $ persistent._nsfw_sexting_attempts = 0
                m 1eua "Great!"
                call nsfw_sexting_init

            "No.":
                m 1eua "Aww..."
                m 1eua "Okay, [player]."

    $ mas_flagEVL("nsfw_monika_sexting_horny", "EVE", EV_FLAG_HFRS)

    call nsfw_monika_sexting_horny_end

    return "no_unlock"

label nsfw_monika_sexting_horny_end:
    # Copy of monika_holdme_end label
    python:
        with MAS_EVL("nsfw_monika_sexting_horny") as sexting_horny_ev:
            sexting_horny_ev.random = False
            sexting_horny_ev.conditional = (
                "mas_canShowRisque(aff_thresh=1000) "
                "and persistent._nsfw_sexting_success_last != None "
                "and persistent._nsfw_monika_sexting_frequency != 3 "
                "and mas_timePastSince(persistent._nsfw_sexting_last_sexted, datetime.timedelta(hours=12)) "
                "and mas_timePastSince(mas_getEVL_last_seen('nsfw_monika_sexting_horny'), datetime.timedelta(hours=12))"
            )
            sexting_horny_ev.action = EV_ACT_RANDOM
        mas_rebuildEventLists()
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_sexualpast",
            category=['sex'],
            prompt="[player]'s sexual past",
            conditional="mas_canShowRisque(aff_thresh=400)",
            action=EV_ACT_RANDOM,
            aff_range=(mas_aff.ENAMORED, None)
        )
    )

label nsfw_monika_sexualpast:
    m 1rubsd "Umm... [player]?"
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
                m 1rsblu "But..."
                m 1lkbfb "I want to have sex with you, too."
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