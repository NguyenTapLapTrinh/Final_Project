import csv

def create_data(stt = "STT",name = 'Name', time = "Time", helmet = "Helmet", vest = "Vest", glove = "Glove", note = "Note"):
    data = []
    data.append(stt)
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

def write_report(file_path, stt, name, time, list_data):
    helmet, vest, glove, note = parse_list(list_data)
    with open(file_path, 'a', newline='') as csv_file:
        data_csv = create_data(stt, name, time, helmet, vest, glove, note)
        writer = csv.writer(csv_file)
        writer.writerow(data_csv)

def edit_report(file_path, name, time, list_data):
    helmet, vest, glove, note = parse_list(list_data)
    rows = []

    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)    
        # Loop through each row in the CSV file
        for row in reader:
            # Check if this is the row we want to edit
            if row[1] == name:
                # Modify the row data
                row[2] = time
                row[3] = helmet
                row[4] = vest
                row[5] = glove
                row[6] = note
            
            # Add the row to the list of updated data
            rows.append(row)

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for line in rows:
            writer.writerow(line)   


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
        if i == 1:
            vest = "No"
            device -=1
            continue
        if i == 2:
            glove = "No"
            device -=1
            continue

    if device != 3:
        note = "Not safety"        

    return helmet,vest,glove,note

    