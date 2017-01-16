# aws-iot-phyton-piface-digital2

Create a text file `/etc/systemd/system/garagentor.service` with this contents:

```
[Unit]
Description=garagentor

[Service]
Type=forking
ExecStart=/home/pi/garagentor/start_garagentor.sh
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```
