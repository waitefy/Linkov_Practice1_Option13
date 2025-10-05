import os
import shutil
import socket
import sys


class Shell:
    def __init__(self, vfs, phys_vfs):
        self.username = os.getlogin()
        self.hostname = socket.gethostname()
        self.vfs = vfs
        self.phys_vfs = phys_vfs

    def cmd_ls(self, args):
        print('ls', *args)

    def cmd_cd(self, args):
        print('cd', *args)

    @staticmethod
    def cmd_exit():
        sys.exit(0)

    def cmd_bash(self, args):
        for arg in args:
            if os.path.exists(arg):
                if os.path.isfile(arg):
                    self.run_script(arg)
                    return
                print(f'bash: {arg}: Это каталог')
        print('bash: ошибка')

    def cmd_vfs_init(self, args=None):
        if args and '--wipe' in args:
            answer = input('Вы действительно хотите очистить физическое представление VFS? [y/N]: ')
            if answer.lower() in ('y', 'д'):
                clear_dir(self.phys_vfs)
                print('Физическое представление VFS очищено')
            else:
                print('vfs-init: Операция отменена')
                return
        self.vfs = default_vfs(self.username)
        print('VFS инициализирована')

    def execute(self, command, args=None):
        if command == 'ls':
            self.cmd_ls(args)
        elif command == 'cd':
            self.cmd_cd(args)
        elif command == 'exit':
            self.cmd_exit()
        elif command == 'bash':
            self.cmd_bash(args)
        elif command.startswith('./'):
            self.cmd_bash([command[2:]])
        elif command == 'vfs-init':
            self.cmd_vfs_init(args)
        else:
            print(f'{command}: команда не найдена')

    def repl(self):
        while True:
            parts = input(f'{self.username}@{self.hostname}:~$ ').strip().split()
            if parts:
                command, args = parts[0], parts[1:]
                self.execute(command, args)

    def run_script(self, script_path):
        with open(script_path, 'r', encoding='utf-8') as script:
            for line in script.readlines():
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                command, args = parts[0], parts[1:]
                print(f'{self.username}@{self.hostname}:~$ {line}')
                if command != 'exit':
                    self.execute(command, args)
                else:
                    print('exit: Недопустимо в скрипте, строка пропущена')


def build_node(path):
    if os.path.isdir(path):
        try:
            return {
                'type': 'dir', 'children': {
                    node: build_node(os.path.join(path, node))
                    for node in sorted(os.listdir(path))
                }
            }
        except PermissionError:
            return {'type': 'dir', 'children': {}}
    try:
        with open(path, 'rb') as f:
            data = f.read()
    except OSError:
        data = b''
    return {'type': 'file', 'data': data}


def default_vfs(user: str):
    return {
        'type': 'dir',
        'children': {
            'home': {'type': 'dir', 'children': {user: {'type': 'dir', 'children': {}}}},
            'etc': {'type': 'dir', 'children': {}},
            'var': {'type': 'dir', 'children': {}},
            'README.txt': {'type': 'file', 'data': b'Hello VFS\n'},
        }
    }


def clear_dir(root):
    for name in os.listdir(root):
        path = os.path.join(root, name)
        try:
            if os.path.isdir(path) and not os.path.islink(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except PermissionError:
            print('Отказано в доступе')


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
        f'    VFS: {vfs_path}\n'
        f'    Script: {start_script_path}\n'
    )


def main():
    vfs_path, start_script_path = settings_input()
    debug_output(vfs_path, start_script_path)
    sh = Shell(build_node(vfs_path), vfs_path)
    print('Начало выполнения стартового скрипта')
    sh.run_script(start_script_path)
    print('Стартовый скрипт выполнен успешно')
    sh.repl()


if __name__ == '__main__':
    main()
