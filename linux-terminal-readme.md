# Linux Termial Commands

### Check Ubuntu version
```
lsb_release -a
```

### Check Ubuntu type x86 or x64
```
uname -m
```

### Change folder location to Downloads
```
cd ~/Downloads
```

### Current folder location in termail
```
pwd
```

### Open Folder from terminal

Current Terminal location
```
xdg-open .
```

To any enter location is Terminal
```
xdg-open /home/ngoyal/MyWorkspace/MyApp
```

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

### Get hostname
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

### Make the script executable

```
chmod +x path/script.sh
```

### Rename file
sudo mv /etc/old_filename /etc/new_filename

```
sudo mv /etc/mongod.conf.bak.29122024-153742 /etc/mongod.conf
```

### Delete file or directory
```
sudo rm /etc/filename
```
```
sudo rm -r /etc/directory_name
```
```
sudo rm /etc/mongod.conf
```

### Copy file or directory from /etc to /home

```
sudo cp /etc/mongod.conf /home/ngoyal/MyWorkspace/MyApp/
```

```
sudo cp /home/ngoyal/MyWorkspace/MyApp/mongod.conf /etc/
```

```
sudo cp -r /home/ngoyal/MyWorkspace/MyApp/package/app-apis /opt/app-apis/
```

### Move file or directory

```
sudo mv /home/ngoyal/app-apis /opt/app-apis
```

### Check file exists
```
[ -e /path/to/your/file ] && echo "true" || echo "false"
```

### Check Active Ports on the VM

```
sudo lsof -i -P -n | grep LISTEN
```

```
sudo netstat -tuln | grep dotnet
```

### View systemd service logs

```
sudo journalctl -u serviceName.service -e
```