# Mechanical Workshop Project

## Overview
The Mechanical Workshop project is a Python application designed to manage car parts inventory and customer orders for various car models. It allows users to read models, orders, and parts from text files, manage inventory, and process customer requests efficiently.

## Project Structure
```
mechanical_workshop/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── src/
    ├── main.py
    ├── array_ordered_positional_list.py
    ├── doubly_linked_base.py
    ├── linked_ordered_positional_list.py
    ├── Piezas.py
    ├── modelos.txt
    ├── pedidos.txt
    ├── stok_piezas.txt
    └── test/
        └── testing.py
```

## Files Description
- **src/main.py**: Entry point of the application. Initializes the `Concesionario` class and runs the process to read models, orders, and parts, and manage inventory and orders.
- **src/array_ordered_positional_list.py**: Implements the `ArrayOrderedPositionalList` class, providing methods for adding, deleting, and accessing elements in an array-based ordered list.
- **src/doubly_linked_base.py**: Defines the `_DoublyLinkedBase` class, serving as a base for implementing a doubly linked list with node insertion and deletion methods.
- **src/linked_ordered_positional_list.py**: Contains the `LinkedOrderedPositionalList` class, extending `_DoublyLinkedBase` to provide an ordered positional list using a doubly linked structure.
- **src/Piezas.py**: Defines the `Pieza` class, representing a car part with attributes for the part name and quantity, including comparison methods for ordering and equality checks.
- **src/modelos.txt**: Contains the models of cars and their required parts and quantities.
- **src/pedidos.txt**: Contains customer orders for different car models.
- **src/stok_piezas.txt**: Contains the available car parts and their quantities.
- **src/test/testing.py**: Unit tests for the application.
- **.gitignore**: Specifies files and directories to be ignored by Git, such as compiled Python files and virtual environment directories.
- **requirements.txt**: Lists the dependencies required for the project, which can be installed using pip.
- **LICENSE**: Contains the licensing information for the project.

## Setup Instructions
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```
This will start the process of reading models, orders, and parts, and managing the inventory and orders.

## Running Tests
To run the unit tests, execute:
```
python -m unittest src/test/testing.py
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.