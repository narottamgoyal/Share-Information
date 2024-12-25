# Export multiple collections

```
$database = "db-1"
$collections = @("collection-2", "collection-2")

foreach ($collection in $collections) {
    Write-Host "Dumping $collection..."
    mongodump --username "adminUser" --password "securePassword" --authenticationDatabase "admin" --db=$database --collection=$collection --out C:\Users\NAROT\AppData\Local\Temp\db\exportedData\backup --gzip
}
```

# Export in JSON Format

```
mongoexport --username "adminUser" --password "securePassword" --authenticationDatabase "admin" --db GMJD-Develop-Phase-1 --collection User --out C:\Users\NAROT\AppData\Local\Temp\db\exportedData\json\User.json --jsonArray
```

# Export as mongodump

```
mongodump --username "adminUser" --password "securePassword" --authenticationDatabase "admin" --db GMJD-Develop-Phase-1 --collection User --out C:\Users\NAROT\AppData\Local\Temp\db\exportedData\backup --gzip
```