import csv
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

def write_report(file_path, name, time, list_data):
    helmet, vest, glove, note = parse_list(list_data)
    with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
        data_csv = create_data(name, time, helmet, vest, glove, note)
        writer = csv.writer(csv_file)
        writer.writerow(data_csv)
    return note

def edit_report(file_path, name, time, list_data):
    helmet, vest, glove, note = parse_list(list_data)
    rows = []
    find = False
    with open(file_path, 'r', encoding='utf8') as csv_file:
        reader = csv.reader(csv_file)  
        # Loop through each row in the CSV file
        for row in reader:
            # Check if this is the row we want to edit
            if row[0] == name:
                # Modify the row data
                row[1] = time
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

    