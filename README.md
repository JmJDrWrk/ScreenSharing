ScreenSharing
I created this script because I needed to use a Raspberry Pi without a screen. By referencing this script in a Raspberry Pi OS service file, I can now see what's happening on the Pi whenever it turns on, as long as I know the IP address of the device.

Steps to Achieve the Same Setup
Copy Files: Copy your Python script to a known directory, along with the provided cursor.png image.

Install Dependencies: Ensure all necessary dependencies are installed. You can test the script by running python3 script.py to confirm it's working. If it doesn't run manually, it won't work automatically at startup.

Create the Service File: Open a terminal and create a new systemd service file:

bash
Copiar código
sudo nano /etc/systemd/system/screen_streamer.service
Add the Following Content:

ini
Copiar código
[Unit]
Description=Flask Screen Streaming Service
After=graphical.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/screen_streamer.py
WorkingDirectory=/home/pi
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi
Environment=DISPLAY=:0

[Install]
WantedBy=graphical.target
Enable and Start the Service:

bash
Copiar código
sudo systemctl enable screen_streamer.service
sudo systemctl start screen_streamer.service
sudo systemctl status screen_streamer.service
Check the Service Status: The status command should show something like "active". If you encounter issues, you can check the logs with:

bash
Copiar código
sudo journalctl -u screen_streamer.service -b
Testing
To verify it's working on the Raspberry Pi itself (if you have a screen connected), open a web browser and navigate to localhost:5000/screen. If nothing appears, the script may not be functioning properly.

Once confirmed to be working, you can reboot your system. Then, from another device on the same network, access the stream by entering the Raspberry Pi's IP address in a browser, followed by :5000/screen. For example:

bash
Copiar código
192.168.54.177:5000/screen
