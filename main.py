from itertools import groupby
import re

# Читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Достаем из таблицы фамилию/имя/отчество
list_value = contacts_list[1:]

family_list, name_list, patronymic_list = [], [], []
fio_list = [" ".join(value[:3]) for value in list_value]
for fio in fio_list:
    f = fio.split(" ")
    fam = [value for value in f if value]
    family_list.append(fam[0])
    name_list.append(fam[1])
    if len(fam) == 3:
        patronymic_list.append(fam[2])
    else:
        patronymic_list.append(" ")

# Достаем организацию
organization_list = [organization[3] for organization in list_value]

# Достаем e-mail
email_list = [email[6] for email in list_value]

# Достаем позицию
pozition_list = [pozition[4] for pozition in list_value]

# Достаем телефон
telephone_list = ["".join(telephone[5]) for telephone in list_value]
telephone_list_text = " , ".join(telephone_list)
pattern = (r"(\+7|8)\s*\(?(\d\d\d)\)?[-\s]*(\d\d\d)[-\s]*(\d+)[-\s]*(\d\d)\s*\(?(\w+\.\s*\d+)*\)?")
result = re.sub(pattern, r"+7(\2)\3-\4-\5 \6", telephone_list_text)
telephone_list_upd = result.split(" , ")

# Создание общего списка
new_list = [list(x) for x in zip(family_list, name_list, patronymic_list, organization_list, pozition_list, telephone_list_upd, email_list)]
new_list.sort(key=lambda x: (x[0], x[1]))
grouped_list = [list(data) for _, data in groupby(new_list, key=lambda x: (x[0], x[1]))]

# Объединение дублирующей информации о пользователе
change_list = []
change_list.append(contacts_list[0])
for groups in grouped_list:
    if len(groups) == 2:
        list_unit = []
        if groups[0][0] == groups[1][0]:
            list_unit.append(groups[0][0])
        if groups[0][1] == groups[1][1]:
            list_unit.append(groups[0][1])
        if groups[0][2] == groups[1][2]:
            list_unit.append(groups[0][2])
        else:
            list_unit.append(groups[0][2] + groups[1][2])
        if groups[0][3] == groups[1][3]:
            list_unit.append(groups[0][3])
        else:
            list_unit.append(groups[0][3] + groups[1][3])
        if groups[0][4] == groups[1][4]:
            list_unit.append(groups[0][4])
        else:
            list_unit.append(groups[0][4] + groups[1][4])
        if groups[0][5] == groups[1][5]:
            list_unit.append(groups[0][5])
        else:
            list_unit.append(groups[0][5] + groups[1][5])
        if groups[0][6] == groups[1][6]:
            list_unit.append(groups[0][6])
        else:
            list_unit.append(groups[0][6] + groups[1][6])
        change_list.append(list_unit)
    else:
        change_list.append(groups[0])

# Сохранение преобразованных данных в другой файл
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f)
    datawriter.writerows(change_list)