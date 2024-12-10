## Copy Message Body to property

    ${in.body}

## Copy data to property

    ${property.p_Quote_Header}

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
not(//root/*)
```