# Enable authentication in mongo db

- Locate and Open mongod.cfg (or mongod.conf)
    ```
    sudo nano /etc/mongod.conf
    ```
- Comment Authorization if its enabled or not disabled
    ```
    #security:
    #authorization: "enabled"
    ```
- Save and Close the File (press CTRL + X to exit, then press Y to confirm saving changes, and Enter to save.)
- Restart MongoDB
    ```
    sudo systemctl restart mongod
    ```
- Connent to mongo shell via `mongosh`
    ```
    mongosh
    ```
- Create an Administrative User

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

- Create Additional Users in a **specific database**

    Select specific database

    ```
    use test (TestDb)
    db.createUser({
    user: "testUser",
    pwd: "testPassword",
    roles: [{ role: "readWrite", db: "test" }]
    })
    ```