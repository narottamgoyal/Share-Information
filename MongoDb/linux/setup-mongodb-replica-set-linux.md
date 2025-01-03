
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

## Remove secondary node (Execute from primary node)
```
use admin
rs.status()
rs.remove('127.0.0.1:27020')

rs.status()
use local
db.system.replset.remove({})
db.replset.election.drop()
db.replset.minvalid.drop()
```

# Run secondary instance in the existing running ubuntu VM

Create a New Data Directory
```
sudo mkdir -p /data/mongo3
```

Make sure the permissions are correct
```
sudo chown -R mongodb:mongodb /data/mongo3
```

Start MongoDB on Port 27020
```
sudo mongod --dbpath /data/mongo3 --port 27020 --fork --logpath /var/log/mongodb/mongo3.log
```

Start MongoDB on Port 27020, with replica set (make sure replSet name is same as your primary replica name)
```
sudo mongod --dbpath /data/mongo3 --port 27020 --fork --logpath /var/log/mongodb/mongo3.log --replSet rs0
```

Check if the New Instance is Running
```
ps aux | grep mongod
```
> output

This instance is running on id `6882`
```
ngoyal@ngoyal-VirtualBox:~/MyWorkspace/MyApp$ ps aux | grep mongod

root        6882  0.9  3.6 3705432 144420 ?      Sl   21:07   0:04 mongod --dbpath /data/mongo3 --port 27020 --fork --logpath /var/log/mongodb/mongo3.log

mongodb     7127  2.5  4.9 2935520 198272 ?      Ssl  21:12   0:05 /usr/bin/mongod --config /etc/mongod.conf

ngoyal      7278  0.0  0.0   9080  2432 pts/4    S+   21:15   0:00 grep --color=auto mongod
```

Connect to the New Instance
```
mongosh --port 27020
```

initiate replica set if required
```
rs.initiate()
```

Kill this secondary instance
```
sudo kill 6882
```

Stop the process more forcefully
```
sudo kill -9 6882
```

Now connect to primary mongodb node
```
mongosh
use admin
rs.add({ host: "127.0.0.1:27020", priority: 0, votes: 0 })
rs.status()
```

