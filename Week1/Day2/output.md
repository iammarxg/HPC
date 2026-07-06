# Basic Prompt

This bash script creates a compressed `.tar.gz` archive of a specified folder and saves it with a timestamp.

### The Backup Script (`backup.sh`)

```bash
#!/bin/bash

# --- Configuration ---
# The folder you want to back up
SOURCE_DIR="/path/to/your/source_folder"

# The directory where you want to store backups
BACKUP_DIR="/path/to/your/backup_destination"

# Create a timestamp for the filename
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Name of the backup file
BACKUP_NAME="backup_$TIMESTAMP.tar.gz"

# --- Execution ---

# Check if backup directory exists, if not, create it
mkdir -p "$BACKUP_DIR"

# Create the archive
echo "Starting backup of $SOURCE_DIR..."
tar -czf "$BACKUP_DIR/$BACKUP_NAME" -C "$SOURCE_DIR" .

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Backup successfully created: $BACKUP_DIR/$BACKUP_NAME"
else
    echo "Backup failed!"
fi
```

### How to use it:

1.  **Create the file:**
    `nano backup.sh`
2.  **Paste the code above** and update the `SOURCE_DIR` and `BACKUP_DIR` variables.
3.  **Make it executable:**
    ```bash
    chmod +x backup.sh
    ```
4.  **Run it:**
    ```bash
    ./backup.sh
    ```

---

### Pro-Tips:

*   **Automate with Cron:** If you want this to run automatically every day at 2:00 AM, type `crontab -e` and add this line:
    ```bash
    0 2 * * * /path/to/your/backup.sh
    ```
*   **Remove old backups:** If you want to delete backups older than 30 days to save space, add this line to the end of the script:
    ```bash
    find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +30 -delete
    ```
*   **Why `tar -czf`?**
    *   `-c`: Create a new archive.
    *   `-z`: Compress with gzip.
    *   `-f`: Specifies the filename.
    *   `-C`: Changes to the source directory first so the backup doesn't include the full absolute path of your folders.


# Improved Prompt

To create a backup script, we will use the `tar` command with the `czf` flags (create, gzip, file).

### The Bash Script (`backup.sh`)

Create a file named `backup.sh` and paste the following code into it:

```bash
#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_folder> <destination_folder>"
    exit 1
fi

SOURCE_DIR=$1
DEST_DIR=$2
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FOLDER_NAME=$(basename "$SOURCE_DIR")
BACKUP_NAME="${FOLDER_NAME}_backup_${DATE}.tar.gz"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory $SOURCE_DIR does not exist."
    exit 1
fi

# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Create the tar archive
echo "Backing up $SOURCE_DIR to $DEST_DIR/$BACKUP_NAME..."
tar -czf "$DEST_DIR/$BACKUP_NAME" -C "$(dirname "$SOURCE_DIR")" "$FOLDER_NAME"

# Check if backup was successful
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $DEST_DIR/$BACKUP_NAME"
else
    echo "Backup failed."
    exit 1
fi
```

### How to use it:

1.  **Make the script executable:**
    ```bash
    chmod +x backup.sh
    ```

2.  **Run the script:**
    Pass the path of the folder you want to back up and the path where you want the backup saved:
    ```bash
    ./backup.sh /home/user/documents /home/user/backups
    ```

### Key features of this script:
*   **Dynamic Naming:** It uses `date +%Y-%m-%d_%H-%M-%S` to ensure every backup has a unique timestamp.
*   **Robustness:** It checks if the source folder exists before starting.
*   **Safety:** It uses `mkdir -p` to ensure the destination folder exists; if it doesn't, it creates it automatically.
*   **Path Handling:** It uses `basename` and `dirname` to ensure that the tar file contains the folder correctly without including the full absolute path of the source directory (which prevents "removing leading / from member names" warnings).


# Detailed Prompt

This script uses `tar` to create a compressed archive of the source directory and includes logic to prune older backups based on the retention count provided.

