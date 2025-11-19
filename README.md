[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Cross--platform-green)](#)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)](#)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# 🧹 Deduplicate!

A lightweight, command-line Python tool that scans directories for duplicate files using **SHA-256 hashing**.
It identifies identical files across nested folders and gives you the option to **delete** or **move** them safely.

---

## ✨ Features

- 🔍 **Recursive Scan** - Searches through all subdirectories.
- 🔑 **Secure Hashing** - Compares file contents using SHA-256.
- 🗂️ **Smart Duplicate Detection** - Detects identical files even with different names.
- 🪣 **Move or Delete** - Move duplicates to a separate directory or delete them permanently.
- 🧠 **Logging** - Every action is logged in `deduplicate.log` for traceability.
- 🧾 **Error Handling** - Graceful exits and detailed exception logging.

---

## 🧰 Requirements

- Python 3.8+

Install Required Packages via:

```
python -m pip install -r requirements.txt
```

---

## ⚙️ Usage

### 🔧 Command Syntax

```
python dedupe.py -p <path> [-v] [-mv <destination>] [-del] [-o <destination>]
```

### 🧩 Arguments

| Flag   | Long Form             | Description                                   | Example            |
| ------ | --------------------- | --------------------------------------------- | ------------------ |
| `-v`   | `--version`           | Program Version Number                        | `-v`               |
| `-vv`  | `--verbose`           | Detailed Output for Debugging                 | `-vv`               |
|  `-p`  | `--path`              | Path to search for duplicates                 | `-p ./Downloads`   |
| `-mv`  | `--move-duplicates`   | Move duplicates to specified directory        | `-mv ./duplicates` |
| `-del` | `--delete-duplicates` | Delete all duplicate files after confirmation | `-del`             |
| `-o`   | `--output-file`       | Path to save output file                      | `-o ./output.txt`  |
| `-i`   | `--ignore-path`       | Path to Ignore Search & Comparison            | `-i ./cache/`      |
| `-kn`  | `--keep-newest`       | Option to Keep the Newest File                | `-kn`              |
| `-f`   | `--full`              | More Accurate Duplicate Check                 | `-f`               |
| `-q`   | `--quick`             | Less Accurate Duplicate Check                 | `-q`               |

---

### 💻 Examples

**Find duplicates in current directory**

```
python dedupe.py -p ./
```

**Find duplicates in current directory & create output file**

```
python dedupe.py -p ./ -o ./output.txt
```

**Move all duplicates to a separate folder**

```
python dedupe.py -p ./Documents -mv ./Duplicates
```

**Delete duplicates (with confirmation)**

```
python dedupe.py -p ./test -del
```

**Ignore directory from search**

```
python dedupe.py -p ./test -i ./test/cache/
```

**Get current version of program**

```
python dedupe.py -v
```

---

## 🧠 How It Works

1. **Scan:** Deduplicate recursively scans all files in the given directory & optionally ignore specific directory.
2. **Hash:** Each file’s contents are hashed using **SHA-256**, creating a unique signature.
3. **Compare:** Files with identical hashes are grouped together.
4. **Action:** You choose whether to **move** or **delete** duplicates.
5. **Log:** Every operation is recorded in `deduplicate.log`.

---

## 📄 Example Output

```

Scanning Path './test' For Duplicate Files...
✅ Duplicate Files Found:
- ./test/subdir/a_copy.txt
  ⚠️ Are you sure you want to delete all duplicates? (Y/N): y
  ✅ Duplicate Files Successfully Deleted.
```

---

## 🎯 Upcoming Features

- **Export Options** Option to Export Duplicates as .json File or SQLite Database.
- **Updated Unit Tests** Add Unit Tests for All Available Features.
- **Dry Run** Add Dry Run Option For a Safe Run Before Deletion/Move.

## 🧑‍💻 Author

Created by [**Ibby I.**](https://github.com/IbbyI)

Developer passionate about automation, efficiency, and clean code.
