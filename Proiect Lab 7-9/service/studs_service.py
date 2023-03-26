from domain.entities import Student
from domain.validators import StudentValidator
from repository.studs_repo import StudFileRepoInheritance, InMemoryRepository_Stud
from operator import lt, gt
from functools import reduce

class StudentService:
    """
        GRASP Controller
        Responsabil de efectuarea operatiilor cerute de utilizator
        Coordoneaza operatiile necesare pentru a realiza actiunea declansata de utilizator
        (i.e. declansare actiune: utilizator -> ui-> obiect tip service in ui -> service -> service coordoneaza operatiile
        folosind alte obiecte (e.g. repo, validator) pentru a realiza efectiv operatia)
        """
    def __init__(self, repo, validator):
        """
        Initializeaza service
        :param repo: obiect de tip repo care ne ajuta sa gestionam multimea de studenti
        :type repo: InMemoryRepository_Stud
        :param validator: validator pentru verificarea studentilor
        :type validator: StudentValidator
        """
        self.__repo = repo
        self.__validator = validator

    def add_student(self, student_id, nume, grup):
        """
        Adauga student
        :param student_id: id-ul studentului
        :type student_id: int
        :param nume: numele studentului
        :type nume: str
        :param grup: numarul de grup al studentului
        :type grup: int
        :return: obiectul de tip Student creat
        :rtype:-; studentul s-a adaugat in lista
        :raises: ValueError daca studentul are date invalide, daca id-ul exista deja in lista
        """
        s = Student(student_id, nume, grup)

        self.__validator.validate(s)
        self.__repo.store_from_file(s)
        #self.__repo.store(s)
        return s

    def add_student_clasic(self, student_id, nume, grup):
        """
        Adauga student
        :param student_id: id-ul studentului
        :type student_id: int
        :param nume: numele studentului
        :type nume: str
        :param grup: numarul de grup al studentului
        :type grup: int
        :return: obiectul de tip Student creat
        :rtype:-; studentul s-a adaugat in lista
        :raises: ValueError daca studentul are date invalide, daca id-ul exista deja in lista
        """
        s = Student(student_id, nume, grup)

        self.__validator.validate(s)
        #self.__repo.store_from_file(s)
        self.__repo.store(s)
        return s

    def generate_students(self):
        """
        Genereaza studenti
        :return: obiectele de tip Student create
        :rtype:-; studentii care s-au adaugat in lista
        :raises: -
        """
        s = Student(1221, 'Alina Soare', 211)

        self.__validator.validate(s)
        self.__repo.store(s)
        print("hahaha muie")

        s = Student(8104, 'Radu Boxeru', 925)

        self.__validator.validate(s)
        self.__repo.store(s)

        s = Student(1234, 'Calin Dancea', 213)

        self.__validator.validate(s)
        self.__repo.store(s)

        s = Student(1574, 'Lorena Berchesan', 122)

        self.__validator.validate(s)
        self.__repo.store(s)

        s = Student(3799, 'Iulia Negrila', 925)

        self.__validator.validate(s)
        self.__repo.store(s)

        s = Student(2004, 'Tudor Timis', 931)

        self.__validator.validate(s)
        self.__repo.store(s)

        return s

    def get_all_students(self):
        """
        Returneaza o lista cu toti studentii disponibili
        :return: lista de studenti disponibili
        :rtype: list of objects de tip Student
        """
        return self.__repo.get_all_students()

    def delete_students(self, student_id):
        return self.__repo.delete_by_id(student_id)

    def update_student(self, student_id, nume, grup):
        """
        Modifica datele serialului cu id dat
        :param id: id-ul serialului de modificat
        :type id: str
        :param titlu: noul titlu al serialului
        :type titlu: str
        :param an_aparitie: noul an de aparitie al serialului
        :type an_aparitie: int
        :param eps: noul numar de episoade pentru serial
        :type eps: int
        :return: serialul modificat
        :rtype:Serial
        :raises: ValueError daca noile date nu sunt valide, sau nu exista serial cu id dat
        """
        s = Student(student_id, nume, grup)

        self.__validator.validate(s)
        return self.__repo.update(student_id, s)

    def delete_by_grup(self, grup):
        """
        Sterge toate serialele din perioada year_start - year_end
        :param year_start: anul de inceput al perioadei
        :type year_start: int
        :param year_end: anul de sfarsit al perioadei
        :type year_end: int (year_start < year_end)
        :return: numarul de seriale sterse
        :rtype: int
        """
        existenta_grup = self.__repo.find_grup(grup)
        if existenta_grup is None:
            raise ValueError('Nu exista aceasta grupa pt a fi stearsa.')

        how_many_deleted = self.__repo.delete_by_criteria(
            lambda x: x.getGrup() == grup)
        return how_many_deleted

    def filter_by_id(self, student_id):
        """
        Returneaza lista de seriale care au mai multe episoade decat numarul dat
        :param number_of_episodes: numarul de episoade dat
        :type number_of_episodes:int
        :return: lista de seriale care indeplinesc criteriul
        :rtype: list of Serial objects
        """
        student = self.__repo.find_r(student_id)
        if student is None:
            raise ValueError('Nu exista student cu acest id pt a fi afisat.')

        all_studs = self.get_all_students()
        filtered_list = [student for student in all_studs if student.getID() == student_id]
        return filtered_list

    def filter_by_grup(self, grup):
        """
        Returneaza lista de seriale care au mai multe episoade decat numarul dat
        :param number_of_episodes: numarul de episoade dat
        :type number_of_episodes:int
        :return: lista de seriale care indeplinesc criteriul
        :rtype: list of Serial objects
        """
        existenta_grup = self.__repo.find_grup_r(grup)
        if existenta_grup is None:
            raise ValueError('Nu exista aceasta grupa pt a fi afisata.')

        all_studs = self.get_all_students()
        filtered_list = [student for student in all_studs if student.getGrup() == grup]
        return filtered_list

    def comp(self, x, y, key, func):
        return func(self.find_key(x, key), self.find_key(y, key))

    def comp2(self, x, y, key, key2, func):
        if self.find_key(x, key) == self.find_key(y, key):
            return func(self.find_key(x, key2), self.find_key(y, key2))
        else:
            return func(self.find_key(x, key), self.find_key(y, key))

    def comp_combinat(self, x, y, func):
        if x.getGrup() == y.getGrup():
            return func(x.getID(), y.getID())
        else:
            return func(x.getGrup(), y.getGrup())

    def mergeSort(self, list, key=None, reversed=False, cmp=comp2):
       if len(list) > 1:

          # Finding the mid of the array
          mid = len(list) // 2

          # Dividing the array elements
          L = list[:mid]

          # into 2 halves
          R = list[mid:]

          # Sorting the first half
          self.mergeSort(L, key, reversed)

          # Sorting the second half
          self.mergeSort(R, key, reversed)

          i = j = k = 0

          # Copy data to temp arrays L[] and R[]
          while i < len(L) and j < len(R):
              key2 = 'id'
              #if cmp(self, self.find_key(L[i], key), self.find_key(R[j], key), (gt if reversed else lt)):
              if cmp(self, L[i], R[j], key, key2, (gt if reversed else lt)):
                  list[k] = L[i]
                  i += 1
              #elif cmp(self, self.find_key(L[i], key), self.find_key(R[j], key), (gt if reversed else lt)) == False:
              elif cmp(self, L[i], R[j], key, key2, (gt if reversed else lt)) == False:
                  list[k] = R[j]
                  j += 1
              k += 1

          # Checking if any element was left
          while i < len(L):
             list[k] = L[i]
             i += 1
             k += 1

          while j < len(R):
             list[k] = R[j]
             j += 1
             k += 1

    def find_key(self, element, key):
        if key == 'id':
            return element.getID()
        elif key == 'grup':
            return element.getGrup()
        elif key == 'nume':
            return element.getNume()
        else:
            return element.getID()

    def comp3(self, x, y, key, key2, func):
        idx = int(self.find_key(x, key))*10000 + int(self.find_key(x, key2))
        idy = int(self.find_key(y, key))*10000 + int(self.find_key(y, key2))

        return func(idx, idy)

    def BingoSort(self, arr, key=None, reversed=False, cmp=comp3):
       last = len(arr) - 1
       nextmax = arr[last]
       ciclari = 0
       key2 = 'id'


       for i in range (last-1, -1, -1):
          #if cmp(self, self.find_key(nextmax, key), self.find_key(arr[i], key), (gt if reversed else lt)):
          if cmp(self, nextmax, arr[i], key, key2, (gt if reversed else lt)):
              nextmax = arr[i]
              ciclari = ciclari + 1


       #while last > 0 and self.find_key(arr[last], key2) == self.find_key(nextmax, key2):
       while last > 0 and (int(self.find_key(arr[last], key))*10000 + int(self.find_key(arr[last], key2))) == (int(self.find_key(nextmax, key))*10000 + int(self.find_key(nextmax, key2))):
          last = last - 1
          ciclari = ciclari + 1

       while last > 0:
          prevmax = nextmax
          nextmax = arr[last]
          ciclari = ciclari + 1
          for i in range (last-1, -1, -1):
             ciclari = ciclari + 1
             #if cmp(self, self.find_key(nextmax, key), self.find_key(arr[i], key), (gt if reversed else lt)) :
             if cmp(self, nextmax, arr[i], key, key2, (gt if reversed else lt)):
                #if self.find_key(arr[i], key) != self.find_key(prevmax, key):
                if int(self.find_key(arr[i], key))*10000 + int(self.find_key(arr[i], key2)) != int(self.find_key(prevmax, key))*10000 + int(self.find_key(prevmax, key2)):
                   nextmax = arr[i]
                else:
                   arr[i], arr[last] = arr[last], arr[i]
                   last = last - 1

          #while last > 0 and self.find_key(arr[last], key) == self.find_key(nextmax, key):
          while last > 0 and (int(self.find_key(arr[last], key))*10000 + int(self.find_key(arr[last], key2))) == (int(self.find_key(nextmax, key))*10000 + int(self.find_key(nextmax, key2))):
             last = last - 1
             ciclari = ciclari + 1
       print(ciclari)

    def bingo(self, list, key=None, reversed=False, cmp=comp2):
        last = len(list) - 1
        #maxx = list[last]
        key2 = 'id'
        #key2 = key
        while last > 0:
            maxx = list[last]
            ok = 0
            for i in range (last-1, -1, -1):
                if cmp(self, maxx, list[i], key, key2, (gt if reversed else lt)):
                    maxx = list[i]
                    imaxx = i
                    ok = 1
            if ok == 1:
                list[last], list[imaxx] = list[imaxx], list[last]
            last = last - 1

    def keyID(self, val):
        return val.getID()

    def keyNume(self, val):
        return val.getNume()

    def keyGrup(self, val):
        return val.getGrup()

    def keyNone(self, val):
        return val

    def cmp_combinat(self, val1, val2):
        if self.keyGrup(val1) > self.keyGrup(val2):
            return 1
        if self.keyGrup(val1) == self.keyGrup(val2):
            if self.keyID(val1) > self.keyID(val2):
                return 1
            else:
                return -1
        if self.keyGrup(val1) < self.keyGrup(val2):
            return -1

    def cmp(self, val1, val2):
        if val1 > val2:
            return 1
        if val1 == val2:
            return 0
        if val1 < val2:
            return -1

    def merge_sort(self, list, key, reversed, cmp):
        if len(list) > 1:

            # Finding the mid of the array
            mid = len(list) // 2

            # Dividing the array elements
            L = list[:mid]

            # into 2 halves
            R = list[mid:]

            # Sorting the first half
            self.merge_sort(L, key, reversed, cmp)

            # Sorting the second half
            self.merge_sort(R, key, reversed, cmp)

            i = j = k = 0

            # Copy data to temp arrays L[] and R[]
            if reversed == False:
                while i < len(L) and j < len(R):
                    if cmp(key(L[i]), key(R[j])) < 0:
                        list[k] = L[i]
                        i += 1
                    elif cmp(key(L[i]), key(R[j])) >= 0:
                        list[k] = R[j]
                        j += 1
                    k += 1
            else:
                while i < len(L) and j < len(R):
                    if cmp(key(L[i]), key(R[j])) > 0:
                        list[k] = L[i]
                        i += 1
                    elif cmp(key(L[i]), key(R[j])) <= 0:
                        list[k] = R[j]
                        j += 1
                    k += 1

            # Checking if any element was left
            while i < len(L):
               list[k] = L[i]
               i += 1
               k += 1

            while j < len(R):
               list[k] = R[j]
               j += 1
               k += 1

    def bingo_sort(self, list, key, reversed, cmp):
        if len(list) <= 1:
            return list
        if reversed == True:
            swap_val = reduce(lambda val, current: current if cmp(key(current), key(val)) >= 0 else val, list)
        else:
            swap_val = reduce(lambda val, current: current if cmp(key(current), key(val)) < 0 else val, list)
        index_swap = 0
        while index_swap < len(list):
            index_current = index_swap
            next_val = list[index_current]
            if reversed:
                while index_current < len(list):
                    if cmp(key(list[index_current]), key(next_val)) >= 0:
                        next_val = list[index_current]
                    if key(list[index_current]) == key(swap_val):
                        list[index_swap], list[index_current] = list[index_current], list[index_swap]
                        index_swap = index_swap + 1
                    index_current = index_current + 1
                swap_val = next_val
            else:
                while index_current < len(list):
                    if cmp(key(list[index_current]), key(next_val)) < 0:
                        next_val = list[index_current]
                    if key(list[index_current]) == key(swap_val):
                        list[index_swap], list[index_current] = list[index_current], list[index_swap]
                        index_swap = index_swap + 1
                    index_current = index_current + 1
                swap_val = next_val
        return list

