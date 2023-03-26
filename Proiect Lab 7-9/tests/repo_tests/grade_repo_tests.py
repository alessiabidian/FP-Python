import unittest

from domain.entities import Nota, Laborator, Student
from exceptions.exceptions import DuplicateIDException, GradeNotFoundException
from repository.grades_repo import InMemoryRepository_Grade, GradeFileRepoInheritance


class TestCaseInMemoryRepository_Grade(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = InMemoryRepository_Grade()
        self.__add_predefined_grades()

    def __add_predefined_grades(self):
        s = Student(8104, 'Radu Boxeru', 925)
        l = Laborator(305, 'Alg de sortare', '27.03.2022')
        n = Nota(l, s, 9)

        self.__repo.store(n)

        s = Student(8104, 'Radu Boxeru', 925)
        l = Laborator(101, 'Algoritm Nr Prim', '22.11.2021')
        n = Nota(l, s, 1)

        self.__repo.store(n)

        s = Student(8104, 'Radu Boxeru', 925)
        l = Laborator(202, 'Algoritm Oglindit', '10.12.2021')
        n = Nota(l, s, 3)

        self.__repo.store(n)

        s = Student(1221, 'Alina Soare', 211)
        l = Laborator(305, 'Alg de sortare', '27.03.2022')
        n = Nota(l, s, 10)

        self.__repo.store(n)

        s = Student(1234, 'Calin Dancea', 213)
        l = Laborator(305, 'Alg de sortare', '27.03.2022')
        n = Nota(l, s, 6)

        self.__repo.store(n)

        s = Student(3799, 'Iulia Negrila', 925)
        l = Laborator(305, 'Alg de sortare', '27.03.2022')
        n = Nota(l, s, 10)

        self.__repo.store(n)

        s = Student(1574, 'Lorena Berchesan', 122)
        l = Laborator(301, 'Proiect Cheltuieli cu stergeri si adaugari', '19.01.2022')
        n = Nota(l, s, 4)

        self.__repo.store(n)

        s = Student(3799, 'Tudor Timis', 931)
        l = Laborator(202, 'Algoritm Oglindit', '10.12.2021')
        n = Nota(l, s, 7)

        self.__repo.store(n)

    def test_find(self):
        s = Student(3799, 'Tudor Timis', 931)
        l = Laborator(202, 'Algoritm Oglindit', '10.12.2021')
        n = Nota(l, s, 7)
        p = self.__repo.find(n)
        self.assertTrue(n.getStudent().getID() == 3799)
        self.assertTrue(n.getLab().getDescriere() == 'Algoritm Oglindit')

        n = Nota(l, s, 10)
        p1 = self.__repo.find(n)
        self.assertIs(p1, None)

    def test_size(self):
        self.assertEqual(self.__repo.size(), 8)

    def test_get_all(self):
        crt_grades = self.__repo.get_all_grades()
        self.assertIsInstance(crt_grades, list)

        self.assertEqual(len(crt_grades), 8)

    def test_store(self):
        initial_size = self.__repo.size()
        s = Student(1048, 'Tina', 931)
        l = Laborator(202, 'Algoritm Oglindit', '10.12.2021')
        n = Nota(l, s, 9)
        self.__repo.store(n)

        self.assertEqual(self.__repo.size(), initial_size + 1)


"""class TestCaseStudFileRepoInheritance(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = StudFileRepoInheritance('test_students_repo.txt')
        
    def test_find(self):
        p = self.__repo.find(2001)
        self.assertTrue(p.getNume() == 'Lorena Berchesan')
        self.assertTrue(p.getGrup() == 122)

        p1 = self.__repo.find(1000)
        self.assertIs(p1, None)

    def test_size(self):
        self.assertEqual(self.__repo.size(), 3)

        self.__repo.delete_by_id(1998)
        self.__repo.delete_by_id(7587)

        self.assertEqual(self.__repo.size(), 3)

        self.__repo.store(Student(4004, 'T Popoviciu', 918))
        self.assertEqual(self.__repo.size(), 4)
        self.__repo.store(Student(1024, 'Gheorghe F', 918))
        self.assertEqual(self.__repo.size(), 5)

    def test_get_all(self):
        crt_students = self.__repo.get_all_students()
        self.assertIsInstance(crt_students, list)

        self.assertEqual(len(crt_students), 3)

        self.__repo.delete_by_id(2001)

        crt_students = self.__repo.get_all_students()
        self.assertEqual(len(crt_students), 4)

    def test_store(self):
        initial_size = self.__repo.size()
        s1 = Student(1500, 'Lorena Petrut', 313)
        self.__repo.store_from_file(s1)

        self.assertEqual(self.__repo.size(), initial_size + 1)

    def test_delete_by_criteria(self):
        initial_size = self.__repo.size()
        how_many_deleted = self.__repo.delete_by_criteria(lambda x: x.getGrup() == 123)
        self.assertTrue(how_many_deleted == 1)
        self.assertTrue(self.__repo.size() == initial_size - 1)

        # self.assertRaises(StudentNotFoundException, self.__repo.delete, 'wrongID')

    def test_update(self):
        student3 = Student(5060, 'Kim KW', 137)

        modified_student = self.__repo.update(2001, student3)
        self.assertEqual(modified_student.getNume(), 'Kim KW')
        self.assertEqual(modified_student.getGrup(), 137)"""


unittest.main()