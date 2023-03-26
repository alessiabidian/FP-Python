from domain.entities import Student
from exceptions.exceptions import CorruptedFileException, DuplicateIDException, StudentNotFoundException

class InMemoryRepository_Stud:
    """
        Clasa creata cu responsabilitatea de a gestiona
        multimea de studenti (i.e. sa ofere un depozit persistent pentru obiecte
        de tip Student)
    """
    def __init__(self):
        # students - multimea de studenti pe care o gestionam

        self.__students = []

    def find(self, id):
        """
        Cauta studentul cu id dat
        :param student_id:
        :return:
        """
        for student in self.__students:
            if student.getID() == id:
                return student
        return None

    def find_recursiv(self, all_students, i, id):
        """
        Cauta studentul cu id dat
        :param student_id:
        :return:
        """
        if i >= 0:
            if all_students[i].getID() == id:
                return all_students[i]
            else:
                return self.find_recursiv(all_students, i-1, id)
        return None

    def find_grup(self, grup):
        """
        Cauta studentul cu id dat
        :param student_id:
        :return:
        """
        for student in self.__students:
            if student.getGrup() == grup:
                return grup
        return None

    def find_grup_recursiv(self, all_students, i, grup):
        """
        Cauta studentul cu id dat
        :param student_id:
        :return:
        """
        if i >= 0:
            if all_students[i].getGrup() == grup:
                return grup
            else:
                return self.find_grup_recursiv(all_students, i-1, grup)
        return None

    def store(self, student):
        """
        Adauga un student in lista
        :param student: studentul care se adauga
        :type student: Student
        :return: -; lista de studenti se modifica prin adaugarea studentului dat
        :rtype:
        """
        if self.find(student.getID()) is not None:
            #raise ValueError('Exista deja student cu acest ID.')
            raise DuplicateIDException()

        self.__students.append(student)

    def get_all_students(self):
        """
        Returneaza o lista cu toate studentii existenti
        :rtype: list of objects de tip Student
        """
        return self.__students

    def size(self):
        """

        :return:
        """
        return len(self.__students)

    def delete_by_id(self, id):
        """
        Sterge studentul dupa id
        :param id: id-ul dat
        :type id: int
        :param id:
        :return:
        """
        #self.__students = [student for student in self.__students if not student.getID() == id]
        student = self.find(id)
        if student is None:
            #raise ValueError('Nu exista student cu acest id pt a fi sters.')
            raise StudentNotFoundException()

        self.__students.remove(student)
        return student

    def update(self, student_id, modified_student):
        """
        Modifica datele studentului cu id dat
        :param id: id dat
        :type id: str
        :param modified_student: student-ul cu datele noi
        :type modified_student: Student
        :return: studentul modificat
        :rtype: Student
        """

        # self.delete_by_id(id)
        # self.store(modified_show)
        # return modified_show

        student = self.find(student_id)
        if student is None:
            #raise ValueError('Nu exista student cu acest id.')
            raise StudentNotFoundException()

        student.setID(modified_student.getID())
        student.setNume(modified_student.getNume())
        student.setGrup(modified_student.getGrup())
        return student

    def delete_by_criteria(self, filter_function):
        """
        Sterge serialele din multime dupa un criteriu dat
        :param filter_function: functia (criteriul dupa care se sterg serialele)
        :type filter_function: function
        :return: numarul de seriale sterse
        :rtype: int
        """

        initial_no_students = self.size()
        self.__students = [student for student in self.__students if not filter_function(student)]
        return initial_no_students - self.size()

