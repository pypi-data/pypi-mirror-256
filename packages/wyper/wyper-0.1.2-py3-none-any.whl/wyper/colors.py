c_primary = c_primarytext = c_inverseprimary =\
c_windowbg = c_windowtext = c_inversewindowbg =\
c_disabled = c_disabledtext =\
c_accent = c_inverseaccent = c_accenttext =\
c_iconbutton = c_crop = (0, 0, 0)


scheme = "pitchblack"

def setSchemeDark():  # Default Theme
    global c_primary, c_primarytext, c_inverseprimary
    global c_windowbg, c_windowtext, c_inversewindowbg
    global c_disabled, c_disabledtext
    global c_accent, c_inverseaccent, c_accenttext
    global c_iconbutton, c_crop
    global scheme

    scheme = "dark"

    c_primary = (40, 40, 40)
    c_primarytext = (240, 240, 240)
    c_inverseprimary = (120, 120, 120)

    c_windowbg = (20, 20, 20)
    c_windowtext = (255, 255, 255)
    c_inversewindowbg = (50, 50, 50)

    c_disabled = (30, 30, 30)
    c_disabledtext = (100, 100, 100)

    c_accent = (0, 96, 207)
    c_inverseaccent = (213, 226, 240)
    c_accenttext = (185, 209, 237)

    c_crop = c_white
    c_iconbutton = c_white

def setSchemeLight():
    global c_primary, c_primarytext, c_inverseprimary
    global c_windowbg, c_windowtext, c_inversewindowbg
    global c_disabled, c_disabledtext
    global c_accent, c_inverseaccent, c_accenttext
    global c_iconbutton, c_crop
    global scheme

    scheme = "light"

    c_primary = (243, 243, 243)
    c_primarytext = (70, 70, 70)
    c_inverseprimary = (180, 180, 180)

    c_windowbg = (255, 255, 255)
    c_windowtext = (10, 10, 10)
    c_inversewindowbg = (230, 230, 230)

    c_disabled = (240, 240, 240)
    c_disabledtext = (150, 150, 150)

    c_accent = (0, 96, 207)
    c_inverseaccent = (213, 226, 240)
    c_accenttext = (220, 245, 255)
    
    c_crop = (220,220,220)
    c_iconbutton = (255, 255, 255)

c_white = (255, 255, 255)