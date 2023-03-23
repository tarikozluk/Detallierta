import telebot
import os
from dotenv import load_dotenv
from pyzabbix import ZabbixAPI
from datetime import datetime, timedelta
from re import search
import pyodbc
import time
from pythonping import ping
import lb_regex
import ns_collector
###todo: NSSM CONF FOR PYTHON API SERVICE WILL BE ADDED LATER: DONE

load_dotenv()
Bot_Token = os.getenv("BOT_TOKEN")
Chat_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(Bot_Token)


@bot.message_handler(commands=['getLastValue'])
def send_lastvalue(message):
    try:
        zapi = ZabbixAPI(os.getenv("ZABBIX_URL"))
        zapi.login(os.getenv("ZABBIX_USERNAME"), os.getenv("ZABBIX_PASSWORD"))
        time_till = time.mktime(datetime.now().timetuple())
        time_from = time_till - 60 * 6 * 6  # last 8 days for now
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
    try:
        zapi = ZabbixAPI(os.getenv("ZABBIX_URL"))
        zapi.login(os.getenv("ZABBIX_USERNAME"), os.getenv("ZABBIX_PASSWORD"))
        time_till = time.mktime(datetime.now().timetuple())
        time_from = time_till - 60 * 6 * 6  # last 8 days for now
        responsible = message.text.split(" ")[1]
        print(responsible)
        problems = zapi.problem.get(selectTags="extend",
                                    time_from=time_from,
                                    severities=["1", "2", "3", "4", "5"],
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
            try:
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
            except:
                bot.send_message(chat_id=Chat_ID, text="Son Değer Bulunamadı")

    except:
        bot.send_message(chat_id=Chat_ID, text="Lütfen Sorumlu Ekibi giriniz. Örnek: /getAlarms ResponsibleTeam")




@bot.message_handler(commands=['Help', 'help'])
def send_hello_by_cron(message):
    bot.send_message(chat_id=Chat_ID, text="Uygulama Yönetimi Ekibinin yardımsever botuna hoş geldiniz. \nKomutlar ve örnek kullanımları aşağıdaki gibidir.\nEkiplerin mevcut alarmlarını görmek için /getalarms <Responsible>\nSon Değerleri görmek için /getLastValue <alarm id>\nPing atmak için /ping <site adı>\n/learnlbname <lb>\n/learnservers <correct_lb>")

@bot.message_handler(commands=['ping', 'Ping'])
def send_ping(message):
    try:
        ping_adress = message.text.split(" ")[1]
        ping_response = ping(str(ping_adress), verbose=False, count=1, size=1, interval=1,timeout=10)
        ping_text = str(ping_response)
        start_index = ping_text.find("from ") + len("from ")
        end_index = ping_text.find(",", start_index)
        ip_address = ping_text[start_index:end_index]
        bot.send_message(chat_id=Chat_ID, text=ping_text+"\n"+ip_address)
    except:
        bot.send_message(chat_id=Chat_ID, text="Hata")


@bot.message_handler(commands=['Learnlbname', 'learnlbname'])
def CorrectLB_fromLB(message):
    try:
        target_LB= message.text.split(" ")[1]
        lb_expand_name = lb_regex.lb_name_finder(target_LB)
        bot.send_message(chat_id=Chat_ID, text=lb_expand_name)

    except:
        bot.send_message(chat_id=Chat_ID, text="LB'de Hata bulundu. Lütfen LB'yi kontrol ediniz veya komutu doğru yazınız\n Komut: /learnservers <LB>")

@bot.message_handler(commands=['learnservers', 'Learnservers'])
def servernames_fromLB(message):
    try:
        target_servers = message.text.split(" ")[1]
        servers_expand_name = ns_collector.getServersfromNS(target_servers)

        bot.send_message(chat_id=Chat_ID, text=servers_expand_name)
    except:
        bot.send_message(chat_id=Chat_ID, text="LB'de Hata bulundu. Lütfen LB'yi kontrol ediniz veya komutu doğru yazınız\n Komut: /learnservers <LB>")
if __name__ == '__main__':

    bot.polling(
        none_stop=True,
        interval=0,
        timeout=20
    )

