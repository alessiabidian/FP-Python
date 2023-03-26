from domain.entities import Laborator
from exceptions.exceptions import DuplicateIDException, LaboratorNotFoundException

class InMemoryRepository_Lab:
    """
        Clasa creata cu responsabilitatea de a gestiona
        multimea de probleme de lab (i.e. sa ofere un depozit persistent pentru obiecte
        de tip laborator)
    """
    def __init__(self):
        #labs - multimea de probleme de lab pe care o gestionam

        self.__labs = []

    def find(self, id):
        """
        Cauta studentul cu id dat
        :param student_id:
        :return:
        """
        for laborator in self.__labs:
            if laborator.getNR() == id:
                return laborator
        return None

    def size(self):
        """

        :return:
        """
        return len(self.__labs)

    def store(self, laborator):
        """
        Adauga un lab in lista
        :param laborator: problema de lab care se adauga
        :type laborator: Laborator
        :return: -; lista de probleme se modifica prin adaugarea problemei date
        :rtype:
        """
        if self.find(laborator.getNR()) is not None:
            #raise ValueError('Exista deja problema cu acest nr.')
            raise DuplicateIDException()
        self.__labs.append(laborator)

    def update(self, nrlab_nrprobl, modified_laborator):
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

        laborator = self.find(nrlab_nrprobl)
        if laborator is None:
            #raise ValueError('Nu exista problema de laborator cu acest id.')
            raise LaboratorNotFoundException()

        laborator.setNR(modified_laborator.getNR())
        laborator.setDescriere(modified_laborator.getDescriere())
        laborator.setDeadline(modified_laborator.getDeadline())
        return laborator

    def delete_by_nrprobl(self, nrprobl):
        """
        Sterge labul dupa id
        :param id: id-ul dat
        :type id: int
        :param id:
        :return:
        """
        #self.__students = [student for student in self.__students if not student.getID() == id]
        laborator = self.find(nrprobl)
        if laborator is None:
            #raise ValueError('Nu exista problema cu acest id pt a fi sters.')
            raise LaboratorNotFoundException()

        self.__labs.remove(laborator)
        return laborator

    def get_all_labs(self):
        """
        Returneaza o lista cu toate lab-urile existente
        :rtype: list of objects de tip Lab
        """
        return self.__labs

class LabFileRepoInheritance(InMemoryRepository_Lab):
    def __init__(self, filename):
        InMemoryRepository_Lab.__init__(self)
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
            #lab = [token.strip() for token in line.split(';')]
            #nrlab_nrprobl = int(lab[0])
            #descriere = str(lab[1])
            #deadline = str(lab[2])
        for i in range(0, dim, 3):
            nrlab_nrprobl, descriere, deadline = [lines[i].strip(), lines[i+1].strip(), lines[i+2].strip()]
            a = Laborator(int(nrlab_nrprobl), str(descriere), str(deadline))
            InMemoryRepository_Lab.store(self, a)
        f.close()

    def __save_to_file(self):
        laborator_list = InMemoryRepository_Lab.get_all_labs(self)
        with open(self.__filename, 'w') as f:
            for laborator in laborator_list:
                #laborator_string = str(laborator.getNR()) + ';' + str(laborator.getDescriere()) + ';' + str(
                    #laborator.getDeadline()) + '\n'
                laborator_string = str(laborator.getNR()) + '\n' + str(laborator.getDescriere()) + '\n' + str(
                    laborator.getDeadline()) + '\n'
                f.write(laborator_string)

    def store_from_file(self, laborator):
        InMemoryRepository_Lab.store(self, laborator)
        self.__save_to_file()

    def update(self, id, new_laborator):
        updated_laborator = InMemoryRepository_Lab.update(self, id, new_laborator)
        self.__save_to_file()
        return updated_laborator

    def delete_by_nrprobl(self, nr):
        deleted_laborator = InMemoryRepository_Lab.delete_by_nrprobl(self, nr)
        self.__save_to_file()
        return deleted_laborator

    def get_all_labs(self):
        return InMemoryRepository_Lab.get_all_labs(self)

    def size(self):
        return InMemoryRepository_Lab.size(self)

    def find(self, nr):
        return InMemoryRepository_Lab.find(self, nr)


def test_store_labs():
    test_repo = InMemoryRepository_Lab()
    lab1 = Laborator(704, 'Alg de nr egale', '06.06.2022')
    test_repo.store(lab1)

    assert(test_repo.size() == 1)

def test_delete_by_nrprobl():
    test_repo = InMemoryRepository_Lab()
    lab1 = Laborator(704, 'Alg de palindrom', '06.06.2022')
    test_repo.store(lab1)
    lab2 = Laborator(705, 'Alg de backtracking', '24.02.2022')
    test_repo.store(lab2)

    deleted_lab = test_repo.delete_by_nrprobl(704)
    assert (deleted_lab.getDescriere() == 'Alg de palindrom')
    assert (test_repo.size() == 1)

    lab_left = test_repo.find(705)
    assert (lab_left.getDescriere() == 'Alg de backtracking')

    try:
        test_repo.delete_by_nrprobl('wrongid')
        assert False
    except ValueError:
        assert True


def test_update():
    test_repo = InMemoryRepository_Lab()
    lab1 = Laborator(704, 'Alg de palindrom', '06.06.2022')
    test_repo.store(lab1)
    lab2 = Laborator(705, 'Alg de backtracking', '24.02.2022')
    test_repo.store(lab2)
    lab3 = Laborator(709, 'Alg de nr prim', '24.02.2022')

    modified_lab = test_repo.update(705, lab3)
    assert (modified_lab.getDescriere() == 'Alg de nr prim')
    assert (modified_lab.getDeadline() == '24.02.2022')
'''
    try:
        test_repo.update(109, Laborator(109, 'Alg de nr prim', '24.02.2022'))
        assert False
    except ValueError:
        assert True

test_store_labs()
test_delete_by_nrprobl()
test_update()
'''