<h1 align="center">Эмулятор командной оболочки UNIX-подобной ОС</h1>
<p align="center">
  <i>CLI-эмулятор с виртуальной файловой системой (VFS) в памяти и командами, имитирующими работу терминала UNIX.</i>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-green.svg"></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-black"></a>
  <a href="#"><img src="https://img.shields.io/badge/Status-Completed-success"></a>
</p>

---

## Цель проекта
Разработать **эмулятор языка оболочки**, который максимально точно имитирует поведение командной строки UNIX-подобных систем.  
Работа с файлами осуществляется **в памяти** — физическая ФС не изменяется.

---

## Быстрый запуск

```bash
git clone https://github.com/waitefy/Linkov_Practice1_Option13.git
cd Linkov_Practice1_Option13
python3 main.py
```

При запуске программа запросит:
```
Путь к VFS: vfs_example
Путь к стартовому скрипту: start.sh
```

---

## Этапы разработки

| Этап | Цель | Статус |
|------|------|---------|
| 1. REPL | CLI, парсер, заглушки (`ls`, `cd`, `exit`) | ✅ |
| 2. Конфигурация | Параметры запуска, выполнение стартовых скриптов | ✅ |
| 3. VFS | Виртуальная ФС в памяти, `vfs-init` | ✅ |
| 4. Основные команды | `ls`, `cd`, `wc`, `tree`, `whoami` | ✅ |
| 5. Дополнительные команды | `cp` (копирование файлов внутри VFS) | ✅ |

---

## Реализованные команды

| Команда | Назначение |
|----------|-------------|
| `ls` | Список содержимого каталога |
| `cd` | Переход в каталог |
| `wc` | Подсчёт строк, слов и байт |
| `tree` | Древовидное отображение VFS |
| `whoami` | Отображает имя текущего пользователя |
| `cp` | Копирует файлы в пределах VFS |
| `vfs-init` | Сбрасывает виртуальную ФС на дефолтную |
| `bash <script>` | Выполняет команды из скрипта |
| `./<script>` | Альтернатива `bash script` |
| `exit` | Завершает работу эмулятора |

---

## Тестовые сценарии

Папка [`scripts/`](scripts) содержит тестовые сценарии для проверки всех этапов проекта:

```
scripts/
├── test_basics.sh     # проверка ls, cd, whoami
├── test_wc.sh         # тестирование wc
├── test_tree.sh       # проверка tree
├── test_vfs.sh        # тестирование vfs-init
├── test_cp.sh         # проверка команды cp
└── test_errors.sh     # обработка ошибок
```

Пример запуска:

```bash
python3 main.py
# Путь к VFS: VFS_some_files
# Путь к стартовому скрипту: scripts/test_cp.sh
```

---

### Пример `scripts/test_cp.sh`

```bash
ls /
tree /
cp /README.txt /copy1.txt
ls /
cp /README.txt /home
ls /home
cp /README.txt home/user/readme_copy.txt
ls /home/user
cp /no_such_file /tmp.txt
cp /home /copy_home
cp /README.txt /copy1.txt
wc /copy1.txt
cd /home/user
cp ../../README.txt ./copied.txt
ls .
wc copied.txt ../../README.txt
cp /README.txt /no/such/dir/file.txt
cd /
tree /
```

---

## Основные технические решения

- Виртуальная файловая система реализована как рекурсивный словарь:
  ```python
  { "type": "dir"|"file", "children"?: {...}, "data"?: bytes }
  ```
- Навигация реализована через методы:
  - `resolve_path()` — нормализация относительных путей
  - `get_node()` — поиск узла по абсолютному пути
- Все команды инкапсулированы в классе `Shell`
- Скрипты выполняются построчно (`bash` и `./`)

---

<p align="center">
  <img src="https://img.shields.io/badge/Author-Matvey%20Linkov-blue?style=for-the-badge&logo=github" />
</p>

<p align="center">
  <sub>Предмет: <b>Конфигурационное управление</b> • Группа: <b>ИКБО-31-24</b> • 2025</sub>
</p>
