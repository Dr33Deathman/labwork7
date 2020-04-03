import os
import csv
import json


class Name():

    def __init__(self, fname: str, lname: str, mname= ""):
        # Конструктор класса Name, который на вход принимает 3 аргумента. Третий аргумент не обязателен, если его не указать, то он примет значение ""
        self.first_name = fname
        self.last_name = lname
        self.middle_name = mname

    def __str__(self) -> str:
        # Метод класса Name, который нужен чтобы определить результат работы str(Name)

        # Если в Name пользователя нет отчества (Middle name), то он будет будет принимать другое значение
        if self.middle_name != "":
            return self.first_name + " " + self.last_name + " " + self.middle_name
        else:
            return self.first_name + " " + self.last_name
        
        # Example:
        # str(Name) вернет Ахмедов Кямран 


class Student():

    def __init__(self, id_: str, name: Name):
        # Конструктор класса Student, который принимает 2 аргумента. Первый аргумент это ID студента, второй это его ФИО в типе данных Name, который мы описали до этого
        self.student_id = id_
        self.name = name

    def __str__(self) -> str:
        # Метод класса Student, который нужен чтобы определить результат работы str(Student)
        return str(self.name) + ", student ID: " + self.student_id

        # Example:
        # str(Student) вернет Ахмедов Кямран, student ID: 19B030754


class Assistant():

    def __init__(self, name: Name, year: int = 2):
        # Конструктор класса Assistant, принимает на вход два аргумента. Первый это его ФИО, второй это его год обучения. Если год обучения не указан, то год обучения будет вторым
        self.name = name
        self.year_of_study = year

    def get_name(self) -> str:
        # Example:
        # Assistant.get_name() вернет Alik Akhmetov
        return str(self.name)
        

    def __str__(self) -> str:
        # Метод класса Student, который нужен чтобы определить результат работы str(Student)
        return str(self.name) + ", studying " + str(self.year_of_study) + " year"
        # Example:
        # str(Assistant) вернет Alik Akhmetov, studying 2 year


