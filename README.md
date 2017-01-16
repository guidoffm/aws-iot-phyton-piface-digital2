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
- Make the py file runable by running `chmod +x garagentor.py`
- Make the shell script runable by running `chmod +x start_garagentor.sh`
- Run the Python script
- Open the AWS IoT console and go to `Test`
  - In `Subscribe to a topic` section enter `garage/inputs` or your changed topic
  - Press buttons on the PiFace Digital 2 board
  - You should see a new message for each button press and each button release
  - In the `Publish`section enter `garage/outputs` or your changed topic
  - For the body enter `{"isSet": true, "pin": 0}` and push the `Publish to topic` button.
  - You should hear one relay switching and one LED should light up
  - Use `{"isSet": false, "pin": 0}` to switch it off again

## To run the program as a Linux service
### Create a text file `/etc/systemd/system/garagentor.service` (with sudo or as root) with this contents:

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
### Enable the service (with sudo or as root)
`systemctl enable garagentor`

### Start the service (with sudo or as root)
`systemctl start garagentor`
