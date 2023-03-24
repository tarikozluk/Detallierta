# Detallierta
Detailed Alert API Service for Phone and Mail 

#How to Create a Windows Service for Python Environment

First of all we must download a NSSM package from the link: [NSSM Packages](https://nssm.cc/download)

Unzip the file and go to win32 or 64 folders according to the computer's settings

``` nssm install <service_name>```

A GUI will be created where you must specify python exe, startup directory and arguments. This part is just like setting the action part while scheduling the task.

``` nssm start <service_name>``` or ```sc start <service_name>```

### Setup for future updates
Clone the repository and create a .env file at the destination path.

1. zabbix credentials and url
2. NS(Citrix) credentials and url
3. Elasticsearch environment credentials
4. bot token or smtp credentials or which one you want. You can customize them according to your own environment.
