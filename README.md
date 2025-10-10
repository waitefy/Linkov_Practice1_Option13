<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/UNIX%20Shell%20Emulator-%F0%9F%94%A5%20VFS%20in%20Memory-000000?logo=gnu-bash&logoColor=white" alt="UNIX Shell Emulator">
  </a>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-111"></a>
  <a href="#"><img src="https://img.shields.io/badge/license-MIT-111"></a>
  <a href="#"><img src="https://img.shields.io/badge/status-Study%20Project-0ea5e9"></a>
</p>

<h1 align="center">Эмулятор командной оболочки UNIX-подобной ОС</h1>
<p align="center"><i>CLI-эмулятор с виртуальной файловой системой (VFS) в памяти и командами: <b>ls</b>, <b>cd</b>, <b>whoami</b>, <b>wc</b>, <b>tree</b>, <b>cp</b>, <b>vfs-init</b>, запуск скриптов.</i></p>

---

## О проекте

> Цель: сделать эмулятор максимально похожим на реальную командную строку UNIX.  
> Вся работа с файлами ведётся **только в памяти**: исходником VFS выступает выбранная директория, далее эмулятор оперирует её «снимком» (dict-структуры).

```
username@hostname:~$ python main.py
username@hostname:~$  # приглашение формируется из реальных username/hostname
```

---

## Быстрый старт

```bash
python main.py
# Путь к VFS: vfs_examples/files
# Путь к стартовому скрипту: scripts/start_all.txt
```

---

## Этапы и прогресс

| Этап | Цель | Статус |
|---|---|---|
| 1. REPL | CLI, парсер, заглушки `ls`, `cd`, `exit`, ошибки | ✅ |
| 2. Конфигурация | Ввод путей VFS/скрипта, отладочный вывод, исполнение скрипта | ✅ |
| 3. VFS | VFS в памяти, `vfs-init` (опц. `--wipe`), тестовые VFS | ✅ |
| 4. Основные команды | `ls`, `cd`, `wc`, `tree`, `whoami` | ✅ |
| 5. Доп. команды | `cp` (файл→файл, файл→каталог, проверки) | ✅ |

---

## Команды эмулятора

```text
ls /etc
cd /home/user
whoami
wc /README.txt
tree /home
cp /README.txt /home/user
vfs-init
bash scripts/start_all.txt
./scripts/test_cp.txt
```

---

## Скрипты тестирования

```
scripts/
├─ test_bash.sh
├─ test_basics.sh
├─ test_cp.sh
├─ test_errors.sh
├─ test_errors_2.sh
├─ test_ls_cd.sh
├─ test_tree.sh
├─ test_vfs.sh
├─ test_vfs_2.sh
├─ test_wc.sh
```

---

## Технические детали

- **VFS** — словарь `{ "type": "dir"|"file", "children"?, "data"? }`  
- **Навигация** — `resolve_path()` нормализует путь; `get_node()` ищет узел  
- **Скрипты** — `bash file` и `./path` выполняют команды построчно

---

## Лицензия

MIT — используй и модифицируй свободно в учебных целях.

<p align="center">
  <sub>Предмет: <b>Конфигурационное управление</b> • Группа: <b>ИКБО-31-24</b> • 2025</sub>
</p>
