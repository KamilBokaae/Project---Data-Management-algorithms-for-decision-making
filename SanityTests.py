from main import *

def SanityTestForAlgorithm1():
    # 0 in category = Blue
    # 1 in category = Red

    i1 = Item('a', 9, 0)
    i2 = Item('b', 8, 0)
    i3 = Item('c', 7, 0)
    i4 = Item('d', 6, 1)
    i5 = Item('e', 5, 1)
    i6 = Item('f', 5, 1)
    i7 = Item('g', 4, 1)
    i8 = Item('h', 3, 0)
    i9 = Item('i', 2, 0)
    i10 = Item('j', 2, 1)
    i11 = Item('k', 1, 0)
    i12 = Item('l', 1, 1)

    ListOfItems = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12]
    returnedList = TopKSelectionFromSortedList(ListOfItems, K=3, d=2, floorList=[1, 1], ceilList=[2, 2])
    assert (len(returnedList) == 3)
    assert (returnedList[0].id == 'a')
    assert (returnedList[1].id == 'b')
    assert (returnedList[2].id == 'd')


def SanityTestForAlgorithm2():
    # 0 in category = Blue
    # 1 in category = Red

    i1 = Item('a', 6, 0)
    i2 = Item('b', 4, 1)
    i3 = Item('c', 1, 0)
    i4 = Item('d', 8, 0)
    i5 = Item('e', 2, 1)
    i6 = Item('f', 3, 0)
    i7 = Item('g', 1, 1)
    i8 = Item('h', 2, 0)
    i9 = Item('i', 9, 1)
    i10 = Item('j', 5, 1)
    i11 = Item('k', 7, 0)
    i12 = Item('l', 5, 1)

    ListOfItems = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12]
    returnedList = SecretaryAlgorithm(ListOfItems, 3, 12, 2, [1, 1], [2, 2], [6, 6])
    assert (len(returnedList) == 3)
    assert (returnedList[0].id == 'd')
    assert (returnedList[1].id == 'i')
    assert (returnedList[2].id == 'l')

SanityTestForAlgorithm1()
SanityTestForAlgorithm2()