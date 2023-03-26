from domain.entities import Nota, Student, Laborator
from domain.validators import NotaValidator, StudentValidator, LaboratorValidator
from repository.grades_repo import InMemoryRepository_Grade
from repository.studs_repo import InMemoryRepository_Stud
from repository.labs_repo import InMemoryRepository_Lab
from exceptions.exceptions import GradeNotValid, StudentNotFoundException, LaboratorNotFoundException, GradeAlreadyAssignedException, ValidationException


class NotaService:
    """
        GRASP Controller
        Responsabil de efectuarea operatiilor cerute de utilizator
        Coordoneaza operatiile necesare pentru a realiza actiunea declansata de utilizator
        (i.e. declansare actiune: utilizator -> ui-> obiect tip service in ui -> service -> service coordoneaza operatiile
        folosind alte obiecte (e.g. repo, validator) pentru a realiza efectiv operatia)
        """
    def __init__(self, nota_repo, nota_validator, student_repo, lab_repo):
        """
        Initializeaza service
        :param repo: obiect de tip repo care ne ajuta sa gestionam multimea de seriale
        :type repo: InMemoryRepository
        :param validator: validator pentru verificarea serialelor
        :type validator: ShowValidator
        """
        self.__nota_repo = nota_repo
        self.__nota_validator = nota_validator
        self.__student_repo = student_repo
        self.__lab_repo = lab_repo

    def sort_list_by_grade(self, nota_list):
        """
        Returneaza lista de seriale care au mai multe episoade decat numarul dat
        :param number_of_episodes: numarul de episoade dat
        :type number_of_episodes:int
        :return: lista de seriale care indeplinesc criteriul
        :rtype: list of Serial objects
        """
        sorted_list = nota_list
        for i in range(len(sorted_list) - 1):
            for j in range(i + 1, len(sorted_list)):
                if sorted_list[i].getNota() >= sorted_list[j].getNota():
                    grade = sorted_list[j]
                    sorted_list[j] = sorted_list[i]
                    sorted_list[i] = grade

        return sorted_list

    def sort_list_alpha(self, nota_list):
        """
        Returneaza lista de seriale care au mai multe episoade decat numarul dat
        :param number_of_episodes: numarul de episoade dat
        :type number_of_episodes:int
        :return: lista de seriale care indeplinesc criteriul
        :rtype: list of Serial objects

        """
        sorted_list = nota_list
        for i in range(len(sorted_list) - 1):
            for j in range(i + 1, len(sorted_list)):
                if sorted_list[i].getStudent().getNume() >= sorted_list[j].getStudent().getNume():
                    grade = sorted_list[j]
                    sorted_list[j] = sorted_list[i]
                    sorted_list[i] = grade

        return sorted_list

    def average_grade(self, student_id):
        all_grades = self.get_all()
        sum = 0
        t= 0

        for i in range(len(all_grades)):
            if all_grades[i].getStudent().getID() == student_id:
                sum = sum + all_grades[i].getNota()
                t = t + 1

        return float(sum/t)

    def nr_note_per_lab(self, nrlab_nrprobl):
        all_grades = self.get_all()
        nr = 0

        for i in range(len(all_grades)):
            if all_grades[i].getLab().getNR() == nrlab_nrprobl:
                nr = nr + 1

        return nr

    def find_duplicate_lab(self, nr, lab_list):
        """
                Cauta nota cu id-ul dat
                :param student_id:
                :return:
        """
        if len(lab_list) == 0:
            return None
        else:
            for i in range(len(lab_list)):
                if lab_list[i].getNR() == nr:
                    return lab_list[i]
        return None

    def lab_and_nrnote(self):
        """
        Returneaza doua liste
        :return: lista de seriale care indeplinesc criteriul
        :rtype: list of Serial objects
        """
        all_grades = self.get_all()
        lab_list = []
        nrnote_list = []

        for i in range(len(all_grades)):
            nr = all_grades[i].getLab().getNR()
            duplicat = self.find_duplicate_lab(nr, lab_list)
            if duplicat is None:
                lab = all_grades[i].getLab()
                nr = self.nr_note_per_lab(all_grades[i].getLab().getNR())
                nrnote_list.append(nr)
                lab_list.append(lab)

        return lab_list, nrnote_list

    def sort_list_by_nrnote_desc(self, lab_list, nrnote_list):
        """
        Returneaza 2 liste sortate: cu laboratoare si cu note
        :param lab_list:
        :type lab_list: list
        :param nrnote_list:
        :type nrnote_list: list
        :return: liste sortate
        :rtype: list of Laborator objects, list of nrnote
        """
        sorted_list_lab = lab_list
        sorted_nrnote_list = nrnote_list
        for i in range(len(sorted_list_lab) - 1):
            for j in range(i + 1, len(sorted_list_lab)):
                if sorted_nrnote_list[i] <= sorted_nrnote_list[j]:
                    nr = sorted_nrnote_list[i]
                    sorted_nrnote_list[i] = sorted_nrnote_list[j]
                    sorted_nrnote_list[j] = nr

                    lab = sorted_list_lab[j]
                    sorted_list_lab[j] = sorted_list_lab[i]
                    sorted_list_lab[i] = lab

        return sorted_list_lab, sorted_nrnote_list

    def find_duplicate(self, student_id, list):
        """
        Cauta un student deja existent in lista filtrata
        :param student_id:
        :return:
        """
        if len(list) == 0:
            return None
        else:
            for i in range(len(list)):
                if list[i].getID() == student_id:
                    return list[i]
        return None

    def filter_by_average_grade(self):
        """
        Returneaza 2 liste: una cu studenti si una cu media notelor lor (<=5)
        :return: listele care indeplinesc criteriul
        :rtype: list of Students objects, list of average grade
        """
        all_grades = self.get_all()
        filtered_list = []
        mediile = []

        for i in range(len(all_grades)):
            if self.average_grade(all_grades[i].getStudent().getID()) <= 5:
                id = all_grades[i].getStudent().getID()
                duplicat = self.find_duplicate(id, filtered_list)
                if duplicat is None:
                    grade = all_grades[i]
                    student = all_grades[i].getStudent()
                    avg = self.average_grade(all_grades[i].getStudent().getID())
                    mediile.append(avg)
                    filtered_list.append(student)

        return filtered_list, mediile

    def find_already_assigned(self,  student_id, nrlab_nrprobl):
        all_grades = self.get_all()

        for i in range(len(all_grades)):
            if all_grades[i].getStudent().getID() == student_id and all_grades[i].getLab().getNR() == nrlab_nrprobl:
                return all_grades[i]
        return None

    def create_nota(self, student_id, nrlab_nrprobl, nota):
        """
        Creeaza un rating
        :param show_id: id-ul show-ului evaluat
        :type show_id: str
        :param client_id: id-ul clientului care evalueaza
        :type client_id: str
        :param no_stars: numarul de stele acordate serialului (1-5)
        :type no_stars: float
        :return: rating-ul creat cu datele date
        :rtype: Rating
        :raises: ShowNotFoundException
                 ClientNotFoundException
                 ValidationException
                 RatingAlreadyAssignedException
        """
        student = self.__student_repo.find(student_id)
        if student is None:
            #raise ValueError('Nu exista student cu acest ID.')
            raise StudentNotFoundException()

        laborator = self.__lab_repo.find(nrlab_nrprobl)

        if laborator is None:
            #raise ValueError('Nu exista problema cu acest NR.')
            raise LaboratorNotFoundException()

        grade_dupe = self.find_already_assigned(student_id, nrlab_nrprobl)
        if grade_dupe is not None:
            #raise ValueError('Exista deja o nota assignata acestui student si acestei probleme.')
            raise GradeAlreadyAssignedException()

        grade = Nota(laborator, student, nota)
        #if self.__nota_validator.validate(grade) is not None:
            #raise GradeNotValid()
        self.__nota_validator.validate(grade)
        self.__nota_repo.store(grade)
        return grade

    def get_all(self):
        return self.__nota_repo.get_all_grades()

    def generate_grades(self):
        """
        Genereaza note pt studenti
        :return: obiectele de tip Nota create
        :rtype:-; notele care s-au adaugat in lista
        :raises: -
        """
        s = Student(8104, 'Radu Boxeru', 925)
        l = Laborator(305, 'Alg de sortare', '27.03.2022')
        n = Nota(l, s, 9)

        self.__nota_validator.validate(n)
        self.__nota_repo.store(n)

        s = Student(8104, 'Radu Boxeru', 925)
        l = Laborator(101, 'Algoritm Nr Prim', '22.11.2021')
        n = Nota(l, s, 1)

        self.__nota_validator.validate(n)
        self.__nota_repo.store(n)

        s = Student(8104, 'Radu Boxeru', 925)
        l = Laborator(202, 'Algoritm Oglindit', '10.12.2021')
        n = Nota(l, s, 3)

        self.__nota_validator.validate(n)
        self.__nota_repo.store(n)

        s = Student(1221, 'Alina Soare', 211)
        l = Laborator(305, 'Alg de sortare', '27.03.2022')
        n = Nota(l, s, 10)

        self.__nota_validator.validate(n)
        self.__nota_repo.store(n)

        s = Student(1234, 'Calin Dancea', 213)
        l = Laborator(305, 'Alg de sortare', '27.03.2022')
        n = Nota(l, s, 6)

        self.__nota_validator.validate(n)
        self.__nota_repo.store(n)

        s = Student(3799, 'Iulia Negrila', 925)
        l = Laborator(305, 'Alg de sortare', '27.03.2022')
        n = Nota(l, s, 10)

        self.__nota_validator.validate(n)
        self.__nota_repo.store(n)

        s = Student(1574, 'Lorena Berchesan', 122)
        l = Laborator(301, 'Proiect Cheltuieli cu stergeri si adaugari', '19.01.2022')
        n = Nota(l, s, 4)

        self.__nota_validator.validate(n)
        self.__nota_repo.store(n)

        s = Student(3799, 'Tudor Timis', 931)
        l = Laborator(202, 'Algoritm Oglindit', '10.12.2021')
        n = Nota(l, s, 7)

        self.__nota_validator.validate(n)
        self.__nota_repo.store(n)

        return n

