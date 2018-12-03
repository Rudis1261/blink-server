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

Something along the lines of:
```bluetooth.btcommon.BluetoothError: (2, 'No such file or directory'```

```shell
# https://stackoverflow.com/a/46810116
# Adding compatibility mode to the service will help start it

sudo vim /etc/systemd/system/dbus-org.bluez.service

# Find the line with the `ExecStart` and replace it  with
ExecStart=/usr/lib/bluetooth/bluetoothd -C

# And complete the action with the following commands
sudo sdptool add SP
systemctl daemon-reload
sudo service bluetooth restart
```

You should be able to check the status to confirm that it now uses to `/usr/lib/bluetooth/bluetoothd -C` by running this command:
```shell
sudo service bluetooth status
```

### OTHER KNOWN ISSUES

Pyhon3:
Unfortunately pybluez does not work properly on Python3, it was meant to be part of Python itself, but wasn't ported properly. For now the server **will only work on Python2.7**.
