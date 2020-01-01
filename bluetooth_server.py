#!/usr/bin/env python
import os
import time
from bluetooth import *
from core import *

# Change the PWD to this location
abspath = os.path.abspath(__file__)
dname   = os.path.dirname(abspath)
os.chdir(dname)

# BLUETOOTH SECTION
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "sinkServer",
                   service_id       = uuid,
                   service_classes  = [ uuid, SERIAL_PORT_CLASS ],
                   profiles         = [ SERIAL_PORT_PROFILE ]
)

print("READY FOR CONNECTIONS, RFCOMM channel %d" % port)

while True:
    client_sock, client_info = server_sock.accept()
    print("INBOUND CONNECTION ", client_info)
    try:
        while True:
            data = client_sock.recv(1024)
            if len(data) == 0: break

            print("COMMAND RECEIVED [%s]" % data)
            if data == "marco":
                client_sock.send("polo\n")
            else:
                commandKeys(data)
    except IOError:
        pass

    print("Bye bye")
    client_sock.close()

# Close the Socket
server_sock.close()
print("SELF-DESTRUCT COMPLETE")
