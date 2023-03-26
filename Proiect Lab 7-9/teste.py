from random import randint
import random, string
from operator import lt, gt


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


print(randint(1000, 9999))
for i in range(1, 5):
    print(randomword(10))


def reverse(arr):
    n = len(arr)
    for i in range(0, n // 2):
        arr[i], arr[n - i - 1] = arr[n - i - 1], arr[i]

    # return arr


def mergeSort(arr, asc):
    if len(arr) > 1:

        # Finding the mid of the array
        mid = len(arr) // 2

        # Dividing the array elements
        L = arr[:mid]

        # into 2 halves
        R = arr[mid:]

        # Sorting the first half
        mergeSort(L, asc)

        # Sorting the second half
        mergeSort(R, asc)

        i = j = k = 0

        if asc == True:
            # Copy data to temp arrays L[] and R[]
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
        else:
            # Copy data to temp arrays L[] and R[]
            while i < len(L) and j < len(R):
                if L[i] > R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def BingoSort(arr):
    last = len(arr) - 1
    nextmax = arr[last]

    for i in range(last - 1, 0, -1):
        if arr[i][1] > nextmax[1]:
            nextmax = arr[i]
    while last > 0 and arr[last][1] == nextmax[1]:
        last = last - 1

    while last > 0:
        prevmax = nextmax
        nextmax = arr[last]
        for i in range(last - 1, -1, -1):
            if arr[i][1] > nextmax[1]:
                if arr[i][1] != prevmax[1]:
                    nextmax = arr[i]
                else:
                    arr[i], arr[last] = arr[last], arr[i]
                    last = last - 1
        while last > 0 and arr[last][1] == nextmax[1]:
            last = last - 1


def printList(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print('\n')

from functools import reduce
lst = [[1, 4, 5], [1, 57, 7], [5, 17, 2], [2, 89, 1], [2, 3, 1], [0, 1143, 7], [1, 22, 6], [5, 17, 4], [5, 9, 11]]
cpylst = []
auxl = []
for el in lst:
    auxl = el.copy()
    auxl.pop(1)
    cpylst.append(auxl)

print(cpylst)
cpylst.pop(2)
print(lst)
print(cpylst)

def compare(v1, v2):
    if v1[0] != v2[0]:
        return v1[0] - v2[0]
    elif v1[1]!=v2[1]:
        return v1[1] - v2[1]
    else:
        return v1[2] - v2[2]

max = reduce(lambda val, cur: cur if compare(cur, val) > 0 else val, lst)
print(str("Maximul este: ") + str(max))

def comp(x, y, func):
    return func(x, y)


ascending = True
if comp(15, 5, (lt if ascending else gt)):
    print("Da")
else:
    print("Nu")

from operator import lt, gt



def keyNume(element):
    return element.obtineStudent().obtineNume()


def keyNota(element):
    return element.obtineNota_Primita()


def keyAparitie(element):
    return element[3]


def keyNone(element):
    return element

# lista_note=bingo_sort(lista_note, key=keyNume, reversed=False,comp=lt)
def bingo_sort(lista, key, reversed, comp):
    if len(lista) <= 1:
        return lista
    if reversed == True:
        valoare_swap = reduce(lambda val, cur: cur if not comp(key(cur), key(val)) else val, lista)
    else:
        valoare_swap = reduce(lambda val, cur: cur if comp(key(cur), key(val)) else val, lista)
    index_swap = 0
    while index_swap < len(lista):
        index_curent = index_swap
        valoarea_urmatoare = lista[index_curent]
        if reversed:
            while index_curent < len(lista):
                if comp(key(lista[index_curent]), key(valoarea_urmatoare)) <= 0:
                    valoarea_urmatoare = lista[index_curent]
                if key(lista[index_curent]) == key(valoare_swap):
                    lista[index_swap], lista[index_curent] = lista[index_curent], lista[index_swap]
                    index_swap = index_swap + 1
                index_curent = index_curent + 1
            valoare_swap = valoarea_urmatoare
        else:
            while index_curent < len(lista):
                if comp(key(lista[index_curent]), key(valoarea_urmatoare)) > 0:
                    valoarea_urmatoare = lista[index_curent]
                if key(lista[index_curent]) == key(valoare_swap):
                    lista[index_swap], lista[index_curent] = lista[index_curent], lista[index_swap]
                    index_swap = index_swap + 1
                index_curent = index_curent + 1
            valoare_swap = valoarea_urmatoare
    return lista

lisst=[1, 2, 3]
#lisst.pop(1)
#print(lisst)
# mergeSort(lst, False)
#BingoSort(lst)
#printList(lst)
#print(lst[0][0])

"""
1221;Alina Soare;211
8104;Radu Boxeru;925
1234;Calin Dancea;213
1574;Lorena Berchesan;122
3799;Iulia Negrila;925
2004;Tudor Timis;931
2000;Ilinca Timis;931
9175;Bianca Sirea;215
1177;Luana Cicios;112
6414;Filip Alexandru Georgian;922

101;Algoritm Nr Prim;22.11.2021
202;Algoritm Oglindit;10.12.2021
301;Proiect Cheltuieli cu stergeri si adaugari;19.01.2022
305;Alg de palindrom;27.02.2022
401;Backtracking;03.04.2022
402;Alg de citire din fisier;04.04.2022
501;Alg de concatenare cuvinte;12.04.2022
502;Proiect liste inlantuite;20.04.2022
601;Proiect cu update si undo liste;18.05.2022

305
8104
9
101
8104
1
202
8104
3
305
1221
10
305
1234
6
305
3799
10
301
1574
4
202
3799
7

305;8104;9
101;8104;1
202;8104;3
305;1221;10
305;1234;6
305;3799;10
301;1574;4
202;3799;7
"""
