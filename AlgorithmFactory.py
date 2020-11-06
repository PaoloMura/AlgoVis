# class for creating algorithm instances

from LinearSearch import LinearSearch
from BinarySearch import BinarySearch
from BubbleSort import BubbleSort
from InsertionSort import InsertionSort
from MergeSort import MergeSort


class AlgoFactory(object):
    def __init__(self):
        super().__init__()

    def create_lin_sear(self, array, mediator):
        return LinearSearch(array, mediator)
    
    def create_bin_sear(self, array, mediator):
        return BinarySearch(array, mediator)

    def create_bub_sort(self, array, mediator):
        return BubbleSort(array, mediator)

    def create_ins_sort(self, array, mediator):
        return InsertionSort(array, mediator)

    def create_mer_sort(self, array, mediator):
        return MergeSort(array, mediator)
