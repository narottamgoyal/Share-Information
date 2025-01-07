# Install dotnet core 8 sdk
Update Package Index: Ensure your package index is up-to-date by running
```
sudo apt-get update
```
Install .NET 8 SDK: Execute the following command to install the .NET 8 SDK
```
sudo apt-get install -y dotnet-sdk-8.0
```
Verify Installation
```
dotnet --version
```

# Note : If process is blocked by some another process

Find Process
```
ps aux | grep unattended-upgr
```
Kill all the proces(seprated by space)
```
sudo kill -9 693 6415
```

# Install dotnet core 8 Runtime Only
Update Package Index: Ensure your package index is up-to-date by running
```
sudo apt-get update
```
Install the .NET Runtime
```
sudo apt-get install -y dotnet-runtime-8.0
```

ASP.NET Core Runtime for web apps
```
sudo apt-get install -y aspnetcore-runtime-8.0
```

Verify Installation
```
dotnet --info
```

# Test

```
dotnet App.API.dll
```

```
dotnet App.API.dll --urls "http://0.0.0.0:8080"
```

```
dotnet App.API.dll --urls "http://localhost:8080"
```