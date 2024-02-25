function SetRadioGroup () {
    basic.showNumber(RadioGroup)
    while (true) {
        if (input.isGesture(Gesture.Shake)) {
            RadioGroup = (RadioGroup + 1) % 10
            basic.showNumber(RadioGroup)
        }
        if (input.buttonIsPressed(Button.A)) {
            break;
        }
    }
    basic.clearScreen()
    basic.showNumber(RadioGroup)
    radio.setGroup(RadioGroup)
    PlayerHealth = 3
    OpponentHealth = 3
    MainBattleLoop()
}
radio.onReceivedNumber(function (receivedNumber) {
    Opponent = receivedNumber
})
function MainBattleLoop () {
    while (true) {
        // Player can only change their choice if not confirmed already
        if (Ready == 0 && input.isGesture(Gesture.Shake) == true) {
            // Cycles through 0, 1, 2
            Hand = (Hand + 1) % 3
        }
        if (input.buttonIsPressed(Button.A)) {
            Ready = 1
            // Send hand chosen by player. 0 - rock, 1 - paper, 2 - scissors
            radio.sendNumber(Hand)
            // Show confirmation if opponent has not already sent a move. If not, then the result of the match will be shown straight away.
            if (Opponent == -1) {
                basic.showIcon(IconNames.Yes)
            }
        }
        // Show hand picked
        if (Hand == 0) {
            basic.showIcon(IconNames.SmallSquare)
        } else if (Hand == 1) {
            basic.showIcon(IconNames.Square)
        } else {
            basic.showIcon(IconNames.Scissors)
        }
        if (Opponent > -1 && Ready == 1) {
            // Match result calculated as (self - opponent)
            // Winning results:
            // 0 - 2 = -2
            // 2 - 1 =  1
            // 1 - 0 =  1.
            // Losing results:
            // 2 - 0 =  2
            // 1 - 2 = -1
            // 0 - 1 = -1.
            // 0 is draw
            MatchResult = Hand - Opponent
            if (MatchResult == -2 || MatchResult == 1) {
                OpponentHealth += -1
                // You win!
                basic.showIcon(IconNames.Happy)
                music._playDefaultBackground(music.builtInPlayableMelody(Melodies.PowerUp), music.PlaybackMode.UntilDone)
            } else if (MatchResult == 2 || MatchResult == -1) {
                PlayerHealth += -1
                // You lose!
                basic.showIcon(IconNames.Sad)
                music._playDefaultBackground(music.builtInPlayableMelody(Melodies.PowerDown), music.PlaybackMode.UntilDone)
            } else {
                // Draw!
                basic.showIcon(IconNames.Surprised)
                music._playDefaultBackground(music.builtInPlayableMelody(Melodies.BaDing), music.PlaybackMode.UntilDone)
            }
            basic.pause(2500)
            Opponent = -1
            Ready = 0
            if (OpponentHealth < 1) {
                TotalWins += 1
                music._playDefaultBackground(music.builtInPlayableMelody(Melodies.Entertainer), music.PlaybackMode.InBackground)
                basic.showString("You Win!")
                break;
            } else if (PlayerHealth < 1) {
                music._playDefaultBackground(music.builtInPlayableMelody(Melodies.Wawawawaa), music.PlaybackMode.InBackground)
                basic.showString("You Lose!")
                break;
            }
        }
    }
    HomeScreen()
}
function HomeScreen () {
    // Draw your monster here!
    basic.showLeds(`
        # . # . #
        . # . # .
        . # # # .
        # # . # #
        . # # # .
        `)
    while (true) {
        if (input.buttonIsPressed(Button.A)) {
            break;
        }
        if (input.buttonIsPressed(Button.B)) {
            basic.showString("Wins:")
            basic.showNumber(TotalWins)
            basic.pause(2000)
            HomeScreen()
        }
    }
    SetRadioGroup()
}
let MatchResult = 0
let OpponentHealth = 0
let PlayerHealth = 0
let Opponent = 0
let Ready = 0
let Hand = 0
let RadioGroup = 0
let TotalWins = 0
TotalWins = 0
RadioGroup = 0
Hand = 0
// Used for "three way handshake"
Ready = 0
// Stores received opponent hand. -1 marks no choice
Opponent = -1
HomeScreen()
