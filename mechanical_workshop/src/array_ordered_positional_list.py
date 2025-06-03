class ArrayOrderedPositionalList:
    """An array-based implementation of a sequential container of elements allowing positional access."""

    def __init__(self):
        """Create an empty list."""
        self._data = []

    #------------------------------- accessors -------------------------------
    def first(self):
        """Return the first Position in the list (or None if list is empty)."""
        if self.is_empty():
            return None
        else:
            return 0
        
    def last(self):
        """Return the last Position in the list (or None if list is empty)."""
        if self.is_empty():
            return None
        else:
            return len(self._data) - 1

    def before(self, p):
        """Return the Position just before Position p (or None if p is first)."""
        if not isinstance(p, int) or p < 0 or p >= len(self._data):
            raise IndexError('p is not a valid position')
        if p == 0:
            return None
        else:
            return p - 1
        
    def after(self, p):
        """Return the Position just after Position p (or None if p is last)."""
        if not isinstance(p, int) or p < 0 or p >= len(self._data):
            raise IndexError('p is not a valid position')
        if p == len(self._data) - 1:
            return None
        else:
            return p + 1

    def __len__(self):
        """Return the number of elements in the list."""
        return len(self._data)

    def is_empty(self):
        """Return True if the list is empty."""
        return len(self._data) == 0

    def __iter__(self):
        """Generate a forward iteration of the elements of the list."""
        return iter(self._data)

    def get_element(self, p):
        """Return the Element at position p of the list."""
        if not isinstance(p, int) or p < 0 or p >= len(self._data):
            raise IndexError('p is not a valid position')
        return self._data[p]

    #------------------------------- mutators -------------------------------
    
    def add(self, e):
        """Insert element e into list maintaining order and return new Position."""
        if self.is_empty():
            self._data.append(e)
            return 0
        
        # Find the correct position to insert
        pos = 0
        for i, item in enumerate(self._data):
            if e <= item:
                pos = i
                break
            pos = i + 1
        
        # Insert at the found position
        self._data.insert(pos, e)
        return pos
        
    def delete(self, p):
        """Remove and return the element at Position p."""
        if not isinstance(p, int) or p < 0 or p >= len(self._data):
            raise IndexError('p is not a valid position')
        return self._data.pop(p)

    def replace(self, p, e):
        """Replace the element at Position p with e.

        Return the element formerly at Position p.
        """
        if not isinstance(p, int) or p < 0 or p >= len(self._data):
            raise IndexError('p is not a valid position')
        old_value = self._data[p]
        self.delete(p)
        new_pos = self.add(e)
        return old_value