import random
from myIterable import MyIterable
import math

class MergeSort:
    @staticmethod
    def _merge(list1, list2, order):
        new_list = []
        i = 0
        j = 0
        while i < len(list1) and j < len(list2):
            if order(list1[i], list2[j]):
                new_list.append(list1[i])
                i += 1
            else:
                new_list.append(list2[j])
                j += 1
        while i < len(list1):
            new_list.append(list1[i])
            i += 1
        while j < len(list2):
            new_list.append(list2[j])
            j += 1
        return new_list


    def merge_sort(self, objects, order):
        if len(objects) <= 1:
            return objects
        middle = len(objects) // 2
        list1 = objects[:middle]
        list1 = self.merge_sort(list1, order)
        list2 = objects[middle:]
        list2 = self.merge_sort(list2, order)
        return self._merge(list1, list2, order)

class CombSort:
    @staticmethod
    def sort(objects, order):
        is_sorted = False
        gap = len(objects) - 1
        shrink = 1.3

        while not is_sorted:
            gap = math.floor(gap / shrink)
            if gap <= 1:
                is_sorted = True

            i = 0
            while i + gap < len(objects) - 1:
                if not order(objects[i], objects[i + 1]):
                    objects[i], objects[i + 1] = objects[i + 1], objects[i]
                    is_sorted = False
                i += 1