class StudFileRepoInheritance(InMemoryRepository_Stud):
    def __init__(self, filename):
        InMemoryRepository_Stud.__init__(self)
        self.__filename = filename
        self.__load_from_file()

    def __load_from_file(self):
        try:
            f = open(self.__filename, 'r')
            # f = io.open(self.__filename, mode='r', encoding='utf-8')
        except IOError:
            raise CorruptedFileException()

        lines = f.readlines()
        dim = len(lines)
        #for line in lines:
            #student_id, nume, grup = [token.strip() for token in line.split(';')]
            #student = [token.strip() for token in line.split(';')]
            #student_id = int(student[0])
            #nume = str(student[1])
            #grup = int(student[2])
        for i in range(0, dim, 3):
            student_id, nume, grup = [lines[i].strip(), lines[i+1].strip(), lines[i+2].strip()]
            a = Student(int(student_id), str(nume), int(grup))
            InMemoryRepository_Stud.store(self, a)
        f.close()

    def __save_to_file(self):
        student_list = InMemoryRepository_Stud.get_all_students(self)
        with open(self.__filename, 'w') as f:
            for student in student_list:
                #student_string = str(student.getID()) + ';' + str(student.getNume()) + ';' + str(
                    #student.getGrup()) + '\n'
                student_string = str(student.getID()) + '\n' + str(student.getNume()) + '\n' + str(student.getGrup()) + '\n'
                f.write(student_string)

    def store_from_file(self, student):
        InMemoryRepository_Stud.store(self, student)
        self.__save_to_file()

    def update(self, id, new_student):
        updated_student = InMemoryRepository_Stud.update(self, id, new_student)
        self.__save_to_file()
        return updated_student

    def delete_by_id(self, id):
        deleted_student = InMemoryRepository_Stud.delete_by_id(self, id)
        print(deleted_student)
        self.__save_to_file()
        return deleted_student

    def get_all_students(self):
        return InMemoryRepository_Stud.get_all_students(self)

    def size(self):
        return InMemoryRepository_Stud.size(self)

    def delete_by_criteria(self, filter_function):
        how_many_deleted = InMemoryRepository_Stud.delete_by_criteria(self, filter_function)
        self.__save_to_file()
        return how_many_deleted

    def find(self, id):
        return InMemoryRepository_Stud.find(self, id)

    def find_r(self, id):
        all_students = self.get_all_students()
        i = len(all_students) - 1
        return InMemoryRepository_Stud.find_recursiv(self, all_students, i, id)

    def find_grup(self, grup):
        return InMemoryRepository_Stud.find_grup(self, grup)

    def find_grup_r(self, grup):
        all_students = self.get_all_students()
        i = len(all_students) - 1
        return InMemoryRepository_Stud.find_grup_recursiv(self, all_students, i, grup)

def test_store_students():
    test_repo = InMemoryRepository_Stud()
    student1 = Student(1789, 'Denis Ilea', 314)
    test_repo.store(student1)

    assert(test_repo.size() == 1)

    student2 = Student(4545, 'Kim Kardashian', 114)
    test_repo.store(student2)

    assert (test_repo.size() == 2)

def test_delete_by_id():
    test_repo = InMemoryRepository_Stud()
    student1 = Student(1789, 'Denis Ilea', 314)
    test_repo.store(student1)
    student2 = Student(1009, 'Denisa Petrusa', 414)
    test_repo.store(student2)

    deleted_student = test_repo.delete_by_id(1789)
    assert (deleted_student.getNume() == 'Denis Ilea')
    assert (test_repo.size() == 1)

    student_left = test_repo.find(1009)
    assert (student_left.getNume() == 'Denisa Petrusa')

    try:
        test_repo.delete_by_id('wrongid')
        assert False
    except ValueError:
        assert True


def test_update():
    test_repo = InMemoryRepository_Stud()
    student1 = Student(1789, 'Denis Ilea', 314)
    test_repo.store(student1)
    student2 = Student(1009, 'Denisa Petrusa', 414)
    test_repo.store(student2)
    student3 = Student(1009, 'Kim K', 211)

    modified_student = test_repo.update(1009, student3)
    assert (modified_student.getNume() == 'Kim K')
    assert (modified_student.getGrup() == 211)
'''
    try:
        test_repo.update(1789, Student(134, 'Kim K', 211))
        assert False
    except ValueError:
        assert True
test_store_students()
test_delete_by_id()
test_update()
'''

