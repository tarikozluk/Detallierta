import telebot
import os
from dotenv import load_dotenv
from pyzabbix import ZabbixAPI
from datetime import datetime, timedelta
from re import search
import pyodbc
import time
from apscheduler.schedulers.blocking import BlockingScheduler


###todo: NSSM CONF FOR PYTHON API SERVICE WILL BE ADDED LATER
load_dotenv()
Bot_Token = os.getenv("BOT_TOKEN")
Chat_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(Bot_Token)
zapi = ZabbixAPI(os.getenv("ZABBIX_URL"))
zapi.login(os.getenv("ZABBIX_USERNAME"), os.getenv("ZABBIX_PASSWORD"))
time_till = time.mktime(datetime.now().timetuple())
time_from = time_till - 60 * 6 * 6  # last 8 days for now

@bot.message_handler(commands=['getLastValue'])
def send_lastvalue(message):
    try:
        trigger = message.text.split(" ")[1]
        items = zapi.item.get(
            output="extend",
            #triggerids="{}".format(trigger[0]['triggerid']),
            triggerids="{}".format(trigger),
            time_from=time_from,
            time_till=time_till,
            # search=[{"key_": "system.cpu.util[,idle]"},
            #        {"key_": "vm.memory.size[available]"}]
        )
        lastvalue = items[0]['lastvalue']
        print(lastvalue)
        bot.send_message(chat_id=Chat_ID, text="Son Değer: "+lastvalue)
    except:
        bot.send_message(chat_id=Chat_ID, text="Son Değer Bulunamadı")
@bot.message_handler(commands=['getAlarms', 'getalarms'])
def send_alarmhistory(message):
    responsible = message.text.split(" ")[1]
    print(responsible)


    problems = zapi.problem.get(selectTags="extend",
                                time_from=time_from,
                                severities=["1","2","3", "4", "5"],
                                tags=[{'tag': 'Responsible', 'value': '{}'.format(responsible)}],
                                # recent=["true", "false"],
                                recent="true",
                                time_till=time_till)
    print(problems)
    for problem in problems:
        trigger = zapi.trigger.get(triggerids=problem['objectid'], selectHosts='extend')
        interface = zapi.hostinterface.get(hostids=trigger[0]['hosts'][0]['hostid'])
        group = zapi.hostgroup.get(hostids=trigger[0]['hosts'][0]['hostid'])
        enabled = "Enabled"
        if trigger[0]['hosts'][0]['status'] == "1":
            enabled = "Disabled"
        timestamp = int(problem['clock'])
        dt_object = datetime.fromtimestamp(timestamp)

        resolvedtimestamp = int(problem['r_clock'])
        resolveddt_object = datetime.fromtimestamp(resolvedtimestamp)

        if problem['severity'] == "4":
            Status_Severity = "High"
        elif problem['severity'] == "3":
            Status_Severity = "Average"
        elif problem['severity'] == "5":
            Status_Severity = "Disaster"
        elif problem['severity'] == "2":
            Status_Severity = "Warning"
        elif problem['severity'] == "1":
            Status_Severity = "Information"

        if problem['r_clock'] == "0":

            if dt_object > datetime.now() - timedelta(hours=6):
                YollananVeri = (
                        u'\U0001F198\U0001F198\U0001F198\n' + "Alarm Tarihi: {} \nSeviye: {} \nHost Grubu: {}\nHost: {}\nIP: {}\nProblem: {}\n Son Deger icin: /getLastValue {}".format(
                    dt_object,
                    Status_Severity,
                    group[0]['name'],
                    trigger[0]['hosts'][0]['name'],
                    interface[0]['ip'],
                    problem['name'],
                    trigger[0]['triggerid']
                ))
                bot.send_message(chat_id=Chat_ID, text=YollananVeri)
    return trigger, interface, group, enabled, dt_object, resolveddt_object, Status_Severity, YollananVeri

def send_hello_by_cron():
    bot.send_message(chat_id=Chat_ID, text="Hello")

if __name__ == '__main__':

    bot.polling(
        none_stop=True,
        interval=0,
        timeout=20
    )

