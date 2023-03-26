import unittest

from domain.validators import LaboratorValidator
from exceptions.exceptions import ValidationException, LaboratorNotFoundException
from repository.labs_repo import InMemoryRepository_Lab
from service.labs_service import LaboratorService


class TestCaseLabService(unittest.TestCase):
    def setUp(self) -> None:
        repo = InMemoryRepository_Lab()
        validator = LaboratorValidator()
        self.__srv = LaboratorService(repo, validator)

    def test_add_lab(self):

        added_lab = self.__srv.add_laborator(101, 'Algoritm Nr Prim', '22.11.2021')
        self.assertTrue(added_lab.getDescriere() == 'Algoritm Nr Prim')
        self.assertTrue(added_lab.getDeadline() == '22.11.2021')

        self.assertEqual(len(self.__srv.get_all_labs()), 1)
        #self.assertRaises(ValidationException, self.__srv.add_show, '2', 'See', 1200, 12)

    def test_delete_lab(self):

        self.__srv.add_laborator(202, 'Algoritm Oglindit', '10.12.2021')
        deleted_lab = self.__srv.delete_labs(202)

        self.assertEqual(len(self.__srv.get_all_labs()), 0)
        self.assertEqual(deleted_lab.getNR(), 202)
        self.assertEqual(deleted_lab.getDescriere(), 'Algoritm Oglindit')
        self.assertEqual(deleted_lab.getDeadline(), '10.12.2021')
        #self.assertRaises(ShowNotFoundException, self.__srv.delete_show, '2')

    def test_get_all_labs(self):

        self.__srv.add_laborator(301, 'Proiect Cheltuieli cu stergeri si adaugari','19.01.2022')
        self.__srv.add_laborator(305, 'Alg de sortare', '27.03.2022')
        self.assertIsInstance(self.__srv.get_all_labs(), list)
        self.assertEqual(len(self.__srv.get_all_labs()), 2)

    def test_update_lab(self):

        self.__srv.add_laborator(505, 'Alg de backtracking', '28.03.2022')
        updated_lab = self.__srv.update_laborator(505, 'Algoritm de backtracking', '18.09.2022')

        self.assertTrue(updated_lab.getDescriere() == 'Algoritm de backtracking')
        self.assertTrue(updated_lab.getNR() == 505)
        self.assertTrue(updated_lab.getDeadline() == '18.09.2022')
        #self.assertRaises(ShowNotFoundException,self.__srv.update_show,'INVALID ID', 'See', 2019, 16)

unittest.main()
