# Enable authentication in mongo db

### Start MongoDB without Authentication

Comment security section

```
#security:
```

or start MongoDB without the --auth option to create the first user.

```
mongod --dbpath /path/to/your/db
```

- Connect to MongoDB
  Use the mongo shell to connect to your MongoDB instance.

```
mongo
```

### Create an Administrative User

Switch to the admin database and create an administrative user.

```
use admin
db.createUser({
  user: "adminUser",
  pwd: "securePassword",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "clusterAdmin", db: "admin" }]
})
```

### Enable Authentication

Stop the MongoDB server and start it again with the --auth option to enable authentication.

Alternatively, you can enable authentication through the MongoDB configuration file (mongod.conf).

Open your mongod.conf file.
Add or modify the security section to enable authorization.

```
security:
  authorization: "enabled"
```

### Connect with Authentication

Reconnect to MongoDB and select admin db along with the newly created user.

```
use admin
db.auth("adminUser","securePassword")
```

- Granting Additional Roles to the **Admin User**, If required

```
use admin
db.grantRolesToUser("adminUser", [
  { role: "userAdminAnyDatabase", db: "admin" },
  { role: "readWriteAnyDatabase", db: "admin" },
  { role: "dbAdminAnyDatabase", db: "admin" },
  { role: "clusterAdmin", db: "admin" }
])
```

- Create Additional Users in a **specific database**

  List all dbs

```
show dbs
```

Select database

```
use TestDb
db.createUser({
  user: "yourUser",
  pwd: "yourPassword",
  roles: [{ role: "readWrite", db: "TestDb" }]
})
```

### View all or specific user

```
db.getUsers()
db.getUser("yourUser")
```

### Reset any user password

```
use TestDb
db.updateUser("yourUser", { pwd: "yourPassword1" })
```

### Delete any existing user

```
use TestDb
db.dropUser("userNameToDelete")
```

## Connection string

User Created in **admin** Database

```
mongodb://<username>:<password>@<host>:<port>/<database>?authSource=<authenticationDatabase>

mongo "mongodb://adminUser:securePassword@localhost:27017/myDatabase?authSource=admin"
```

User Created in Target Database

```
mongodb://<username>:<password>@<host>:<port>/<database>

mongodb://dbUser:dbPassword@localhost:27017/myDatabase
```

## Robo 3t

![Robo-3t](../mongo-auth/robo-3t-1.png)

![Robo-3t](../mongo-auth/robo-3t-2.png)

## Studio 3t

![Studio-3t](../mongo-auth/Studio-3t-1.png)

![Studio-3t](../mongo-auth/Studio-3t-2.png)
