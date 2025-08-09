# -FILE-INTEGRITY-CHECKER

*Company*: CODTECH IT SOLUTIONS

*NAME*: Sree venkat Ramanujula

*INTERN ID*:CT06DH1414

*DOMAIN*: CYBER SECURITY & ETHICAL HACKING

*DURACTION*: 6 WEEKS

*MENTOR*: NEELA SANTOSH

## **Description of the File Monitoring Script**

This Python file monitoring script is a simple yet powerful tool for tracking changes in files within a chosen directory. It works by calculating **cryptographic hash values** for each file and comparing them over time to detect **modifications, additions, and deletions**. This makes it ideal for use in **security auditing, file integrity checking, or project monitoring**.

### **How It Works**

The script uses Python’s `hashlib` library to generate a hash for each file. By default, it uses the **SHA-256** hashing algorithm, which is secure and highly reliable for detecting even the smallest change in file content. You can also choose other hashing algorithms (like `md5` or `blake2b`) using the `--hash` option.

The directory is scanned recursively with `os.walk()`, collecting all file paths except those that match ignored extensions (if specified with `--ignore`). Each file’s hash is stored in a dictionary, and on every scan cycle, the script compares the current hash values to the previous ones.

The detection process works like this:

* **New files** – If a file wasn’t there before, it is marked as `[+] New file`.
* **Modified files** – If the hash value changes, it is marked as `[!] Modified`.
* **Deleted files** – If a file is missing, it is marked as `[-] Deleted`.

These events are printed to the console in real time and also written to a **log file** (`file_changes.log`) with timestamps.

---

### **Key Features**

1. **Cross-Platform** – Works on Windows, macOS, and Linux with no changes.
2. **Real-Time Change Detection** – Tracks new, changed, and deleted files during runtime.
3. **Secure Hashing** – Uses cryptographic algorithms to ensure accurate change detection.
4. **Ignore Specific Files** – Ability to skip files by extension (e.g., `.log`, `.tmp`).
5. **Customizable Hash Algorithm** – Choose any algorithm available in `hashlib`.
6. **Verbose Mode** – Use `--verbose` for detailed scanning information.

---

### **Usage**

Run the script from the terminal:

```bash
python file_monitor.py --path /path/to/folder --ignore .log .tmp --hash sha256
```

Options:

* `--path` → Folder to monitor (required)
* `--ignore` → Extensions to skip (optional)
* `--hash` → Hash algorithm (optional, default is `sha256`)
* `--verbose` → Show detailed scanning info (optional)

Example:

```bash
python file_monitor.py --path test_folder --ignore .log .tmp --hash blake2b --verbose
```

---

### **Fixed Scan Interval**

This version has a **fixed 5-second interval** between scans (`time.sleep(5)`). This ensures the script doesn’t consume too much CPU while still detecting changes quickly. You can adjust this value in the code if you want faster or slower checks.

---

### **Practical Uses**

* **Security & Auditing** – Detect unauthorized file modifications in sensitive directories.
* **Development Monitoring** – Track changes to source code or configuration files.
* **Document Tracking** – Keep a history of edits in collaborative folders.
* **Backup Verification** – Ensure backups remain unaltered.

---

### **Advantages**

* No external dependencies – runs with standard Python libraries.
* Minimal resource usage – efficient hashing and scanning.
* Easy to configure – just pass the path and optional filters.
* Accurate – cryptographic hashing detects even a single byte change.
* Permanent record – all events are stored in `file_changes.log`.

---

### **Conclusion**

This script provides a reliable way to **monitor file integrity** in any directory. By using hash-based detection, it ensures that no modification goes unnoticed, even if file timestamps or sizes stay the same. Whether you are a **developer**, **system admin**, or **security analyst**, it’s a practical and lightweight solution for keeping an eye on your files.

---

#OUTPUT

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/12874ed5-7a47-41d6-8446-e23eb942354f" />
