import random

# define all the functions


def choose_password():
    global password
    password = ''
    for it in range(5):
        l = random.choice('12345678')
        password += l
    return password


def check(guess):
    wrong_dig = 0
    right_dig_and_pos = 0
    right_dig = 0
    it = -1
    for digit in guess:
        it += 1
        if digit not in password:
            wrong_dig += 1
        elif digit in password and password[it] == digit:
            right_dig_and_pos += 1
        elif digit in password and password[it] != digit:
            right_dig += 1
    return f'right digits and positions: {right_dig_and_pos}\n' \
           f'right digits but wrong positions: {right_dig}\n' \
           f'wrong digits: {wrong_dig}'


def start_game():
    global username
    username = input('Let\'s play mastermind! enter your username and I\'ll tell you the rules: ')
    print('\nI\'ll generate a password with 5 digits from 1 to 8 and '
          'you\'ll have 12 tries to guess it. (digits CAN be repeated)')
    print('Don\'t worry, I\'ll help you along the way')
    print(f'\nOK {username}, let\'s start!')
    print('---------------------')


# ------------------------------------

# start the game
start_game()


# choose the password
choose_password()


# game workflow
guess = ''
tries = 0
while guess != password:
    print(f'\nBe careful, {username}, you have {12 - tries} tries left')
    try:
        guess = input('enter 5 digits from \'1\' to \'8\', '
                      'and no other character (digits can be repeated, no whitespace): ')
        if not guess.isdigit():
            raise ValueError
        if not 11111 <= int(guess) <= 88888:
            raise ValueError
        if '0' in guess or '9' in guess or ' ' in guess:
            raise ValueError
        tries += 1
        if tries >= 12:
            break
        if guess == password:
            break
        print(check(guess))
    except ValueError:
        print('\n!!please enter exactly 5 digits from 1 to 8, no whitespace!!')


# end message of the game
if tries >= 12:
    print('\nOut of guesses, YOU LOSE\n'
          f'the password was: {password}')
else:
    print('\nCongratulations, YOU WIN\n'
          f'the password was: {password}')

