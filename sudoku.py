import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog
import math

sudoku_field = []

all_empty = []
sudoku_size = 0

all_text_boxes = []
is_unique_set = True
input_text = ""



class Node:
    def __init__(self, value):
        self.Value = value
        self.AllEdges = []

    def __getattr__(self, item):
        return item

    def add_edge(self, value):
        edge = Edge(self, self, value)
        self.AllEdges.append(edge)


class Edge:
    def __init__(self, first, second, value):
        self.Value = value
        self.From = first
        self.To = second


class Tree:
    def __init__(self):
        self.AllNodes = []



current_node = Node((0, 0))
current_edge = Edge(current_node, current_node, -1)
next_node = Node((0, 0))
previous_edge_to_double = []
tree = Tree()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Sudoku solver'
        self.init_UI()

    def init_UI(self):
        global sudoku_size
        self.setWindowTitle(self.title)
        if input_text == "":
            self.get_size()
        self.init_field(input_text)
        self.show()

    def get_size(self):
        global sudoku_size
        dialog = QInputDialog(self)
        i, okPressed = QInputDialog.getInt(dialog, "Size of sudoku", "Choose the size of sudoku", 3, 2, 100, 1)
        if okPressed:
            sudoku_size = i
        else:
            sudoku_size = 2
        dialog.close()

    def init_field(self, input_string):
        counter = 0
        no_blank_string = remove_blanks(input_string)
        for i in range(sudoku_size ** 2):
            if i % sudoku_size == 0:
                border_y = 20
            else:
                border_y = 10
            delta_y = 40 * i
            for j in range(sudoku_size ** 2):
                if j % sudoku_size == 0 and j != 0:
                    border_x = 10
                else:
                    border_x = 5
                delta_x = 40 * j
                self.text = QLineEdit(self)
                if no_blank_string != "" and counter != sudoku_size ** 2:
                    self.text.setText(no_blank_string[counter])
                else:
                    self.text.setText("0")
                counter += 1
                all_text_boxes.append(self.text)
                self.text.move(40 + delta_x + border_x, 40 + delta_y + border_y)
                self.text.resize(40, 40)
        self.init_solve_button()
        self.init_info_bar()

    def init_solve_button(self):
        self.solve_button = QPushButton(self)
        self.solve_button.setText("Solve")
        self.solve_button.move(10, 10)
        self.solve_button.clicked.connect(self.solve_onClick)

    def init_info_bar(self):
        self.info = QLineEdit(self)
        self.info.setText("Input data")
        self.info.move(100, 10)
        self.info.resize(180, 30)
        self.info.setEnabled(False)

    def solve_onClick(self):
        global sudoku_field
        int_count = 0
        string = ''
        for i in all_text_boxes:
            if i.text().isdigit() and i.text() != "0":
                int_count += 1
            string += i.text()
            string += ' '
        string = string[:-1]
        if len(sudoku_field) != 0:
            sudoku_field = []
        sudoku_field=init_field_from_str_zero(string)
        if is_good(sudoku_field):
            sudoku_field = start_solving(sudoku_field)
            self.show_solved(sudoku_field)
            self.info.setText("Successfully")
        else:
            self.info.setText("Unavailable to solve")

    def show_solved(self,field):
        result = ""
        capacity = len(field)
        for i in range(capacity):
            for j in range(int(math.sqrt(math.sqrt(capacity * len(field[0]))))):
                result += field[i][j].__str__()
        for i in range(len(result)):
            all_text_boxes[i].setText(result[i])


def remove_blanks(string):
    result = ""
    for i in string:
        if i != " ":
            result += i
    return result

def get_num_of_shifts_and_transform(string):
    global input_text
    result = ""
    counter = 0
    for i in string:
        if i == '\n':
            counter += 1
            result += ' '
        else:
            result += i
    input_text = result
    return counter

def get_outcome_string():
    input_path = sys.argv[1]
    if input_path != "":
        with open(input_path, 'r') as f:
            global input_text
            input_text += f.read()


def is_good(field):
    position = (0, 0)
    mini_row_count = len(field)
    mini_row_capacity = len(field[0])
    while position != (mini_row_count, 0):
        if not (is_unique(extract_row(position,field)) and is_unique(extract_square(position,field)) and is_unique(
                extract_column(position,field))):
            return False
        if position[1] != mini_row_capacity - 1:
            position = (position[0], position[1] + 1)
        else:
            position = (position[0] + 1, 0)
    return True


def is_unique(set):
    return is_unique_set


def init_field_from_str_zero(string):
    """В двумерный массив из строчки с нулями """
    field = []

    dimension = int(math.sqrt(len(string)))
    mini_row_dimension = int(math.sqrt(dimension))
    num_pos_count = 0
    mini_row = []
    for i in string.split(' '):
        if i != '\n':
            if num_pos_count != mini_row_dimension:
                mini_row.append(int(i))
                num_pos_count += 1
            else:
                field.append(mini_row)
                num_pos_count = 0
                mini_row = []
                mini_row.append(int(i))
                num_pos_count += 1
    field.append(mini_row)

    return field


def is_solved(field):
    """Метод, проверяющий решена ли судоку (нет свободных клеток)"""
    capacity = len(field)
    for i in range(capacity):
        for j in range(int(math.sqrt(math.sqrt(capacity * len(field[0]))))):
            if field[i][j] == 0:
                return False
    return True


