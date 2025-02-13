# mongo-query-example

## Generate _id as string object Id

```
 [BsonId(IdGenerator = typeof(StringObjectIdGenerator))]
 public string Id { get; set; }
```

# Create a collection ("EmployeeDetail") and insert sample records

```
{ "Name" : "A", "Mobile" : "123" , "Salary" : 100 , "Department":[{"Name":"D1"}]}
{ "Name" : "B", "Mobile" : "456" , "Salary" : 200 , "Department":[{"Name":"D1"},{"Name":"D2"}], "Age" : 28}
{ "Name" : "C", "Mobile" : "789" , "Salary" : 300 , "Department":[{"Name":"D1"},{"Name":"D2"},{"Name":"D3"}]}
{ "Name" : "D", "Mobile" : "123" , "Salary" : 400 , "Department":null}
{ "Name" : "E", "Mobile" : "456" , "Salary" : 500 , "Department":[]}
```

# Search document wwhere _id ends with
```
db.getCollection("SupportTicket").find({ "_id": { $regex: /b2879c7ed3$/ } });
```

# Search document where _id matching with substring of id
```
db.yourCollectionName.find({ "_id": { $regex: "b2879c7ed3$" } });
```

```
var idEndingPattern = "b2879c7ed3";
db.yourCollectionName.find({ "_id": { $regex: idEndingPattern + "$" } });
```

# Project limited property / field

// Include only the "version" and "email" fields
```
db.getCollection("User").find({}, { emailId: 1, version: 1 })
```

// Exclude the "password" field
```
db.getCollection("User").find({}, { password: 0 })
```

# Foreach

```
db.getCollection('EmployeeDetail').find({}).forEach(function (record) {
  print("Name: " + record.Name)
});
```

```
// to avoid timeout use "noCursorTimeout" method when db has lots & lots of records
db.getCollection('EmployeeDetail').find({}).noCursorTimeout().forEach(function (record) {
  print("Name: " + record.Name)
})
```

# Convert objectId to string Id

```
db.getCollection('EmployeeDetail').find({}).forEach(function (record) {
  var objectId = record._id;
  record._id = record._id.toString();
  if (typeof objectId === 'object') {
    // duplicate same record with string type id
    db.getCollection('EmployeeDetail').insert(record);
    // remove old record with object type id
    db.getCollection('EmployeeDetail').remove({
      _id: objectId
    });
    print("Name: " + record._id)
  }
})
```

# Group example

```
db.getCollection('EmployeeDetail').aggregate(
  [{
    $group: {
      // group by field name Mobile
      _id: "$Mobile",
      count: {
        $sum: 1
      }
    }
  }, {
    $match: {
      count: {
        $gt: 1
      }
    }
  }]
);
```

```
db.getCollection('EmployeeDetail').aggregate(
  [{
    $group: {
      // group by field name Mobile
      _id: "$Mobile",
      // return additional field information of Name, Salary
      Name: {
        $addToSet: "$Name"
      },
      Salary: {
        $addToSet: "$Salary"
      },
      count: {
        $sum: 1
      }
    }
  }, {
    $match: {
      count: {
        $gt: 1
      }
    }
  }]
);
```

# Remove rows based on some duplicate field values

```
db.getCollection('EmployeeDetail').find({}, {
  "Mobile": 1
}).sort({
  _id: 1
}).forEach(function (record) {
  db.getCollection('EmployeeDetail').remove({
    _id: {
      $gt: record._id
    },
    "Mobile": record.Mobile
  });
});
```

# Operators

```
// Return all where Salary is greater than 200
db.getCollection('EmployeeDetail').find({
  "Salary": {
    $gt: 200
  }
})
```

```
// Return all where Salary is greater than and equal to 200
db.getCollection('EmployeeDetail').find({
  "Salary": {
    $gte: 200
  }
})
```

```
// Return all where Salary is less than 200
db.getCollection('EmployeeDetail').find({
  "Salary": {
    $lt: 200
  }
})
```

