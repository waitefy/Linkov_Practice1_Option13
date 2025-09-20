import os
import socket

username = os.getlogin()
hostname = socket.gethostname()
line = input(f'{username}@{hostname}:~$ ')

while line != 'exit':
    parts = line.split()
    command, args = parts[0], parts[1:]

    if command in ('ls', 'cd'):
        print(line)
    else:
        print(f'{command}: команда не найдена')

    line = input(f'{username}@{hostname}:~$ ')
