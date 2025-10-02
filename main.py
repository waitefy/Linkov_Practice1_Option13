import os
import socket
import sys


def repl(username, hostname):
    while True:
        parts = input(f'{username}@{hostname}:~$ ').strip().split()
        if parts:
            command, args = parts[0], parts[1:]
            execute_command(username, hostname, command, *args)


def execute_command(username, hostname, command, *args):
    if command in ('ls', 'cd'):
        print(command, *args)
    elif command == 'bash' or command.startswith('./'):
        if command == 'bash':
            for arg in args:
                if os.path.isfile(arg):
                    run_script(username, hostname, arg)
                    return
            print('bash: ошибка')
        else:
            if os.path.exists(script_path := command[2:]):
                if os.path.isfile(script_path):
                    run_script(username, hostname, script_path)
                else:
                    print(f'bash: {script_path}: Это каталог')
            else:
                print(f'bash: {script_path}: Нет такого файла или каталога')
    elif command == 'exit':
        sys.exit(0)
    else:
        print(f'{command}: команда не найдена')


def settings_input():
    vfs_path = start_script_path = None
    while not vfs_path:
        path = input('Путь к VFS: ')
        if not path:
            continue
        if os.path.exists(path):
            if os.path.isdir(path):
                vfs_path = path
            else:
                print(f'bash: {path}: Это файл')
        else:
            print(f'bash: {path}: Нет такого файла или каталога')

    while not start_script_path:
        path = input('Путь к стартовому скрипту: ')
        if not path:
            continue
        if os.path.exists(path):
            if os.path.isfile(path):
                start_script_path = path
            else:
                print(f'bash: {path}: Это каталог')
        else:
            print(f'bash: {path}: Нет такого файла или каталога')

    return vfs_path, start_script_path


def debug_output(vfs_path, start_script_path):
    print(
        f'Параметры запуска (отладочный вывод):\n'
        f'    VFS: /{vfs_path}\n'
        f'    Script: /{start_script_path}\n'
    )


def run_script(username, hostname, script_path):
    with open(script_path, 'r', encoding='utf-8') as script:
        for line in script.readlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            command, args = parts[0], parts[1:]
            print(f'{username}@{hostname}:~$ {line}')
            if command != 'exit':
                execute_command(username, hostname, command, *args)
            else:
                print('exit: недопустимо в скрипте, строка пропущена')


def main():
    vfs_path, start_script_path = settings_input()
    debug_output(vfs_path, start_script_path)
    username = os.getlogin()
    hostname = socket.gethostname()
    print('Начало выполнения стартового скрипта')
    run_script(username, hostname, start_script_path)
    print('Стартовый скрипт выполнен успешно')
    repl(username, hostname)


if __name__ == '__main__':
    main()