class PP2():

    def __init__(self, a = list(), b = list() ):
        # Конструктор класса PP2, принимает на вход 2 аргуемнта. Первый аргумент это лист, который состоит из Ассистентов с типом данных Assistant, второй аргумент это лист, который состоит из студентов с типом данных Student
        self.assistants = a
        self.students = b
        self.groups = dict() # третее свойство это dict групп учащихся у ассистента. Изначально он всегда пустой dict 

    def get_assistants(self):
        # Метод, нужен чтобы получить list всех ассистентов
        return self.assistants

    def get_students(self):
        # Метод, нужен чтобы получить list всех студентов
        return self.students

    def get_groups(self):
        # Метод, нужен чтобы получить dict всех групп ассистентов внутри курса pp2
        return self.groups

    def add_user_to_Group(self, name: Name, student: Student):
        # Метод, который добавляет Student в группу к Ассистенту по имени name
        
        # Если у ассистента была группа, то он просто добавит в конец листа этого студента с помощью append()   
        if str(name) in self.groups:
            self.groups[str(name)].append(student)
        # Если раньше у ассистента не было группы, то этот метод создаст эту группу, в которую запишет только добавившегося студента
        else:
            self.groups[str(name)] = [student]

    def populate_from_csv(self, path: str):
        # Метод класса PP2, который нужен чтобы людей из csv файла.  Единственный аргумент это путь до файла, откуда нужно добавить людей
        
        with open(path, 'r+', newline='', encoding='utf8') as file: # Открываем файл 

            s = set() # Нужен для проверки был ли у нас уже такой ассистент. Это нужно потому что в csv файле имя одного и того же ассистента написано много раз. Таким образом лист не будет состоять из (например) 18 Аликов, 15 Бекболатов и 20 Дарханов.
            for line in file: # Считываем построчно наш файл

                cur = line.strip().split(',') # Разделяем содержимое нашей строки через запятую и убираем \r\n в конце каждой строки

                if (cur[0].isdigit()): # Проверяем нулевой блок. Так мы должны делать операции только, если нулевой блок является числом
                    names = cur[2].split(' ', 2) # это второй блок, в котором содержатся ФИО. Мы отделяем ФИО через пробел. 
                    # Второй аргумент это сколько максимально отделений может быть. Это нужно для того, чтобы мое отчество, которое состоит из двух слов (Сардар оглы) записывалось как единное целое и не делилось через пробел 
                    
                    assistaintName = cur[3].split(' ') # Блок с фамилией и именем ассистента так же разделяем через пробел 
                    assistantFIO =  assistaintName[0] + ' ' + assistaintName[1] # Чтобы нам было проще работать запишем это в нормальном виде #Example: Alik Akhmetov

                    if not assistantFIO in s: # Если нашего ассистента нет в сете для проверки. 
                        s.add(assistantFIO) # То он добавляет Ассистента в сет, 
                        self.assistants.append(Assistant(Name(assistaintName[0], assistaintName[1]), 2)) # а так же добавляет его в лист ассистентов PP2 

                    if len(names) == 3: # Если ФИО Студента состоит из 3 элементов (Это значит Имя Фамилия и Есть отчество)
                        
                        # С помощью конструкторов создаем объекты и добавляем их.
                        self.students.append(Student(cur[1], Name(names[0], names[1], names[2]))) # То тогда добавляет в лист студентов PP2
                        self.add_user_to_Group(assistantFIO, (Student(cur[1], (Name(names[0], names[1], names[2]).__dict__)).__dict__)) # А так же добавляет его в группу к Ассистенту, который прописан в csv файле
                        # Нам Необходимо превращать каждый новый объект(Сначала Name, потом Student) в dict, чтобы потом можно было сохранить это в JSON файл
                    
                    else: # Проделываем тоже самое, только при условии, что у нашего студента нет отчества
                        self.students.append(Student(cur[1], Name(names[0], names[1])))
                        self.add_user_to_Group(assistantFIO, (Student(cur[1], (Name(names[0], names[1]).__dict__)).__dict__))

    def save_to_json(self, filename: str):
        # Метод который сохраняет все данные в программе в файл, название которого идет как аргумент (filename)
        
        with open(filename, 'w+', encoding='utf8') as file: # открываем файл
            json.dump(self.get_groups(), file, ensure_ascii='', indent=4) # И записываем в него dict с группами, которые мы создавали до этого
            # 1 аргумент - то что сохраняем. оно должно быть dict`ом 
            # 2 аргумент - file, это то место куда сохраняем
            # 3 аргумент - нужен для того, чтобы наш файл сохранялся в правильной кодировке
            # 4 аргумент - нужен чтобы наш файл был красиво табулирован. Для наглядности советую изменить его на 0 и запустить еще раз и посмотреть json файл


# С этого момента начинаются непосредственные действия программы. До этого была лишь предыстория :D

pp2 = PP2([], []) # Создаем объект PP2 с помощью класса, на вход две пустые квадратные схобки. Это значит что мы подаем 2 пустых листа. (Как в примере в гитхабе)
pp2.populate_from_csv('pp2.csv') # Считываем всех людей из файла под названием pp2.csv 
pp2.save_to_json('pp2.json') # Сохраняем все данные в файл под названием pp2.json


# С дополнительными вопросами можете обращаться к автору кода в телеге @Dr33Deathman

#              ! КАРАМБА !
# !!!!! Все комментарии ниже это коды с гитхаба, чтобы проверять работоспособность программы на примерах
# !!!!! Там мы вручную создавали объекты и смотрели результаты кода, работает ли наша программа
# P.S: Спасибо кямрану (С) Алик

# assistant1 = Assistant(Name('Alik', 'Akhmetov'), 2)
# student1 = Student('16BD02006', Name('Daulet', 'Kabdiyev', 'Bolatovich'))
# student2 = Student('16BD02007', Name('Ivan', 'Ivanov', 'Ivanovich'))

# pp2 = PP2([assistant1], [student1, student2])

# print(student1)
# pp2.add_user_to_Group(assistant1.get_name(), student1)
# pp2.add_user_to_Group(assistant1.get_name(), student2)

# print(pp2.get_groups())
