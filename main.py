import datetime
import os
import report
import demo
from time import *

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

STT = 1
if os.path.exists("report"):
    pass
else:
    os.mkdir("report")

while True:
    # Get current time
    time = datetime.datetime.now().time()
    date = datetime.date.today()

    # Format time as string
    time_str = time.strftime("%H:%M:%S")
    date_str = date.strftime("%B-%d-%Y")
    date_temp = date_str.split("-")
    tmp = str(months.index(date_temp[0]) + 1)
    if len(tmp) < 2:
        tmp = '0' + tmp
        
    date_str = date_str.replace(date_temp[0],tmp)
    # Print current time
    print("Current time: ", time_str, "\nDate : ", date_str)

    # Set the path of the folder you want to check
    file_path = "report/report_" + date_str+ ".csv"

    # Check if the file exists
    if os.path.exists(file_path):
        pass
    else:
        report.create_report(file_path)

    list_test = demo.create_data_test()

    report.write_report(file_path,str(STT),"Nguyen",time_str,list_test)
    STT += 1
    user_input = input("Do you want to continue (0 = No, 1 = Yes)\nYour choice: ")
    if user_input == '0':
        break

    sleep(2)





