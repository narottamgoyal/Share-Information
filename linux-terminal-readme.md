# Linux Termial Commands

## VM Info

### Check Ubuntu version
```
lsb_release -a
```

### Check Ubuntu type x86 or x64
```
uname -m
```

### Get Hostname
```
hostname
```

### Get IP

```
hostname -I
```

or

```
ip addr show | grep inet

ip addr show (or ip a): The most modern and preferred method to view the IP address.

ifconfig: An older method (deprecated) but still available on some systems.

hostname -I: A quick and simple method to display the IP address.

nmcli device show: Useful on systems that use NetworkManager.
```

## Check Active Ports

```
sudo lsof -i -P -n | grep LISTEN
```

```
sudo netstat -tuln | grep dotnet
```

## Check Active Proces

### Find Process
```
ps aux | grep unattended-upgr
```

### Kill all the proces(seprated by space)
```
sudo kill -9 693 6415
```

## Locate files and folder in Terminal

### Change folder location to Downloads
```
cd ~/Downloads
```

### Current folder location in terminal
```
pwd
```

> If above command will take you to /root
> To go complete outside of this root folder then

```
ls /
```

### Open Folder from terminal location

```
xdg-open .
```

To any enter location is Terminal
```
xdg-open /home/ngoyal/MyWorkspace/MyApp
```

## File Operation

### Print all files and folders in Terminal
```
dir
dir -l

ls
ls -l // with details

Color:
    Blue: Folder
    Green: Executable files
    Red: .zip, .tar or .gz file types
    Magenta: Image file types
    Gray or White: Normal files
```

### Open any file in terminal text editor

```
sudo nano /<folder_path>/<file_name_.extension>
```

```
sudo nano /etc/mongod.conf

press CTRL + X to exit, then press Y to confirm saving changes, and Enter to save.
```

### Delete File

```
sudo rm /etc/filename
```

### Delete Directory

```
sudo rm -r /etc/directory_name
```

### Copy File

```
sudo cp /etc/mongod.conf /home/ngoyal/MyWorkspace/MyApp/
```

```
sudo cp /home/ngoyal/MyWorkspace/MyApp/mongod.conf /etc/
```

### Copy Directory

```
sudo cp -r /home/ngoyal/MyWorkspace/MyApp/package/app-apis /opt/app-apis/
```

### Move (Cut & Paste) File or Directory

```
sudo mv /home/ngoyal/app-apis /opt/app-apis
```

### Rename File

```
sudo mv /etc/old_filename /etc/new_filename
```

```
sudo mv /etc/mongod.conf.bak.29122024-153742 /etc/mongod.conf
```

### Check file exists

```
[ -e /path/to/your/file ] && echo "true" || echo "false"
```

## Make the script executable

```
chmod +x path/script.sh
```

## View Logs

### Systemd service logs

```
sudo journalctl -u serviceName.service -e
```

# Convert the script's line endings from Windows format (CRLF) to Unix format (LF)
> Error: bash: ./setup.sh: /bin/bash^M: bad interpreter: No such file or directory
In Windows, the line endings are typically \r\n (carriage return + line feed), while in Linux, the line endings are just \n (line feed). The ^M character you see in the error (/bin/bash^M) is the carriage return (\r) that is not valid in Linux environments.

To fix this issue, you need to convert the script's line endings from Windows format (CRLF) to Unix format (LF).
```
sed -i 's/\r//' setup.sh
```

## Seacrh text in all the files from a specific folder

```
grep -r '<text>' /etc/nginx/
```


## Suggested Directory Structure

```
/opt/myapp-backend/       # Backend app code (e.g., Node.js, Python, etc.)
/var/www/myapp/           # Frontend web files (HTML, CSS, JS)
/etc/myapp/               # App configuration files (e.g., .env, config.json)
/var/log/myapp/           # Logs for the web app
/opt/myapp-backend/venv   # Python virtual environment (if applicable)
```