### The Bash Script: `backup.sh`

```bash
#!/bin/bash

# Usage: ./backup.sh /path/to/source /path/to/destination 5

SOURCE_DIR=$1
DEST_DIR=$2
RETENTION_COUNT=$3

# 1. Validate arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <source_directory> <destination_directory> <retention_count>"
    exit 1
fi

# 2. Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist."
    exit 1
fi

# 3. Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# 4. Create the backup filename with a timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="backup_$TIMESTAMP.tar.gz"

echo "Starting backup of $SOURCE_DIR to $DEST_DIR/$BACKUP_NAME..."

# 5. Perform the backup
tar -czf "$DEST_DIR/$BACKUP_NAME" -C "$SOURCE_DIR" .

if [ $? -eq 0 ]; then
    echo "Backup successful."
else
    echo "Backup failed."
    exit 1
fi

# 6. Logic to delete older backups
# We list files in the destination directory, sort them by modification time (oldest first),
# and count how many exist. If the count exceeds the retention limit, we remove the oldest ones.
echo "Cleaning up backups older than $RETENTION_COUNT..."

# Get list of backup files, sorted by time (oldest first)
# 'ls -1tr' lists files one per line, sorted by time, oldest at the top
# 'grep' filters for our specific naming convention to avoid deleting other files
BACKUP_FILES=($(ls -1tr "$DEST_DIR"/backup_*.tar.gz 2>/dev/null))

FILE_COUNT=${#BACKUP_FILES[@]}

if [ "$FILE_COUNT" -gt "$RETENTION_COUNT" ]; then
    FILES_TO_DELETE=$((FILE_COUNT - RETENTION_COUNT))
    
    for (( i=0; i<$FILES_TO_DELETE; i++ )); do
        echo "Removing old backup: ${BACKUP_FILES[$i]}"
        rm "${BACKUP_FILES[$i]}"
    done
    echo "Cleanup complete. Removed $FILES_TO_DELETE old backup(s)."
else
    echo "No cleanup needed. Current backups ($FILE_COUNT) are within retention limit ($RETENTION_COUNT)."
fi
```

### How to use it:

1.  **Save the file:** Save the code above as `backup.sh`.
2.  **Make it executable:**
    ```bash
    chmod +x backup.sh
    ```
3.  **Run the script:**
    ```bash
    ./backup.sh /home/user/data /backups/my_project 5
    ```

### Key Logic Explained:
*   **`ls -1tr`**: This is the core of the cleanup logic. 
    *   `-1`: Lists one file per line.
    *   `-t`: Sorts by modification time (newest first).
    *   `-r`: Reverses the sort order (oldest first).
*   **Array Handling**: By loading the result of `ls` into a bash array (`BACKUP_FILES`), we can easily calculate the total number of files and iterate through only the specific number of files that exceed the `RETENTION_COUNT`.
*   **Error Handling**: The script checks `$?` (the exit status of the previous command) to ensure the `tar` command actually succeeded before attempting to prune old files.


# Creative Prompt

This script is designed for a production environment. It enforces strict error handling, uses absolute paths, and ensures that the backup process is atomic.

### The Backup Utility (`secure_backup.sh`)

