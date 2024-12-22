# Enable authentication in mongo db

### Start MongoDB without Authentication

Comment security section in **mongod.cfg**

```
#security:
#  authorization: "enabled"
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

**or**

```
use admin
db.createUser({
  user: "superadmin",
  pwd: "password",
  roles: [{ role: "root", db: "admin" }]
})
```

>[!NOTE]
> `root` Role
>
> The root role is the superuser role in MongoDB.
>
> A user with the root role has complete control over the MongoDB deployment, including:
> * Managing users and roles (like userAdminAnyDatabase).
> * Reading and writing to any database (like readWriteAnyDatabase).
> * Performing administrative tasks on databases (like dbAdminAnyDatabase).
> * Managing the cluster infrastructure (like clusterAdmin).

### Enable Authentication

Stop the MongoDB server and start it again with the --auth option to enable authentication.

Alternatively, you can enable authentication through the MongoDB configuration file (mongod.conf).

Open your mongod.conf file.
Add or modify the security section to enable authorization.

```
security:
  authorization: "enabled"
```

# Connect with Authentication

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

## Forget the MongoDB admin password

You can reset it, but this process requires stopping the MongoDB server and restarting it in a special mode (--auth disabled) to reset the password. Or comment security section in **mongod.cfg**


### Alternative: Custom Role for Specific Database Patterns
If you need a more restricted yet flexible approach (e.g., access to many but not all databases), you can create a custom role that applies to multiple databases matching specific criteria.

```
use admin
db.createRole({
  role: "customReadWriteRole",
  privileges: [
    { resource: { db: "db-b", collection: "" }, actions: ["readWrite"] },
    { resource: { db: "db-c", collection: "" }, actions: ["readWrite"] },
    // Add more databases here if needed
  ],
  roles: []
})

db.createUser({
  user: "a",
  pwd: "password_a",
  roles: [
    { role: "customReadWriteRole", db: "admin" }
  ]
})
```

# Connection string

## Single Node

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

## Replica Set
```
mongodb://<username>:<password>@<host1>:<port1>,<host2>:<port2>,<host3>:<port3>/<database>?replicaSet=<replicaSetName>&authSource=<admin_or_specificDb>
```

### Single Member Connection
```
mongodb://<username>:<password>@<primaryHost>:<primaryPort>/<database>?replicaSet=<replicaSetName>&authSource=<admin_or_specificDb>
```

### Full Replica Set Connection
```
mongodb://<username>:<password>@<host1>:<port1>,<host2>:<port2>,<host3>:<port3>/<database>?replicaSet=<replicaSetName>&authSource=<admin_or_specificDb>
```

### C# Example
```
mongodb://X:password@host1:27017,host2:27017,host3:27017?replicaSet=rs0&readPreference=primaryPreferred&w=majority&authSource=admin_or_specificDb
```

```
var connectionString = "mongodb://X:password@host1:27017,host2:27017,host3:27017?replicaSet=rs0&readPreference=primaryPreferred&w=majority";
var client = new MongoClient(connectionString);

// Specify the database to work with
var database = client.GetDatabase("demo-db");  // Operations will happen on demo-db

// Perform operations (e.g., read/write)
var collection = database.GetCollection<BsonDocument>("myCollection");
collection.InsertOne(new BsonDocument { { "name", "John" }, { "age", 30 } });
```


## Robo 3t

![Robo-3t](./mongo-auth/robo-3t-1.png)

![Robo-3t](./mongo-auth/robo-3t-2.png)

## Studio 3t

![Studio-3t](./mongo-auth/Studio-3t-1.png)

![Studio-3t](./mongo-auth/Studio-3t-2.png)
