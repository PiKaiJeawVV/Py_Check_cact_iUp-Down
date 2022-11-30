import mysql.connector

db_cacti = mysql.connector.connect(host="10.1.0.27",user="admin",password="1qaz2wsx",database="cacti")
fetch_db = db_cacti.cursor()

db_automation = mysql.connector.connect(host="127.0.0.1",user="admin",password="1qaz2wsx",database="automation")
exec_command = db_automation.cursor()

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

def insert_Notify(_get1,_get2):
    for _name,_ip in zip(_get1,_get2):
        exec_command.execute(f"insert into line_notify (display,host_ip,code,update_time) values ('{_name}','{_ip}','Up',now());")
        db_automation.commit()

chd = deviceDown()
dp3 = chd[0]
dp4 = chd[1]
insert_Notify(dp3,dp4)
print(dp3)
print(dp4)

db_cacti.close()
db_automation.close()