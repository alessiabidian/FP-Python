import unittest
from domain.entities import Nota, Student, Laborator
from domain.validators import NotaValidator
from exceptions.exceptions import ValidationException, GradeNotFoundException
from repository.grades_repo import InMemoryRepository_Grade
from repository.labs_repo import InMemoryRepository_Lab
from repository.studs_repo import InMemoryRepository_Stud
from service.grades_service import NotaService


class TestCaseGradeService(unittest.TestCase):
    def setUp(self) -> None:
        repo = InMemoryRepository_Grade()
        student_repo = InMemoryRepository_Stud()
        lab_repo = InMemoryRepository_Lab()
        validator = NotaValidator()
        self.__srv = NotaService(repo, validator, student_repo, lab_repo)

    def test_create_grade(self):
        s = Student(1574, 'Lorena Berchesan', 122)
        InMemoryRepository_Stud().store(s)
        InMemoryRepository_Lab().store(Laborator(101, 'Algoritm Nr Prim', '22.11.2021'))
        self.assertEqual(len(InMemoryRepository_Stud().get_all_students()), 1)
        added_grade = self.__srv.create_nota(1574, 101, 7)
        self.assertTrue(added_grade.getStudent().getID() == 1574)
        self.assertTrue(added_grade.getLab().getNR() == 101)

        self.assertEqual(len(self.__srv.get_all()), 1)
        #self.assertRaises(ValidationException, self.__srv.add_show, '2', 'See', 1200, 12)

    def test_get_all_shows(self):
        pass
        """added_grade = self.__srv.create_nota(1574, 101, 7)
        added_grade = self.__srv.create_nota(1574, 101, 7)
        self.assertIsInstance(self.__srv.get_all_shows(), list)
        self.assertEqual(len(self.__srv.get_all_shows()), 2)"""

#unittest.main()