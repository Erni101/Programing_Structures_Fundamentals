import os
from linked_ordered_positional_list import LinkedOrderedPositionalList as ListaOrdenada
from Piezas import Pieza

class Concesionario:
    def __init__(self):
        self._modelos = {}  # Diccionario de modelos de coches
        self._piezas = ListaOrdenada()  # Inventario de piezas
        self._pedidos = []  # Lista de pedidos

    def read_orders(self, path="pedidos.txt"):
        """Lee los pedidos desde el archivo especificado."""
        path = os.path.join(os.path.dirname(__file__), path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Ignore empty lines
                        ls = line.split(",")
                        if len(ls) >= 2:
                            customer, model_name = ls[0].strip(), ls[1].strip()
                            self._pedidos.append([customer, model_name])
                            print(f"Por hacer: procesar pedido {model_name} del cliente {customer}")
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo {path}")
        except Exception as e:
            print(f"Error leyendo pedidos: {e}")

    def read_parts(self, path="stok_piezas.txt"):
        """Lee las piezas desde el archivo especificado."""
        path = os.path.join(os.path.dirname(__file__), path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Ignore empty lines
                        ls = line.split(",")
                        if len(ls) >= 2:
                            part_name, qty = ls[0].strip(), int(ls[1].strip())
                            pieza = Pieza(part_name, qty)
                            self._piezas.add(pieza)
                            print(f"Por hacer: añadir al inventario la pieza \"{part_name}\" con ({qty} unidades)")
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo {path}")
        except Exception as e:
            print(f"Error leyendo piezas: {e}")

    def read_models(self, path="modelos.txt"):
        """Lee los modelos desde el archivo especificado."""
        path = os.path.join(os.path.dirname(__file__), path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Ignore empty lines
                        ls = line.split(",")
                        if len(ls) >= 3:
                            model_name, part_name, qty = ls[0].strip(), ls[1].strip(), int(ls[2].strip())
                            pieza = Pieza(part_name, qty)
                            
                            if model_name in self._modelos:
                                self._modelos[model_name].add(pieza)
                            else:
                                partes_ordenadas = ListaOrdenada()
                                partes_ordenadas.add(pieza)
                                self._modelos[model_name] = partes_ordenadas
                            print(f"Por hacer: añadir al catálogo pieza \"{part_name}\" ({qty} unidades) al modelo \"{model_name}\"")
        except FileNotFoundError:
            print(f"Error: No se pudo encontrar el archivo {path}")
        except Exception as e:
            print(f"Error leyendo modelos: {e}")

    def piezas_disponibles(self):
        """Imprime el inventario de piezas disponibles."""
        print("\n---------Stock---------")
        piezas = [f'{pieza.part_name}: {pieza.qty}' for pieza in self._piezas]
        if piezas:
            print(" | ".join(piezas))
        else:
            print("No hay piezas en stock")
        print()

    def catalogo(self):
        """Imprime el catálogo de coches y sus piezas."""
        print("---------Catalogo---------")
        if not self._modelos:
            print("No hay modelos en el catálogo")
        else:
            for modelo, piezas in self._modelos.items():
                print(f'{modelo}:')
                for pieza in piezas:
                    print(f'  {pieza.part_name} - {pieza.qty}')
                print()

    def pedido(self):
        """Imprime los pedidos de coches y verifica si se pueden atender."""
        print("\n---------Pedidos---------")
        if not self._pedidos:
            print("No hay pedidos")
            return
            
        for pedido in self._pedidos:
            cliente, modelo_pedido = pedido[0], pedido[1]
            print(f"\nProcesando pedido de {cliente} para {modelo_pedido}")
            
            if modelo_pedido in self._modelos:
                self.compra(cliente, modelo_pedido, self._modelos[modelo_pedido])
            else:
                print(f'Pedido NO atendido. Modelo {modelo_pedido} fuera de catálogo.')

    def compra(self, cliente, modelo, piezas):
        """Muestra las piezas necesarias para atender el pedido, y en caso de que no haya suficientes, muestra las faltantes."""
        print(f'Pedido de {cliente} - {modelo}:')
        for pieza in piezas:
            print(f'  {pieza.part_name} - {pieza.qty}')
        
        if self.pedido_disponible(piezas):
            print(f'Pedido {modelo} atendido.')
            self.actualizacion(modelo, piezas)
        else:
            print(f'Pedido {modelo} NO atendido. Faltan:')
            self.faltantes(piezas)
            # Remove model from catalog if order cannot be fulfilled
            if modelo in self._modelos:
                del self._modelos[modelo]
                print(f'Eliminado del catálogo: {modelo}')

    def pedido_disponible(self, piezas):
        """Verifica si las piezas necesarias para atender el pedido están disponibles."""
        for pieza in piezas:
            pieza_inventario = self.buscar_inventario(pieza.part_name)
            if not pieza_inventario or pieza.qty > pieza_inventario.qty:
                return False
        return True

    def buscar_inventario(self, part_name):
        """Busca una pieza en el inventario y devuelve la pieza."""
        for pieza in self._piezas:
            if pieza.part_name == part_name:
                return pieza
        return None

    def faltantes(self, piezas):
        """Muestra las piezas que faltan para atender el pedido."""
        for pieza in piezas:
            pieza_inventario = self.buscar_inventario(pieza.part_name)
            disponible = pieza_inventario.qty if pieza_inventario else 0
            faltan = pieza.qty - disponible
            if faltan > 0:
                print(f'  {pieza.part_name} - {faltan}')

    def actualizacion(self, modelo, piezas):
        """Actualiza el inventario después de procesar un pedido."""
        piezas_a_eliminar = []
        modelos_a_eliminar = []
        
        # Update inventory quantities
        for pieza in piezas:
            pieza_inventario = self.buscar_inventario(pieza.part_name)
            if pieza_inventario:
                pieza_inventario.qty -= pieza.qty
                if pieza_inventario.qty <= 0:
                    piezas_a_eliminar.append(pieza_inventario)
        
        # Remove pieces with 0 quantity from inventory
        for pieza_eliminar in piezas_a_eliminar:
            self._eliminar_pieza_inventario(pieza_eliminar.part_name)
            print(f'Eliminada del inventario: {pieza_eliminar.part_name}')
            
            # Find models that require this piece and mark them for removal
            for modelo_nombre, piezas_modelo in list(self._modelos.items()):
                for pieza_modelo in piezas_modelo:
                    if pieza_modelo.part_name == pieza_eliminar.part_name:
                        if modelo_nombre not in modelos_a_eliminar:
                            modelos_a_eliminar.append(modelo_nombre)
                        break
        
        # Remove models that can't be built anymore
        for modelo_eliminar in modelos_a_eliminar:
            if modelo_eliminar in self._modelos:
                del self._modelos[modelo_eliminar]
                print(f'Eliminado del catálogo: {modelo_eliminar}')

    def _eliminar_pieza_inventario(self, part_name):
        """Elimina una pieza del inventario por nombre."""
        # Since we can't modify during iteration, collect positions to delete
        posiciones_a_eliminar = []
        cursor = self._piezas.first()
        
        while cursor is not None:
            if cursor.element().part_name == part_name:
                posiciones_a_eliminar.append(cursor)
            cursor = self._piezas.after(cursor)
        
        # Delete found positions
        for pos in posiciones_a_eliminar:
            self._piezas.delete(pos)

    def proceso(self):
        """Ejecuta el proceso completo del concesionario."""
        print("=== INICIANDO PROCESO DEL CONCESIONARIO ===\n")
        
        self.read_parts()
        self.read_models()
        self.read_orders()
        
        print("\n=== ESTADO INICIAL ===")
        self.piezas_disponibles()
        self.catalogo()
        
        print("=== PROCESANDO PEDIDOS ===")
        self.pedido()
        
        print("\n=== ESTADO FINAL ===")
        self.piezas_disponibles()
        self.catalogo()

if __name__ == "__main__":
    concesionario = Concesionario()
    concesionario.proceso()