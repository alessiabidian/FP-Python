#from termcolor import colored
from service.studs_service import StudentService
from random import randint
import random, string
from operator import itemgetter
from exceptions.exceptions import ValidationException, DuplicateIDException, StudentNotFoundException, \
    LaboratorNotFoundException, GradeAlreadyAssignedException
from operator import lt, gt

class Console:
    def __init__(self, srv_stud, srv_lab, srv_grade):
        """
        Initializeaza consola
        :type srv: StudentService, LaboratorService, NotaService
        """
        self.__srv_stud = srv_stud
        self.__srv_lab = srv_lab
        self.__srv_grade = srv_grade

    def __print_students(self, stud_list):
        """
        Afiseaza toti studentii disponibili

        """
        #stud_list = self.__srv_stud.get_all_students()
        if len(stud_list) == 0:
            print('Nu exista studenti in lista.')
        else:
            print('Lista de studenti este:')
            for student in stud_list:
                # print(student)
                print(
                    'ID Student: ', student.getID(), ' - Nume: ', str(student.getNume()), ' - Nr. grup: ',
                        student.getGrup())

    def __add_student(self):
        """
        Adauga un student cu datele citite de la tastatura
        """

        try:
            student_id = int(input("ID-ul studentului:"))
        except ValueError:
            print('ID-ul studentului trebuie sa fie un numar.')
            return
        nume = str(input("Numele studentului:"))
        try:
            grup = int(input("Nr. de grup:"))
        except ValueError:
            print('Grupul trebuie sa fie un numar.')
            return

        try:
            added_student = self.__srv_stud.add_student(student_id, nume, grup)
            print('Studentul ' + added_student.getNume() + ' cu ID-ul ' + str(
                added_student.getID()) + ' a fost adaugat cu succes.')
        except ValueError as ve:
            print(str(ve))
        except ValidationException as ve:
            print(colored(str(ve), 'red'))
        except DuplicateIDException as e:
            print(colored(str(e), 'red'))

    def __delete_students(self):
        id = int(input('Id-ul studentului de sters: '))
        #self.__print_all_students()
        try:
            deleted_student = self.__srv_stud.delete_students(id)
            print('Studentul cu ID-ul ' + str(deleted_student.getID()) + ' a fost sters cu succes.')
        except ValueError as ve:
            print(str(ve))

    def __delete_by_grup(self):
        """
        Sterge serialele dintr-o perioada data
        """
        try:
            grup = int(input("Grupul de sters:"))
        except ValueError:
            print('Grupul trebuie sa fie numar.')
            return
        try:
            how_many_deleted = self.__srv_stud.delete_by_grup(grup)
            print('S-au sters cu succes', how_many_deleted, 'student\i din grupa:', grup, '.')
        except ValueError as ve:
            print(str(ve))

    def __filter_by_id(self):
        """
        Afiseaza studentul cu id-ul dat
        """
        try:
            student_id = int(input("ID-ul studentului de afisat:"))
        except ValueError:
            print('ID-ul trebuie sa fie un nr. natural, de 4 cifre.')
            return

        try:
            filtered_list = self.__srv_stud.filter_by_id(student_id)
            self.__print_students(filtered_list)
        except ValueError as ve:
            print(str(ve))

    def __filter_by_grup(self):
        """
        Afiseaza studentii dintr-o grupa anume
        """
        try:
            grup = int(input("Grupa de afisat:"))
        except ValueError:
            print('Grupa trebuie sa fie un nr. natural.')
            return
        try:
            filtered_list = self.__srv_stud.filter_by_grup(grup)
            self.__print_students(filtered_list)
        except ValueError as ve:
            print(str(ve))

    def __update_student(self):
        print("Dati datele noi ale studentului cu id-ul citit: ")
        try:
            student_id = int(input("ID-ul studentului:"))
        except ValueError:
            print('ID-ul studentului trebuie sa fie un numar.')
            return
        nume = str(input("Numele studentului:"))
        try:
            grup = int(input("Nr. de grup:"))
        except ValueError:
            print('Grupul trebuie sa fie un numar.')
            return

        try:
            modified_student = self.__srv_stud.update_student(student_id, nume, grup)
            print('Studentul ' + str(modified_student.getNume()) + ' cu id-ul ' + str(
                modified_student.getID()) + ' a fost modificat cu succes.')
        except ValueError as ve:
            print(str(ve))

    def randomword(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def __generate_students(self, n):
        """
        Genereaza random studenti
        """
        for i in range(1, n):
            student_id = randint(1000, 9999)
            letters = string.ascii_lowercase
            nume = str(''.join(random.choice(letters) for i in range(15)))
            grup = randint(100, 999)
            added_student = self.__srv_stud.add_student(student_id, nume, grup)
            print('Studentul ' + added_student.getNume() + ' cu ID-ul ' + str(
                    added_student.getID()) + ' a fost adaugat cu succes.')

    def __sort_list_by_id(self, nota_list):
        """
        Returneaza lista sortata
        :param
        :type
        """
        #print(nota_list[1].getID())
        sorted_list = nota_list

        for i in range(len(sorted_list)-1):
            for j in range(i+1, len(sorted_list)):
                if sorted_list[i].getID() >= sorted_list[j].getID():
                    student = sorted_list[j]
                    sorted_list[j] = sorted_list[i]
                    sorted_list[i] = student

        return sorted_list

    def __merge_sort(self, list):
        """
        Face sortare de tip Merge
        :param list:
        :return:
        """
        val = input('Alegeti Crescator(0) sau Descrescator(1):')
        if val == '0':
            reversed = False
        elif val == '1':
            reversed = True
        else:
            print("Default Ascending.")
        print("Sortarea se poate face dupa key-urile: id, grup, nume, combinat.")
        key = str(input('Dati key-ul:'))
        if key == 'id':
            self.__srv_stud.merge_sort(list, key=self.__srv_stud.keyID, reversed=reversed, cmp=self.__srv_stud.cmp)
        elif key == 'grup':
            self.__srv_stud.merge_sort(list, key=self.__srv_stud.keyGrup, reversed=reversed, cmp=self.__srv_stud.cmp)
        elif key == 'nume':
            self.__srv_stud.merge_sort(list, key=self.__srv_stud.keyNume, reversed=reversed, cmp=self.__srv_stud.cmp)
        elif key == 'combinat':
            self.__srv_stud.merge_sort(list, key=self.__srv_stud.keyNone, reversed=reversed, cmp=self.__srv_stud.cmp_combinat)
        else:
            print("Invalid Key!")
            return
        #self.__srv_stud.mergeSort(list, key, reversed)
        #self.__srv_stud.merge_sort(list, key=self.__srv_stud.keyNone, reversed=reversed, cmp=self.__srv_stud.cmp_primar)

    def __bingo_sort(self, list):
        val = input('Alegeti Crescator(0) sau Descrescator(1):')
        if val == '0':
            reversed = False
        elif val == '1':
            reversed = True
        else:
            print("Default Ascending.")
        print("Sortarea se poate face dupa key-urile: id, grup, nume, combinat.")
        key = str(input('Dati key-ul:'))
        if key == 'id':
            newlist = self.__srv_stud.bingo_sort(list, key=self.__srv_stud.keyID, reversed=reversed, cmp=self.__srv_stud.cmp)
        elif key == 'grup':
            newlist = self.__srv_stud.bingo_sort(list, key=self.__srv_stud.keyGrup, reversed=reversed, cmp=self.__srv_stud.cmp)
        elif key == 'nume':
            newlist = self.__srv_stud.bingo_sort(list, key=self.__srv_stud.keyNume, reversed=reversed, cmp=self.__srv_stud.cmp)
        elif key == 'combinat':
            newlist = self.__srv_stud.bingo_sort(list, key=self.__srv_stud.keyNone, reversed=reversed, cmp=self.__srv_stud.cmp_combinat)
        else:
            print("Invalid Key!")
            return
        #self.__srv_stud.BingoSort(list, key, reversed)
        #self.__srv_stud.bingo(list, key, reversed)  #asta merge, ii functia mea scrisa manual
        #newlist = self.__srv_stud.bingo_sort(list, key1=self.__srv_stud.keyGrup, reversed=reversed, comp=self.__srv_stud.comparare)
        #newlist = self.__srv_stud.bingo_sort(list, key=self.__srv_stud.keyNone, reversed=reversed, cmp=self.__srv_stud.cmp_primar)
        return newlist


    def students_ui(self, ok1, ok3):
        #if ok1 == 0 and ok3 == 0:
            #self.__srv_stud.generate_students()
        #n = int(input("Dati cati studenti sa fie generati: "))
        #self.__generate_students(n)
        while True:
            print('Comenzi disponibile: add, delete_by_id, delete_by_group, filter_by_id, filter_by_group, update, show_all, merge_sort, bingo_sort, exit')
            cmd = input('Comanda este:')
            cmd = cmd.lower().strip()
            if cmd == 'add':
                self.__add_student()
            elif cmd == 'delete_by_id':
                self.__delete_students()
            elif cmd == 'delete_by_group':
                self.__delete_by_grup()
            elif cmd == 'update':
                self.__update_student()
            elif cmd == 'filter_by_id':
                self.__filter_by_id()
            elif cmd == 'filter_by_group':
                self.__filter_by_grup()
            elif cmd == 'sort':
                self.__print_students(self.__sort_list_by_id(self.__srv_stud.get_all_students()))
            elif cmd == 'merge_sort':
                self.__merge_sort(self.__srv_stud.get_all_students())
                self.__print_students(self.__srv_stud.get_all_students())
            elif cmd == 'bingo_sort':
                self.__bingo_sort(self.__srv_stud.get_all_students())
                self.__print_students(self.__srv_stud.get_all_students())
            elif cmd == 'show_all':
                self.__print_students(self.__srv_stud.get_all_students())
            elif cmd == 'exit':
                return 1
            else:
                print('Comanda invalida.')


#- - - - - - - - - - - - - - - - - - - - - - - - - -

    def __print_labs(self, lab_list):
        """
        Afiseaza toate probl de lab disponibile

        """
        #lab_list = self.__srv_lab.get_all_labs()
        if len(lab_list) == 0:
            print('Nu exista probleme de laborator in lista.')
        else:
            print('Lista de probleme este:')
            for laborator in lab_list:
                # print(laborator)
                print(
                    'Nr problema laborator: ', laborator.getNR(), ' - Descriere: ', str(laborator.getDescriere()), ' - Deadline: ',
                        laborator.getDeadline())

    def __add_laborator(self):
        """
        Adauga o problema cu datele citite de la tastatura
        """

        try:
            nrlab_nrprobl = int(input("Numarul problemei de laborator:"))
        except ValueError:
            print('Valoarea trebuie sa fie un numar compus.')
            return
        descriere = str(input("Descriere:"))
        try:
            deadline = str(input("Deadline:"))
        except ValueError:
            print('Deadline-ul trebuie sa fie o data doar cu cifre.')
            return

        try:
            added_laborator = self.__srv_lab.add_laborator(nrlab_nrprobl, descriere, deadline)
            print('Problema de laborator ' + str(added_laborator.getNR()) + ' cu deadline-ul ' + str(
                added_laborator.getDeadline()) + ' a fost adaugat cu succes.')
        except ValueError as ve:
            print(str(ve))
        except ValidationException as ve:
            print(colored(str(ve), 'red'))
        except DuplicateIDException as e:
            print(colored(str(e), 'red'))



    def __delete_labs(self):
        nrlab_nrprobl = int(input('Nr-ul problemei de sters: '))
        try:
            deleted_laborator = self.__srv_lab.delete_labs(nrlab_nrprobl)
            print('Problema cu ID-ul ' + str(deleted_laborator.getNR()) + ' a fost sters cu succes.')
        except ValueError as ve:
                print(str(ve))

    def __update_laborator(self):
        print("Dati datele noi ale problemei de laborator cu id-ul citit: ")
        try:
            nrlab_nrprobl = int(input("Numarul problemei de laborator:"))
        except ValueError:
            print('Valoarea trebuie sa fie un numar compus.')
            return
        descriere = str(input("Descriere:"))
        try:
            deadline = str(input("Deadline:"))
        except ValueError:
            print('Deadline-ul trebuie sa fie o data doar cu cifre.')
            return

        try:
            modified_laborator = self.__srv_lab.update_laborator(nrlab_nrprobl, descriere, deadline)
            print('Problema ' + str(modified_laborator.getNR()) + ' a fost modificata cu succes.')
        except ValueError as ve:
            print(str(ve))

    def __filter_by_nr(self):
        """
        Afiseaza labul cu nr dat
        """
        try:
            nrlab_nrprobl = int(input("Nr-ul problemei de afisat:"))
        except ValueError:
            print('Nr-ul trebuie sa fie un nr. natural, de 4 cifre.')
            return
        try:
            filtered_list = self.__srv_lab.filter_by_nr(nrlab_nrprobl)
            self.__print_labs(filtered_list)
        except ValueError as ve:
            print(str(ve))

    def labs_ui(self, ok2, ok3):
        #if ok2 == 0 and ok3 == 0:
            #self.__srv_lab.generate_labs()
        while True:
            print('Comenzi disponibile: add, delete_by_nr, filter_by_nr, update, show_all, exit')
            cmd = input('Comanda este:')
            cmd = cmd.lower().strip()
            if cmd == 'add':
                self.__add_laborator()
            elif cmd == 'delete_by_nr':
                self.__delete_labs()
            elif cmd == 'filter_by_nr':
                self.__filter_by_nr()
            elif cmd == 'update':
                self.__update_laborator()
            elif cmd == 'show_all':
                self.__print_labs(self.__srv_lab.get_all_labs())
            elif cmd == 'exit':
                return 1
            else:
                print('Comanda invalida.')
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def __sort(self, nota_list, cmd):
        """
        Returneaza lista de seriale care au mai multe episoade decat numarul dat
        :param number_of_episodes: numarul de episoade dat
        :type number_of_episodes:int
        :return: lista de seriale care indeplinesc criteriul
        :rtype: list of Serial objects
        """
        if cmd == 'sort_by_grade':
            sorted_list = self.__srv_grade.sort_list_by_grade(nota_list)
        elif cmd == 'sort_alpha':
            sorted_list = self.__srv_grade.sort_list_alpha(nota_list)
        print("Lista a fost sortata cu succes.")
        return sorted_list

    def __print_first3(self, slab_list, snrnote_list):
        if len(slab_list) == 0:
            print('Nu exista note in lista.')
        else:
            print('Primele 3 laburi cu cele mai multe note:')
            for i in range(0, 3):
                print(i+1, "Laboratorul [", slab_list[i], "]", " Nr notelor: ", snrnote_list[i])

    def __first_3_labs_grades(self):
        lab_list, nrnote_list = self.__srv_grade.lab_and_nrnote()
        slab_list, snrnote_list = self.__srv_grade.sort_list_by_nrnote_desc(lab_list, nrnote_list)
        self.__print_first3(slab_list, snrnote_list)

    def __filter_average(self):
        """

        :return:
        """
        print("Studenții cu media notelor de lab mai mica decât 5:")
        filtered_list, mediile = self.__srv_grade.filter_by_average_grade()
        return filtered_list, mediile

    def __print_grades(self, nota_list):
        """
        Afiseaza o lista de note
        """
        if len(nota_list) == 0:
            print('Nu exista note in lista.')
        else:
            print('Lista de note este:')
            for nota in nota_list:
                print(nota)
                #print('Student: [', str(nota.getStudent().getID()), '; ', str(nota.getStudent().getNume()), '; ', str(nota.getStudent().getGrup()), ']',
               #'Laborator: [', str(nota.getLab().getNR()), str(nota.getLab().getDescriere()), str(nota.getLab().getDeadline()), ']',
               #'Nota: ' + str(nota.getNota()))

    def __print_2_lists(self, filtered_list, mediile):
        """
        Afiseaza o lista de note
        """
        if len(filtered_list) == 0:
            print('Nu exista note in lista.')
        else:
            print('Lista de medii de note sub 5 este:')
            for i in range(len(filtered_list)):
                print("Studentul [", filtered_list[i], "]", " Media notelor: ", mediile[i])

    def __assign_nota(self):
        student_id = int(input('ID student:'))
        nrlab_nrprobl = int(input('Nr problema de lab:'))
        try:
            nota = float(input('Nota:'))
            grade = self.__srv_grade.create_nota(student_id, nrlab_nrprobl, nota)
            print('Nota ', nota, ' de la problema ', nrlab_nrprobl, ' a studentului cu id-ul ', student_id, ' a fost adaugata cu succes.')
        except ValueError as ve:
            print(colored('Nota trebuie sa fie un numar.', 'red'))
            #print(colored(ve, 'red'))
        except ValidationException as ve:
            print(colored(str(ve), 'red'))
        except StudentNotFoundException as ve:
            print(colored(str(ve), 'red'))
        except LaboratorNotFoundException as ve:
            print(colored(str(ve), 'red'))
        except GradeAlreadyAssignedException as ve:
            print(colored(str(ve), 'red'))


    def grades_ui(self, ok1, ok2, ok3):
        #if ok1 == 0:
            #self.__srv_stud.generate_students()
        #if ok2 == 0:
            #self.__srv_lab.generate_labs()
        #if ok3 == 0:
            #self.__srv_grade.generate_grades()
        while True:
            print('Comenzi disponibile: add, sort_by_grade, sort_alpha, filter_average, first_3_labs, show_all, exit')
            cmd = input('Comanda este:')
            cmd = cmd.lower().strip()
            if cmd == 'add':
                self.__assign_nota()
            elif cmd == 'show_all':
                self.__print_grades(self.__srv_grade.get_all())
            elif cmd == 'sort_by_grade':
                nota_lista =self.__srv_grade.get_all()
                self.__print_grades(self.__sort(nota_lista, cmd))
            elif cmd == 'sort_alpha':
                nota_lista =self.__srv_grade.get_all()
                self.__print_grades(self.__sort(nota_lista, cmd))
            elif cmd == 'filter_average':
                filtered_list, mediile = self.__filter_average()
                self.__print_2_lists(filtered_list, mediile)
                #self.__print_grades(self.__filter_average())
                #self.__filter_average()
            elif cmd == 'first_3_labs':
                self.__first_3_labs_grades()
            elif cmd == 'exit':
                return 1
            else:
                print('Comanda invalida.')

    def choose_ui(self):
        ok1 = 0 #pt initializarea studentilor
        ok2 = 0 #pt initializarea laburilor
        ok3 = 0 #pt initializarea notelor
        while True:
            print('Comenzi disponibile pentru: student, laborator, note, exit')
            cmd = input('Categoria dorita este:')
            if cmd == 'student':
                ok1 = self.students_ui(ok1, ok3)
            elif cmd == 'laborator':
                ok2 = self.labs_ui(ok2, ok3)
            elif cmd == 'note':
                ok3 = self.grades_ui(ok1, ok2, ok3)
            elif cmd == 'exit':
                return
            else:
                print('Comanda invalida.')