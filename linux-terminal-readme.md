# Linux Termial Commands

### Check Ubuntu version
```
lsb_release -a
```

### Check Ubuntu type x86 or x64
```
uname -m
```

### Current folder location in termail
```
pwd
```

### Change folder location to Downloads
```
cd ~/Downloads
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