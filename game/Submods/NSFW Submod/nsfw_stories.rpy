# Module for Monika story telling
#
# Stories will get unlocked one at by session
# The unlocking logic has been added to script-ch30
# The topic that triggers the Story menu is monika_short_stories
# Topic is unlocked at the beginning of the game and is not
# random
# New rule: pool property as true means that the story gets unlocked
# by some other way and can't be unlocked randomly


# dict of tples containing the stories event data
default persistent._nsfw_story_database = dict()

# dict storing the last date we saw a new story of normal and scary type
default persistent._nsfw_last_seen_new_story = {"erotic": None}

# store containing stories-related things
init -1 python in nsfw_stories:
    import store
    import datetime

    UNLOCK_NEW = "unlock_new"

    # TYPES:
    TYPE_EROTIC = "erotic"

    # pane constant
    STORY_RETURN = "Nevermind"
    nsfw_story_database = dict()

    #Time between story unlocks of the same type (in hours). Changes over sessions, but also changes after the next story unlocks
    TIME_BETWEEN_NSFW_UNLOCKS = renpy.random.randint(20, 28)

    #TODO: Build functions to 'register' story types. This will add all related info to the map
    #saving the manual additions to each part

    #Story which starts unlocked for a specific type
    FIRST_STORY_EVL_MAP = {
        TYPE_EROTIC: "nsfw_erotic_story_thepen",
    }

    #Override maps to have special conditionals for specific story types
    NEW_STORY_CONDITIONAL_OVERRIDE = {
        TYPE_EROTIC: (
            "nsfw_stories.check_can_unlock_new_story(nsfw_stories.TYPE_EROTIC, ignore_cooldown=store.mas_anni.isAnni())"
        ),
    }

    def check_can_unlock_new_story(story_type=TYPE_EROTIC, ignore_cooldown=False):
        """
        Checks if it has been at least one day since we've seen the last story or the initial story

        IN:
            story_type - story type to check if we can unlock a new one
                (Default: TYPE_EROTIC)
            ignore_cooldown - Whether or not we ignore the cooldown or time between new stories
                (Default: False)
        """
        global TIME_BETWEEN_NSFW_UNLOCKS

        new_story_ls = store.persistent._nsfw_last_seen_new_story.get(story_type, None)

        #Get the first story of this type
        first_story = FIRST_STORY_EVL_MAP.get(story_type, None)

        #If this doesn't have an initial, no go
        if not first_story:
            return False

        can_show_new_story = (
            store.seen_event(first_story)
            and (
                ignore_cooldown
                or store.mas_timePastSince(new_story_ls, datetime.timedelta(hours=TIME_BETWEEN_NSFW_UNLOCKS))
            )
            and len(get_new_stories_for_type(story_type)) > 0
        )

        #If we're showing a new story, randomize the time between unlocks again
        if can_show_new_story:
            TIME_BETWEEN_NSFW_UNLOCKS = renpy.random.randint(20, 28)

        return can_show_new_story

    def get_new_stories_for_type(story_type=TYPE_EROTIC):
        """
        Gets all new (unseen) stories of the given type

        IN:
            story_type - story type to get

        OUT:
            list of locked stories for the given story type
        """
        return store.Event.filterEvents(
            nsfw_story_database,
            pool=False,
            aff=store.mas_curr_affection,
            unlocked=False,
            flag_ban=store.EV_FLAG_HFNAS,
            category=(True, [story_type])
        )

    def get_and_unlock_random_story(story_type=TYPE_EROTIC):
        """
        Unlocks and returns a random story of the provided type

        IN:
            story_type - Type of story to unlock.
                (Default: TYPE_EROTIC)
        """
        #Get locked stories
        stories = get_new_stories_for_type(story_type)

        #Grab one of the stories
        story = renpy.random.choice(stories.values())

        #Unlock and return its eventlabel
        story.unlocked = True

        return story.eventlabel

init 6 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="nsfw_monika_stories",
            category=['sex'],
            prompt="Can you tell me an erotic story?",
            pool=True,
            conditional="mas_canShowRisque(aff_thresh=1000)",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.LOVE, None)
        )
    )

label nsfw_monika_stories:
    if not mas_getEVL_shown_count("nsfw_erotic_story_thepen") >= 1:
        $ pushEvent("nsfw_erotic_story_thepen", skipeval=True)
    else:
        call nsfw_monika_stories_premenu(None)
    return _return

