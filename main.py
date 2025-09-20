import os
import socket
import sys


def repl(username, hostname):
    while True:
        line = input(f'{username}@{hostname}:~$ ')
        execute_command(line, username, hostname)


def execute_command(line, username, hostname):
    if not line.strip():
        return
    parts = line.split()
    command, args = parts[0], parts[1:]

    if command in ('ls', 'cd'):
        print(line)
    elif command == 'exit':
        sys.exit(0)
    else:
        print(f'{command}: команда не найдена')


def main():
    username = os.getlogin()
    hostname = socket.gethostname()
    repl(username, hostname)


if __name__ == '__main__':
    main()
