from flask import Flask, request, abort
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import pprint
import json

# Load Config
with open('configs.json', 'r') as f:
    configs = json.load(f)

# Silence Logging
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)

@app.route('/', methods=['POST'])
def accept_webhook():
    # Gather Request Information
    data = request.get_json(force=True)
    ip_address = request.environ['REMOTE_ADDR']
    user_agent = request.user_agent.string
    # Seperate Webhook Types, Account Only
    for types in data:
        type = types.get('type')
        message = types.get('message')
        if type == 'account':
            print(str(datetime.now()) + " [ACCOUNT-BOT] Account Event From " + user_agent + " At " + ip_address)
            #pprint.pprint(message)
            build_webhookstring(message)
    # Send OK Response
    return "OK"

def build_webhookstring(message):
    # Gather Information
    username = message.get('username')
    level = message.get('level')
    group = message.get('group')
    firstWarningTimestamp = message.get('first_warning_timestamp')
    if firstWarningTimestamp and firstWarningTimestamp > 0:
        firstWarningTimestamp = datetime.fromtimestamp(firstWarningTimestamp)
    failedTimestamp = message.get('failed_timestamp')
    if failedTimestamp and failedTimestamp > 0:
        failedTimestamp = datetime.fromtimestamp(failedTimestamp)
    failed = message.get('failed')
    lastEncounterTime = message.get('last_encounter_time')
    if lastEncounterTime and lastEncounterTime > 0:
        lastEncounterTime = datetime.fromtimestamp(lastEncounterTime)
    creationTimestampMs = message.get('creation_timestamp')
    if creationTimestampMs and creationTimestampMs > 0:
        creationTimestampMs = datetime.fromtimestamp(creationTimestampMs)
    lastUsedTimestamp = message.get('last_used_timestamp')
    if lastUsedTimestamp and lastUsedTimestamp > 0:
        lastUsedTimestamp = datetime.fromtimestamp(lastUsedTimestamp)
    spins = message.get('spins')
    warn = message.get('warn')
    warnExpireMs = message.get('warn_expire_timestamp')
    if warnExpireMs and warnExpireMs > 0:
        warnExpireMs = datetime.fromtimestamp(warnExpireMs)
    warnMessageAcknowledged = message.get('warn_message_acknowledged')
    wasSuspended = message.get('was_suspended')
    suspendedMessageAcknowledged = message.get('suspended_message_acknowledged')
    banned = message.get('banned')
    print(str(datetime.now()) + " [ACCOUNT-BOT] Account Information: " + str(username) + " " + str(level) + " " + str(group) + " " + str(failed))
    # Build Webhook
    webhookString = 'Username: ' + username + \
                    '\nLevel: ' + str(level) + \
                    '\nGroup: ' + str(group) + \
                    '\nCreation: ' + str(creationTimestampMs) + \
                    '\nLastEncounter: ' + str(lastEncounterTime) + \
                    '\nLastUsed: ' + str(lastUsedTimestamp) + \
                    '\nSpins: ' + str(spins) + \
                    '\nFirst Warning: ' + str(firstWarningTimestamp) + \
                    '\nFailed: ' + str(failedTimestamp) + \
                    '\nStatus: ' + str(failed) + \
                    '\nWarning: ' + str(warn) + \
                    '\nWarning Expire: ' + str(warnExpireMs) + \
                    '\nWarning Clicked: ' + str(warnMessageAcknowledged) + \
                    '\nWas Suspended: ' + str(wasSuspended) + \
                    '\nSuspended Clicked: ' + str(suspendedMessageAcknowledged) + \
                    '\nBanned: ' + str(banned)
    #print('[ACCOUNT-BOT] \n' + webhookString)
    # Debug Fire All Account Hooks
    #fire_webhook(webhookString, group)
    # Check Conditions
    if warn == True or banned == True or failed != 'None':
        print(str(datetime.now()) + " [ACCOUNT-BOT] \n" + webhookString)
        fire_webhook(webhookString, group, level)

def fire_webhook(webhookString, group, level):
    if group == 'LEVEL':
        webhookMention = DiscordWebhook(url=configs['AccountBot']['webhookURLLevel'], content=configs['AccountBot']['discordMentionLevel'])
        webhookEmbed = DiscordWebhook(configs['AccountBot']['webhookURLLevel'])
        embed = DiscordEmbed(title='Level Account Issue', description=webhookString, color=configs['AccountBot']['color'])
        embed.set_timestamp()
        webhookEmbed.add_embed(embed)
    elif level == 40:
        webhookMention = DiscordWebhook(url=configs['AccountBot']['webhookURLLevel'], content=configs['AccountBot']['discordMentionLevel'])
        webhookEmbed = DiscordWebhook(url=configs['AccountBot']['webhookURLLevel'])
        embed = DiscordEmbed(title='LEVEL 40 ACCOUNT REMOVE', description=webhookString, color=configs['AccountBot']['color'])
        embed.set_timestamp()
        webhookEmbed.add_embed(embed)
    else:
        webhookMention = DiscordWebhook(url=configs['AccountBot']['webhookURL'], content=configs['AccountBot']['discordMention'])
        webhookEmbed = DiscordWebhook(url=configs['AccountBot']['webhookURL'])
        embed = DiscordEmbed(title='Account Issue', description=webhookString, color=configs['AccountBot']['color'])
        embed.set_timestamp()
        webhookEmbed.add_embed(embed)
    response = webhookMention.execute()
    response = webhookEmbed.execute()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4000', debug = True)
