import os
import paramiko
from stat import S_ISDIR
import time

# Log colors
class LogColors:
    RED = "\033[1;91m"    # Red (bold)
    GREEN = "\033[1;92m"  # Green (bold)
    YELLOW = "\033[1;93m" # Yellow (bold)
    BLUE = "\033[1;94m"   # Blue (bold)
    RESET = "\033[0m"     # Reset

def log(message, color=LogColors.RESET):
    """Print a message in the specified color."""
    print(f"{color}{message}{LogColors.RESET}")

def format_log(tag, message, color):
    """Display a log message with a colored tag."""
    tag_colored = f"{color}{tag}{LogColors.RESET}"
    print(f"{tag_colored} {message}")

def list_remote_files(sftp, remote_dir):
    """Return a list of files (full paths) in a remote directory."""
    files = {}
    try:
        for entry in sftp.listdir_attr(remote_dir):
            remote_path = f"{remote_dir}/{entry.filename}"
            if S_ISDIR(entry.st_mode):
                files.update(list_remote_files(sftp, remote_path))  # Recursive for subfolders
            else:
                files[remote_path] = entry.st_size  # Store file size for comparison
    except FileNotFoundError:
        pass  # Directory does not exist yet
    return files

def calculate_total_size(files):
    """Calculate the total size of local files."""
    return sum(os.path.getsize(file[0]) for file in files)

def transfer_files(local_dir, remote_dir, sftp):
    """
    Transfer all content from local subdirectories to a remote directory via SFTP.
    Only transfers new or modified files.
    """
    format_log("[INFO]", "Scanning local files (excluding root files)...", LogColors.YELLOW)
    local_files = []
    for root, _, filenames in os.walk(local_dir):
        if root == local_dir:
            # Ignore files located directly in the root
            continue
        for filename in filenames:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, local_dir)
            local_files.append((full_path, relative_path))

    format_log("[INFO]", "Scanning remote files...", LogColors.YELLOW)
    remote_files = list_remote_files(sftp, remote_dir)

    format_log("[INFO]", "Starting file transfer...", LogColors.GREEN)
    for local_path, relative_path in local_files:
        remote_path = f"{remote_dir}/{relative_path}"
        local_size = os.path.getsize(local_path)

        if remote_path in remote_files and remote_files[remote_path] == local_size:
            format_log("[SKIP]", f"{remote_path} (already exists and is identical)", LogColors.YELLOW)
        else:
            remote_folder = os.path.dirname(remote_path)
            try:
                sftp.makedirs(remote_folder)
            except IOError:
                pass  # Folder already exists
            format_log("[TRANSFER]", f"{local_path} -> {remote_path}", LogColors.BLUE)
            sftp.put(local_path, remote_path)

# Add a method to create directories for SFTP
def sftp_makedirs(sftp, remote_dir):
    """Create remote directories recursively."""
    dirs = []
    while len(remote_dir) > 1:
        dirs.append(remote_dir)
        remote_dir = os.path.dirname(remote_dir)
    dirs.reverse()
    for dir_path in dirs:
        try:
            sftp.mkdir(dir_path)
        except IOError:
            pass  # Directory already exists

# Add the method to Paramiko SFTPClient
paramiko.SFTPClient.makedirs = sftp_makedirs

def main():
    print("\n\033[1m    🪩 ---------------------------------- 🪩\033[0m")
    print("\033[1m     📀  -  Navidrome SFTP Transfer  -  📀\033[0m")
    print("\033[1m    🪩 ---------------------------------- 🪩\033[0m\n")

    host = input("\033[1m[CONF]\033[0m IPv4 address server: ").strip()
    username = input("\033[1m[CONF]\033[0m Login: ").strip()
    password = input("\033[1m[CONF]\033[0m Password: ").strip()
    remote_dir = input("\033[1m[CONF]\033[0m Remote directory: ").strip()
    local_dir = input("\033[1m[CONF]\033[0m Local directory: ").strip()

    format_log("[INFO]", "Preparing SFTP connection...", LogColors.YELLOW)

    # Confirmation before transfer
    confirmation = input("\n\033[1mAre you sure you want to proceed with the transfer?\033[0m (YES/NO): ").strip().lower()
    if confirmation != "yes":
        format_log("[INFO]", "Transfer canceled by the user.", LogColors.RED)
        return

    # SFTP connection
    try:
        format_log("[INFO]", f"Connecting to {host}...", LogColors.YELLOW)
        transport = paramiko.Transport((host, 22))

        format_log("[INFO]", "Authenticating...", LogColors.YELLOW)
        transport.connect(username=username, password=password)

        format_log("\n[SUCCESS]", "Connection successful\n", LogColors.GREEN)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Check if the remote directory exists
        try:
            format_log("[INFO]", f"Checking existence of remote directory: {remote_dir}", LogColors.YELLOW)
            sftp.listdir(remote_dir)
        except IOError:
            format_log("[ERROR]", f"The remote directory {remote_dir} does not exist. Creating it...", LogColors.RED)
            sftp.makedirs(remote_dir)

        # Transfer files and folders
        transfer_files(local_dir, remote_dir, sftp)

        # Close the connection
        format_log("\n[INFO]", "Closing SFTP connection...", LogColors.YELLOW)
        sftp.close()
        transport.close()
        format_log("\n[SUCCESS]", "Transfer completed successfully. ✅\n", LogColors.GREEN)
    except Exception as e:
        format_log("\n[ERROR]", f"An error occurred: {e}\n", LogColors.RED)

if __name__ == "__main__":
    main()