def test_create_grade():
    nota_repo = InMemoryRepository_Grade()
    nota_validator = NotaValidator()
    student_repo = InMemoryRepository_Stud()
    lab_repo = InMemoryRepository_Lab()
    test_srv = NotaService(nota_repo, nota_validator, student_repo, lab_repo)

    s = Student(8104, 'Radu Boxeru', 925)
    l = Laborator(305, 'Alg de sortare', '27.03.2022')
    n = Nota(l, s, 8)

    nota_validator.validate(n)
    nota_repo.store(n)

    #added_grade = test_srv.create_nota(1221, 101, 8)
    assert (n.getStudent().getID() == 8104)
    assert (n.getLab().getNR() == 305)
    assert (n.getNota() == 8)

    assert (len(test_srv.get_all()) == 1)
'''
    try:
        added_show = test_srv.add_show('See', 1200, 12)
        assert False
    except ValueError:
        assert True
'''

def test_avg_grade():
    nota_repo = InMemoryRepository_Grade()
    nota_validator = NotaValidator()
    student_repo = InMemoryRepository_Stud()
    lab_repo = InMemoryRepository_Lab()
    test_srv = NotaService(nota_repo, nota_validator, student_repo, lab_repo)

    #added_grade = test_srv.create_nota(1221, 101, 9)

    s = Student(8104, 'Radu Boxeru', 925)
    l = Laborator(305, 'Alg de sortare', '27.03.2022')
    n = Nota(l, s, 9)

    nota_validator.validate(n)
    nota_repo.store(n)

    s = Student(8104, 'Radu Boxeru', 925)
    l = Laborator(606, 'Alg', '29.03.2022')
    n = Nota(l, s, 6)

    nota_validator.validate(n)
    nota_repo.store(n)

    assert (test_srv.average_grade(n.getStudent().getID()) == 7.5)

def test_nr_note_per_lab():
    nota_repo = InMemoryRepository_Grade()
    nota_validator = NotaValidator()
    student_repo = InMemoryRepository_Stud()
    lab_repo = InMemoryRepository_Lab()
    test_srv = NotaService(nota_repo, nota_validator, student_repo, lab_repo)

    s = Student(8104, 'Radu Boxeru', 925)
    l = Laborator(305, 'Alg de sortare', '27.03.2022')
    n = Nota(l, s, 9)

    nota_validator.validate(n)
    nota_repo.store(n)

    s = Student(1221, 'Alina Soare', 925)
    l = Laborator(305, 'Alg de sortare', '27.03.2022')
    n = Nota(l, s, 6)

    nota_validator.validate(n)
    nota_repo.store(n)

    assert (test_srv.nr_note_per_lab(n.getLab().getNR()) == 2)

#test_avg_grade()
#test_create_grade()
#test_nr_note_per_lab()