import pickle
from PIL import Image


class Student:
    def __init__(self, matricule, name, classe, groupe, image):
        self.ID = matricule
        self.Name = name
        self.Class = classe
        self.groupe = groupe
        self.pic = image


class Teacher:
    def __init__(self, matricule, matieres, name, groupe, image=None):
        self.ID = matricule
        self.Name = name
        self.matieres = matieres
        self.groupe = groupe
        self.pic = image


class Classe:
    def __init__(self, class_students, matieres_teachers):
        self.students = class_students
        self.matieres_teachers = matieres_teachers


class Matiere:
    def __init__(self, corses, teacher, classe):
        self.corses = corses
        self.teacher = teacher
        self.classe = classe


# __DataBase__
classes = list()
teachers = list()
students = list()
matieres = list()


# data base manager:
def add_class():
    global classes
    class_students = list()
    print("donner les matricules des etudient dans ce classe:")
    i = 1
    while True:
        student = input("éléve " + str(i) + " :")
        if not student:
            print('no more students')
            u = input("Y/N :")
            if u == 'Y':
                break
        class_students.append(student)

    matieres_teachers = list()
    print("donner les matricules des ensegnets dans ce classe et leur matieres")
    i = 1
    while True:
        enseignant = input("éléve " + str(i) + " :")
        _matiere = input('matiere de ' + enseignant + " : ")
        correspond = {enseignant: _matiere}
        if not enseignant:
            print('no more teachers')
            u = input("Y/N :")
            if u == 'Y':
                break
        matieres_teachers.append(correspond)
    classe = Classe(class_students, matieres_teachers)
    classes.append(classe)


def add_matiere():
    global matieres
    class_students = list()
    print("donner les matricules des etudient dans ce classe:")
    i = 1
    while True:
        student = input("éléve " + str(i) + " :")
        if not student:
            print('no more students')
            u = input("Y/N :")
            if u == 'Y':
                break
        class_students.append(student)

    matieres_teachers = list()
    print("donner les matricules des ensegnets dans ce classe et leur matieres")
    i = 1
    while True:
        enseignant = input("éléve " + str(i) + " :")
        _matiere = input('matiere de ' + enseignant + " : ")
        correspond = {enseignant: _matiere}
        if not enseignant:
            print('no more teachers')
            u = input("Y/N :")
            if u == 'Y':
                break
        matieres_teachers.append(correspond)
    pass


def add_teacher():
    pass


def add_student():
    pass

