import json
import sys

from cryptography.fernet import Fernet


def save_config(config: dict) -> None:
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f)


def load_config() -> dict:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config


def check_config(config: dict) -> bool:
    first_number = config.get('first_number')
    second_number = config.get('second_number')
    is_numbers_correct = all((
        isinstance(first_number, int),
        isinstance(second_number, int)
    ))
    return all((config.get('key'), is_numbers_correct))


def create_key(config: dict) -> str:
    secret_number = int(input('Введите секретное число:\n').strip())
    first_number = config['first_number']
    second_number = config['second_number']
    your_number = (first_number**secret_number) % second_number
    print((f'Отправьте вашему собеседнику это число\n'
           f'и получите от него другое число: {your_number}'))
    friend_number = int(input('Введите число вашего собеседника:\n').strip())
    secret_key = (friend_number**secret_number) % second_number
    return secret_key


def input_initial_numbers() -> dict:
    result = {}
    print('Введите 2 начальных числа и отправьте вашему собеседнику:')
    first_number, second_number = map(int, input().split().strip())
    result['first_number'] = first_number
    result['second_number'] = second_number
    return result


def main():
    try:
        config = load_config()
    except IOError:
        config = {}
    if not check_config(config):
        config.update(input_initial_numbers())
        config['key'] = create_key(config)
        save_config(config)
    fernet = Fernet(config['key'])

    while True:
        try:
            print(('Введите 1 если хотите зашифровать\n'
                   'Введите 2 если хотите расшифровать'))
            working_mode = int(input().strip())
            if working_mode == 1:
                your_string = input(
                    'Введите строку которую нужно зашифровать:\n'
                )
                encrypted_message = fernet.encrypt(your_string.encode())
                print(encrypted_message)
            elif working_mode == 2:
                your_string = input(
                    'Введите строку которую нужно расшифровать:\n'
                )
                dectrypted_message = fernet.decrypt(your_string).decode()
                print(dectrypted_message)
            else:
                print('Я не понимаю что ввели!!!')
        except KeyboardInterrupt:
            sys.exit('Вы вышли из программы.')


if __name__ == '__main__':
    main()
