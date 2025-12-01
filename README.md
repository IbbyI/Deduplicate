# 🧹 **Deduplicate**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/deduplicate-cli.svg?color=blue)](https://pypi.org/project/deduplicate-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Platform](https://img.shields.io/badge/Platform-Cross--platform-green)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A lightweight, fast command-line Python tool that scans directories for duplicate files using **SHA-256 hashing**.
It identifies identical files across nested folders.
---

## ✨ Features

- 🔍 **Recursive Scan** - Searches through all subdirectories.
- 🔑 **Secure Hashing** - Compares file contents using SHA-256.
- 🗂️ **Smart Duplicate Detection** - Detects identical files even with different names.
- 🪣 **Move or Delete** - Move duplicates to a separate directory or delete them permanently.
- 🧠 **Logging** - Every action is logged in `deduplicate.log` for traceability.
- 🧾 **Error Handling** - Graceful exits and detailed exception logging.
* ⚠️ **Protected operations** with confirmation prompts
* 🛠️ **Supports full, quick, and automatic hashing strategies**
* 🗜️ **Dry-run mode** for safe testing
* 🧼 **Clean Architecture:** Core logic separated from UI and CLI

---

# 📦 **Project Structure**

```
deduplicate/
│
├── core/           # Pure Logic
├── ui/             # UI Adapters / Printing / Prompts
├── cli/            # CLI Entry Point (Argument Parsing)
│
└── tests/          # Unit Tests
```

---

# 🚀 **Installation**

### **From PyPI (Recommended)**

```
pip install deduplicate-cli
```

Then run:

```
dedupe -p ./Downloads
```

### **From Source**

```
git clone https://github.com/IbbyI/Deduplicate.git
cd Deduplicate
pip install -r requirements.txt
```

---

### 🧩 Arguments

| Flag   | Long Option           | Description                                   | Example            |
| ------ | --------------------- | --------------------------------------------- | ------------------ |
| `-v`   | `--version`           | Program Version Number                        | `-v`               |
| `-vv`  | `--verbose`           | Detailed Output for Debugging                 | `-vv`              |
|  `-p`  | `--path`              | Path to search for duplicates                 | `-p ./Downloads`   |
| `-mv`  | `--move-duplicates`   | Move duplicates to specified directory        | `-mv ./duplicates` |
| `-del` | `--delete-duplicates` | Delete all duplicate files after confirmation | `-del`             |
| `-o`   | `--output-file`       | Path to save output file                      | `-o ./output.txt`  |
| `-i`   | `--ignore-path`       | Path to Ignore Search & Comparison            | `-i ./cache/`      |
| `-kn`  | `--keep-newest`       | Option to Keep the Newest File                | `-kn`              |
| `-f`   | `--full`              | More Accurate Duplicate Check                 | `-f`               |
| `-q`   | `--quick`             | Less Accurate Duplicate Check                 | `-q`               |
| `N/A`  | `--dry-run`           | Tests Run Move and Delete Functionality       | `--dry-run`        |

---

# 💻 **Examples**

### **Find duplicates**

```
dedupe -p ./
```

### **Move duplicates to a folder**

```
dedupe -p ./Documents -mv ./Duplicates
```

### **Delete duplicates (with safety prompt)**

```
dedupe -p ./Photos -del
```

### **Ignore a cache directory**

```
dedupe -p ./project -i ./project/.cache/
```

### **Write results to output file**

```
dedupe -p ./ -o ./duplicates.txt
```

---

# 🧠 **How It Works**

1. **Scan** – Recursively walks the directory.
2. **Hash** – Computes SHA-256 of each file (full, quick, or auto).
3. **Group** – Groups files with identical hashes.
4. **Compare** – Identifies which file to keep (oldest or newest).
5. **Action** – Moves or deletes duplicates depending on CLI flags.
6. **Log** – Everything is recorded to `deduplicate.log`.

---

# 📄 **Example Output**

```
Scanning './test' for duplicates...
Unique Files Found: 42
Duplicate Files Found: 3

⚠️ Delete all duplicates? (Y/N): y
✅ Deleted 3 files.
⚠️ Skipped 2 files.
```

---

# 🧪 **Testing**

This project includes unit tests for:

* hashing functions
* duplicate detection
* compare logic
* file actions (move/delete)

Run tests using:

```
pytest
```

---

# 🧑‍💻 **Author**

**Ibby I.**
GitHub: [https://github.com/IbbyI](https://github.com/IbbyI)

Passionate about automation, performance, clean architecture, and building developer-friendly tools.


# ⭐ **Support the Project**

If you found this useful, consider starring the repo:

👉 [https://github.com/IbbyI/Deduplicate](https://github.com/IbbyI/Deduplicate)

---