def extract_row(position,field):
    """Возращает элементы строки по позиции элемента"""
    mini_row_capacity = len(field[0])
    row = set()
    global is_unique_set
    start_mini_row = position[0]
    while start_mini_row % mini_row_capacity != 0:
        start_mini_row -= 1
    for row_pos in range(start_mini_row, start_mini_row + mini_row_capacity, 1):
        for i in range(mini_row_capacity):
            number = field[row_pos][i]
            if row.__contains__(number):
                is_unique_set = False
            if number != 0:
                row.add(number)
    return row


def extract_column(position,field):
    """Возращает элементы столбца по позиции элемента"""
    mini_row_capacity = len(field[0])
    column = set()
    global is_unique_set
    for i in range(position[0], -1, (-1) * mini_row_capacity):
        number = field[i][position[1]]
        if column.__contains__(number):
            is_unique_set = False
        if number != 0:
            column.add(field[i][position[1]])

    for i in range(position[0] + mini_row_capacity, len(field), mini_row_capacity):
        number = field[i][position[1]]
        if column.__contains__(number):
            is_unique_set = False
        if number != 0:
            column.add(field[i][position[1]])
    return column


def extract_square(position,field):
    """Возращает элементы квадрата по позиции элемента"""
    row_capacity = int(math.sqrt(len(field) * len(field[0])))
    mini_row_capacity = int(math.sqrt(row_capacity))
    square = set()
    global is_unique_set
    starting_pos = position[0]

    starting_pos_list = []
    for i in range(0, len(field), mini_row_capacity ** 2):
        for j in range(mini_row_capacity):
            starting_pos_list.append(i + j)

    while starting_pos not in starting_pos_list:
        starting_pos -= mini_row_capacity

    for row_pos in range(starting_pos, starting_pos + (2 * mini_row_capacity), mini_row_capacity):
        for i in range(mini_row_capacity):
            number = field[row_pos][i]
            if square.__contains__(number):
                is_unique_set = False
            if number != 0:
                square.add(number)
    return square


def get_available_numbers(position,field):
    """Получает на вход число из клетки и возращает лист возможных чисел"""
    dimension = int(math.sqrt(len(field) * len(field[0])))
    all_numbers = set(i for i in range(1, dimension + 1))
    row = extract_row(position,field)
    column = extract_column(position,field)
    square = extract_square(position,field)

    return (row | column | square) ^ all_numbers


def go_up_tree(position_from, position_to,field):
    """Проходит от и до заданных позиций, при этом обнуляя значения"""
    while not position_from == position_to:
        if position_from in all_empty:
            field[position_from[0]][position_from[1]] = 0
        if position_from[1] != 0:
            position_from = (position_from[0], position_from[1] - 1)
        else:
            position_from = (position_from[0] - 1, 2)
    field[position_from[0]][position_from[1]] = 0


def find_empty(position,field):
    """Находит пустую клетку после заданной position """
    mini_row_count = len(field)
    mini_row_capacity = len(field[0])
    if position != (mini_row_count, mini_row_capacity) and not is_solved(field):
        while field[position[0]][position[1]] != 0:
            if position[1] != mini_row_capacity - 1:
                position = (position[0], position[1] + 1)
            else:
                position = (position[0] + 1, 0)
        if position not in all_empty:
            all_empty.append(position)
        return position


def start_solving(field):
    """Метод, решающий судоку"""
    current_node = Node(find_empty((0, 0),field))
    next_node = current_node
    current_edge = Edge(current_node, current_node,-1)
    global previous_edge_to_double

    while not is_solved(field):
        previous_node = current_node
        current_node = next_node
        all_variants = get_available_numbers(current_node.Value, field)
        if len(all_variants) > 1:
            previous_edge_to_double.append(current_edge)
        if len(all_variants) == 0:
            destination_edge = previous_edge_to_double.pop()
            if len(destination_edge.To.all_edges) > 2:
                previous_edge_to_double.append(destination_edge)
            destination_node = destination_edge.To
            go_up_tree(current_node.Value, destination_edge.To.value, field)
            current_node = destination_node
            current_node.all_edges.remove(current_node.all_edges[0])
            current_edge = current_node.all_edges[0]
            value_to_apply = current_edge.value
            position_to_apply = current_node.value

        else:
            for edge_value in all_variants:
                current_node.add_edge(edge_value)
            current_edge = current_node.AllEdges[0]
            value_to_apply = current_edge.value
            position_to_apply = current_node.Value

        field[position_to_apply[0]][position_to_apply[1]] = value_to_apply
        next_node = Node(find_empty(current_node.Value, field))
        if next_node.Value is not None:
            current_edge.To = next_node
        else:
            break
    return field


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("This is sudoku solver. \n Keys: \n -- help - help notice and syntax hints \n "
              "(input_path) - path to file with specially formatted string. \n"
              "Format: \n1 3 4 5 6 \n"
              "2 4 1 2 4  and so on where 0 is blank square")
    else:
        if len(sys.argv) > 1:
            get_outcome_string()
            sudoku_size = int(math.sqrt(get_num_of_shifts_and_transform(input_text) + 1))
        app = QApplication(sys.argv)
        solver = App()
        sys.exit(app.exec_())
