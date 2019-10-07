# Blink Server
### Bluetooth Linux Remote for Android devices

If you ever want to control your Linux computer from your Android phone and no other app seems to work fine (requires WiFi, is too expensive, has a lot of ads, or just simply doesn't work), then Blink might be the right app for you!

This repository contains the server-side code. Also see [the Android repo](https://github.com/drpain/blink) if you're interested in building or tweaking the app yourself.

**THIS SERVER REQUIRES PYTHON 2.7 AND DOES THUS NOT WORK ON PYTHON 3 YET**


## ANDROID APP INSTALLATION

Either get the app on the [PlayStore](https://play.google.com/store/apps/details?id=co.za.thatguy.blink) or build it yourself [from scratch](https://github.com/drpain/blink).

## SERVER INSTALLATION

### Dependencies
The blink-server needs bluez and its python bindings and xdotool in order to function. These can be installed in the following way:

#### Debian Based Systems (Ubuntu, Kubuntu, Debian, etc)
```shell
sudo apt install bluez python-bluez xdotool
```

#### Fedora Based Systems (Fedora, Centos, etc)
```shell
sudo yum install bluez pybluez
```

#### Arch Based Systems (Arch, Manjaro, etc)
```shell
yaourt python2-pybluez xdotool
# or if you use yay instead of yaourt:
yay -S python2-pybluez xdotool
```
If you run Arch, you will probably encounter the compat mode problem. See the FAQ mentioning **compat mode**.


### Cloning the repository
We advise you to install the server in /usr/local/src/blink/ and to make symlinks in /usr/local/bin/ in order to be able to run it easily:

```shell
sudo mkdir -m=777 /usr/local/src/blink-server
git clone https://github.com/drpain/blink-server.git /usr/local/src/blink-server
sudo ln -s /usr/local/src/blink-server/bluetooth_server.py /usr/local/bin/blink-server
```

## STARTING SERVER

Then to start the server, all you need to do is run the server with the following command from your terminal. As long as the server runs, you will be able to send commands to it. 

```shell
sudo blink_server
```

## HELP

The hardest part of this is getting the server installed and running. If you struggle to get the bluetooth to work, check these FAQ:

### I can't connect my phone to my laptop

From this [very useful guide](http://blog.davidvassallo.me/2014/05/11/android-linux-raspberry-pi-bluetooth-communication/):

> There are plenty of guides in the internet on how to get bluetooth working, but the only method that worked consistently for me is the following:
> Disable bluetooth pnat support as there seems to be a bug which stops proper operation with pnat enabled. Full details can be found here:  
> https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=690749

> A workaround is to add the following to /etc/bluetooth/main.conf:
```config
DisablePlugins = pnat
```


### `bluetooth.btcommon.BluetoothError: (2, 'No such file or directory')`
This is a known issue on Ubuntu 15.04 and up, where we'll have to run the bluetooth daemon in **compat mode**. Thanks @jachym for providing a link with the [solution](https://code.google.com/p/pybluez/issues/detail?id=62):

```shell
# Open the config file in your favorite editor
sudo vim /etc/systemd/system/dbus-org.bluez.service

# Find the line with the `ExecStart` and replace it with
ExecStart=/usr/lib/bluetooth/bluetoothd --compat

# Restart the bluetooth daemon
sudo sdptool add SP  # This command isn't necessary on Arch Linux
sudo systemctl daemon-reload  # Only needed if you use systemctl
sudo service bluetooth restart
```

You should be able to check the status to confirm that it now uses to `/usr/lib/bluetooth/bluetoothd -C` by running this command:
```shell
sudo service bluetooth status
```

### `ModuleNotFoundError: No module named 'commands'`

You probably tried running blink-server with Python 3. Because pybluez hasn't been ported as expected to Python 3, blink-server is still restricted to Python 2.7:

Try running `sudo python2 "$(which blink-server)"` instead of `sudo blink-server` to make sure the right version is used.

### `bluetooth.btcommon.BluetoothError: (13, 'Permission denied')`

You probably tried running blink-server without sudo. This is denied, since the process needs root permissions in order to communicate with the bluetooth socket.

Try running `sudo blink-server`
