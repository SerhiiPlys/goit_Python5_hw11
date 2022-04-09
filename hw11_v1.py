""" ДЗ11
"""
from collections import UserDict
from datetime import datetime
import re

class AdressBook(UserDict):

    def __init__(self):
        self.current_value = 0
        super().__init__()  # чтоб не потерять атрибут data родительского класса
                            # посокльку __init__ переопределит такой же метод у родителя
    def __iter__(self):
        return self

    def __next__(self):
        if self.current_value < len(self.data):
            self.current_value += 1
            l1 = []
            for i in self.data:
                l1.append(i)    # сделали нормальный список ключей, который индексируется
            return f'{self.current_value}: \
{l1[self.current_value-1]} - {self.data[l1[self.current_value-1]]}'
        raise StopIteration

    def first(self):
        self.current_value = 0  # возврат итератора в исходное состояние
        
    def iterator(self, items):
        while True:
            print("    N - следующая страница, S - выход из постраничного вывода")
            in_c = input()
            if in_c == "N" or in_c == "n":
                cnt = 0
                print("Новая страница")
                if self.current_value < len(self.data):
                    for i in self:
                        print(i)
                        cnt += 1
                        if cnt == items:
                            break
                else:
                    print("Конец книги")
                    break
            elif in_c == "S" or in_c == "s":
                break
            else:
                print("Сделайте выбор между N и S")
 
    
    def add_record(self,  rec):
        if isinstance(rec, Record):
            self.data.update({rec.name.value:rec})
        else:
            print("Добавить можно только объект класса Record")

    def del_record(self, rec):

            if isinstance(rec, Record):
                l1 = self.data.keys() # получили список ключей
                if rec.name.value in l1: # если такой есть то удаляем
                    self.data.pop(rec.name.value)
                else:
                    print("Нет записи с таким именем")
            else:
                print("Метод принимает только объект класса Record")
        


class Field():  

    __VAL = ''

    def __init__(self):
        self.__value = Field.__VAL

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, n_value):
        self.__value = n_value


class Name(Field):

    def __init__(self, name):
        self.value = name


class Phone(Field):

    def __init__(self):
        self.__phone = ''
        
    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, new_phone):
        if type(new_phone) != str:  # защита от пустого поля
            new_phone = '' # пустую строку можно передать аргументом на соответсвие
        if re.search(r"^\+\([0-9]{3}\)[0-9]{9}$", new_phone) != None:
            self.__phone = new_phone
            print("Телефон корректен")
        else:
            self.__phone = ''
            print("Задайте телефон в виде строки  +(xxx)xxxxxxxxх   ")


class Birthday():

    def __init__(self):
        self.__value = ''

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if type(new_value) == str:  # защита от пустого поля
            try:
                brt = datetime.strptime(new_value, '%d.%m.%Y')
                self.__value = new_value
                print("Дата дня рождения корректна")
            except:
                print("Задайте дату ДР в виде строки dd.mm.YYYY")
        else:
            print("Дата ДР не задана")
            

class Record():

    def __init__(self, name, phone = '', birthday = ''):
        self.name = Name(name)
        self.phone = Phone()
        self.phone.phone = phone
        self.phones = []
        if isinstance(self.phone, Phone) and (self.phone.phone != ''):
            self.phones.append(self.phone)
        else:
            print(f"Создайте Phone(телефон) и воспользуйтесь методом add_phone")
        self.birthday = Birthday()
        self.birthday.value = birthday

    def add_phone(self, p:Phone):

        if isinstance(p, Phone) and (p.phone != None):
            self.phones.append(p)
            print("Объект с телефоном добавлен")
        else:
            print("Создайте номер как объект класса Phone(телефон)")

    def del_phone(self, p:Phone):

        if len(self.phones) >= 1:
            if isinstance(p, Phone) and (p.phone != None):
                for i in self.phones:
                    del_nmb = False           #флаг найденного совпадения
                    if i.phone == p.phone:
                        self.phones.remove(i)
                        del_nmb = True
                        break
                if del_nmb == True:
                    print("Номер удален")
                else:
                    print("Совпадений с заданным номером не найдено")
            else:
                print("Метод принимает объект класса Phone")

        else:
            print("Список номеров пуст")

    def change_phone(self, p:Phone, pn:Phone):

        if (isinstance(p, Phone) and isinstance(pn, Phone) and
           (p.phone != None) and (pn.phone != None)):
            for i in self.phones:
                if i.phone == p.phone:
                    i.phone = pn.phone
                    print("Требуемый номер изменен")
                    break
                else:
                    print("Исходного номера не найдено, добавьте номер через метод add_phone")
        else:
            print("Создайте номер как объект класса Phone")

    def days_to_birthday(self):

        if self.birthday.value != None:
            current_datetime = datetime.now()  # текущая дата
            current_year = current_datetime.year # текущий год
            brt = self.birthday.value[0:6]  # день и месяц ДР
            brt = brt + str(current_year)  # ДР в текущем году
            brt_this_year = datetime.strptime(brt, '%d.%m.%Y')
            dif_day = brt_this_year - current_datetime
            if dif_day.days > 0 :
                print(f"До дня рождения осталось {dif_day.days} дней")
            else:
                print(f"ДР в этом году уже прошло {abs(dif_day.days)} дней назад")
        else:
            print("Задайте ДР")


def main():
    print("ДЗ11")
    Ivan = Record("Ivan")
    Bill = Record("Bill")
    Ivan1 = Record("Ivan1")
    Ivan2 = Record("Ivan2")
    Ivan3 = Record("Ivan3")
    tlf = AdressBook()
    tlf.add_record(Ivan)
    tlf.add_record(Bill)
    tlf.add_record(Ivan1)
    tlf.add_record(Ivan2)
    tlf.add_record(Ivan3)
    tlf.iterator(2)


if __name__ == "__main__":
    main()