label nsfw_monika_stories_premenu(story_type=None):
    python:
        #Because this isn't set properly if it's in the default param value, we assign it here
        if story_type is None:
            story_type = nsfw_stories.TYPE_EROTIC
        end = ""

label nsfw_monika_stories_menu:
    # TODO: consider caching the built stories if we have many story categories
    python:
        #Determine if a new story can be unlocked
        can_unlock_nsfw_story = False

        if story_type in nsfw_stories.NEW_STORY_CONDITIONAL_OVERRIDE:
            try:
                can_unlock_nsfw_story = eval(nsfw_stories.NEW_STORY_CONDITIONAL_OVERRIDE[story_type])
            except Exception as ex:
                store.mas_utils.mas_log.error("Failed to evaluate conditional to unlock new story because '{0}'".format(ex))

                can_unlock_nsfw_story = False

        else:
            can_unlock_nsfw_story = nsfw_stories.check_can_unlock_new_story(story_type)

        # build menu list
        nsfw_stories_menu_items = [
            (story_ev.prompt, story_evl, False, False)
            for story_evl, story_ev in nsfw_stories.nsfw_story_database.iteritems()
            if Event._filterEvent(
                story_ev,
                pool=False,
                aff=mas_curr_affection,
                unlocked=True,
                flag_ban=EV_FLAG_HFM,
                category=(True, [story_type])
            )
        ]

        # also sort this list
        nsfw_stories_menu_items.sort()

        # TODO: Build a generalized switch for more than just two items

        #Add new random story
        if nsfw_stories.check_can_unlock_new_story(nsfw_stories.TYPE_EROTIC) == True:
            nsfw_stories_menu_items.append(("A new erotic story", nsfw_stories.UNLOCK_NEW, True, False))
        else:
            nsfw_stories_menu_items.append(("A new erotic story", nsfw_stories.UNLOCK_NEW, False, False))

        final_item = (nsfw_stories.STORY_RETURN, False, False, False, 0)

    # move Monika to the left
    show monika 1eua at t21

    $ renpy.say(m, "Which story would you like to hear?" + end, interact=False)

    call screen mas_gen_scrollable_menu(nsfw_stories_menu_items, mas_ui.SCROLLABLE_MENU_TXT_LOW_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    # return value?
    if _return:
        $ story_to_push = _return

        #UNLOCKS GENERIC EROTIC.
        #If we're unlocking new, check if it's possible to do so. If not, we raise dlg
        if story_to_push == nsfw_stories.UNLOCK_NEW:
            if not can_unlock_nsfw_story: #temp
                show monika at t11
                $ _story_type = story_type
                m 1ekc "Sorry, [player]... I can't really think of a new [_story_type] story right now..."
                m 1eka "If you give me some time, I might be able to think of one soon... But in the meantime, I can always tell you an old one again~"
                
                show monika 1eua
                jump nsfw_monika_stories_menu

            else:
                python:
                    persistent._nsfw_last_seen_new_story[story_type] = datetime.datetime.now()
                    story_to_push = nsfw_stories.get_and_unlock_random_story(story_type)

            #Then push
        $ pushEvent(story_to_push, skipeval=True)

        show monika at t11

    else:
        return "prompt"

    return

# Stories start here
label nsfw_story_begin:
    python:
        story_begin_quips = [
            _("Alright, let's start the story."),
            _("Ready to hear the story?"),
            _("Ready for story time?"),
            _("Let's begin~"),
            _("Are you ready?")
        ]
        story_begin_quip=renpy.random.choice(story_begin_quips)
    $ mas_gainAffection(modifier=0.2)
    m 3eua "[story_begin_quip]"
    m 1duu "Ahem."
    return

init 6 python:
    addEvent(
        Event(
            persistent._nsfw_story_database,
            eventlabel="nsfw_erotic_story_thepen",
            prompt="The Pen",
            category=[nsfw_stories.TYPE_EROTIC],
            unlocked=True
        ),
        code="NST"
    )

label nsfw_erotic_story_thepen:
    python:
        if persistent.playthrough >= 2:
            inspired_monika = True
        else:
            inspired_monika = False
    
    if not mas_getEVL_shown_count("nsfw_erotic_story_thepen") >= 1:
        m 1etb "An erotic story?"
        m 1duu "Let me think.{w=0.3}.{w=0.3}."
        m 3guu "Alright, I have one in mind."
    else:
        call nsfw_story_begin

    if inspired_monika:
        m 3eub "Do you remember when Yuri mentioned how she took the main character's pen and did some...ahem..."
        extend 1rkblsdlb "questionable things with it?"
        m 3eubla "Well, that's the inspiration for this story."
    m 3eub "The other day while you were gone, I wanted to try something."
    m 3hksdlb "It might sound strange, but hear me out!"
    m 3rubla "I was in a horny mood..."
    m 3rkblb "And I felt the urge to masturbate."
    if renpy.seen_label("nsfw_sexting_finale"):
        m 3ekblb "But, I didn't want to just play with myself with my fingers like we did when we sexted."
    else:
        m 3ekblb "But, I didn't want to just play with myself using my fingers."
    m 2esbla "I wanted to try something {i}different{/i}, you know?"
    m 2eub "So...I was in my room, searching for something that would make it more exciting..."
    extend 3eua "when I found my pen sitting on the desk."
    if inspired_monika:
        m 3rkblb "My mind immediately went back to when I overheard that Yuri had used the main character's pen to stimulate herself."
        m 3rtblu "I wondered if it was that good of a feeling, or if she was just so obsessed with him that anything would have done it."
    else:
        m 3rkblb "My mind immediately filled with thoughts of using it."
    m 1hublb "Ahaha! I can't see your face, but I can already tell you're asking why, right?"
    m 1eubla "Well, I understand you might think it's strange."
    m 3tubla "But when you don't have anything but your fingers to masturbate with..."
    extend 3hublb "you get kind of desperate. Ahaha~"
    m 4eublb "Anyway, I took the pen and walked back to the bed."
    m 4tublb "I first stripped down to my underwear, reclined back on my bed, and made myself comfortable."
    m 4tublu "I spread my legs {i}just a little{/i}, and started using the pen on my...sensitive parts."
    m 2tublb "On its own, it wasn't that special."
    m 5tublb "But then I started to fantasize about you..."
    m 5dubla "I closed my eyes, "
    extend 5dubsb "and I pictured your face sitting directly above mine, with your index finger rubbing between my legs."
    m 5dkbsa "In my mind, you leaned down to kiss me, and I could almost feel your lips pressed against mine."
    m 2tkbsb "I felt my body getting hot, and the area down there began to feel a lot more moist than before..."
    m 2gkbsa "I started rubbing myself faster, and faster~"
    m 2tkbsu "I imagined that you were getting rougher with me as your finger was making its way up and down my pussy."
    m 2tkbsa "You were pressing your tongue against my lips, as if asking permission to enter."
    m 2hubsa "Ehehe~ I was more than willing to give it..."
    m 2tkbsb "I pictured myself using my own tongue and forcing my way into your mouth."
    m 1hkbssdlb "I don't know why, but I imagined that you were taken aback from my boldness. Ahaha~"
    m 1tkbsb "It was then that I felt myself getting close."
    m 1ekbsb "I kept the pace going, but I could feel my arm starting to get sore from the continuous movement."
    m 1tkbsa "I ignored it. After all, in my mind it was your arm doing the work~"
    m 1tsbsa "I got that feeling in my lower half that told me I about to come..."
    m 2tsbsb "I imagined my arms wrapping around your head and pulling you in as you finished me off."
    m 2ekbsb "As I orgasmed, I felt my body jolt from the pleasure."
    m 3rkbsa "It felt like there was a swirling buildup in my lower half..."
    m 3subsb "...Which all at once flushed out of my body like a burst of fireworks."
    m 1subsa "It was like an electric pulse making its way through my body every few seconds, jolting me stiff."
    m 5eubsa "But it felt incredible..."
    m 5hkbsb "It took twenty whole seconds before my body calmed down enough for me to open my eyes."
    m 5gkbsa "My arm flopped to the side, the now-drenched pen dropping to the floor."
    m 5hubsb "Ahaha! It was really something, [player]."
    if persistent._nsfw_genitalia == "P":
        m 5tubsb "I bet that story got {i}you{/i} all stiff and aroused too, huh [player]?"
    elif persistent._nsfw_genitalia == "V":
        m 5tubsb "I bet that story got {i}you{/i} all drenched down there too, huh [player]?"
    else:
        m 5tubsb "I bet that story got you all excited, huh, [player]?"
    m 5gubsu "You'd better do something about it, or it might become a problem, [mas_get_player_nickname()]." #Cheeky grin
    m 5hubsa "Ehehe~"
