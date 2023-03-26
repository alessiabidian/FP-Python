from domain.entities import Laborator
from repository.labs_repo import InMemoryRepository_Lab
from domain.validators import LaboratorValidator

class LaboratorService:
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
        :param repo: obiect de tip repo care ne ajuta sa gestionam multimea de probleme de lab
        :type repo: InMemoryRepository_Lab
        :param validator: validator pentru verificarea serialelor
        :type validator: LaboratorValidator
        """
        self.__repo = repo
        self.__validator = validator

    def add_laborator(self, nrlab_nrprobl, descriere, deadline):
        """
        Adauga pb de lab
        :param nrlab_nrprobl: nr de problema a laboratorului
        :type nrlab_nrprobl: int
        :param descriere: descriere problemei
        :type descriere: str
        :param deadline: deadline ul problemei
        :type deadline: str
        :return: obiectul de tip Laborator creat
        :rtype:-; problema s-a adaugat in lista
        :raises: ValueError daca problema de lab are date invalide
        """
        l = Laborator(nrlab_nrprobl, descriere, deadline)

        self.__validator.validate(l)
        #self.__repo.store(l)
        self.__repo.store_from_file(l)
        return l

    def generate_labs(self):
        """
        Genereaza probleme de lab
        :return: obiectele de tip Laborator create
        :rtype:-; problemele care s-au adaugat in lista
        :raises: -
        """
        l = Laborator(101, 'Algoritm Nr Prim', '22.11.2021')

        self.__validator.validate(l)
        self.__repo.store(l)

        l = Laborator(202, 'Algoritm Oglindit', '10.12.2021')

        self.__validator.validate(l)
        self.__repo.store(l)

        l = Laborator(301, 'Proiect Cheltuieli cu stergeri si adaugari','19.01.2022')

        self.__validator.validate(l)
        self.__repo.store(l)

        l = Laborator(305, 'Alg de sortare', '27.03.2022')

        self.__validator.validate(l)
        self.__repo.store(l)

        return l

    def filter_by_nr(self, nrlab_nrprobl):
        """
        Returneaza lista de seriale care au mai multe episoade decat numarul dat
        :param number_of_episodes: numarul de episoade dat
        :type number_of_episodes:int
        :return: lista de seriale care indeplinesc criteriul
        :rtype: list of Serial objects
        """
        lab = self.__repo.find(nrlab_nrprobl)
        if lab is None:
            raise ValueError('Nu exista aceasta problema de laborator.')
        all_labs = self.get_all_labs()
        filtered_list = [laborator for laborator in all_labs if laborator.getNR() == nrlab_nrprobl]
        return filtered_list

    def delete_labs(self, nrlab_nrprobl):
        return self.__repo.delete_by_nrprobl(nrlab_nrprobl)

    def update_laborator(self, nrlab_nrprobl, descriere, deadline):
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
        l = Laborator(nrlab_nrprobl, descriere, deadline)

        self.__validator.validate(l)
        return self.__repo.update(nrlab_nrprobl, l)

    def get_all_labs(self):
        """
        Returneaza o lista cu toate problemele de lab disponibile
        :return: lista de probleme disponibile
        :rtype: list of objects de tip Laborator
        """
        return self.__repo.get_all_labs()


def test_add_lab():
    repo = InMemoryRepository_Lab()
    validator = LaboratorValidator()
    test_srv = LaboratorService(repo, validator)

    added_lab = test_srv.add_laborator(404, 'Alg nr impar', '5.12.2021')
    assert (added_lab.getNR() == 404)
    assert (added_lab.getDescriere() == 'Alg nr impar')
    assert (added_lab.getDeadline() == '5.12.2021')

    assert (len(test_srv.get_all_labs()) == 1)
'''
    try:
        added_show = test_srv.add_show('See', 1200, 12)
        assert False
    except ValueError:
        assert True
'''

def test_delete_by_nr():
    repo = InMemoryRepository_Lab()
    validator = LaboratorValidator()
    test_srv = LaboratorService(repo, validator)
    test_srv.generate_labs()

    list_dlt_lab = test_srv.delete_labss(101)
    assert (list_dlt_lab.getNR() == 101)

def test_update_laborator():
    repo = InMemoryRepository_Lab()
    validator = LaboratorValidator()
    test_srv = LaboratorService(repo, validator)

    test_srv.add_laborator(104, 'Alg de backtracking', '06.06.2022')
    updated_laborator = test_srv.update_laborator(104, 'Alg de palindrom', '07.06.2022')

    assert (updated_laborator.getDescriere() == 'Alg de palindrom')
    assert (updated_laborator.getDeadline() == '07.06.2022')

    try:
        test_srv.update_student('INVALID ID', 'Alg de palindrom', '07.06.2022')
        assert False
    except ValueError:
        assert True

def test_filter_by_nr():
    repo = InMemoryRepository_Lab()
    validator = LaboratorValidator()
    test_srv = LaboratorService(repo, validator)

    test_srv.add_laborator(104, 'Alg de backtracking', '06.06.2022')
    test_srv.add_laborator(207, 'Alg de sortare', '21.01.2022')
    test_srv.add_laborator(104, 'Alg de nr prim', '28.02.2022')

    filtered_list = test_srv.filter_by_nr(207)
    assert (len(filtered_list)==1)
    assert (len(test_srv.get_all_labs()) == 1)
'''
test_add_lab()
test_filter_by_nr()
test_update_laborator()
test_delete_by_nr()
'''