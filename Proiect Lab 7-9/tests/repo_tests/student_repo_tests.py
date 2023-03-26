import unittest

from domain.entities import Student
from exceptions.exceptions import DuplicateIDException, StudentNotFoundException
from repository.studs_repo import InMemoryRepository_Stud, StudFileRepoInheritance


class TestCaseInMemoryRepository_Stud(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = InMemoryRepository_Stud()
        self.__add_predefined_students()

    def __add_predefined_students(self):
        s1 = Student(1574, 'Lorena Berchesan', 122)
        s2 = Student(4098, 'Diana Berchesan', 123)
        s3 = Student(2033, 'Sorina Berchesan', 124)
        s4 = Student(1998, 'Matei Berchesan', 125)
        s5 = Student(7587, 'Oana Berchesan', 126)

        self.__repo.store(s1)
        self.__repo.store(s2)
        self.__repo.store(s3)
        self.__repo.store(s4)
        self.__repo.store(s5)

    def test_find(self):
        p = self.__repo.find(1574)
        self.assertTrue(p.getNume() == 'Lorena Berchesan')
        self.assertTrue(p.getGrup() == 122)

        p1 = self.__repo.find(1000)
        self.assertIs(p1, None)

    def test_size(self):
        self.assertEqual(self.__repo.size(), 5)

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

        self.assertEqual(len(crt_students), 5)

        self.__repo.delete_by_id(7587)

        crt_students = self.__repo.get_all_students()
        self.assertEqual(len(crt_students), 4)

    def test_store(self):
        initial_size = self.__repo.size()
        s1 = Student(1500, 'Lorena Petrut', 313)
        self.__repo.store(s1)

        self.assertEqual(self.__repo.size(), initial_size + 1)

    def test_delete_by_criteria(self):
        initial_size = self.__repo.size()
        how_many_deleted = self.__repo.delete_by_criteria(lambda x: x.getGrup() == 123)
        self.assertTrue(how_many_deleted == 1)
        self.assertTrue(self.__repo.size() == initial_size - 1)

        self.assertRaises(StudentNotFoundException, self.__repo.delete_by_id, 1000)

    def test_update(self):
        student3 = Student(5060, 'Kim KW', 137)
        student4 = Student(5060, 'Inna T', 512)
        self.__repo.store(student3)

        self.assertRaises(DuplicateIDException, self.__repo.store, student4)

        modified_student = self.__repo.update(1574, student3)
        self.assertEqual(modified_student.getNume(), 'Kim KW')
        self.assertEqual(modified_student.getGrup(), 137)
        self.assertRaises(StudentNotFoundException, self.__repo.update, 1000, student4)


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

        self.__repo.delete_by_id(1888)

        self.assertEqual(self.__repo.size(), 4)

        self.__repo.store_from_file(Student(4004, 'T Popoviciu', 918))
        self.assertEqual(self.__repo.size(), 5)
        self.__repo.store_from_file(Student(1024, 'Gheorghe F', 918))
        self.assertEqual(self.__repo.size(), 6)

    def test_get_all(self):
        crt_students = self.__repo.get_all_students()
        self.assertIsInstance(crt_students, list)

        self.assertEqual(len(crt_students), 4)

        self.__repo.delete_by_id(2001)

        crt_students = self.__repo.get_all_students()
        self.assertEqual(len(crt_students), 3)

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

        modified_student = self.__repo.update(8010, student3)
        self.assertEqual(modified_student.getNume(), 'Kim KW')
        self.assertEqual(modified_student.getGrup(), 137)
"""

unittest.main()