```
// Return all where Salary is less than and equal to 200
db.getCollection('EmployeeDetail').find({
  "Salary": {
    $lte: 200
  }
})
```

```
// Return all where Department Name is not equal to D1
db.getCollection('EmployeeDetail').find({
  "Department.Name": {
    $ne: "D1"
  }
})
```

# Add Index

```
db.getCollection('EmployeeDetail').createIndex({
  Name: 1
})
```

# Add new field to any array

```
db.yourCollection.update(
  {},
  {
    $set: {
      "subNames.$[].field": 'value'
    }
  },
  {
    multi: true
  }
)
```

# Rename Field

```
db.getCollection('EmployeeDetail').updateMany(
   {},
   { $rename: { "oldFieldName": "newFieldName" } }
)
```

# Update Row

```
// Add or update field
db.getCollection('EmployeeDetail').update({
  "Name": "A"
}, {
  $set: {
    Age: NumberInt(18)
  }
}, {
  upsert: false,
  multi: true
})
```

```
// Remove field
db.getCollection('EmployeeDetail').update({
  "Mobile": "123"
}, {
  $unset: {
    Age: 1
  }
}, {
  upsert: false,
  multi: true
})

//upsert: If set to true, creates a new document when no document matches the query criteria. The default value is false
// multi:	If set to true, updates multiple documents that meet the query criteria. If set to false, updates one document. The default value is false
```

# Sort Rows

```
// Sort all the rows
db.getCollection('EmployeeDetail').find({}).sort({
  $natural: -1
})
```

```
// Sort by salary field
db.getCollection('EmployeeDetail').find({}).sort({
  "Salary": 1
})
```

# Array Queries

```
// Return all where Department Name is D5
db.getCollection('EmployeeDetail').find({
  "Department.Name": "D5"
})
```

```
// Return all where Department field is null
db.getCollection('EmployeeDetail').find({
  Department: null
})
```

```
// Return all where Department array size is 0
db.getCollection('EmployeeDetail').find({
  Department: {
    $size: 0
  }
});
```

```
// filter example
db.getCollection('EmployeeDetail').find({}).forEach(function (record) {
  if (record.Department != null) {
    var dept = record.Department.filter(function (de) {
      return de.Name !== "D2";
    });

    print("old array length:" + record.Department.length + ", New length" + dept.length);
    record.Department = dept;

    db.getCollection('EmployeeDetail').replaceOne({
      _id: record._id
    }, record);
  } else {
    // do something else
  }
  print("Name: " + record.Name)
});
```

# Some basic query examples

```
// field exists or not
db.getCollection('EmployeeDetail').find({
  "Age": {
    $exists: false
  }
})
```

```
// count example
var count = db.getCollection('EmployeeDetail').find({}).count();
if (count == 0) {
  print("No Record");
} else {
  print("Record count:" + count);
}

```

```
// skip and limit example
db.getCollection('EmployeeDetail').find({}).skip(1).limit(2)
```

```
// How to deal with multiple mongodb collection
db.getMongo().getDB("MongoQueryDemo").getCollection('EmployeeDetail').find({})

```

# Update nested array or subarray of document

### Update specific item in subarray

```
db.getCollection("BidDetails").updateOne(
    { "_id" : "65ab327fda246cb73088b15a", "serviceProviderResponses.isQuoteAccepted": null }, 
    {
       "$set": { "serviceProviderResponses.$.isQuoteAccepted": true } 
    }
)
```

### Update all item of subarray

```
db.getCollection("BidDetails").updateOne(
    { "_id" : "65ab327fda246cb73088b15a", "serviceProviderResponses.isQuoteAccepted": null }, 
    {
       "$set": { "serviceProviderResponses.$[].isQuoteAccepted": true } 
    }
)
```

```
  var update = Builders<BidDetails>.Update
  .Set("serviceProviderResponses.$[].isQuoteAccepted", true);
```

### Create unique index but ignore null values
```
db.collectionName.createIndex(
   {houseName: 1},
   {unique: true, partialFilterExpression: {houseName: {$type: "string"}}}
);
```
