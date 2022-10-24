## Sexting Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice
##
## This is an override for the default `screen choice` object for use in the Sexting minigame
## To use it, add ' (sextchoice)' to the dialogue option, space included.
## The code will replace & remove it from the choice.

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            $ opt = i.caption[i.caption.find("(")+1:i.caption.find(")")]
            $ caption = i.caption.replace(" ("+opt+")", "")
            textbutton caption:
                if opt=="sextchoice":
                    style "sextchoice_button"
               # if no opt, defaults to choice_button
                action i.action

style sextchoice_button is choice_button is generic_button_light:
    xcenter 0.5
    xsize(840)
    ymaximum(420)
    padding (100, 5, 100, 5)

style sextchoice_button_dark is choice_button is generic_button_dark:
    xcenter 0.5
    xsize(840)
    ymaximum(420)
    padding (100, 5, 100, 5)

style sextchoice_button_text is choice_button is generic_button_text_light
style sextchoice_button_text_dark is choice_button is generic_button_text_dark


## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True
