def SetRadioGroup():
    global OnRadioScreen
    OnRadioScreen = 1
    basic.show_number(RadioGroup)

def on_received_number(receivedNumber):
    global Opponent
    Opponent = receivedNumber
radio.on_received_number(on_received_number)

def SetPlayerStats():
    global PlayerHealth, OpponentHealth
    PlayerHealth = 3
    OpponentHealth = 3

def on_button_pressed_a():
    global Ready, OnRadioScreen, OnMainBattleLoop, OnHomeScreen
    if OnMainBattleLoop == 1:
        Ready = 1
        # Send hand chosen by player. 0 - rock, 1 - paper, 2 - scissors
        radio.send_number(Hand)
        # Show confirmation if opponent has not already sent a move. If not, then the result of the match will be shown straight away.
        if Opponent == -1:
            basic.show_icon(IconNames.YES)
    if OnRadioScreen == 1:
        OnRadioScreen = 0
        radio.set_group(RadioGroup)
        OnMainBattleLoop = 1
        if PlayerHealth < 1 or OpponentHealth < 1:
            SetPlayerStats()
    # Go to SetRadioGroup screen
    if OnHomeScreen == 1:
        OnHomeScreen = 0
        SetRadioGroup()
input.on_button_pressed(Button.A, on_button_pressed_a)

def MainBattleLoop():
    global OnMainBattleLoop, MatchResult, OpponentHealth, PlayerHealth, Opponent, Ready, TotalWins
    OnMainBattleLoop = 1
    basic.show_leds("""
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        """)
    # Show hand picked
    if Hand == 0:
        basic.show_icon(IconNames.SMALL_SQUARE)
    elif Hand == 1:
        basic.show_icon(IconNames.SQUARE)
    else:
        basic.show_icon(IconNames.SCISSORS)
    while Opponent > -1 and Ready == 1:
        # Match result calculated as (self - opponent)
        # Winning results:
        # 0 - 2 = -2
        # 2 - 1 =  1
        # 1 - 0 =  1.
        # Losing results:
        # 2 - 0 =  2
        # 1 - 2 = -1
        # 0 - 1 = -1.
        # 0 is draw
        MatchResult = Hand - Opponent
        if MatchResult == -2 or MatchResult == 1:
            OpponentHealth += -1
            # You win!
            basic.show_icon(IconNames.HAPPY)
            music._play_default_background(music.built_in_playable_melody(Melodies.POWER_UP),
                music.PlaybackMode.UNTIL_DONE)
        elif MatchResult == 2 or MatchResult == -1:
            PlayerHealth += -1
            # You lose!
            basic.show_icon(IconNames.SAD)
            music._play_default_background(music.built_in_playable_melody(Melodies.POWER_DOWN),
                music.PlaybackMode.UNTIL_DONE)
        else:
            # Draw!
            basic.show_icon(IconNames.SURPRISED)
            music._play_default_background(music.built_in_playable_melody(Melodies.BA_DING),
                music.PlaybackMode.UNTIL_DONE)
        basic.pause(5000)
        Opponent = -1
        Ready = 0
    if PlayerHealth < 1:
        TotalWins += 1
        basic.show_string("You Win!")
        music._play_default_background(music.built_in_playable_melody(Melodies.ENTERTAINER),
            music.PlaybackMode.UNTIL_DONE)
    elif OpponentHealth < 1:
        basic.show_string("You Lose!")
        music._play_default_background(music.built_in_playable_melody(Melodies.WAWAWAWAA),
            music.PlaybackMode.UNTIL_DONE)
    else:
        pass
    OnMainBattleLoop = 0
    HomeScreen()
def HomeScreen():
    global OnHomeScreen
    OnHomeScreen = 1
    while OnHomeScreen == 1:
        basic.show_leds("""
            # . # . #
            . # . # .
            . # # # .
            # # . # #
            . # # # .
            """)

def on_button_pressed_b():
    global OnHomeScreen
    if OnHomeScreen == 1:
        OnHomeScreen = 0
        basic.show_string("Total Wins:")
        basic.show_number(TotalWins)
        basic.pause(2000)
        HomeScreen()
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_gesture_shake():
    global Hand, RadioGroup
    # Player can only change their choice if not confirmed already
    if Ready == 0 and OnMainBattleLoop == 1:
        # Cycles through 0, 1, 2
        Hand = (Hand + 1) % 3
    if OnRadioScreen == 1:
        RadioGroup = (RadioGroup + 1) % 10
        basic.show_number(RadioGroup)
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

MatchResult = 0
OnHomeScreen = 0
OpponentHealth = 0
PlayerHealth = 0
Opponent = 0
Ready = 0
Hand = 0
RadioGroup = 0
OnMainBattleLoop = 0
OnRadioScreen = 0
TotalWins = 0
TotalWins = 0
OnRadioScreen = 0
OnMainBattleLoop = 0
RadioGroup = 0
Hand = 0
# Used for "three way handshake"
Ready = 0
# Stores received opponent hand. -1 marks no choice
Opponent = -1
HomeScreen()