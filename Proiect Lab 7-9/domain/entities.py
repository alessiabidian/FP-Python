class Student:
    def __init__(self, student_id, nume, grup):
        """
        Creeaza un nou student cu student_id, nume, grup dat
        :param student_id: id-ul studentului
        :type student_id: int
        :param nume: numele studentului
        :type nume: str
        :param grup: grupa din care face parte studentul
        :type grup: int (>0)
        """
        self.__student_id = student_id
        self.__nume = nume
        self.__grup = grup

    def getID(self):
        return self.__student_id

    def getNume(self):
        return self.__nume

    def getGrup(self):
        return self.__grup

    def setID(self, value):
        self.__student_id = value

    def setNume(self, value):
        self.__nume = value

    def setGrup(self, value):
        self.__grup = value

    def __eq__(self, other):
        """
        Verifica egalitatea intre studentul curent si studentul other
        :param other:
        :type other: Student
        :return: True daca id-urile sunt egale , False altfel
        :rtype: bool
        """
        if self.__student_id == other.getID():
            return True
        return False

    def __str__(self):
        return "ID-ul Studentului: " + str(self.getID()) + '; Nume: ' + str(self.__nume) + '; Nr. grupului: ' + str(self.__grup)

class Laborator:
    def __init__(self, nrlab_nrprobl, descriere, deadline):
        """
        Creeaza o noua problema cu nrlab_nrprobl, descriere, deadline
        :param nrlab_nrprobl: nr problemei
        :type nrlab_nrprobl: str
        :param descriere: descrierea problemei
        :type descriere:
        :param deadline: deadline
        :type deadline: int (>0)
        """
        self.__nrlab_nrprobl = nrlab_nrprobl
        self.__descriere = descriere
        self.__deadline = deadline

    def getNR(self):
        return self.__nrlab_nrprobl

    def getDescriere(self):
        return self.__descriere

    def getDeadline(self):
        return self.__deadline

    def setNR(self, value):
        self.__nrlab_nrprobl = value

    def setDescriere(self, value):
        self.__descriere = value

    def setDeadline(self, value):
        self.__deadline = value

    def __eq__(self, other):
        """
        Verifica egalitatea intre problema curenta si problema other
        :param other:
        :type other: Laborator
        :return: True daca problemele sunt egale (=au acelasi nr), False altfel
        :rtype: bool
        """
        if self.__nrlab_nrprobl == other.getNR():
            return True
        return False

    def __str__(self):
        return "Numarul problemei de la laborator: " + str(self.__nrlab_nrprobl) + '; Descriere: ' + str(self.__descriere) + '; Deadline: ' + str(self.__deadline)

class Nota:
    def __init__(self, laborator, student, nota):
        """
        Creeaza o noua nota cu nrlab_nrprobl, nota, student_id dat
        :param nrlab_nrprobl: nr problemei
        :type nrlab_nrprobl: int
        :param nota: nota studentului
        :type nota: int (1-10)
        :param student_id: id ul studentului ce are nota data
        :type student_id: int (nr cifre == 4)
        """
        self.__laborator = laborator
        self.__nota = nota
        self.__student = student

    def getLab(self):
        return self.__laborator

    def getNota(self):
        return self.__nota

    def getStudent(self):
        return self.__student

    def setLab(self, value):
        self.__laborator = value

    def setNota(self, value):
        self.__nota = value

    def setStudent(self, value):
        self.__student = value

    def __eq__(self, other):
        """
        Verifica egalitatea intre nota curenta si nota other
        :param other:
        :type other: Nota
        :return: True daca serialele sunt egale (=au acelasi id de student si id de problema), False altfel
        :rtype: bool
        """
        if self.__student == other.getStudent() and self.__Laborator == other.getLaborator():
            return True
        return False

    def __str__(self):
        return 'Student: [' + str(self.__student.getID()) + '; ' + str(self.__student.getNume()) + '; ' +  str(self.__student.getGrup()) + ']  ' + \
               'Laborator: [' + str(self.__laborator.getNR()) + '; ' + str(self.__laborator.getDescriere()) + '; ' + str(self.__laborator.getDeadline()) + ']  ' + \
               'Nota: ' + str(self.__nota)

def test_create_student():
    student1 = Student(8014, 'Ovidiu Toma', 916)
    assert (student1.getID() == 8014)
    assert (student1.getNume() == 'Ovidiu Toma')
    assert (student1.getGrup() == 916)

def test_create_laborator():
    laborator1 = Laborator(501, 'Problema pe matrici', '12.03.2022')
    assert (laborator1.getNR() == 501)
    assert (laborator1.getDescriere() == 'Problema pe matrici')
    assert (laborator1.getDeadline() == '12.03.2022')

def test_create_nota():
    student1 = Student(8014, 'Ovidiu Toma', 916)
    laborator1 = Laborator(501, 'Problema pe matrici', '12.03.2022')

    nota1 = Nota(laborator1, student1, 8)

    assert (nota1.getStudent() == student1)
    assert (nota1.getLab() == laborator1)
    assert (nota1.getNota() == 8)


def test_equals_students():
    student1 = Student(8014, 'Ovidiu Toma', 916)
    student2 = Student(8014, 'Ovidiu Toma', 916)

    assert (student1 == student2)

    student3 = Student(1245, 'Ilinca Gheorghe', 414)
    assert (student1 != student3)

test_create_nota()