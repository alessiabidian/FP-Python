import unittest

from domain.entities import Laborator
from exceptions.exceptions import DuplicateIDException, LaboratorNotFoundException
from repository.labs_repo import InMemoryRepository_Lab, LabFileRepoInheritance


"""class TestCaseInMemoryRepository_Lab(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = InMemoryRepository_Lab()
        self.__add_predefined_students()

    def __add_predefined_students(self):
        l1 = Laborator(101, 'Algoritm Nr Prim', '22.11.2021')
        l2 = Laborator(202, 'Algoritm Oglindit', '10.12.2021')
        l3 = Laborator(301, 'Proiect Cheltuieli cu stergeri si adaugari','19.01.2022')
        l4 = Laborator(305, 'Alg de sortare', '27.03.2022')
        l5 = Laborator(404, 'Alg de backtracking', '10.05.2022')

        self.__repo.store(l1)
        self.__repo.store(l2)
        self.__repo.store(l3)
        self.__repo.store(l4)
        self.__repo.store(l5)

    def test_find(self):
        p = self.__repo.find(202)
        self.assertTrue(p.getDescriere() == 'Algoritm Oglindit')
        self.assertTrue(p.getDeadline() == '10.12.2021')

        p1 = self.__repo.find(910)
        self.assertIs(p1, None)

    def test_size(self):
        self.assertEqual(self.__repo.size(), 5)

        self.__repo.delete_by_nrprobl(101)
        self.__repo.delete_by_nrprobl(404)

        self.assertEqual(self.__repo.size(), 3)

        self.__repo.store(Laborator(402, 'Alg de suma', '21.06.2022'))
        self.assertEqual(self.__repo.size(), 4)
        self.__repo.store(Laborator(403, 'Proiect de liste cu stergeri', '01.06.2022'))
        self.assertEqual(self.__repo.size(), 5)

    def test_get_all(self):
        crt_labs = self.__repo.get_all_labs()
        self.assertIsInstance(crt_labs, list)

        self.assertEqual(len(crt_labs), 5)

        self.__repo.delete_by_nrprobl(202)

        crt_labs = self.__repo.get_all_labs()
        self.assertEqual(len(crt_labs), 4)

    def test_store(self):
        initial_size = self.__repo.size()
        l = Laborator(501, 'Alg de nr prime intre ele', '03.03.2022')
        self.__repo.store(l)

        self.assertEqual(self.__repo.size(), initial_size + 1)

    def test_update(self):
        laborator3 = Laborator(502, 'Proiect cu undo', '13.02.2022')

        modified_lab = self.__repo.update(301, laborator3)
        self.assertEqual(modified_lab.getDescriere(), 'Proiect cu undo')
        self.assertEqual(modified_lab.getDeadline(), '13.02.2022')
        #self.assertRaises(ClientNotFoundException, self.__repo.update, '243545', Client(3, 'Alfred', 67))
"""

class TestCaseStudFileRepoInheritance(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = LabFileRepoInheritance('test_labs_repo.txt')

    def test_find(self):
        p = self.__repo.find(202)
        self.assertTrue(p.getDescriere() == 'Algoritm Oglindit')
        self.assertTrue(p.getDeadline() == '10.12.2021')

        p1 = self.__repo.find(910)
        self.assertIs(p1, None)

    def test_size(self):
        self.assertEqual(self.__repo.size(), 4)

        deleted1 = self.__repo.delete_by_nrprobl(101)
        deleted2 = self.__repo.delete_by_nrprobl(404)
        self.assertTrue(deleted1.getNR() == 101)
        self.assertTrue(deleted2.getNR() == 404)

        self.assertEqual(self.__repo.size(), 2)

        self.__repo.store_from_file(Laborator(402, 'Alg de suma', '21.06.2022'))
        self.assertEqual(self.__repo.size(), 3)
        self.__repo.store_from_file(Laborator(403, 'Proiect de liste cu stergeri', '01.06.2022'))
        self.assertEqual(self.__repo.size(), 4)

    def test_get_all(self):
        crt_labs = self.__repo.get_all_labs()
        self.assertIsInstance(crt_labs, list)

        self.assertEqual(len(crt_labs), 5)

        self.__repo.delete_by_nrprobl(202)

        crt_labs = self.__repo.get_all_labs()
        self.assertEqual(len(crt_labs), 4)

    def test_store(self):
        initial_size = self.__repo.size()
        l1 = Laborator(501, 'Algoritmi ...', '23.03.2023')
        self.__repo.store_from_file(l1)

        self.assertEqual(self.__repo.size(), initial_size + 1)

    def test_update(self):
        l3 = Laborator(506, 'Algoritm suma factori primi', '25.07.2022')

        modified_lab = self.__repo.update(301, l3)
        self.assertEqual(modified_lab.getDescriere(), 'Algoritm suma factori primi')
        self.assertEqual(modified_lab.getDeadline(), '25.07.2022')


unittest.main()