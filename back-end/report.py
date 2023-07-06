import csv
import time
import unidecode
def create_data(name = 'Name', time = "Time", helmet = "Helmet", vest = "Vest", glove = "Glove", note = "Note"):
    data = []
    data.append(name)
    data.append(time)
    data.append(helmet)
    data.append(vest)
    data.append(glove)
    data.append(note)
    return data

def create_report(file_path):
    with open(file_path, 'w', newline='') as csv_file:
        data_csv = create_data()
        writer = csv.writer(csv_file)
        writer.writerow(data_csv)

def write_report(file_path, name, time_r, list_data):
    helmet, vest, glove, note = parse_list(list_data)
    while True:
        try:
            with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
                data_csv = create_data(name, time_r, helmet, vest, glove, note)
                writer = csv.writer(csv_file)
                writer.writerow(data_csv)
        except:
            time.sleep(0.5)
        else:
            break

    return note

def edit_report(file_path, name, time_r, list_data):
    helmet, vest, glove, note = parse_list(list_data)
    rows = []
    find = False
    while True:
        try:
            with open(file_path, 'r', encoding='utf8') as csv_file:
                reader = csv.reader(csv_file)  
                # Loop through each row in the CSV file
                for row in reader:
                    # Check if this is the row we want to edit
                    if row[0] == name and row[1] != "Time":
                        # Modify the row data
                        row[1] = time_r
                        row[2] = helmet
                        row[3] = vest
                        row[4] = glove
                        row[5] = note
                        find = True
                    
                    # Add the row to the list of updated data
                    rows.append(row)
            if find:
                with open(file_path, 'w', newline='', encoding='utf8') as csv_file:
                    writer = csv.writer(csv_file)
                    for line in rows:
                        writer.writerow(line)   

        except:
            time.sleep(0.5)
        else:
            break
    return find,note


def parse_list(list):
    helmet = "Yes"
    vest = "Yes"
    glove = "Yes"
    note = "Safety"

    device = 3

    for i in list:
        if i == 0:  
            helmet = "No"
            device -=1
            continue
        elif i == 1:
            vest = "No"
            device -=1
        elif i == 2:
            glove = "No"
            device -=1

    if device != 3:
        note = "Not safety"        

    return helmet,vest,glove,note

def update_report(old_name, new_name):
    import glob
    path = glob.glob(r"report/**.csv")
    for csv_path in path:
        list_data = []
        while True:
            try:
                with open(csv_path, 'r', encoding='utf8', errors='ignore') as csv_file:
                    reader = csv.reader(csv_file) 
                    for row in reader:
                        if unidecode.unidecode(row[0]) == unidecode.unidecode(old_name) and row[1] != "Time":
                            row[0] = new_name
                        list_data.append(row)
                with open(csv_path, 'w', newline='', encoding='utf8') as csv_file:
                    writer = csv.writer(csv_file)
                    for line in list_data:
                        writer.writerow(line)
            except:
                time.sleep(0.5)
            else:
                break
    