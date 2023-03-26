from domain.entities import Student, Laborator, Nota
from repository.studs_repo import StudFileRepoInheritance
from repository.labs_repo import LabFileRepoInheritance
from domain.validators import NotaValidator, StudentValidator, LaboratorValidator

class InMemoryRepository_Grade:
    """
        Clasa creata cu responsabilitatea de a gestiona
        multimea de note (i.e. sa ofere un depozit persistent pentru obiecte
        de tip nota)
    """
    def __init__(self):
        # grades - multimea de note pe care o gestionam
        self.__grades = []

    def find(self, n):
        """
        Cauta nota cu id-ul dat
        :param student_id:
        :return:
        """
        for nota in self.__grades:
            if n == nota:
                return nota
        return None

    def size(self):
        """

        :return:
        """
        return len(self.__grades)

    def store(self, nota):
        """
        Adauga o nota in lista
        :param nota: nota care se adauga
        :type nota: Nota
        :return: -; lista de note se modifica prin adaugarea notei date
        :rtype:
        """
        self.__grades.append(nota)

    def get_all_grades(self):
        """
        Returneaza o lista cu toate grade-urile existente
        :rtype: list of objects de tip Nota
        """
        return self.__grades

class GradeFileRepoInheritance(LabFileRepoInheritance, StudFileRepoInheritance, InMemoryRepository_Grade):
    def __init__(self, filename):
        InMemoryRepository_Grade.__init__(self)
        LabFileRepoInheritance.__init__(self, 'data/labs.txt')
        StudFileRepoInheritance.__init__(self, 'data/students.txt')
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
            #grade = [token.strip() for token in line.split(';')]
            #print(int(grade[0]))
            #laborator = LabFileRepoInheritance.find(self, int(grade[0]))
            #student = StudFileRepoInheritance.find(self, int(grade[1]))
            #nota = int(grade[2])
        for i in range(0, dim, 3):
            nrlab_nrprobl, student_id, nota = [lines[i].strip(), lines[i+1].strip(), lines[i+2].strip()]
            laborator = LabFileRepoInheritance.find(self, int(nrlab_nrprobl))
            list = LabFileRepoInheritance.get_all_labs(self)
            student = StudFileRepoInheritance.find(self, int(student_id))
            a = Nota(laborator, student, float(nota))
            NotaValidator.validate(self, a)
            InMemoryRepository_Grade.store(self, a)
        f.close()

    def __save_to_file(self):
        grade_list = InMemoryRepository_Grade.get_all_grades(self)
        with open(self.__filename, 'w') as f:
            for grade in grade_list:
                #grade_string = str(grade.getLab().getNR()) + ';' + str(grade.getStudent.getID()) + ';' + str(
                    #grade.getNota()) + '\n'
                grade_string = str(grade.getLab().getNR()) + '\n' + str(grade.getStudent().getID()) + '\n' + str(
                    grade.getNota()) + '\n'
                f.write(grade_string)

    def store(self, grade):
        InMemoryRepository_Grade.store(self, grade)
        self.__save_to_file()

    def get_all_grades(self):
        return InMemoryRepository_Grade.get_all_grades(self)

    def size(self):
        return InMemoryRepository_Grade.size(self)

    def find(self, n):
        return InMemoryRepository_Grade.find(self, n)


def test_store_grades():
    test_repo = InMemoryRepository_Grade()
    s = Student(8104, 'Radu Boxeru', 925)
    l = Laborator(305, 'Alg de sortare', '27.03.2022')
    n = Nota(l, s, 9)

    test_repo.store(n)

    s = Student(2345, 'Raluca Dragan', 135)
    l = Laborator(208, 'Alg de cautare', '14.04.2022')
    n = Nota(l, s, 7)

    test_repo.store(n)

    s = Student(1678, 'Irina Fluture', 121)
    l = Laborator(305, 'Alg de sortare', '02.05.2022')
    n = Nota(l, s, 5)

    test_repo.store(n)

    assert(test_repo.size() == 3)

test_store_grades()