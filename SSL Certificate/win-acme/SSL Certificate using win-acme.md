# Request for SSL cerificate using ACME exe

## Prerequisite

- Download it from [www.win-acme.com](https://www.win-acme.com) or [win-acme.v2.2.9.1701.x64.pluggable.zip](https://github.com/win-acme/win-acme/releases)
- Run the above exe in Admin mode

## Steps

> C:\win-acme>wacs.exe

```
 A simple Windows ACMEv2 client (WACS)
 Software version 2.2.9.1701 (release, pluggable, standalone, 64-bit)
 Connecting to https://acme-v02.api.letsencrypt.org/...
 Connection OK!
 Scheduled task not configured yet
 Please report issues at https://github.com/win-acme/win-acme

 N: Create certificate (default settings)
 M: Create certificate (full options)
 R: Run renewals (0 currently due)
 A: Manage renewals (0 total)
 O: More options...
 Q: Quit
```

> Please choose from the menu: **m**

```
Running in mode: Interactive, Advanced

Please specify how the list of domain names that will be included in the
certificate should be determined. If you choose for one of the "all bindings"
options, the list will automatically be updated for future renewals to
reflect the bindings at that time.

1: Read bindings from IIS
2: Manual input
3: CSR created by another program
C: Abort
```

> How shall we determine the domain(s) to include in the certificate?: **2**

```
Description: A host name to get a certificate for. This may be a
comma-separated list.

Host: testadminapi.domain.com

Source generated using plugin Manual: testadminapi.domain.com
```

> Friendly name '[Manual] testadminapi.domain.com'. <Enter> to accept or type desired name: **testadmin**

```
By default your source identifiers are covered by a single certificate. But
if you want to avoid the 100 domain limit, want to prevent information
disclosure via the SAN list, and/or reduce the operational impact of a single
validation failure, you may choose to convert one source into multiple
certificates, using different strategies.

1: Separate certificate for each domain (e.g. \*.example.com)
2: Separate certificate for each host (e.g. sub.example.com)
3: Separate certificate for each IIS site
4: Single certificate
C: Abort
```

> Would you like to split this source into multiple certificates?: **2**

```
The ACME server will need to verify that you are the owner of the domain
names that you are requesting the certificate for. This happens both during
initial setup _and_ for every future renewal. There are two main methods of
doing so: answering specific http requests (http-01) or create specific dns
records (dns-01). For wildcard identifiers the latter is the only option.
Various additional plugins are available from
https://github.com/win-acme/win-acme/.

1: [http] Save verification files on (network) path
2: [http] Serve verification files from memory
3: [http] Upload verification files via FTP(S)
4: [http] Upload verification files via SSH-FTP
5: [http] Upload verification files via WebDav
6: [dns] Create verification records manually (auto-renew not possible)
7: [dns] Create verification records with acme-dns (https://github.com/joohoi/acme-dns)
8: [dns] Create verification records with your own script
9: [tls-alpn] Answer TLS verification request from win-acme
C: Abort
```

> How would you like prove ownership for the domain(s)?: **6**

```
After ownership of the domain(s) has been proven, we will create a
Certificate Signing Request (CSR) to obtain the actual certificate. The CSR
determines properties of the certificate like which (type of) key to use. If
you are not sure what to pick here, RSA is the safe default.

1: Elliptic Curve key
2: RSA key
C: Abort
```

> What kind of private key should be used for the certificate?: **2**

```
When we have the certificate, you can store in one or more ways to make it
accessible to your applications. The Windows Certificate Store is the default
location for IIS (unless you are managing a cluster of them).

1: IIS Central Certificate Store (.pfx per host)
2: PEM encoded files (Apache, nginx, etc.)
3: PFX archive
4: Windows Certificate Store (Local Computer)
5: No (additional) store steps
```

> How would you like to store the certificate?: **4**

```
1: [WebHosting] - Dedicated store for IIS
2: [My] - General computer store (for Exchange/RDS)
3: [Default] - Use global default, currently WebHosting
```

> Choose store to use, or type the name of another unlisted store: **3**

```
1: IIS Central Certificate Store (.pfx per host)
2: PEM encoded files (Apache, nginx, etc.)
3: PFX archive
4: Windows Certificate Store (Local Computer)
5: No (additional) store steps
```

> Would you like to store it in another way too?: **5**

```
With the certificate saved to the store(s) of your choice, you may choose one
or more steps to update your applications, e.g. to configure the new
thumbprint, or to update bindings.

1: Create or update bindings in IIS
2: Start external script or program
3: No (additional) installation steps
```

> Which installation step should run first?: **3**

```
Plugin Manual generated source testadminapi.domain.com with 1 identifiers
Plugin Host created 1 order
Cached order has status pending, discarding
[testadminapi.domain.com] Authorizing...
[testadminapi.domain.com] Authorizing using dns-01 validation (Manual)

Domain: testadminapi.domain.com
Record: \_acme-challenge.testadminapi.domain.com
Type: TXT
Content: "-ixfrkdz3dZefYm_OHCdROHcNCVcFt5QyXtWsuSpvtw"
Note: Some DNS managers add quotes automatically. A single set
is needed.
```

> Please press <Enter> after you've created and verified the record

![create-txt-record](../1.png)

```
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers

The correct record has not yet been found by the local resolver. That means
it's likely the validation attempt will fail, or your DNS provider needs a
little more time to publish and synchronize the changes.

1: Retry check
2: Ignore and continue
3: Abort

How would you like to proceed?: 1

[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers

The correct record has not yet been found by the local resolver. That means
it's likely the validation attempt will fail, or your DNS provider needs a
little more time to publish and synchronize the changes.

1: Retry check
2: Ignore and continue
3: Abort

How would you like to proceed?: 1
```

```
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers

The correct record has not yet been found by the local resolver. That means
it's likely the validation attempt will fail, or your DNS provider needs a
little more time to publish and synchronize the changes.

1: Retry check
2: Ignore and continue
3: Abort
```

> How would you like to proceed?: **2**

```
[testadminapi.domain.com] Record -ixfrkdz3dZefYm_OHCdROHcNCVcFt5QyXtWsuSpvtw successfully created
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers
[testadminapi.domain.com] Will retry in 30 seconds (retry 1/10)...
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers
[testadminapi.domain.com] Will retry in 30 seconds (retry 2/10)...
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers
[testadminapi.domain.com] Will retry in 30 seconds (retry 3/10)...
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers
[testadminapi.domain.com] Will retry in 30 seconds (retry 4/10)...
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers
[testadminapi.domain.com] Will retry in 30 seconds (retry 5/10)...
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers
[testadminapi.domain.com] Will retry in 30 seconds (retry 6/10)...
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers
[testadminapi.domain.com] Will retry in 30 seconds (retry 7/10)...
[testadminapi.domain.com][173.201.75.28] No TXT records found
[testadminapi.domain.com] Preliminary validation failed on 1/2 nameservers
[testadminapi.domain.com] Will retry in 30 seconds (retry 8/10)...
[testadminapi.domain.com] Preliminary validation succeeded
[testadminapi.domain.com] Authorization result: valid

Domain: testadminapi.domain.com
Record: \_acme-challenge.testadminapi.domain.com
Type: TXT
Content: "-ixfrkdz3dZefYm_OHCdROHcNCVcFt5QyXtWsuSpvtw"
```

> Please press <Enter> after you've deleted the record

```
[testadminapi.domain.com] Record -ixfrkdz3dZefYm_OHCdROHcNCVcFt5QyXtWsuSpvtw deleted
Downloading certificate testadmin [testadminapi.domain.com]
Store with CertificateStore...
Installing certificate in the certificate store
Adding certificate testadmin [testadminapi.domain.com] @ 2024/6/2 in store WebHosting
Adding Task Scheduler entry with the following settings

- Name win-acme renew (acme-v02.api.letsencrypt.org)
- Path C:\win-acme
- Command wacs.exe --renew --baseuri "https://acme-v02.api.letsencrypt.org/"
- Start at 09:00:00
- Random delay 04:00:00
- Time limit 02:00:00
```

> Do you want to specify the user the task will run as? (y/n\*) - **yes**

> Enter the username (Domain\username): narottamgoyal

```
Enter the user's password: **\*\***
Failed to create task
Adding renewal for testadmin
Next renewal due after 2024/7/26
Certificate testadmin created
```

```
N: Create certificate (default settings)
M: Create certificate (full options)
R: Run renewals (0 currently due)
A: Manage renewals (1 total)
O: More options...
Q: Quit

```

# Renew

    N: Create certificate (default settings)
    M: Create certificate (full options)
    R: Run renewals (0 currently due)
    A: Manage renewals (1 total, 1 in error)
    O: More options...
    Q: Quit

> Please choose from the menu: **A**

    Welcome to the renewal manager. Actions selected in the menu below will be
    applied to the following list of renewals. You may filter the list to target
    your action at a more specific set of renewals, or sort it to make it easier
    to find what you're looking for.

    1: testadmin - 1 renewal, due 2024/7/26, 2 errors

    E: Edit renewal
    D: Show details for the renewal
    L: Show command line for the renewal
    R: Run the renewal
    S: Run the renewal (force)
    T: Run the renewal (force, no cache)
    U: Analyze duplicates for the renewal
    C: Cancel the renewal
    V: Revoke certificate(s) for the renewal
    Q: Back

> Choose an action or type numbers to select renewals: **S** (not T, its for fresh new process)

    Plugin Manual generated source testadminapi.domain.com with 1 identifiers
    Plugin Host created 1 order
    Force renewing testadmin
    Using cache for testadmin [testadminapi.domain.com]. To get a new certificate within 1 days, run with --nocache.
    Store with CertificateStore...
    Installing certificate in the certificate store
    Adding certificate testadmin [testadminapi.domain.com] @ 2024/6/26 in store WebHosting
    Adding certificate CN=R10, O=Let's Encrypt, C=US in store CA
    Next renewal due after 2024/8/20
    Renewal for testadmin succeeded

    Welcome to the renewal manager. Actions selected in the menu below will be
    applied to the following list of renewals. You may filter the list to target
    your action at a more specific set of renewals, or sort it to make it easier
    to find what you're looking for.

> 1: testadmin - 2 renewals, due 2024/8/20

### Next Expiry Date - 2024/12/24

# Find certificate in windows store

Steps:

- Win + R > mmc
- File > Add/Remove Snap-in
- Certificates > Computer account > Local computer
- Certificates > Web Hosting > Certificates
