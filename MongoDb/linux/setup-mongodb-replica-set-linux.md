
# Configure MongoDB for Replica Set in linux VM

## Setup Primary Node

1. Create `security.keyFile`
    ```
    sudo bash -c "openssl rand -base64 756 > /etc/mongo-keyfile"
    ```

    Set Correct Permissions: Adjust the permissions for the keyfile to make it secure and accessible only to MongoDB:

    ```
    sudo chown mongodb:mongodb /etc/mongo-keyfile
    sudo chmod 400 /etc/mongo-keyfile
    ```

2. Edit the MongoDB Configuration File
    ```
    sudo nano /etc/mongod.conf
    ```

    Add or Modify the replication Section
    ```
    security:
      keyFile: /etc/mongo-keyfile
      authorization: "enabled"


    replication:
      replSetName: "rs0"
    ```

    Restart MongoDB: Apply the changes by restarting the MongoDB service
    ```
    sudo systemctl restart mongod
    ```

3. Initialize the Replica Set
    ```
    use admin
    db.auth("adminUser","securePassword")
    rs.initiate()
    rs.status()
    ```

4. (Optional) Add Additional Members

    4.1. Add Secondary node IP
    ```
    rs.add("<secondary-ip>:27017")
    rs.conf()
    rs.status()
    ```
    4.2. Configure Firewall Rules
    Make sure the replica set members can communicate with each other on MongoDB's default port (27017):

    Allow MongoDB Traffic: Use ufw or a cloud firewall (if applicable) to allow traffic between the nodes:
    ```
    sudo ufw allow from <secondary-ip> to any port 27017
    sudo ufw allow from <primary-ip> to any port 27017
    ```

    4.3. Restart UFW: Apply the changes:
    ```
    sudo ufw reload
    ```

5. Verify Connectivity
    ```
    ping <primary-ip>
    ping <secondary-ip>
    ```

## Setup Secondary Node

1. Dont create new `security.keyFile`. All the nodes are suppose to have `security.keyFile` content.
2. There are 2 ways to copy `security.keyFile` from primary to secondary node.
   - Manually Copy
   - Automatically Copy

    2.1. Steps to Copy and Paste the Key File **manually**

    On the Primary VM: Open the key file and copy its contents
    ```
    sudo cat /etc/mongo-keyfile
    ```
    On the Secondary VM: Log into the secondary VM and create the key file:
    ```
    sudo nano /etc/mongo-keyfile
    ```
    ```
    Save the Key File:

    In the editor (e.g., nano),
    save the file:
    Press Ctrl + O,
    then Enter to save.
    Press Ctrl + X to exit.
    ```

    2.2. Steps to Copy and Paste the Key File **automatically**
    ```
    scp /etc/mongo-keyfile <secondary-user>@<secondary-ip>:/etc/mongo-keyfile
    ```
3. Set the Correct Permissions:
   Adjust the file ownership and permissions to meet MongoDB's requirements:
    ```
    sudo chown mongodb:mongodb /etc/mongo-keyfile
    sudo chmod 400 /etc/mongo-keyfile
    ```
4. Now repeat step number 2 from primary node
5. Goto Primary node, execute step number 4, Now its mandatory.
6. Now in secondary node, copy and execute only step number 4.2, 4.3, 5 from primary node
7. (Optional) Priority and Hidden Members using Mongo shell script
     - Set Node Priority: You can configure priority for each node to influence the election process. For instance, you might set the primary node's priority to 1 and the secondary node's priority to 0.5:
        ```
        cfg = rs.conf()
        cfg.members[1].priority = 0.5
        rs.reconfig(cfg)
        ```
     - Hidden or Delayed Secondary: If the secondary is meant for backups or analytics, you can make it hidden or delayed:
        ```
        cfg = rs.conf()
        cfg.members[1].hidden = true
        cfg.members[1].priority = 0
        rs.reconfig(cfg)
        ```

## Connection String

**Standalone instance**
```
mongodb://<username>:<password>@<host>:<port>?authSource=<authenticationDatabase>

mongodb://testUser:testPassword@192.168.0.105:27017?authSource=test
```

**Replica set**
```
mongodb://<username>:<password>@<host1>:<port1>,<host2>:<port2>,<host3>:<port3>?replicaSet=<replicaSetName>&authSource=<admin_or_specificDb>

mongodb://app_user:app_password@192.168.0.105:27017?replicaSet=rs0&readPreference=primaryPreferred&w=majority&authSource=admin
```

