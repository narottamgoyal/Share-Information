# Useful Regex

### Select all text which are under double quotes
    "([^"]*)"

### Select all text except which are under double quotes
    [^"]+(?=(?:[^"]*"[^"]*")*[^"]*$)
