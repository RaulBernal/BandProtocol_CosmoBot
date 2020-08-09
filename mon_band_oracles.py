#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import botogram
import json

from config_band import token, path_to_daemon, path_to_cli, url_api, band_address, bandvaloper_address, chain_id


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
@bot.command("sendfile")  # sample to build a textfile and send it by telegram
def getpeers_command(chat, message, args):
    """This will show the online NODES (both)"""
    get_nodes = os.popen(path_to_cli + " status").read()
    loaded_json = json.loads(get_nodes)
    msg = ""
    count = 0
    file_peers = os.path.join(path_to_cli + '/peers.txt') 
    chat.send ("Building a list...") 
    print ("List of online NODES")
    print ("==========================")
    for tx in loaded_json:
        msg = msg + "IP: " +  tx["addr"] + ", version: " + tx["subver"] + "\n"
        count = count + 1 
    print (msg + "\nTotal: " + str(count))
    with open(file_peers, 'w') as f:
        f.write(msg+ "\nTotal: " + str(count))
    chat.send_file(path=file_peers, caption='This file contains all peers connected to your masternode/fullnode')
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
    oracle_running =  os.popen(path_to_cli + 'query oracle validator' + bandvaloper_address + ' -o json | jq .is_active').read()
    if oracle_running == "true":
        print("Hey! your ORACLES are running!")
    else:
         for chat in shared["subs"]:
            bot.chat(chat).send("Hey! your BAND validator is down!")
         #to-do 
#==============================================================================

# This runs the bot, until ctrl+c is pressed
if __name__ == "__main__":
    bot.run()
    
