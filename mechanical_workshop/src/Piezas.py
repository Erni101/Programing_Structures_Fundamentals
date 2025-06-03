class Pieza:
    """Clase que representa una pieza de coche."""
    
    def __init__(self, part_name, qty):
        self.part_name = part_name
        self.qty = qty

    def __str__(self):
        return f"{self.part_name}: {self.qty}"

    def __repr__(self):
        return f"Pieza('{self.part_name}', {self.qty})"

    def __lt__(self, other):
        if isinstance(other, Pieza):
            return self.part_name < other.part_name
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Pieza):
            return self.part_name == other.part_name
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Pieza):
            return self.part_name <= other.part_name
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Pieza):
            return self.part_name > other.part_name
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Pieza):
            return self.part_name >= other.part_name
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Pieza):
            return self.part_name != other.part_name
        return NotImplemented