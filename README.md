# CloudFlareUpdater
Updates CloudFlare hosts based on your current IP address.

## Requirements
The following requirements must be met:
* python3
* requests library for python3 (install using pip)

## Usage
Copy `config.py.example` to `config.py` and configure your domains in your copy.

Then in a terminal, run the following command in a terminal window:

```bash
/path/where/you/downloaded/updater.py
```

It is advised to install a cronjob to run this command to make sure the CloudFlare configuration is always up to date.