def test_add_student():
    repo = StudFileRepoInheritance()
    validator = StudentValidator()
    test_srv = StudentService(repo, validator)

    added_student = test_srv.add_student(7013, 'Dan Barna', 117)
    assert (added_student.getNume()=='Dan Barna')
    assert (added_student.getID()==7013)
    assert (added_student.getGrup() == 117)

    assert (len(test_srv.get_all_students()) == 1)


def test_delete_by_id():
    repo = InMemoryRepository_Stud()
    validator = StudentValidator()
    test_srv = StudentService(repo, validator)
    test_srv.generate_students()

    list_dlt_student = test_srv.delete_students(1221)
    assert (list_dlt_student.getID() == 1221)

def test_update_student():
    repo = InMemoryRepository_Stud()
    validator = StudentValidator()
    test_srv = StudentService(repo, validator)

    test_srv.add_student(1349, 'Alexia Nistor', 217)
    updated_student = test_srv.update_student(1349, 'Alexia Tania Nistor', 217)

    assert (updated_student.getNume() == 'Alexia Tania Nistor')
    assert (updated_student.getGrup() == 217)

    try:
        test_srv.update_student('INVALID ID', 'Alexia Nistor', 217)
        assert False
    except ValueError:
        assert True

def test_filter_by_id():
    repo = InMemoryRepository_Stud()
    validator = StudentValidator()
    test_srv = StudentService(repo, validator)

    test_srv.add_student(1349, 'Alexia Nistor', 217)
    test_srv.add_student(1350, 'Lorena Petrut', 218)
    test_srv.add_student(1669, 'Luana Cicios', 923)

    filtered_list = test_srv.filter_by_id(1349)
    assert (len(filtered_list)==1)
    assert (len(test_srv.get_all_students()) == 3)



