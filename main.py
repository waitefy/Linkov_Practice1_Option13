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
        self.cwd = '/'

    def resolve_path(self, path):
        if not path or path == '.':
            return self.cwd or '/'
        raw = path if path.startswith('/') else (
                    self.cwd.rstrip('/') + '/' + path)
        stack = []
        for part in raw.split('/'):
            if part == '' or part == '.':
                continue
            elif part == '..':
                if stack:
                    stack.pop()
            else:
                stack.append(part)
        return '/' + '/'.join(stack)

    def get_node(self, abs_path):
        node = self.vfs
        if abs_path == '/':
            return node
        for name in abs_path.strip('/').split('/'):
            children = node['children']
            if name not in children:
                return None
            node = children[name]
        return node

    def cmd_ls(self, args):
        for path in args or [self.cwd]:
            abs_path = self.resolve_path(path)
            if (node := self.get_node(abs_path)) is None:
                print(f"ls: невозможно получить доступ к '{path}': "
                      f"Нет такого файла или каталога")
            elif node['type'] == 'file':
                print(abs_path.rsplit('/',1)[-1])
            elif node['children']:
                print('\t'.join(sorted(node['children'].keys())))

    def cmd_cd(self, args):
        if not args: args = []
        if len(args) > 1:
            print('bash: cd: слишком много аргументов')
            return
        abs_path = self.resolve_path(args[0]) if args else '/'
        if (node := self.get_node(abs_path)) is None:
            print(f'bash: cd: {args[0]}: Нет такого файла или каталога')
        elif node['type'] == 'file':
            print(f'bash: cd: {args[0]}: Это не каталог')
        else:
            self.cwd = abs_path

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
                return
        print('bash: ошибка')

    def cmd_vfs_init(self, args):
        if args and '--wipe' in args:
            answer = input('Вы действительно хотите очистить '
                           'физическое представление VFS? [y/N]: ')
            if answer.lower() in ('y', 'д'):
                clear_dir(self.phys_vfs)
                print('Физическое представление VFS очищено')
            else:
                print('vfs-init: Операция отменена')
                return
        self.vfs = default_vfs(self.username)
        self.cwd = '/'
        print('VFS инициализирована')

    def cmd_wc(self, args):
        if not args:
            return
        total_lines = total_words = total_bytes = 0
        for path in args:
            abs_path = self.resolve_path(path)
            node = self.get_node(abs_path)
            if node is None:
                print(f'wc: {path}: Нет такого файла или каталога')
                continue
            if node['type'] == 'dir':
                print(f'{0:7d}{0:8d}{0:8d} {path}')
                print(f'wc: {path}: Это каталог')
                continue
            data = node['data']
            line_count = data.count(b'\n')
            word_count = len(data.decode('utf-8', 'replace').split())
            byte_count = len(data)
            print(f'{line_count:7d}{word_count:8d}{byte_count:8d} {path}')
            total_lines += line_count
            total_words += word_count
            total_bytes += byte_count
        if len(args) > 1:
            print(f'{total_lines:7d}{total_words:8d}{total_bytes:8d} итого')

    def cmd_tree(self, args):
        for path in args or [self.cwd]:
            abs_path = self.cwd if not path else self.resolve_path(path)
            node = self.get_node(abs_path)
            if node is None:
                print(f'\n{path}  [error opening dir]\n\n'
                      f'0 directories, 0 files')
                continue
            root = '.'
            if abs_path != self.cwd:
                root = '/' if abs_path == '/' else \
                abs_path.rsplit('/', 1)[-1]
            dirs = files = 0
            def walk(n, prefix=''):
                nonlocal dirs, files
                if n['type'] != 'dir':
                    return
                names = sorted(n['children'].keys())
                for i, name in enumerate(names):
                    child = n['children'][name]
                    last = (i == len(names) - 1)
                    branch = '└── ' if last else '├── '
                    print(prefix + branch + name)
                    if child['type'] == 'dir':
                        dirs += 1
                        walk(child, prefix + ('    ' if last else '│   '))
                    else:
                        files += 1
            if node['type'] == 'file':
                print((abs_path.rsplit('/', 1)[-1] or '/'))
                files = 1
            else:
                print(root)
                walk(node)
            print(f'\n{dirs} directories, {files} files')

    def cmd_whoami(self, args):
        if args:
            print(f'whoami: лишний операнд «{args[0]}»')
            return
        print(self.username)

    def cmd_cp(self, args):
        if not args:
            print('cp: пропущен операнд, задающий файл')
            return
        if len(args) < 2:
            print(f"cp: после '{args[0]}' пропущен операнд, "
                  f"задающий целевой файл")
            return
        dst_path = args[-1]
        for src_path in args[:-1]:
            abs_src = self.resolve_path(src_path)
            abs_dst = self.resolve_path(dst_path)
            src_node = self.get_node(abs_src)
            if src_node is None:
                print(f"cp: не удалось выполнить '{src_path}': "
                      f"Нет такого файла или каталога")
                return
            if src_node['type'] != 'file':
                print(f"cp: не указан -r; пропускается каталог '{src_path}'")
                return
            dst_parent_path = abs_dst.rsplit('/', 1)[0] or '/'
            dst_name = abs_dst.rsplit('/', 1)[-1]
            parent_node = self.get_node(dst_parent_path)
            if parent_node is None or parent_node['type'] != 'dir':
                print(f"cp: невозможно создать обычный файл '{dst_path}': "
                      f"Нет такого каталога")
                return
            dst_node = self.get_node(abs_dst)
            if dst_node and dst_node['type'] == 'dir':
                dst_name = abs_src.rsplit('/', 1)[-1]
                parent_node = dst_node
            parent_node['children'][dst_name] = {
                'type': 'file',
                'data': src_node['data'][:]
            }

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
        elif command == 'wc':
            self.cmd_wc(args)
        elif command == 'tree':
            self.cmd_tree(args)
        elif command == 'whoami':
            self.cmd_whoami(args)
        elif command == 'cp':
            self.cmd_cp(args)
        else:
            print(f'{command}: команда не найдена')

    def repl(self):
        while True:
            parts =\
                input(f'{self.username}@{self.hostname}:~'
                      f'{self.cwd if self.cwd != "/" else ""}$ ')\
                .strip().split()
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
                print(f'{self.username}@{self.hostname}:~'
                      f'{self.cwd if self.cwd != "/" else ""}$ {line}')
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


def default_vfs(user):
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
            break
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
            break
        if os.path.exists(path):
            if os.path.isfile(path):
                start_script_path = path
            else:
                print(f'bash: {path}: Это каталог')
        else:
            print(f'bash: {path}: Нет такого файла или каталога')

    return vfs_path, start_script_path


def debug_output(vfs_path, start_script_path):
    if vfs_path or start_script_path:
        print(f'Параметры запуска (отладочный вывод):')
        if vfs_path: print(f'    VFS: {vfs_path}')
        if start_script_path: print(f'    Script: {start_script_path}')
        print()


def main():
    vfs_path, start_script_path = settings_input()
    debug_output(vfs_path, start_script_path)
    sh = Shell(build_node(vfs_path) if vfs_path else {}, vfs_path)
    if vfs_path is None:
        sh.vfs = default_vfs(sh.username)
    if start_script_path:
        print('Начало выполнения стартового скрипта')
        sh.run_script(start_script_path)
        print('Стартовый скрипт выполнен успешно')
    sh.repl()


if __name__ == '__main__':
    main()
