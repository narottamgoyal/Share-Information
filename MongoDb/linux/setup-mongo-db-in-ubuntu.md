# Setup mongo db in Ubuntu Linux VM

1. [Download Mongo Server](https://www.mongodb.com/try/download/community)
   - Select later version - 8.0.4
   - Plateform - Ubuntu 22.04 x64
     - Find the right plateform
        ```
        lsb_release -a
        ```
        ```
        uname -m
        ```
   - Package - Server
   - Download (downloaded file name: mongodb-org-server_8.0.4_amd64.deb)
2. Open Terminal
   - Goto downloads folder path
        ```
        cd ~/Downloads
        ```
   - Install
        ```
        sudo dpkg -i mongodb-org-server_8.0.4_amd64.deb
        ```
3. Verify
   - Start MongoDB: If MongoDB isn't already running, start the service using
        ```
        sudo systemctl start mongod
        ```
   - Enable MongoDB to Start on Boot: To make sure MongoDB starts automatically when your system reboots, run
        ```
        sudo systemctl enable mongod
        ```
   - Verify MongoDB is Running: You can verify MongoDB is running by checking its status
        ```
        sudo systemctl status mongod
        ```

# Install MongoDB Shell in linux Terminal
-  Check if MongoDB Shell (mongosh) is Installed
    ```
    which mongosh
    ```
-  Download the .deb package for mongosh (replace the version with the latest)
    ```
    wget https://downloads.mongodb.com/compass/mongodb-mongosh_1.10.0_amd64.deb
    ```
-  Install the .deb package
    ```
    sudo dpkg -i mongodb-mongosh_1.10.0_amd64.deb
    ```
-  Install missing dependencies (if any)
    ```
    sudo apt --fix-broken install
    ```
-  Verify Installation
    ```
    mongosh
    ```
-  Show all existing DB names
    ```
    show dbs
    ```

# Install mongodump
- Check if MongoDB Tools are Installed
     ```
     mongodump --version
     ```
- Install MongoDB Database Tools
     ```
     wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo tee /etc/apt/trusted.gpg.d/mongodb.asc
     echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
     ```

     ```
     sudo apt update
     sudo apt install mongodb-database-tools
     mongodump --version
     ```
- Update Path (if needed)
     ```
     export PATH=$PATH:/path/to/mongodb/bin
     ```

# Stop & Restart the MongoDB Service
   - Status
        ```
        sudo systemctl status mongod
        ```
   - Stop
        ```
        sudo systemctl stop mongod
        ```
   - Start
        ```
        sudo systemctl start mongod
        ```
   - Restart
        ```
        sudo systemctl restart mongod
        ```

# Remove MongoDB
   - Stop the MongoDB Service
        ```
        sudo systemctl stop mongod
        ```
   - Remove Mongo Org Packages
        ```
        sudo apt-get purge mongodb-org*
        ```
   - Remove Other MongoDB Packages (if you installed specific components like mongodb-org-server or mongodb-org-tools):
        ```
        sudo apt-get remove --purge mongodb*
        ```
   - Remove Configuration Files and Databases (Optional)
        ```
        sudo rm -r /var/lib/mongodb
        sudo rm -r /var/log/mongodb
        sudo rm -r /etc/mongod.conf /etc/mongodb.conf
        ```
   - Verify Uninstallation
        ```
        mongod --version
        ```
   - Clean Up Unused Dependencies (Optional)
        ```
        sudo apt-get autoremove
        ```


# MongoDB is Bound to localhost Only (Below steps are only for testing)
By default, MongoDB binds to localhost (127.0.0.1) for security reasons. To allow external access:

Open the MongoDB configuration file

```
sudo nano /etc/mongod.conf
```

Look for the bindIp parameter and ensure it includes the VM's IP address (or 0.0.0.0 for all interfaces)

```
net:
  bindIp: 127.0.0.1,133.133.3.133 (your VM IP)
```
Restart mongo db
```
sudo systemctl restart mongod
```