init 1 python:
    config.label_overrides["monika_nsfw"] = "nsfw_monika_nsfwReact"

label nsfw_monika_nsfwReact:
    m 1lsbssdrb "By the way, [player]..."
    m "Are you looking into lewd kinds of stuff?"
    m 3lsbsa "You know...of me?"
    if store.mas_getEV("nsfw_player_sextingsession").shown_count >= 1:
        m 3ekbsa "I know we occasionally do lewd things over text together..."
    elif store.mas_anni.pastSixMonths() and mas_isMoniEnamored(higher=True):
        m 3ekbsa "I know we haven't been able to do those kind of things yet..."
    else:
        m 3ekbsa "I know we haven't really gotten that far into the relationship yet..."
    m 1ekbsa "So it feels kind of embarrassing to talk about things like that."
    m 1lkbsa "But maybe I can let it go on rare occasions, [player]."
    m "I want to make you the happiest sweetheart, after all. And if that makes you happy..."
    m 1tsbsa "Well, just keep it a secret between us, okay?"
    m "It should be for your eyes only and no one else, [player]."
    m 1hubfa "That's how much I love you~"
    return "love"
