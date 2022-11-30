# N_fetch_db_finish.py
import datetime
import time
import requests
import mysql.connector

#Global variable for connnect DB
#django_db = mysql.connector.connect(host="172.18.0.2",user="root",password="benz4466",database="django_db")

db_cacti = mysql.connector.connect(host="127.0.0.1",user="admin",password="1qaz2wsx",database="automation")
exec_command = db_cacti.cursor()

class Autimation_option:
    def _timeline(self):
        timestr = datetime.datetime.now()
        date = timestr.strftime("%d-%m-%Y")
        time_now = timestr.strftime("%X")
        time_stamp = date + ' ' + time_now
        return date,time_now,time_stamp

    def _send(self,*args):
        url = 'https://notify-api.line.me/api/notify'
        token = 'xoQZ0Qaq5e0lf4eFraNNs7bOVwOioE9YyNNq8zqBLjw' #<-- Token line
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        meassage = args
        requests.post(url, headers=headers, data = {'message':meassage})

class Connect_database:
    def _fetch_db(self):
        exec_command.execute(f"select * from line_notify where status='000';")
        id_list = []
        display_list = []
        host_ip_list = []
        code_list = []
        cus_id_list = []
        message_list = []
        update_time = []
        status_list = []
        for fetch in exec_command:
            get_list = fetch[0]
            get_display = fetch[1]
            get_host_ip = fetch[2]
            get_code = fetch[3]
            get_cus_id = fetch[4]
            get_message = fetch[5]
            get_update_time = fetch[6]
            get_status = fetch[8]
            id_list.append(get_list)
            display_list.append(get_display)
            host_ip_list.append(get_host_ip)
            code_list.append(get_code)
            cus_id_list.append(get_cus_id)
            message_list.append(get_message)
            update_time.append(get_update_time)
            status_list.append(get_status)
        return id_list,display_list,host_ip_list,code_list,cus_id_list,message_list,update_time,status_list
    
    def _update_db(self,_get_id):
        exec_command.execute(f"UPDATE line_notify set status = '001' WHERE id = '{_get_id}';")
        db_cacti.commit()

if __name__ == "__main__":
    option1 = Autimation_option()
    option2 = Connect_database() #<-- Class Database
    timeoption = option1._timeline()
    index_time = timeoption[2]
    result = option2._fetch_db()
    index0 = result[0]
    index1 = result[1]
    index2 = result[2]
    index3 = result[3]
    index4 = result[4]
    index5 = result[5]
    index6 = result[6]
    index7 = result[7]

    for result_id,resert_display,result_ip,result_code,result_cus_id,result_message,result_update_time,result_status in zip(index0,index1,index2,index3,index4,index5,index6,index7):
        #print(result_id,result_ip,result_status)
        if result_status == '000':
            option2._update_db(result_id)
            #option1._send(f"{result_ip} Can Internet \nTime: {index_time} \nDB_django : finish_log")
            option1._send(f"{resert_display} {result_ip} {result_code} {result_cus_id} {result_message} {result_update_time}")
        else:
            db_cacti.close()
            break
    db_cacti.close()