import os
import paramiko
import socket
from stat import S_ISDIR
from getpass import getpass
from tqdm import tqdm

# --- Log colors ---
class LogColors:
    RED = "\033[1;91m"
    GREEN = "\033[1;92m"
    YELLOW = "\033[1;93m"
    BLUE = "\033[1;94m"
    RESET = "\033[0m"

def format_log(tag, message, color):
    print(f"{color}{tag}{LogColors.RESET} {message}")

# --- Remote file listing ---
def list_remote_files(sftp, remote_dir):
    files = {}
    try:
        for entry in sftp.listdir_attr(remote_dir):
            remote_path = f"{remote_dir}/{entry.filename}"
            if S_ISDIR(entry.st_mode):
                files.update(list_remote_files(sftp, remote_path))
            else:
                files[remote_path] = entry.st_size
    except FileNotFoundError:
        pass
    return files

# --- Transfer with filter and progress ---
def transfer_files(local_dir, remote_dir, sftp):
    ignored_extensions = (".tmp", ".ds_store", ".log")

    format_log("[INFO]", "Scanning local files (excluding root)...", LogColors.YELLOW)
    local_files = []
    for root, _, filenames in os.walk(local_dir):
        if root == local_dir:
            continue
        for filename in filenames:
            if filename.lower().endswith(ignored_extensions):
                continue
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, local_dir)
            local_files.append((full_path, relative_path))

    remote_files = list_remote_files(sftp, remote_dir)

    format_log("[INFO]", f"{len(local_files)} files to evaluate for transfer.\n", LogColors.YELLOW)
    for local_path, relative_path in tqdm(local_files, desc="Transferring", unit="file"):
        remote_path = f"{remote_dir}/{relative_path}"
        local_size = os.path.getsize(local_path)

        if remote_path in remote_files and remote_files[remote_path] == local_size:
            continue  # Identical file already exists
        remote_folder = os.path.dirname(remote_path)
        try:
            sftp.makedirs(remote_folder)
        except IOError:
            pass
        sftp.put(local_path, remote_path)

# --- SFTP mkdirs helper ---
def sftp_makedirs(sftp, remote_dir):
    dirs = []
    while len(remote_dir) > 1:
        dirs.append(remote_dir)
        remote_dir = os.path.dirname(remote_dir)
    dirs.reverse()
    for dir_path in dirs:
        try:
            sftp.mkdir(dir_path)
        except IOError:
            pass

paramiko.SFTPClient.makedirs = sftp_makedirs

# --- Main logic ---
def main():
    print("\n\033[1m    🪩 ---------------------------------- 🪩\033[0m")
    print("\033[1m     📀  -  Navidrome SFTP Transfer  -  📀\033[0m")
    print("\033[1m    🪩 ---------------------------------- 🪩\033[0m\n")
    host = input("\033[1m[CONF]\033[0m IPv4 server address: ").strip()
    username = input("\033[1m[CONF]\033[0m Login: ").strip()
    password = getpass("\033[1m[CONF]\033[0m Password: ")
    remote_dir = input("\033[1m[CONF]\033[0m Remote directory: ").strip()
    local_dir = input("\033[1m[CONF]\033[0m Local directory: ").strip()

    confirmation = input("\n\033[1mAre you sure you want to proceed with the transfer?\033[0m (YES/NO): ").strip().lower()
    if confirmation != "yes":
        format_log("[CANCELLED]", "Transfer cancelled by user.", LogColors.RED)
        return

    # --- Check port ---
    try:
        format_log("\n[INFO]", f"Checking SSH availability on {host}:22...", LogColors.YELLOW)
        with socket.create_connection((host, 22), timeout=5):
            pass
    except Exception:
        format_log("[ERROR]", "SSH port 22 is unreachable. Check the host or firewall.", LogColors.RED)
        return

    # --- Connect and transfer ---
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        try:
            sftp.listdir(remote_dir)
        except IOError:
            format_log("[INFO]", "Remote directory doesn't exist, creating...", LogColors.YELLOW)
            sftp.makedirs(remote_dir)

        transfer_files(local_dir, remote_dir, sftp)

        sftp.close()
        transport.close()
        format_log("\n[DONE]", "Transfer complete ✅\n", LogColors.GREEN)

    except Exception as e:
        format_log("\n[ERROR]", f"An error occurred: {e}\n", LogColors.RED)

if __name__ == "__main__":
    main()

