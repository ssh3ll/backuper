# backuper
backuper is a simple Python script which allows to perform backups of your preferred files and directories.
Even though the script has been developed for working on Mac OS X and some Linux distributions, like Ubuntu and Linux Mint, with the proper changes it can work on Windows as well. Actually, the tool relies on several command line utilities such as sudo and chown, but they will be removed in the future.


If you've ever had to compress several files/directories, sometimes same files in different locations, backuper may be the tool that fit your needs. ZIP and GZIP are supported and more will be implemented.

### Installation

The installation is pretty easy to do. In order to install the script as a command line utility, which will be available to any other user on the same machine and that has proper privileges, is sufficient to run the installation script as depicted below.

Note that this may require a password.

```
python installer.py
```


### Remove the tool
Run the uninstall script as described below. Also this one may require a password.

```
./uninstall.sh
```


### Examples

- manual backup into your Desktop
```
backuper -add /path/to/your/files
backuper -ad /path_to_Desktop
backuper -y
```


- schedule the script to run every hour -- using cron
```
 echo "0 */3 * * * /usr/local/bin/backuper -y" |crontab -
```

- anacron every day
```
1	0	bckp	/usr/local/bin/backuper -y
```
