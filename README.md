# aws-iot-phyton-piface-digital2

This project is for connecting a Raspberry Pi with Piface Digital 2 board to AWS IoT (Amazon Web Services Internet of Things).

To get this running for you:

- Create an AWS account if you don't alraeady have one
- Log in into AWS console: https://console.aws.amazon.com
- Go to "Internet of Things" => AWS
- Create a new "Thing"
- Have a client created for you using Linux and Python. Download client and expand the zip file.
- Replace the pem, key and crt files in the project with the files from your downloaded client
- Edit the py file and adjust these values:
  - host
  - certificatePath 
  - privateKeyPath 
- You may adjust the name sof the topics used for send and receive

## To run the program as a Linux service
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
`systemctl enable garagentor`
`systemctl start garagentor`
