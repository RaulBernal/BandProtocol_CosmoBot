#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import botogram #pip3 install botogram2
import json
import pexpect  #pip3 install pexpect before run the first time

from config_band import token, path_to_daemon, path_to_cli, url_api, band_address, bandvaloper_address, chain_id, priv_key, wallet_name, url_explorer


bot = botogram.create(token)
bot.about = "Mon_Band_Oracles for get info about Band chain. \nIf you found any bugs or have suggestions for new functionalities...\nPlease contact us!"
bot.owner = "Tips and bugs to: @D00hanPijo"
#==========================================================================
@bot.command("getblockcount")
def getblockcount_command(chat, message, args):
    """Check this to know if your fullnode-validator is synced"""
    get_block = os.popen(path_to_cli + 'status').read()
    loaded_json = json.loads(get_block)
   
    #gaiacli status | jq '.sync_info.latest_block_height'

    print("Result:", loaded_json['sync_info']['latest_block_height'])
    block = str(loaded_json['sync_info']['latest_block_height'])
    chat.send("The current Block is "+block)
#==========================================================================
@bot.command("getbalance")
def getlist_command(chat, message, args):
    """This will show the balance of your config address"""
    msg = ""
    get_last = os.popen(path_to_cli + 'query staking delegations ' + band_address + ' -o json | jq .[0].balance').read()
    loaded_json = json.loads(get_last)
    denom = loaded_json["denom"]
    amount = loaded_json["amount"]
    msg = 'You have ' + amount + denom
    chat.send(msg)
#==========================================================================
@bot.command("getvalidators")
def getmasternode_command(chat, message, args):
    """This will show the online VALIDATORS"""
    get_validators = os.popen(path_to_cli + ' query staking validators -o json').read()
    loaded_json = json.loads(get_validators)
    msg = ""
    count = 0
    chat.send ("List of online VALIDATORS") 
    print ("List of online VALIDATORS")
    print ("==========================")
    for tx in loaded_json:
        msg = msg + '*' + str(tx["description"]["moniker"]) + '* - Jailed: ' + str(tx["jailed"]) + '\n' 
        count = count + 1
    print (msg + "\nTotal: " + str(count))
    chat.send(msg + "\nTotal: " + str(count))
#==========================================================================
@bot.command("getyodastatus")
def getyodastatus_command(chat, message, args):
    """This will check status of ORACLES"""
    oracle_running =  os.popen(path_to_cli + 'query oracle validator ' + bandvaloper_address + ' -o json | jq .is_active').read()
    if oracle_running.find('true') == 0:
        chat.send("Hey! your ORACLES are running!")
    else:
        chat.send("Hey! your ORACLES are down!")
#==========================================================================
@bot.command("sendtxyoda")
def sendtxyoda_command(chat, message, args):
    """This will send a ACTIVATE tx for ORACLES"""
    command = path_to_cli + " tx oracle activate --from " + wallet_name + " --chain-id " + chain_id + " -y  -o json"
    child = pexpect.spawn(command) #command
    child.expect ("Enter keyring passphrase:") #input expected
    child.sendline (priv_key) #Send password
    child.expect ("Enter keyring passphrase:") #input expected
    child.sendline (priv_key) #Send password 
    child.interact() 
    chat.send ('TX sent. Check if is running \n/getyodastatus') 
#==========================================================================
@bot.command("explorer")  # sample to build a textfile and send it by telegram
def explorer_command(chat, message, args):
    chat.send ('Click at the URL: ' + url_explorer)

#==========================================================================
@bot.prepare_memory          #Automated actions
def init(shared):
    shared["subs"] = []

@bot.command("subscribe")
def subscribe_command(shared, chat, message, args):
    """Subscribe to the hourly daemon checking"""
    subs = shared["subs"]
    subs.append(chat.id)
    shared["subs"] = subs
    

@bot.timer(3600) #every hour
def checker(bot, shared):
    get_info = os.popen(path_to_cli + 'status | jq .sync_info.catching_up').read()
    if get_info.find('false') == 0: #if found false is synced
        print('Daemon is running')
    else:    
         for chat in shared["subs"]:
            bot.chat(chat).send("Hey! your BAND validator is down!")
         #something to do if is down
         #starting = os.popen(path_to_daemon + " start").read()
    get_power = os.popen(path_to_cli + 'status | jq .validator_info.voting_power').read()
    if get_power.find('"0"') == 0: #if found false is jailed
        print('Validator is JAILED!!!')
        for chat in shared["subs"]:
            bot.chat(chat).send("Hey! your BAND validator is down!")

    else:    
        print('Validator have got POWER')
    
    oracle_running =  os.popen(path_to_cli + 'query oracle validator ' + bandvaloper_address + ' -o json | jq .is_active').read()
    if oracle_running.find('true') == 0:
        print("Hey! your ORACLES are running!")
    else:
         for chat in shared["subs"]:
            bot.chat(chat).send("Hey! your ORACLES are down!")
         #to-do 
#==============================================================================

# This runs the bot, until ctrl+c is pressed
if __name__ == "__main__":
    bot.run()
    
