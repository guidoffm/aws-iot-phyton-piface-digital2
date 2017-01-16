# aws-iot-phyton-piface-digital2

```
cat /etc/systemd/system/garagentor.service
```
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
