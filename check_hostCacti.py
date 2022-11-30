import mysql.connector
import time
import datetime

t1 = time.time()
db_cacti = mysql.connector.connect(host="10.1.0.27",user="admin",password="1qaz2wsx",database="cacti")
fetch_db = db_cacti.cursor()

db_automation = mysql.connector.connect(host="127.0.0.1",user="admin",password="1qaz2wsx",database="automation")
exec_command = db_automation.cursor()

#db_nms2 = mysql.connector.connect(host="192.168.71.29",user="admin",password="htvnms",database="htv",port=3306)
#insert_db = db_nms2.cursor()

timenow = datetime.datetime.now()
date = timenow.strftime("%d-%m-%Y")
date_yf = timenow.strftime("%Y-%m-%d")
time_now = timenow.strftime("%X")
#For fetch Mysql snmptt
time_format_snmp = timenow.strftime("%a %b %-d %-H:%-M:")
#-----------------------------------------------------------------------------------------------------------------------------------------------#
time_stamp = date + " " + time_now

# Time for cal
time_day_text = timenow.strftime("%a")
time_month_text = timenow.strftime("%b")
time_day_number = timenow.strftime("%-d")
time_h = timenow.strftime("%-H")
time_m = timenow.strftime("%M")
time_s = timenow.strftime("%-S")
now_5min = datetime.datetime.now() - datetime.timedelta(minutes=5)
day_text = now_5min.strftime("%a")
month_text = now_5min.strftime("%b")
day_number = now_5min.strftime("%-d")
time_h_2 = now_5min.strftime("%H")
time_m_2 = now_5min.strftime("%M")
time_s_2 = now_5min.strftime("%-S")
m_int = int(time_m_2)
d_int = int(day_number)

def insert_Notify(_get1,_get2):
    for _name,_ip in zip(_get1,_get2):
        exec_command.execute(f"insert into line_notify (display,host_ip,code,update_time) values ('{_name}','{_ip}','Up',now());")
        db_automation.commit()

def host_down():
    fetch_db.execute(f"select description2,hostname from host where disabled!='on' and status='1';")
    print(fetch_db.statement)
    name_list = []            
    host_list = []
    for firsh_fetch in fetch_db:
        get_name = firsh_fetch[0]
        get_host = firsh_fetch[1]
        name_list.append(get_name)
        host_list.append(get_host)
    return name_list,host_list

hd = host_down()
dp1 = hd[0]
dp2 = hd[1]

def deviceDown():
    fetch_db.execute(f"select description,hostname from deviceDown where status = '000';")
    print(fetch_db.statement)
    name_list = []
    host_list = []
    for firsh_fetch in fetch_db:
        get_name = firsh_fetch[0]
        get_host = firsh_fetch[1]
        name_list.append(get_name)
        host_list.append(get_host)
    return name_list,host_list

chd = deviceDown()
dp3 = chd[0]
dp4 = chd[1]

def insert_down(name,host):
    fetch_db.execute(f"insert into deviceDown (description,hostname,deviceState,create_time) values ('{name}','{host}','Down',now());")
    print(fetch_db.statement)
    db_cacti.commit()
    0

def enable(get):
    for hostname in get:
        fetch_db.execute(f"update deviceDown set up_time = now(), status = '001' where hostname = '{hostname}' and status = '000';")
        print(fetch_db.statement)
        db_cacti.commit()
        0

def check_online(list1,list2):
    list_check = [list_in for list_in in list1 + list2 if list_in not in list1 or list_in not in list2]
    return list_check

def get_hd(name,ip):
    for z,x in zip (name,ip): insert_down(z,x)
    0


len_hd = len(dp2)
len_chd = len(dp4)

print(f"Cacti_HostDown : {len_hd}")
print(f"Keep_HostDown : {len_chd}")

if len_hd == 0:
    enable(dp4)
    insert_Notify(dp3,dp4)
elif len_hd != len_chd and len_hd < len_chd:
    _name = check_online(dp1,dp3)
    _ip = check_online(dp2,dp4)
    enable(_ip)
    insert_Notify(_name,_ip)
    print(_name)
    print(_ip)
    
elif len_hd != len_chd:
    _name = check_online(dp1,dp3)
    _ip = check_online(dp2,dp4)
    get_hd(_name,_ip)
    print(_name)
    print(_ip)
else:
    pass

t2 = time.time() - t1
print(f"{t2:0.2f}")

db_cacti.close()
db_automation.close()
