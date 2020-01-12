class MyIterable:
    """
    An iterable class to replace the list
    """
    def __init__(self, myList):
        self._objects = myList

    def __setitem__(self, key, value):
        self._objects[key] = value

    def __getitem__(self, item):
        return self._objects[item]

    def __delitem__(self, key):
        self._objects.__delitem__(key)

    def append(self, someObject):
        self._objects.append(someObject)
    
    def remove(self, someObject):
        self._objects.remove(someObject)
        
    def pop(self, index=None):
        if index:
            self._objects.pop(index)
        else:
            self._objects.pop()

    def __iter__(self):
        self._num = 0
        return self

    def __next__(self):
        num = self._num
        if num < len(self._objects):
            self._num += 1
            return self._objects[num]
        else:
            raise StopIteration
    
    def __len__(self):
        return len(self._objects)
    
    def __str__(self):
        return str(self._objects)