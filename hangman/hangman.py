# import all modules

import random


# define all functions

def choose_word():
    with open('words_hangman', 'r') as file:
        words = file.readlines()
        words = [line.strip() for line in words]
        global secret_word
        secret_word = random.choice(words)
    return secret_word


def display(secret_word):
    print('\n')
    for letter in secret_word:
        if letter in user_guesses:
            print(letter, end='')
        else:
            print('_', end='')


def pos_message():
    print(f'\nYou got it {username}! Keep going!\n'
          f'You still have {7 - errors} errors left')


def neg_message():
    print(f'\nCome on {username}, you can do better... Try with another letter!\n'
          f'You still have {7 - errors} errors left')


def start_game():
    print("Let's see if you can guess my secret word...\n")
    global username
    username = input('enter your username to start the game: ')


class LetterAlreadyChosen(Exception):
    pass


class MoreThanOneLetter(Exception):
    pass

# choose the secret word

choose_word()

# define variables

user_guesses = set()
set_secret_word = {x for x in secret_word}
username = ''
errors = 0

# start the game

start_game()

# while loop

while not set_secret_word.issubset(user_guesses) and errors < 7:
    try:
        letter = input(f'\n{username}, enter a letter: ').strip()
        if not letter.isalpha():
            raise ValueError
        if len(letter) > 1:
            raise MoreThanOneLetter
        if letter in user_guesses:
            raise LetterAlreadyChosen

        user_guesses.add(letter)
        display(secret_word)
        if letter in secret_word and not set_secret_word.issubset(user_guesses) and errors < 7:
            pos_message()
        elif letter not in secret_word and not set_secret_word.issubset(user_guesses) and errors < 7:
            errors += 1
            neg_message()
    except ValueError:
        print('\nplease enter a letter')
    except MoreThanOneLetter:
        print('\nplease enter only one letter')
    except LetterAlreadyChosen:
        print('\nyou already entered this letter, try with another one')


# end message

if errors >= 7:
    print(f"\n\nYou're out of guesses, YOU LOSE!\n"
          f"the secret word was {secret_word}")
else:
    print('\n\nCongratulations, YOU WIN!')
