## Renew SSL Certificate

### Option 1

Below Command will give you option
```
sudo certbot certonly --force-renewal -d myapp.domain.com
```

Below command will renew certificate using nginx
```
sudo certbot certonly --force-renewal -d yourdomain.com --nginx
```

### Option 2 using TXT

Below command will ask you to enter domain name
```
sudo certbot certonly --manual --preferred-challenges dns
```

Or you can pass domain name as parameter
```
sudo certbot certonly --manual --preferred-challenges dns -d myapp.domain.com
```