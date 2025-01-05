#!/bin/bash

# Set the MongoDB connection parameters (adjust these as needed)
MONGO_HOST="localhost"         # Hostname or IP address of the MongoDB instance
MONGO_PORT="27017"             # Port where MongoDB is running
MONGO_USER="adminUser"   # MongoDB username (optional if authentication is required)
MONGO_PASS="securePassword"   # MongoDB password (optional if authentication is required)

# Define the two databases and their backup options
DB1_NAME="test"
DB1_BACKUP_ALL=true           # Set to true to backup entire DB1, false for specific collections
DB1_COLLECTIONS=("collection1" "collection2")  # List of collections to backup if DB1_BACKUP_ALL=false

DB2_NAME="GMJD-Catalogs"
DB2_BACKUP_ALL=true          # Set to true to backup entire DB2, false for specific collections
DB2_COLLECTIONS=("collection3" "collection4")  # List of collections to backup if DB2_BACKUP_ALL=false

# Date and Time format (YYYY-MM-DD_HH-MM-SS)
DATE=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_DIR="/home/ngoyal/ExportAppDb/backup/$DATE"

# Create a backup directory
mkdir -p "$BACKUP_DIR"

# Backup Database 1
if [ "$DB1_BACKUP_ALL" = true ]; then
  echo "Backing up entire database: $DB1_NAME"
  mongodump --host "$MONGO_HOST" --port "$MONGO_PORT" --username "$MONGO_USER" --password "$MONGO_PASS" --authenticationDatabase "admin" \
            --db "$DB1_NAME" --out "$BACKUP_DIR"
else
  echo "Backing up specific collections for $DB1_NAME: ${DB1_COLLECTIONS[@]}"
  for COLLECTION in "${DB1_COLLECTIONS[@]}"; do
    mongodump --host "$MONGO_HOST" --port "$MONGO_PORT" --username "$MONGO_USER" --password "$MONGO_PASS" --authenticationDatabase "admin" \
              --db "$DB1_NAME" --collection "$COLLECTION" --out "$BACKUP_DIR"
  done
fi

# Backup Database 2
if [ "$DB2_BACKUP_ALL" = true ]; then
  echo "Backing up entire database: $DB2_NAME"
  mongodump --host "$MONGO_HOST" --port "$MONGO_PORT" --username "$MONGO_USER" --password "$MONGO_PASS" --authenticationDatabase "admin" \
            --db "$DB2_NAME" --out "$BACKUP_DIR"
else
  echo "Backing up specific collections for $DB2_NAME: ${DB2_COLLECTIONS[@]}"
  for COLLECTION in "${DB2_COLLECTIONS[@]}"; do
    mongodump --host "$MONGO_HOST" --port "$MONGO_PORT" --username "$MONGO_USER" --password "$MONGO_PASS" --authenticationDatabase "admin" \
              --db "$DB2_NAME" --collection "$COLLECTION" --out "$BACKUP_DIR"
  done
fi

echo "Backup completed and stored in $BACKUP_DIR"

