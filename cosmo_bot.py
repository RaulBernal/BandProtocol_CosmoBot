#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import os
import botogram
import json

from config import token, path_to_daemon, path_to_cli, url_api, cosmos_address


bot = botogram.create(token)
bot.about = "CosmoBot for get info about chain. \nIf you found any bugs or have suggestions for new functionalities...\nPlease contact us!"
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
    get_last = os.popen(path_to_cli + ' query account ' + cosmos_address + ' -o json').read()
    loaded_json = json.loads(get_last)
    denom = loaded_json["value"]["coins"][0]["denom"]
    amount = loaded_json["value"]["coins"][0]["amount"]
    msg = 'You have ' + amount + ' ' + denom
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
@bot.command("getpeers")
def getpeers_command(chat, message, args):
    """This will show the online NODES (both)"""
    get_nodes = os.popen(path_to_bin + "/bitcanna-cli getpeerinfo").read()
    loaded_json = json.loads(get_nodes)
    msg = ""
    count = 0
    file_peers = os.path.join(path_to_bin + '/peers.txt') 
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

# This runs the bot, until ctrl+c is pressed
if __name__ == "__main__":
    bot.run()
