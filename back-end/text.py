def writeLine(name,unicode_name):
    with open("db/name.txt", "rb") as file:
        list_name = file.readlines()
    with open("db/name.txt", "wb") as file:
        unicode_text = name + "_" + unicode_name +"\n"
        unicode_text = unicode_text.encode()
        list_name.append(unicode_text)
        file.writelines(list_name)


def findFullName(unicode_name):
    with open("db/name.txt", "rb") as file:
        line = file.readlines()
        test =unicode_name+"\n"
        for i in line:
            i = i.decode()
            i = i.split("_")
            if test == i[1]:
                return i[0]
            
def deleteUser(name):
    file_list = []
    name += "\n"
    with open("db/name.txt", "rb") as file:
        file_list = file.readlines()
        for i in file_list:
            line = i.decode()
            line = line.split("_")
            line = line[1]
            if name == line:
                file_list.remove(i)  
    with open("db/name.txt", "wb") as file:
        file.writelines(file_list)   

def editUser(name,new_name,unicode_name):
    file_list = []
    name += "\n"
    with open("db/name.txt", "rb") as file:
        file_list = file.readlines()
        for i in file_list:
            line = i.decode()
            line = line.split("_")
            line = line[1]
            print(line)
            if name == line:
                position = file_list.index(i)
                file_list.remove(i)
                new_line = new_name + "_" + unicode_name + "\n"
                new_line = new_line.encode()
                file_list.insert(position,new_line)
                print(new_line)
    with open("db/name.txt", "wb") as file:
        file.writelines(file_list)     