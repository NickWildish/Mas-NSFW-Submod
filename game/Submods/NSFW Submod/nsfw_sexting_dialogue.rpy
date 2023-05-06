init python in mas_nsfw_sexting_dialogue:
    import store

    ## SEXTING PROMPTS ##

    ## CATEGORIES ("types", 1st element of the tuple) ##
    # "CMP" -          | Prompts, Quips, and Responses | Compliment
    # |-"THK" -        | Responses                     | Thankyou
    # |-"CMP" -        | Responses                     | Return compliment
    # |-"CRM" -        | Responses                     | Compliment remark
    # "CMD" -          | Prompts, Quips, and Responses | Command
    # |-"CPL" -        | Responses                     | Comply
    # "STM" -          | Prompts, Quips, and Responses | Statement
    # "ARA" -          | Responses                     | "Ara ara" equivalent
    # "DES" -          | Prompts, Quips, and Responses | Desire
    # |-"LED" -        | Responses                     | Leading
    # |-"PLY" -        | Prompts and Quips             | Player-centred desire
    # |-"MON" -        | Prompts and Quips             | Monika-centred desire
    # |-"DRM" -        | Responses                     | Desire remarks
    # | |-"PLY" -      | Responses                     | Player-centred remark
    # | |-"MON" -      | Responses                     | Monika-centred remark
    # "QUE" -          | Prompts, Quips, and Responses | Question
    # |-"QYS" -        | Prompts, Quips, and Responses | Question with "Yes" answer
    # |-"QNO" -        | Prompts, Quips, and Responses | Question with "No" answer
    # |-"QAG" -        | Prompts, Quips, and Responses | Question with "Agree" answer
    # |-"QDG" -        | Prompts, Quips, and Responses | Question with "Disagree" answer
    # |-"QSP" -        | Prompts, Quips, and Responses | Question with "Specific" answer
    # |-"QAT" -        | Prompts, Quips, and Responses | Tag question with "Affirm" answer
    # |-"QDT" -        | Prompts, Quips, and Responses | Tag question with "Deny" answer
    # "ANS" -          | Responses                     | Answer
    # |-"ADK" -        | Responses                     | Answer with "Don't know" answer
    # |-"AYS" -        | Responses                     | Answer with "Yes" answer
    # |-"ANO" -        | Responses                     | Answer with "No" answer
    # |-"AAG" -        | Responses                     | Answer with "Agree" answer
    # |-"ADG" -        | Responses                     | Answer with "Disagree" answer
    # |-"ASP" -        | Responses                     | Answer with "Specific" answer
    # |-"AAT" -        | Responses                     | Answer with "Affirm" answer
    # |-"ADT" -        | Responses                     | Answer with "Deny" answer

    # The "subtype" (2nd element of the tuple) allows the response to be more specific.
    # The subtype is independent from the type. But of course, only certain combinations of types and subtypes will be used.
    # Some are more common than others.

    # Subtypes are encoded with these crappy, cryptic three-letter tags. Each prompt has only one tag - try to pick the most specific one possible.
    # If you don't know what to pick / don't want to bother with this just pick "GEN".
    # Not all will be used but I have listed the codes here for future expansion.

    # "GEN" - Generic, use this for lines with no specific subtype.
    # "KIS" - Special subtype for prompts that should immediately trigger a kiss.
    # "UND" - Special subtype for prompts where Monika should undress.
    # "CHE" - Special subtype for prompts where there is cheesiness afoot / cheesy lines.

    # "MPS" - Monika's personality
    # "MFS" - Monika's face in general
    # | "MFE" - Monika's eyes
    # | "MFL" - Monika's lips
    # | "MFN" - Monika's nose
    # | "MFC" - Monika's cheeks
    # "MBD" - Monika's body in general
    # "MTH" - Monika's thighs
    # "MHR" - Monika's hair
    # "MBR" - Monika's breasts
    # "MCK" - Monika's nipples
    # "MVG" - Monika's vagina
    # "MBH" - Monika's anus
    # "MFT" - Monika's feet
    # "MCL" - Monika's clothes
    # "MCT" - Monika's thighhighs

    # "PPS" - Player's personality
    # "PFS" - Player's face in general
    # | "PFE" - Player's eyes
    # | "PFL" - Player's lips
    # | "PFN" - Player's nose
    # | "PFC" - Player's cheeks
    # "PBD" - Player's body in general
    # "PTH" - Player's thighs
    # "PHR" - Player's hair
    # "PBR" - Player's breasts. Prompts with this go under sext_prompts_sexy_f.
    # "PCK" - Player's nipples
    # "PVG" - Player's vagina. Prompts with this go under sext_prompts_sexy_v.
    # "PBH" - Player's anus. It is assumed that all players have anuses...
    # "PFT" - Player's feet
    # "PCL" - Player's clothes
    # "PPN" - Player's penis. Prompts with this go under sext_prompts_sexy_p.

    # "ONM" - masturbation, Monika
    # "ONP" - masturbation, player

    # "FSM" - player touching Monika
    # "FSP" - Monika touching player
    # "FBJ" - fellatio. Prompts with this go under sext_prompts_sexy_p.
    # "FHJ" - handjob. Prompts with this go under sext_prompts_sexy_p.
    # "FFJ" - footjob. Prompts with this go under sext_prompts_sexy_p.
    # "FFM" - vaginal fingering, Monika receiving
    # "FFP" - vaginal fingering, player receiving. Prompts with this go under sext_prompts_sexy_v.
    # "FXM" - anal fingering, Monika receiving
    # "FXP" - anal fingering, player receiving
    # "FCM" - cunnilingus, Monika receiving
    # "FCP" - cunnilingus, player receiving. Prompts with this go under sext_prompts_sexy_v.
    # "FAM" - anilingus, Monika receiving
    # "FAP" - anilingus, player receiving
    # "FTY" - acts involving sex toys
    # "FBM" - player using bondage on Monika
    # "FBP" - Monika using bondage on player
    # "FHH" - acts involving hand-holding
    # "FKS" - acts involving kissing

    # "IVG" - intercourse, general
    # "IPV" - intercourse, player with penis. Prompts with this go under sext_prompts_sexy_p.
    # "IVV" - intercourse, player with vagina. Prompts with this go under sext_prompts_sexy_v.
    # "IAM" - anal, Monika receiving
    # "IAP" - anal, player receiving
    # "IOM" - Monika's orgasm
    # "IOP" - Player's orgasm
    # "IOT" - orgasming together

    # "CFM" - Player's semen on Monika's face. Prompts with this go under Prompts with this go under sext_prompts_sexy_p..
    # "COM" - Player's semen on Monika's breasts. Prompts with this go under sext_prompts_sexy_p.
    # "CBM" - Player's semen on Monika's body in general. Prompts with this go under sext_prompts_sexy_p.
    # "CMM" - Player's semen in Monika's mouth. Prompts with this go under sext_prompts_sexy_p.
    # "CPM" - Player's semen in Monika's pussy. Prompts with this go under sext_prompts_sexy_p.
    # "CAM" - Player's semen in Monika's butt. Prompts with this go under sext_prompts_sexy_p.

    # "SUB" - Player action is dominating
    # "DOM" - Player action is submitting

    # This horrible three-letter code system works with regex!
    # The first letter indicates a general topic:
    # M - Monika's body, appearance, traits
    # P - Player's body, appearance, traits
    # O - masturbation ("onanism")
    # F - foreplay and nonpenetrative actions
    # I - intercourse and orgasm
    # C - Player's semen ("cum"). These C subtypes are only applicable for players with penises.
    # The second letter is A or X if the subtype has to do with "butt stuff".
    # The third letter is M if Monika receives it, and P if the player receives it.

    monika_nickname = store.persistent._mas_monika_nickname

    # Sexting prompts for your average compliment
    sext_prompts_cute = [
    #   |---------------------|--------------|---------------------------------------------------------------------------|
    #   |        Types        |   Subtypes   |                                 Prompt                                    |
    #   |---------------------|--------------|---------------------------------------------------------------------------|
        (["CMP"],              ["GEN"],        _("Every day with you is a good day.")), #8
        (["CMP"],              ["GEN"],        _("Everything makes me think of you.")), #16
        (["CMP"],              ["GEN"],        _("You live rent-free in my heart.")), #3
        (["CMP"],              ["MBD", "CHE"], _("I guess your parents are bakers, because they made you such a cutie pie!")), #0
        (["CMP"],              ["MBD"],        _("Seeing you every day always makes me grin like an idiot.")), #13
        (["CMP"],              ["MBD"],        _("The night sky holds nothing to your beauty.")), #10
        (["CMP"],              ["MBD"],        _("You look stunning today.")), #2
        (["CMP"],              ["MFE"],        _("You have gorgeous eyes.")), #5
        (["CMP"],              ["MFL"],        _("You have a beautiful smile.")), #6
        (["CMP"],              ["MFS"],        _("The one thing I can't resist in this life is your lips.")), #1
        (["CMP"],              ["MHR"],        _("You have beautiful hair.")), #4
        (["CMP"],              ["MPS"],        _("I always have a great time with you.")), #7
        (["CMP"],              ["MPS"],        _("I really like getting to know you.")), #15
        (["CMP"],              ["MPS"],        _("You make my heart happy.")), #19
        (["CMP"],              ["MPS"],        _("You never fail to give me butterflies.")), #18
        (["DES", "MON"],       ["FSP"],        _("I want you to hold me.")), # 20
        (["DES", "PLY"],       ["GEN"],        _("Cuddling with you would be perfect right about now.")), #11
        (["DES", "PLY"],       ["GEN"],        _("I wish I could hold you close right now.")), #9
        (["QUE", "QSP", 0],    ["MBD"],        _("Why are you so cute?")), #12
        (["QUE", "QSP", 1],    ["MBD"],        _("Is it getting hot in here, or is it just you?")), #17
        (["QUE", "QYS"],       ["GEN"],        _("Our first kiss after you cross over is going to be wonderful, don't you think?")), #14
    ]

    # Sexting prompts for your more 'risque' options
    sext_prompts_hot = [
    #   |--------------|--------------|---------------------------------------------------------------------------|
    #   |     Type     |   Subtypes   |                                 Prompt                                    |
    #   |--------------|--------------|---------------------------------------------------------------------------|
        (["CMD"],       ["UND", "DOM"], _("Take off your clothes. I want to see your beautiful body.")), #11
        (["CMP"],       ["GEN"],        _("You're all I can think about.")), #17
        (["CMP"],       ["MBD"],        _("You have a really sexy figure.")), #0
        (["CMP"],       ["MBD"],        _("You're so sexy.")), #15
        (["CMP"],       ["MBD"],        _("Your body is so hot.")), #14
        (["CMP"],       ["UND", "MBD"], _("I'm picturing you naked right now... Damn, you look good.")),
        (["DES", "MON"],["FSM"],        _("I want to feel your hot breath on my skin as we feel each other.")), #13
        (["DES", "PLY"],["FSM", "DOM"], _("I want to lay you down on my bed as we kiss.")), #12
        (["DES", "PLY"],["FSM", "DOM"], _("When we're together, I want to have you lie back and let me take care of you.")), #18
        (["DES", "PLY"],["FSM", "FSP"], _("I want to hold your hands in mine.")), #4
        (["DES", "PLY"],["FSM", "MHR"], _("I want to run my hands through your hair.")), #3
        (["DES", "PLY"],["FSM"],        _("I want to bring you in close.")), #1
        (["DES", "PLY"],["KIS"],        _("I really want to kiss you right now.")), #5
        (["DES", "PLY"],["KIS"],        _("I want to hold you in my arms as we kiss.")), #9
        (["DES", "PLY"],["KIS"],        _("I want to kiss your lips passionately.")), #2
        (["DES", "PLY"],["MBD"],        _("I want to run my hands along your body while I kiss your neck.")), #6
        (["STM"],       ["GEN"],        _("I can't wait to be alone with you.")), #16
        (["STM"],       ["GEN"],        _("I feel nervous about telling you all of the sexual desires I have when it comes to you.")), #7
        (["STM"],       ["KIS"],        _("If kissing is the language of love, then we have a lot to talk about.")), #8
        (["STM"],       ["PCL"],        _("I'm wearing something you might like right now.")), #19
        (["STM"],       ["UND"],        _("What you're wearing would look even better on my bedroom floor.")), #10
    ]

    # Sexting prompts for your most 'risque' options
    sext_prompts_sexy = [
    #   |---------------------|--------------|---------------------------------------------------------------------------|
    #   |        Type         |   Subtypes   |                                 Prompt                                    |
    #   |---------------------|--------------|---------------------------------------------------------------------------|
        (["CMD"],              ["ONM", "DOM"], _("Gently spread open your pussy lips for me, " + monika_nickname + ".")),
        (["CMD"],              ["ONM", "DOM"], _("I want you to gently rub your clit, " + monika_nickname + ".")),
        (["CMD"],              ["ONM", "DOM"], _("I want you to stick those soft fingers of yours up your pussy for me, " + monika_nickname + ".")),
        (["CMD"],              ["ONM", "DOM"], _("Start touching yourself more quickly, " + monika_nickname + ".")),
        (["CMD"],              ["ONM", "DOM"], _("Touch yourself slowly for me, " + monika_nickname + ".")),
        (["CMP"],              ["GEN"],        _("Everything about you turns me on.")),
        (["CMP"],              ["GEN"],        _("I bet you have the sexiest sounding moans in the world.")),
        (["CMP"],              ["GEN"],        _("I honestly think you're probably the most attractive person ever to have existed.")),
        (["CMP"],              ["GEN"],        _("I think you seriously have to be the hottest person alive.")),
        (["CMP"],              ["GEN"],        _("You're the best girl. And not just in the Literature Club - I mean in general.")),
        (["CMP"],              ["GEN"],        _("Yuri and Sayori weren't wrong when they said you're more desirable than the rest of the Literature Club combined.")),
        (["CMP"],              ["IOM", "MFS"], _("I bet you have a really hot orgasm face.")),
        (["CMP"],              ["MBD"],        _("Getting to see you naked is the best part of my day.")),
        (["CMP"],              ["MBD"],        _("You have a tremendously cute body.")),
        (["CMP"],              ["MBD"],        _("You have the sexiest body I've ever seen.")),
        (["CMP"],              ["MBD"],        _("Your body is perfectly shaped. I love how athletic you are.")),
        (["CMP"],              ["MBD"],        _("Your naked body is the most splendid thing I've ever witnessed.")),
        (["CMP"],              ["MBH"],        _("I bet you have a cute, tight little asshole, don't you?")),
        (["CMP"],              ["MBR"],        _("You have magnificent breasts.")),
        (["CMP"],              ["MCL", "MBD"], _("I get so flustered when you undress for me. You're gorgeous.")),
        (["CMP"],              ["MCL", "MBR"], _("Back when you wore that school uniform, one thing I really liked was how well the blazer fit around your breasts.")),
        (["CMP"],              ["MPS", "SUB"], _("I think there is something insanely sexy about a woman being in control. Don't you agree?")),
        (["CMP"],              ["MVG", "MBD"], _("I imagine your pussy must be gorgeous if it's anything like the rest of you.")),
        (["CMP"],              ["MZR", "MCL"], _("I love how you dress. Your thighhighs are incredibly hot.")),
        (["DES", "MON"],       ["FCM", "SUB"], _("I wish you were here so you could grind your pussy on my face until you come.")),
        (["DES", "MON"],       ["FCM", "SUB"], _("I wish you were here so you could sit on my face right now.")),
        (["DES", "MON"],       ["IAP", "SUB"], _("I want you to bend me over and fuck my ass with a strap-on.")),
        (["DES", "MON"],       ["ONP", "DOM"], _("I want to watch you masturbate for me.")),
        (["DES", "MON"],       ["ONP"],        _("I want to see you do with your pen what Yuri did with the main character's.")),
        (["DES", "PLY"],       ["FAM", "FFM"], _("I want to eat your ass out and finger you until you come.")),
        (["DES", "PLY"],       ["FAM"],        _("I want to bury my face in your ass.")),
        (["DES", "PLY"],       ["FAM"],        _("I want to snuggle my face in your ass.")),
        (["DES", "PLY"],       ["FCM", "IOM"], _("I want to lick your clit until you come.")),
        (["DES", "PLY"],       ["FCM"],        _("I'm dying to run my hot, sticky tongue over your pussy lips.")),
        (["DES", "PLY"],       ["FSM", "MBD"], _("I want to run my hands all over your smooth, toned body.")),
        (["DES", "PLY"],       ["FSM", "MBD"], _("When you cross over, I'm going to explore every single corner of your naked body.")),
        (["DES", "PLY"],       ["FTY"],        _("I want to brings sex toys into the bedroom with us and use them on you.")),
        (["DES", "PLY"],       ["IAM"],        _("I wish we were in the same room so I could fuck your ass right this moment.")),
        (["DES", "PLY"],       ["IOM"],        _("I want to hear you breathing in my ear when I make you orgasm.")),
        (["DES", "PLY"],       ["IOM"],        _("When you and I are finally together, I want to make you come so hard.")),
        (["DES", "PLY"],       ["IVG", "DOM"], _("I want to pin you down to the bed and have my way with you.")),
        (["DES", "PLY"],       ["IVG", "KIS"], _("I'm imagining us making out as we fuck again, and again, and again...")),
        (["DES", "PLY"],       ["IVG"],        _("I can't wait to be by your side. Or on top if you prefer.")),
        (["DES", "PLY"],       ["IVG"],        _("I wish I could fuck you in that spaceroom right now.")),
        (["DES", "PLY"],       ["IVG"],        _("I wish I could stay in that spaceroom with you forever so we could fuck each other every day until the end of time.")),
        (["DES", "PLY"],       ["IVG"],        _("If I could spend the rest of eternity with you in that spaceroom, I'd make you come every day until the universe ended.")),
        (["DES", "PLY"],       ["KIS", "FCM"], _("I wish I could kiss you... On both of your pairs of lips.")),
        (["DES", "PLY"],       ["MBR", "DOM"], _("I want to hold you down and fuck your breasts.")),
        (["DES", "PLY"],       ["MCK"],        _("I want to lick your nipples.")),
        (["DES", "PLY"],       ["MCK"],        _("I wish I could suck on your nipples right now.")),
        (["DES", "PLY"],       ["MTH", "FCM"], _("I can't wait to feel your thighs squeezing my head.")),
        (["DES", "PLY"],       ["UND", "FCM"], _("If you were here, I'd take your panties off with my teeth and... I'll just let you finish that sentence off.")),
        (["QUE", "QSP", 0],    ["ONP"],        _("I was just lying in bed for the last hour thinking about you... Guess what I was doing?")),
        (["QUE", "QSP", 1],    ["FSM", "MBD"], _("If I were with you right now, where would you want me to touch you?")),
        (["STM"],              ["FCM"],        _("Just the thought of eating you out makes me salivate.")),
        (["STM"],              ["GEN"],        _("I can't get aroused to the thought of anyone but you.")),
        (["STM"],              ["GEN"],        _("I can't wait to be alone with you.")),
        (["STM"],              ["GEN"],        _("I get so turned on thinking about you.")),
        (["STM"],              ["GEN"],        _("You're the only person I have eyes for, " + monika_nickname + ".")),
        (["STM"],              ["ONM"],        _("Be careful not to spill too much of your...juices on your chair, " + monika_nickname + ".")),
        (["STM"],              ["ONP"],        _("I get so horny thinking about you when I touch myself.")),
        (["STM"],              ["ONP"],        _("I'm clicking this option with one hand, because the other hand is busy.")),
    ]

    # Prompt choices specific to players with penises.
    sext_prompts_sexy_p = [
    #   |--------------|--------------|---------------------------------------------------------------------------|
    #   |     Type     |   Subtypes   |                                 Prompt                                    |
    #   |--------------|--------------|---------------------------------------------------------------------------|
        (["CMP"],       ["CFM"],        _("I bet you would look real cute with my cum all over your face.")),
        (["CMP"],       ["CMM"],        _("I bet you would look real cute with my cum dripping out of your mouth.")),
        (["CMP"],       ["KIS", "FBJ"], _("Your lips are perfect for kissing... I bet they'd be perfect for wrapping around my shaft as well.")),
        (["DES", "MON"],["CFM", "IOP"], _("I want to come all over your face and watch you try to lick it off.")),
        (["DES", "MON"],["CMM", "FBJ"], _("When we're together, I want you to take my cock in your mouth and swallow all my cum.")),
        (["DES", "MON"],["IAM", "DOM"], _("When we're finally together, I want you to take my cock up your ass, " + monika_nickname + ".")),
        (["DES", "MON"],["IPV"],        _("I'm picturing you bouncing up and down on my cock right now.")),
        (["DES", "MON"],["MFT", "FFJ"], _("I want you to rub your feet on my hard cock.")),
        (["DES", "PLY"],["CBM", "IOP"], _("I wish I could blow my load all over your thighs right now.")),
        (["DES", "PLY"],["CMM", "FBJ"], _("I want to see you swallow my thick, creamy load after blowing me.")),
        (["DES", "PLY"],["COM", "MBR"], _("I want to come all over your breasts.")),
        (["DES", "PLY"],["FBJ"],        _("I can't wait to you see you drooling all over my cock.")),
        (["DES", "PLY"],["FBJ"],        _("I'm just imagining my thick cock filling your mouth.")),
        (["DES", "PLY"],["FHJ"],        _("I wish it was your hand jerking me off right now.")),
        (["DES", "PLY"],["FHJ"],        _("I wish you could feel my throbbing cock right now.")),
        (["STM"],       ["ONP"],        _("I can't jerk off to anything but you any more, " + monika_nickname + ".")),
        (["STM"],       ["ONP"],        _("I'm stroking my rigid cock just for you, " + monika_nickname + ".")),
        (["STM"],       ["PPN", "ONP"], _("The onomatopoeia 'doki doki' sometimes gets translated as 'throbbing'... I'm sure you can imagine what I'm doing right now.")),
        (["STM"],       ["PPN"],        _("I get really hard just thinking about you.")),
    ]
    # if store.persistent._nsfw_genitalia == "P":
    #     sext_prompts_sexy.extend(sext_prompts_sexy_p)

    # I did not write any V / M / F prompts yet but these are here so they can be enabled later

    # Prompt choices specific to players with vaginas.
    # sext_prompts_sexy_v = [
    #     _(),
    # ]
    # if store.persistent._nsfw_genitalia == "V":
    #     sext_prompts_sexy.extend(sext_prompts_sexy_v)

    # Prompt choices specific to male players.
    # sext_prompts_sexy_m = [
    #     _(),
    # ]
    # if store.persistent.gender == "M":
    #     sext_prompts_sexy.extend(sext_prompts_sexy_m)

    # Prompt choices specific to female players.
    # sext_prompts_sexy_f = [
    #     _(),
    # ]
    # if store.persistent.gender == "F":
    #     sext_prompts_sexy.extend(sext_prompts_sexy_f)

    # Sexting prompts for the haha funnies

    # Each prompt requires a corresponding response in the return_sext_responses() function.
    # The subtype must be a string matching with the index (labelled ID) of the prompt under the sext_responses_funny list to work properly.
    sext_prompts_funny = [
    #   |-------|----|-------------------------------------------------------------------------------|
    #   | Types | ID |                                     Prompt                                    |
    #   |-------|----|-------------------------------------------------------------------------------|
        (["FUN"], "0", _("I put on my robe and wizard hat.")), #0
        (["FUN"], "1", _("It's not my fault that I fell for you... You tripped me!")), #1
        (["FUN"], "3", _("I looked hot today, you missed out.")), #3
        (["FUN"], "4", _("You like jazz?")), #4
        (["FUN"], "5", _("What do you want to do to me right now?")), #5 - Please fold my clothes neatly
        (["FUN"], "6", _("You've been a naughty girl.")), #6 - Santa will bring you a lump of coal
        (["FUN"], "7", _("I'm about to blow your mind with my sexting. Ready?")), #7 - Lay me into bed, your hands caress my body. Your palms are sweaty. Knees weak. Arms spaghetti.
        (["FUN"], "8", _("Want to have a threesome?")), #8
        (["FUN"], "9", _("What's a fantasy that you have for when we have sex one day?")), #9 - Scratching back, once a squirrel did that to me.
        (["FUN"],"10", _("What is a question that's on your mind right now?")), #10 - Where is your hand? In my bowl of Doritos.
        (["FUN"],"11", _("I kinda wanna do naughty things to you...")), #11 - Cool aid man - "Oh yeah."
        (["FUN"],"13", _("Are you feeling good right now?")), #13 - Hi [text here], I'm Dad.
        (["FUN"],"14", _("What's one of you're fetishes?")), #14 - Proper grammar... Well then your in luck.
        (["FUN"],"16", _("Would thou perchance wish to partake in coitus?")), #16
        (["FUN"],"17", _("You have big, beautiful nipples.")), #17
        (["FUN"],"18", _("Do I make you horny baby?")), #18 - Do I make you randy?
        (["FUN"],"19", _("You're so cute.")), #19 - You're stuch a stud / babe - You're a wizard, Harry.
    ]

    sext_prompts_funny_p = [
    #   |-------|----|-------------------------------------------------------------------------------|
    #   | Types | ID |                                     Prompt                                    |
    #   |-------|----|-------------------------------------------------------------------------------|
        (["FUN"],"12", _("You want to know what I have that is massive?")), #12 - My college debt.
        (["FUN"],"15", _("My wang is as hard as a prosthetic leg.")), #15 - Change for women. I'm as wet as
    ]
    if store.persistent._nsfw_genitalia == "P":
        sext_prompts_funny.extend(sext_prompts_funny_p)

    sext_prompts_funny_m = [
    #   |-------|----|-------------------------------------------------------------------------------|
    #   | Types | ID |                                     Prompt                                    |
    #   |-------|----|-------------------------------------------------------------------------------|
        (["FUN"], "2",  _("Do you like my shirt? It's made out of boyfriend material.")), #2
    ]
    if store.persistent.gender == "M":
        sext_prompts_funny.extend(sext_prompts_funny_m)

    # needs matching response

    # if store.mas_submod_utils.isSubmodInstalled("Custom Room Furnished Spaceroom V3"):
    #    sext_prompts_funny.extend([
    #        (["FUN"], "20", _("I want to fuck you on top of the piano.")),
    #    ])

    ## SEXTING QUIPS ##
    # Sexting quips for your average compliment
    sext_quips_cute = [
    #   |--------------|--------------|---------------------------------------------------------------------------|
    #   |     Type     |   Subtypes   |                                 Prompt                                    |
    #   |--------------|--------------|---------------------------------------------------------------------------|
        (["CMP"],       ["CHE"],        _("Are you a parking ticket? Because you've got 'FINE' written all over you")), #15
        (["CMP"],       ["CHE"],        _("Have you had your license get suspended for driving girls crazy?")), #17
        (["CMP"],       ["CHE"],        _("I should start calling you 'Mozzarella' since you're so cheesy")), #13
        (["CMP"],       ["CHE"],        _("If you were a chicken you'd be impeccable")), #4
        (["CMP"],       ["CHE"],        _("If you were a vegetable, you'd be a 'cute-cumber'")), #19
        (["CMP"],       ["GEN"],        _("You're such a cutie pie")), #9
        (["CMP"],       ["PPS"],        _("I love how kind you are")), #8
        (["CMP"],       ["PPS"],        _("I love how sweet you are")), #7
        (["CMP"],       ["PPS"],        _("You're just the cutest")), #1
        (["DES", "DRM"],["GEN"],        _("Your words are so flattering to me")), #5
        (["DES", "LED"],["GEN"],        _("Do tell me more")), #3
        (["DES", "MON"],["FSP"],        _("I wish I could hold you right now")), #11
        (["DES", "MON"],["KIS"],        _("I just want to kiss you right now")), #10
        (["DES", "PLY"],["PPS"],        _("Once we meet in the real world we need to do something about your cuteness")), #12
        (["STM"],       ["CHE"],        _("Are you a loan? Because you sure have my interest")), #18
        (["STM"],       ["CHE"],        _("Are you just saying that to get into my pants?{w=1.0} Ahaha! Just kidding~")), #6
        (["STM"],       ["CHE"],        _("If I could rearrange the alphabet I'd put 'U' and 'I' together")), #14
        (["STM"],       ["CHE"],        _("My clothes are made out of girlfriend material")), #16
        (["STM"],       ["CHE"],        _("Who told you that you could be this cheesy?")), #0
        (["STM"],       ["GEN"],        _("I love it when you get all cute like this")), #2
        (["STM"],       ["MFE", "MFS"], _("I'm quite happy with my eyes")),
        (["STM"],       ["MHR"],        _("I'm very proud of my hair")),
        (["STM"],       ["MPS"],        _("I always strive to be kind and supportive for you")),
        (["STM"],       ["MPS"],        _("I really feel like I can be myself around you")),
        (["STM"],       ["MPS"],        _("I'm so glad you like my personality so much")),
        # ([""], ["MFS"], _("")),
        # ([""], ["MFS"], _("")),
        # ([""], ["MFS"], _("")),
        # ([""], ["MFS", "MFE"], _("")),
        # ([""], ["MFS", "MFE"], _("")),
        # ([""], ["MFS", "MFL"], _("")),
        # ([""], ["MFS", "MFL"], _("")),
        # ([""], ["MFS", "MFL"], _("")),
        # ([""], ["MFS", "MFN"], _("")),
        # ([""], ["MFS", "MFN"], _("")),
        # ([""], ["MFS", "MFN"], _("")),
        # ([""], ["MFS", "MFC"], _("")),
        # ([""], ["MFS", "MFC"], _("")),
        # ([""], ["MFS", "MFC"], _("")),
        # ([""], ["MBD"], _("")),
        # ([""], ["MBD"], _("")),
        # ([""], ["MBD"], _("")),
        # ([""], ["MHR"], _("")),
        # ([""], ["MHR"], _("")),
        # ([""], ["MCL"], _("")),
        # ([""], ["MCL"], _("")),
        # ([""], ["MCL"], _("")),
    ]

    # Sexting quips for your more 'risque' options
    sext_quips_hot = [
    #   |--------------|--------------|---------------------------------------------------------------------------|
    #   |     Type     |   Subtypes   |                                 Prompt                                    |
    #   |--------------|--------------|---------------------------------------------------------------------------|
        (["CMP"],       ["GEN"],        _("You are my biggest turn-on")), #6
        (["DES", "MON"],["FHH"],        _("Once I cross over, I want to hold your hand. How lewd~")), #12
        (["DES", "MON"],["FKS"],        _("How would you feel about a makeout session once I cross over?")), #13
        (["DES", "MON"],["FKS"],        _("I would love to kiss you right now...among other things~")), #1
        (["DES", "MON"],["FSM"],        _("I want to feel you touching me all over")), #4
        (["DES", "MON"],["FTY"],        _("Have you thought about using toys with me? I wouldn't mind trying it with you")), #10
        (["DES", "MON"],["GEN"],        _("I can't wait to see you when I cross over")), #11
        (["DES", "MON"],["ONP", "ONM"], _("Is one of your hands busy right now? I might need to join you if so")), #18
        (["DES", "MON"],["PBD"],        _("I plan to wrap my arms around you and squish that cute butt of yours")), #15
        (["DES", "MON"],["PBD"],        _("I want to feel your body up and down...your chest especially")), #19
        (["STM"],       ["FSP", "PCL"], _("If I was with you now there would be no chance of you keeping your clothes on")), #5
        (["STM"],       ["GEN"],        _("Don't think that getting me this riled up will have no consequences")), #14
        (["STM"],       ["GEN"],        _("I could just eat you up")), #3
        (["STM"],       ["GEN"],        _("I want you to tell me more about what we'll do together in your world...in the bedroom particularly~")), #17
        (["STM"],       ["GEN"],        _("I've fantasized so much about when we finally get to talk like this")), #7
        (["STM"],       ["GEN"],        _("The border between our realities can be a real clam jam")), #16
        (["STM"],       ["GEN"],        _("You turn me on so much when you talk like that")), #8
        (["STM"],       ["GEN"],        _("You're making me feel really horny now")), #9
        (["STM"],       ["PBD"],        _("You know, I was daydreaming about you today. It was hot")), #2
        (["STM"],       ["PPS"],        _("Who said that you could be this hot?")), #0
    ]

    # Purely for describing player's eyes
    if store.persistent._mas_pm_eye_color:
        if isinstance(store.persistent._mas_pm_eye_color, tuple):
            eye_desc = "beautiful"
        else:
            eye_desc = store.persistent._mas_pm_eye_color
    else:
        eye_desc = "beautiful"

    # Sexting quips for your most 'risque' options
    sext_quips_sexy = [
    #   |--------------|--------------|---------------------------------------------------------------------------|
    #   |     Type     |   Subtypes   |                                 Prompt                                    |
    #   |--------------|--------------|---------------------------------------------------------------------------|
        (["CMD"],       ["FSM", "DOM"], _("I'm being so bad right now. I need you to punish me")), #8
        (["CMP"],       ["CHE"],        _("So, aside from being sexy, what do you do for a living?")), #1
        (["CMP"],       ["MVG"],        _("You really know how to make a girl wet")), #17
        (["DES", "MON"],["FKS"],        _("I can't wait to kiss you for real")), #3
        (["DES", "MON"],["FSM", "FSP"], _("I want to feel your warmth pressing against me")), #9
        (["DES", "MON"],["FSM", "SUB"], _("I'm tempted to leave a bite mark on your neck so everyone knows you're mine")), #7
        (["DES", "MON"],["PBD"],        _("I can't wait to see your sexy body when we're together")), #2
        (["DES", "MON"],["PCL"],        _("When I get to your world, I'm ripping your clothes off the second I walk through the door. I hope you're prepared")), #6
        (["DES", "PLY"],["IVG"],        _("I want you to tell me how much you want to do it with me")), #12
        (["DES", "PLY"],["KIS", "FKS"], _("I want you to kiss me~ Right now~")), #10
        (["DES", "PLY"],["MVG", "FCM"], _("I want to feel your tongue down there")), #18
        (["STM"],       ["FSM", "FSP"], _("I want to look into your " + eye_desc + " eyes as we press our bodies together")), #13
        (["STM"],       ["GEN"],        _("Who said that you could be this sexy?")), #0
        (["STM"],       ["GEN"],        _("Yes~ Just like that~")), #19
        (["STM"],       ["ONM"],        _("I'm touching myself right now just to the thought of you")), #5
        (["STM"],       ["PPS"],        _("I love how you talk to me when you're turned on")), #11
        (["STM"],       ["PPS"],        _("I love it when you're naughty")), #14
        (["STM"],       ["PVG"],        _("You're making me so wet")), #4
    ]

    sext_quips_sexy_p = [
    #   |--------------|--------------|---------------------------------------------------------------------------|
    #   |     Type     |   Subtypes   |                                 Prompt                                    |
    #   |--------------|--------------|---------------------------------------------------------------------------|
        (["DES", "PLY"],["GEN"],        _("I want to feel you deep inside me")), #16
    ]
    if store.persistent._nsfw_genitalia == "P":
        sext_quips_sexy.extend(sext_quips_sexy_p)

    sext_quips_sexy_m = [
    #   |--------------|--------------|---------------------------------------------------------------------------|
    #   |     Type     |   Subtypes   |                                 Prompt                                    |
    #   |--------------|--------------|---------------------------------------------------------------------------|
        (["STM"],       ["GEN"],        _("You're such a bad boy")), #15
    ]
    if store.persistent.gender == "M":
        sext_quips_sexy.extend(sext_quips_sexy_m)

    sext_quips_sexy_4 = [
    #   |--------------|--------------|---------------------------------------------------------------------------|
    #   |     Type     |   Subtypes   |                                 Prompt                                    |
    #   |--------------|--------------|---------------------------------------------------------------------------|
        (["STM"],       ["GEN"],        _("You're such a bad girl")), #15
    ]
    if store.persistent.gender == "F":
        sext_quips_sexy.extend(sext_quips_sexy_f)

    ## SEXTING RESPONSES ##
    sext_responses_cute = [
    #   |---------------------|-------|-------------------------------------------------------------------------------|
    #   |         Type        |Subtype|                                     Prompt                                    |
    #   |---------------------|-------|-------------------------------------------------------------------------------|
        (["ANS", "ASP", 0],    ["GEN"], _("I could ask you the same thing")), #20
        (["ANS", "ASP", 1],    ["GEN"], _("I don't know, you tell me"))
        (["ANS", "AYS"],       ["GEN"], _("Of course")),
        (["CMP", "CMP"],       ["GEN"], _("That's so nice of you to say")), #7
        (["CMP", "CMP"],       ["GEN"], _("You are just the cutest")), #9
        (["CMP", "CMP"],       ["GEN"], _("You make me so happy")), #16
        (["CMP", "CMP"],       ["GEN"], _("You're so kind")), #17
        (["CMP", "CMP"],       ["GEN"], _("You're so sweet")), #6
        (["CMP", "CMP"],       ["GEN"], _("You're so sweet, you know that?")), #14
        (["CMP", "CMP"],       ["GEN"], _("You're such a cutie")), #12
        (["CMP", "CMP"],       ["GEN"], _("You're the sweetest")), #5
        (["CMP", "CRM"],       ["CHE"], _("You're so cheesy")), #8
        (["CMP", "CRM"],       ["GEN"], _("Stop it, you're making me blush")), #15
        (["CMP", "CRM"],       ["GEN"], _("That's so sweet")), #13
        (["CMP", "CRM"],       ["GEN"], _("That's so sweet")), #18
        (["CMP", "CRM"],       ["GEN"], _("That's sweet")), #19
        (["CMP", "CRM"],       ["GEN"], _("You always bring a smile to my face")), #11
        (["CMP", "CRM"],       ["GEN"], _("You always know exactly what to say")), #10
        (["CMP", "THK"],       ["CHE"], _("That's cheesy")), #3
        (["CMP", "THK"],       ["CHE"], _("That's so cheesy")), #4
        (["CMP", "THK"],       ["CHE"], _("That's very cheesy")), #2
        (["CMP", "THK"],       ["GEN"], _("Thank you")), #0
        (["CMP", "THK"],       ["GEN"], _("Thanks")), #1
        (["DES", "DRM", "MON"],["GEN"], _("I would love to do that")), #23
        (["DES", "DRM", "PLY"],["GEN"], _("I would love it if you did that")), #22
        (["DES", "LED"],       ["GEN"], _("Do you really?")), #21
    ]

    sext_responses_hot = [
    #   |--------------|-------|-------------------------------------------------------------------------------|
    #   |     Type     |Subtype|                                     Prompt                                    |
    #   |--------------|-------|-------------------------------------------------------------------------------|
        (["CMD", "CPL"],["GEN"], _("Anything for you")) #20
        (["CMP", "CRM"],["GEN"], _("You know exactly what to say")), #2
        (["CMP", "CRM"],["GEN"], _("You make me so happy talking like that")), #19
        (["DES", "DRM"],["GEN"], _("Don't tempt me to try and break the screen to get to you")), #6
        (["DES", "DRM"],["GEN"], _("I feel so good when you talk like that")), #10
        (["DES", "DRM"],["GEN"], _("I like the sound of that")), #1
        (["DES", "DRM"],["GEN"], _("I've never felt this way before")), #3
        (["DES", "DRM"],["GEN"], _("That is so hot")), #9
        (["DES", "DRM"],["GEN"], _("That's hot")), #16
        (["DES", "DRM"],["GEN"], _("That's so hot")), #15
        (["DES", "DRM"],["GEN"], _("You don't hold back, do you?")), #14
        (["DES", "DRM"],["GEN"], _("You know just what to say to get me all flustered...")), #13
        (["DES", "DRM"],["GEN"], _("You make my body feel warm")), #11
        (["DES", "DRM"],["GEN"], _("You're getting me all riled up")), #5
        (["DES", "DRM"],["GEN"], _("You're making me all flustered")), #12
        (["DES", "DRM"],["GEN"], _("You're making me feel all tingly")), #4
        (["DES", "DRM"],["GEN"], _("You're so hot when you talk like that")), #8
        (["DES", "DRM"],["RCN"], _("Please keep going")), #7
        (["DES", "LED"],["GEN"], _("Is that right?")), #18
        (["DES", "LED"],["GEN"], _("Is that so?")), #17
        (["DES", "LED"],["GEN"], _("What else do you desire?")), #0
    ]

    sext_responses_sexy = [
    #   |---------------------|--------------|---------------------------------------------------------------------------|
    #   |        Types        |   Subtypes   |                                 Prompt                                    |
    #   |---------------------|--------------|---------------------------------------------------------------------------|
        (["ANS", "ASP", 0],    ["ONP"],        _("I don't know~ Maybe you can demonstrate for me right now what you were doing")),
        (["ANS", "ASP", 0],    ["ONP"],        _("I think I can have a guess")),
        (["ANS", "ASP", 1],    ["FSM", "MBD"], _("I'd want you to play with my breasts")),
        (["ANS", "ASP", 1],    ["FSM", "MBD"], _("I'd want you to touch me down there")),
        (["ANS", "ASP", 1],    ["FSM", "MBD"], _("You can touch me anywhere you like")), # You can touch my hair! Undress me everywheeeere!
        (["CMD", "CPL"],       ["GEN"],        _("Anything for you")),
        (["CMD", "CPL"],       ["ONM"],        _("Like this?")),
        (["CMP", "CRM"],       ["GEN"],        _("You just have a way with words, don't you?")), #11
        (["DES", "DRM", "MON"],["GEN"],        _("You really know how to please a woman")), #18
        (["DES", "DRM", "MON"],["RCN", "DOM"], _("Tell me what else you want to do to me")), #7
        (["DES", "DRM", "PLY"],["RCN", "SUB"], _("Tell me what else you want me to do to you")), #20
        (["DES", "DRM"],       ["GEN"],        _("Have you always been this sexy?")), #16
        (["DES", "DRM"],       ["GEN"],        _("That is so sexy")), #1
        (["DES", "DRM"],       ["GEN"],        _("This feels too good")), #9
        (["DES", "DRM"],       ["GEN"],        _("When did you learn to talk like that?")), #15
        (["DES", "DRM"],       ["GEN"],        _("You're getting me so turned on")), #6
        (["DES", "DRM"],       ["GEN"],        _("You're getting me so worked up")), #8
        (["DES", "DRM"],       ["GEN"],        _("You're so sexy when you talk like that")), #0
        (["DES", "DRM"],       ["RCN"],        _("Keep going")), #4
        (["DES", "DRM"],       ["RCN"],        _("Keep talking like that")), #12
        (["DES", "DRM"],       ["RCN"],        _("More")), #13
        (["DES", "DRM"],       ["RCN"],        _("Please don't stop")), #5
        (["DES", "DRM"],       ["RCN"],        _("Please keep going")), #14
        (["DES", "DRM"],       ["RCN"],        _("Say that again")), #19
        (["DES", "DRM"],       ["RCN"],        _("Whatever you're doing...it's working")), #10
        (["DES", "LED"],       ["GEN"],        _("Is that right?")), #2
        (["DES", "LED"],       ["GEN"],        _("Is that so?")), #3
        (["STM"],              ["GEN"],        _("I am so wet right now")), #17
    ]