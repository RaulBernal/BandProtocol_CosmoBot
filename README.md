# mon_band_oracles.py & config_band.py
Simple Bot to monitorize Band chain and Oracles services and reporters

**You need for running this script:**
* To have a Bot created in Telegram with @BotFather and a valid API KEY
* Linux system with a fullnode/masternode running and synced
* Python3 and pip3 installed 
* Botogram
* Set your config at file config_band.py (Token and route to binaries)

# Step-by-step guide:

**1) Create your own Bot in Telegram**

You can find the official Telegram instructions right here:
https://core.telegram.org/bots#6-botfather

**2) The linux masternode/fullnode side**

Download the script mon_band_oracles.py and config_band.py

When you run the script mon_band_oracles.py the first time it indicates that you need the Botogram library

$ python3 mon_band_oracles.py
Traceback (most recent call last):
  File "mon_band_oracles.py", line 4, in <module>
    import botogram
ImportError: No module named 'botogram'

The easy way is:

* $ sudo apt-get install python3-pip
* $ sudo pip3 install botogram2
* $ sudo pip3 install pexpect #another module to install

If the last command fails, you can check this info:

* You can install botogram following this instructions:
https://github.com/python-botogram/botogram

* You can easily install it with pip (if needed) following this instructions:
https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3


Change your own setting, edit with nano or vi:  nano band_config.py 
* You must change the path to the binaries
* Must also replace your API Token 


Execute it!!!

$ python3 mon_band_oracles.py

12:49.27 -   INFO    - Your bot is now running!
12:49.27 -   INFO    - Press Ctrl+C to exit.

**3) Search the bot in Telegram (use the @alias) and /start it**
Type /help for receive all commands descriptions
Type /subscribe to receive alerts when ORACLES are down or node is UNSYNCED
