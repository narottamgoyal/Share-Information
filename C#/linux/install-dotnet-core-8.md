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

## Create API Package
- Publish
  - Target Runtime: `linux-x64`
  - Deployment Mode: `Self-contained`
  - Configuration: `Release`
  - Target Framework: `.NET 8`

## Run API

```
dotnet App.API.dll
```

```
dotnet App.API.dll --urls "http://0.0.0.0:8080"
```

```
dotnet App.API.dll --urls "http://localhost:8080"
```