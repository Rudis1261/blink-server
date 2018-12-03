# Blink Server
### Bluetooth Linux Remote for Android devices

Where you want to be able to control your Linux Computer, and Wifi is not an option. This is something I wrote, because nothing else on the market seemed to work. This is the server you would need to be able to run the Blink Android Application. 

## ANDROID APP INSTALLATION

https://play.google.com/store/apps/details?id=co.za.thatguy.blink

## SERVER INSTALLATION

**REQUIRES PYTHON2.7 TO WORK**

Install the server with the following commands in your terminal. 

#### Installation on Debian Based Systems (Ubuntu, Kubuntu, Debian etc)
``` 
sudo apt-get install bluez python-bluez xdotool
```
```
git clone https://github.com/drpain/blink-server.git ~/.blink
```

#### Installation on Fedora Based Systems (Fedora, Centos)
```
sudo yum install bluez pybluez
```
```
git clone https://github.com/drpain/blink-server.git ~/.blink
```

#### Installation on Arch Based Systems (Arch, Manjaro)
```
yaourt pybluez xdotool
```
```
git clone https://github.com/drpain/blink-server.git ~/.blink
```
You also need to add --compat as described below.

## STARTING SERVER

Then to start the server, all you need to do is run the server with the following command from your terminal. As long as the server runs, you will be able to send commands to it. 

```
sudo ~/.blink/bluetooth_server.py
```

## HELP

The hardest part of this is getting the server installed and running. If you struggle to get the bluetooth to work, maybe this will help:

*This guide helped me allot, original post: [Bluetooth Setup](http://blog.davidvassallo.me/2014/05/11/android-linux-raspberry-pi-bluetooth-communication/)*
> There are plenty of guides in the internet on how to get bluetooth working, but the only method that worked consistently for me is the following:
> Disable bluetooth pnat support as there seems to be a bug which stops proper operation with pnat enabled. Full details can be found here:  
> https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=690749

> A workaround is to add the following to /etc/bluetooth/main.conf:
```
DisablePlugins = pnat
```


### Permissions Issues:
This has been reported as helpfull for sorting out permissions issues on Ubuntu 15.10. Thanks @jachym for providing the link:
https://code.google.com/p/pybluez/issues/detail?id=62

```shell
# TLDR
# Adding the --compat to the bluetooth server configuration. And restarting the bluetooth service
# SYSTEM D systems like REHL addopted it first, but now Ubuntu 15 also has
# List of OS's running SYSTEM D
# https://en.wikipedia.org/wiki/Systemd

sudo vim /usr/lib/systemd/system/bluetooth.service

# change this: ExecStart=/usr/libexec/bluetooth/bluetoothd
# to this: ExecStart=/usr/libexec/bluetooth/bluetoothd --compat
# Restart the bluetooth service
sudo service bluetooth restart

# Check that it has changed by running 
sudo service bluetooth status | grep -i --compat
```


### OTHER KNOWN ISSUES

I will try and document the known issues and fixes as they arise. 

Fedora 22 error:

```
File "/usr/lib64/python2.7/site-packages/bluetooth/bluez.py", line 176, in advertise_service
  raise BluetoothError (str (e))
bluetooth.btcommon.BluetoothError: (2, 'No such file or directory')
```

Fedora 22 Fix:
https://thatguy.co.za/Blog/Article/python-bluez-issues-since-upgrading-to-fedora-22

Pyhon3:
Unfortunately pybluez does not work properly on Python3, it was meant to be part of Python itself, but wasn't ported properly. For now the server **will only work on Python2.7**.
