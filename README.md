# CloudFlareUpdater
Updates CloudFlare hosts based on your current IP address.

## Requirements
The following requirements must be met:
* python3
* requests library for python3 (install using pip)

## Usage
Configure your domains in config.py and run it using the following command:

```bash
./updater.py
```

It is advised to install a cronjob to run this command to make sure the CloudFlare configuration is always up to date.
