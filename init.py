import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

dino_keys = [Key.up, Key.down]
pacman_keys = [Key.up, Key.right, Key.down, Key.left]

current_keys = dino_keys
card_actions = { "some_card_num":current_keys[0] }

def play_dino():
    #testing time
    current_keys = dino_keys
    current_key = 0
    end_time = 100

    keyboard.press( Key.up )
    keyboard.release( Key.up )

    while( end_time > 0 ):
        key_to_press = card_actions["some_card_num"]

        keyboard.press( key_to_press )
        keyboard.release( key_to_press )

        current_key += 1
        next_key = current_key % len( current_keys )
        card_actions["some_card_num"] = current_keys[next_key]

        end_time -= 1

        time.sleep(1)

def play_pacman():
    #testing time
    current_keys = pacman_keys
    current_key = 0
    end_time = 100

    while( end_time > 0 ):
        key_to_press = card_actions["some_card_num"]

        keyboard.press( key_to_press )
        keyboard.release( key_to_press )

        current_key += 1
        next_key = current_key % len( current_keys )
        card_actions["some_card_num"] = current_keys[next_key]

        if ( 0 == next_key ):
            current_keys.reverse()

        end_time -= 1
        time.sleep(1)

if __name__ == '__main__':
    #testing time
    time.sleep(5)

    play_pacman()
