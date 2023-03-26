import unittest

from domain.validators import StudentValidator
from exceptions.exceptions import ValidationException, StudentNotFoundException, DuplicateIDException
from repository.studs_repo import InMemoryRepository_Stud
from service.studs_service import StudentService


class TestCaseStudentService(unittest.TestCase):
    def setUp(self) -> None:
        repo = InMemoryRepository_Stud()
        validator = StudentValidator()
        self.__srv = StudentService(repo, validator)

    def test_add_student(self):

        added_student = self.__srv.add_student_clasic(1221, 'Alina Soare', 211)
        self.assertTrue(added_student.getID() == 1221)
        self.assertTrue(added_student.getNume() == 'Alina Soare')

        self.assertEqual(len(self.__srv.get_all_students()), 1)
        #self.assertRaises(ValidationException, self.__srv.add_show, '2', 'See', 1200, 12)

    def test_delete_students(self):

        self.__srv.add_student_clasic(2004, 'Tudor Timis', 931)
        deleted_student = self.__srv.delete_students(2004)

        self.assertEqual(len(self.__srv.get_all_students()), 0)
        self.assertEqual(deleted_student.getNume(), 'Tudor Timis')
        self.assertEqual(deleted_student.getGrup(), 931)

    def test_get_all_students(self):

        self.__srv.add_student_clasic(3799, 'Iulia Negrila', 925)
        self.__srv.add_student_clasic(1574, 'Lorena Berchesan', 122)
        self.assertIsInstance(self.__srv.get_all_students(), list)
        self.assertEqual(len(self.__srv.get_all_students()), 2)

    def test_update_student(self):

        self.__srv.add_student_clasic(1234, 'Calin Dancea', 213)
        updated_student = self.__srv.update_student(1234, 'Calin Mihail Dancea', 214)

        self.assertTrue(updated_student.getNume() == 'Calin Mihail Dancea')
        self.assertTrue(updated_student.getID() == 1234)
        self.assertTrue(updated_student.getGrup() == 214)
        #self.assertRaises(ShowNotFoundException,self.__srv.update_show,'INVALID ID', 'See', 2019, 16)

    def test_add(self):
        """
        Black box
        :return:
        """
        student = self.__srv.add_student_clasic(3799, 'Iulia Negrila', 925)
        self.assertTrue(student.getID() == 3799)
        self.assertEqual(type(student.getID()), int)

        self.assertRaises(DuplicateIDException, self.__srv.add_student_clasic, 3799, 'Ilinca', 125)



unittest.main()