```bash
#!/bin/bash

# --- Configuration ---
SOURCE_DIR="/data/critical_files"
DEST_DIR="/backups/archives"
RETENTION_COUNT=7
LOG_FILE="/var/log/backup_utility.log"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="backup_$TIMESTAMP.tar.gz"
CHECKSUM_FILE="$DEST_DIR/$ARCHIVE_NAME.sha256"

# --- Security & Integrity Checks ---
set -o errexit  # Exit on error
set -o nounset  # Exit on unset variables
set -o pipefail # Catch errors in piped commands

# Ensure destination exists
mkdir -p "$DEST_DIR"

# --- Execution ---
echo "[$(date)] Starting backup of $SOURCE_DIR" >> "$LOG_FILE"

# 1. Create Tarball
tar -czf "$DEST_DIR/$ARCHIVE_NAME" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

# 2. Generate SHA-256 Checksum
cd "$DEST_DIR"
sha256sum "$ARCHIVE_NAME" > "$CHECKSUM_FILE"
CHECKSUM=$(cat "$CHECKSUM_FILE" | awk '{print $1}')
FILE_SIZE=$(du -h "$ARCHIVE_NAME" | cut -f1)

# 3. Log Operation
echo "[$(date)] SUCCESS: $ARCHIVE_NAME | Size: $FILE_SIZE | SHA256: $CHECKSUM" >> "$LOG_FILE"

# 4. Rotation (Keep only N most recent)
# List files by time, exclude the ones we want to keep, and delete the rest
cd "$DEST_DIR"
ls -t backup_*.tar.gz | tail -n +$((RETENTION_COUNT + 1)) | xargs -r rm -f
ls -t *.sha256 | tail -n +$((RETENTION_COUNT + 1)) | xargs -r rm -f

echo "[$(date)] Rotation complete. Retention set to $RETENTION_COUNT." >> "$LOG_FILE"
```

### Administrative Guidelines for Deployment:

1.  **Permissions:** Ensure the script is owned by `root` and is not writable by any other user.
    *   `chown root:root secure_backup.sh`
    *   `chmod 700 secure_backup.sh`
2.  **Execution:** Run this via `root`'s crontab to ensure it has the necessary read permissions for the source directory.
    *   `sudo crontab -e`
    *   Add: `0 2 * * * /usr/local/bin/secure_backup.sh` (Runs daily at 2:00 AM).
3.  **Integrity Verification:** To verify a backup manually, run:
    *   `sha256sum -c backup_YYYYMMDD_HHMMSS.tar.gz.sha256`
4.  **Security Hardening:**
    *   **Off-site storage:** The `DEST_DIR` should ideally be a mounted network share or an encrypted cloud bucket to prevent local hardware failure from destroying the backups.
    *   **Encryption:** If the data is sensitive, add a `gpg -c` command to the tar pipeline to encrypt the archive before it hits the disk.
    *   **Log Integrity:** Consider shipping the `LOG_FILE` to a remote syslog server to prevent an attacker from modifying the logs to hide unauthorized access or backup tampering.


# Clear Constraints Prompt

* The script utilizes `rsync` for efficient data transfer, `sha256sum` for integrity verification, and `find` to enforce the retention policy by deleting directories older than the specified limit.
* It performs strict argument validation and checks for the existence of the source directory before proceeding with the backup process.
* All actions, including errors and checksum results, are logged to a file named `backup.log` in the destination directory.

```bash
#!/bin/bash

# Check for exactly 3 arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <source> <destination> <retention_limit_days>"
    exit 1
fi

SOURCE="$1"
DEST_BASE="$2"
RETENTION="$3"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_PATH="$DEST_BASE/backup_$TIMESTAMP"
LOG_FILE="$DEST_BASE/backup.log"

# Check if source exists
if [ ! -d "$SOURCE" ]; then
    echo "Error: Source directory $SOURCE does not exist."
    exit 1
fi

# Create destination if not exists
mkdir -p "$DEST_BASE"

{
    echo "--- Backup started at $(date) ---"
    
    # Perform backup
    rsync -av "$SOURCE/" "$BACKUP_PATH/"
    
    # Generate checksum
    find "$BACKUP_PATH" -type f -exec sha256sum {} + > "$BACKUP_PATH/checksum.sha256"
    echo "Checksum generated."

    # Manage retention
    find "$DEST_BASE" -maxdepth 1 -type d -name "backup_*" -mtime +"$RETENTION" -exec rm -rf {} +
    echo "Retention policy applied (older than $RETENTION days removed)."
    
    echo "--- Backup completed at $(date) ---"
} >> "$LOG_FILE" 2>&1
```