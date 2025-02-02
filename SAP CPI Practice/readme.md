## Read Message Body

    ${in.body}

## Read property

    ${property.p_nameOrSomething}

## Set Data type in property

```
java.lang.Integer
```

```
java.lang.String
```

```
java.lang.Object
```

```
org.w3c.dom.Document
```

## Loop Index

    ${property.CamelLoopIndex}

## Route Condion:

Property should be not null and empty

```
${property.CRTErrorMessage} != null and ${property.CRTErrorMessage} != ''
Property can be null or empty
```

```
${property.skipRecordID} = '' or ${property.skipRecordID} = null
```

```
${property.aa} = 'aa' or ${property.aa} = 'bb'
```

```
${property.aa.toLowerCase()} = 'true'
```

```
not(//root/*)
```
