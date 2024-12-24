$database = "db-1"
$collections = @("collection-2", "collection-2")

foreach ($collection in $collections) {
    Write-Host "Dumping $collection..."
    mongodump --username "adminUser" --password "securePassword" --authenticationDatabase "admin" --db=$database --collection=$collection --out C:\Users\NAROT\AppData\Local\Temp\db\exportedData\backup --gzip
}