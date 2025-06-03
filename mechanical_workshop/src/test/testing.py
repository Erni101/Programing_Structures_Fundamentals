import unittest
import os
import sys
import tempfile
from io import StringIO

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import Concesionario
from Piezas import Pieza

class TestConcesionario(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test files
        with open("stok_piezas.txt", "w", encoding='utf-8') as f:
            f.write("motor,5\nrueda,20\npuerta,10\n")
            
        with open("modelos.txt", "w", encoding='utf-8') as f:
            f.write("Sedan,motor,1\n")
            f.write("Sedan,rueda,4\n")
            f.write("Sedan,puerta,4\n")
            f.write("SUV,motor,1\n")
            f.write("SUV,rueda,4\n")
            f.write("SUV,puerta,5\n")
            
        with open("pedidos.txt", "w", encoding='utf-8') as f:
            f.write("Juan,Sedan\n")
            f.write("Ana,SUV\n")

        # Initialize concesionario
        self.concesionario = Concesionario()
        
        # Capture output during setup
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        self.concesionario.read_parts("stok_piezas.txt")
        self.concesionario.read_models("modelos.txt")
        self.concesionario.read_orders("pedidos.txt")
        
        # Restore stdout
        sys.stdout = old_stdout

    def tearDown(self):
        """Clean up after each test method."""
        # Change back to original directory
        os.chdir(self.old_cwd)
        
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.test_dir)

    def test_piezas_disponibles(self):
        """Test that parts are correctly loaded into inventory."""
        # Check if parts are in inventory
        found_parts = {}
        for pieza in self.concesionario._piezas:
            found_parts[pieza.part_name] = pieza.qty
            
        self.assertIn("motor", found_parts)
        self.assertIn("rueda", found_parts)
        self.assertIn("puerta", found_parts)
        self.assertEqual(found_parts["motor"], 5)
        self.assertEqual(found_parts["rueda"], 20)
        self.assertEqual(found_parts["puerta"], 10)

    def test_modelos_leidos(self):
        """Test that models are correctly loaded."""
        self.assertIn("Sedan", self.concesionario._modelos)
        self.assertIn("SUV", self.concesionario._modelos)
        
        # Check Sedan parts
        sedan_parts = {}
        for pieza in self.concesionario._modelos["Sedan"]:
            sedan_parts[pieza.part_name] = pieza.qty
            
        self.assertIn("motor", sedan_parts)
        self.assertIn("rueda", sedan_parts)
        self.assertIn("puerta", sedan_parts)
        self.assertEqual(sedan_parts["motor"], 1)
        self.assertEqual(sedan_parts["rueda"], 4)
        self.assertEqual(sedan_parts["puerta"], 4)

    def test_pedidos_leidos(self):
        """Test that orders are correctly loaded."""
        self.assertEqual(len(self.concesionario._pedidos), 2)
        self.assertEqual(self.concesionario._pedidos[0], ["Juan", "Sedan"])
        self.assertEqual(self.concesionario._pedidos[1], ["Ana", "SUV"])

    def test_pedido_disponible(self):
        """Test order availability checking."""
        sedan_piezas = self.concesionario._modelos["Sedan"]
        self.assertTrue(self.concesionario.pedido_disponible(sedan_piezas))
        
        # Test with insufficient stock
        suv_piezas = self.concesionario._modelos["SUV"]
        # SUV requires 5 doors but we only have 10 total, should still be available
        self.assertTrue(self.concesionario.pedido_disponible(suv_piezas))

    def test_buscar_inventario(self):
        """Test inventory search functionality."""
        pieza = self.concesionario.buscar_inventario("motor")
        self.assertIsNotNone(pieza)
        self.assertEqual(pieza.part_name, "motor")
        self.assertEqual(pieza.qty, 5)
        
        # Test non-existent part
        pieza_no_existe = self.concesionario.buscar_inventario("ventana")
        self.assertIsNone(pieza_no_existe)

    def test_pieza_class(self):
        """Test the Pieza class functionality."""
        pieza1 = Pieza("motor", 5)
        pieza2 = Pieza("rueda", 10)
        pieza3 = Pieza("motor", 3)
        
        # Test string representation
        self.assertEqual(str(pieza1), "motor: 5")
        
        # Test comparison operators
        self.assertTrue(pieza1 < pieza2)  # motor < rueda alphabetically
        self.assertTrue(pieza1 == pieza3)  # same part name
        self.assertFalse(pieza1 != pieza3)  # same part name
        self.assertTrue(pieza2 > pieza1)  # rueda > motor alphabetically

    def test_ordered_list_functionality(self):
        """Test that the ordered list maintains order."""
        from linked_ordered_positional_list import LinkedOrderedPositionalList
        lista = LinkedOrderedPositionalList()