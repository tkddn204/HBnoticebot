virtualenv venv --distribute
source venv/bin/activate

pip install -r requirements.txt

sudo cp HBnoticebot.service /lib/systemd/system/HBnoticebot.service
sudo chmod 644 /lib/systemd/system/HBnoticebot.service
sudo systemctl daemon-reload
sudo systemctl enable HBnoticebot.service
sudo systemctl start HBnoticebot.service
sleep 3
sudo systemctl status HBnoticebot.service
