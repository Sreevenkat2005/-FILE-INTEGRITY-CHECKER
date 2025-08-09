import hashlib
import os
import time
import argparse
import traceback
from datetime import datetime
import sys

SCAN_DELAY_SECONDS = 5  # fixed delay between scans

def get_file_hash(file_path, hash_algo="sha256", verbose=False):
    try:
        hash_func = getattr(hashlib, hash_algo)()
    except Exception:
        if verbose:
            print(f"Unsupported hash algorithm: {hash_algo}")
        return None

    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
        if verbose:
            print(f"Could not hash '{file_path}': {e}")
        return None
    except Exception as e:
        if verbose:
            print(f"Unexpected error hashing '{file_path}': {e}")
            traceback.print_exc()
        return None

def get_all_files(directory, ignore_exts=None):
    files = []
    for root, _, filenames in os.walk(directory):
        for fname in filenames:
            if ignore_exts and os.path.splitext(fname)[1].lower() in ignore_exts:
                continue
            files.append(os.path.join(root, fname))
    return files

def log_change(message, log_file="file_changes.log"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - {message}"
    print(entry)
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception as e:
        print(f"Warning: couldn't write to log file '{log_file}': {e}")

def monitor_directory(directory, ignore_exts=None, hash_algo="sha256", verbose=False):
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"Error: path is not a directory or does not exist: {directory}")
        sys.exit(1)

    if verbose:
        print(f"Monitoring directory: {directory}")
        print(f"Hash algorithm: {hash_algo}")
        print(f"Ignoring extensions: {sorted(ignore_exts) if ignore_exts else 'None'}")
        print(f"Scan delay: {SCAN_DELAY_SECONDS} seconds")
        print("Gathering initial file list...")

    files = get_all_files(directory, ignore_exts)
    file_hashes = {}
    for f in files:
        file_hashes[f] = get_file_hash(f, hash_algo, verbose=verbose)

    log_change(f"Monitoring started. Initial files: {len(file_hashes)}")

    try:
        while True:
            if verbose:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Scanning...")

            current_files = get_all_files(directory, ignore_exts)
            current_set = set(current_files)
            previous_set = set(file_hashes.keys())

            # Check for new or modified files
            for f in current_files:
                current_hash = get_file_hash(f, hash_algo, verbose=verbose)
                if f not in file_hashes:
                    log_change(f"[+] New file: {f}")
                elif current_hash != file_hashes[f]:
                    log_change(f"[!] Modified: {f}")
                file_hashes[f] = current_hash

            # Check for deleted files
            for f in list(previous_set - current_set):
                log_change(f"[-] Deleted: {f}")
                file_hashes.pop(f, None)

            if verbose:
                print(f"Files monitored now: {len(file_hashes)} (added: {len(current_set - previous_set)}, removed: {len(previous_set - current_set)})")

            time.sleep(SCAN_DELAY_SECONDS)
    except KeyboardInterrupt:
        log_change("Monitoring stopped by user.")
    except Exception as e:
        print("Fatal error in monitor loop:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor a folder for file changes using hash comparison (debug-friendly).")
    parser.add_argument("--path", required=True, help="Path to folder to monitor")
    parser.add_argument("--ignore", nargs="*", help="File extensions to ignore (include the dot), e.g. --ignore .log .tmp")
    parser.add_argument("--hash", default="sha256", help="Hash algorithm (default: sha256)")
    parser.add_argument("--verbose", action="store_true", help="Show verbose/debug output")

    args = parser.parse_args()

    ignore_set = set([ext.lower() for ext in args.ignore]) if args.ignore else None

    monitor_directory(
        directory=args.path,
        ignore_exts=ignore_set,
        hash_algo=args.hash,
        verbose=args.verbose
    )
