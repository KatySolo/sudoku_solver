## -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QInputDialog
import math

input_sudoku_field = []

all_empty = []
size = 0
all_text_box = []
uniqueFlag = True


str = "009582160017096030568070902426105700700024013090760054600800401900013825801207300"
str_4 = "3410 0200 0020 0143"
input_sudoku_string_easy = "009 582 160" \
                           "017 096 030" \
                           "568 070 902" \
                           "426 105 700" \
                           "700 024 013" \
                           "090 760 054" \
                           "600 800 401" \
                           "900 013 825" \
                           "801 207 300"
input_sudoku_string_medium = "004036005" \
                             "020000069" \
                             "000500080" \
                             "008007900" \
                             "000000051" \
                             "050260300" \
                             "300090000" \
                             "006000504" \
                             "080640200"
input_sudoku_string_medium_2 = "010080069" \
                               "028014005" \
                               "790002000" \
                               "030005084" \
                               "500800701" \
                               "074003000" \
                               "006700900" \
                               "200390800" \
                               "089020150"
input_sudoku_string_medium_3 = "020507000" \
                               "385000000" \
                               "000200035" \
                               "004015000" \
                               "000020309" \
                               "803009040" \
                               "000050428" \
                               "018900060" \
                               "530640000"
input_sudoku_string_hard = "004008000" \
                           "010000000" \
                           "900060004" \
                           "000009403" \
                           "000700005" \
                           "080040000" \
                           "059070000" \
                           "000206090" \
                           "000000800"
input_sudoku_string_hardcore = "100007090" \
                               "030020008" \
                               "009600500" \
                               "005300900" \
                               "010080002" \
                               "600004000" \
                               "300000010" \
                               "040000007" \
                               "007000300"
input_sudoku_string_hardcore_2 = "7700108000" \
                                 "090000032" \
                                 "000005000" \
                                 "000000100" \
                                 "960020000" \
                                 "000000800" \
                                 "000000000" \
                                 "005001000" \
                                 "320000006"


class Node:
    def __init__(self, value):
        self.value = value
        self.all_edges = []

    def __getattr__(self, item):
        return item

    def add_edge(self, value):
        edge = Edge(self, self, value)
        self.all_edges.append(edge)


class Edge:
    def __init__(self, first, second, value):
        self.value = value
        self.From = first
        self.To = second


class Tree:
    def __init__(self):
        # self.all_nodes = [root_value]
        self.all_nodes = []
        # self.root=root_value


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Sudoku solver'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.sudoku_size = 1
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.get_size()
        # self.init_field()
        if not self.isInputParams:
            self.get_size()
            self.init_field()
        else:
            self.sudoku_size = int(math.sqrt(len(input_text)))
            self.init_field()
            start_solving()
            self.show_solved()
        self.show()

    def isInputParams(self):
        input_path = sys.argv[1]
        if input_path != "":
            with open(input_path, 'r') as f:
                global input_text
                input_text += f.read()
            return True
        return False

    def get_size(self):
        dialog = QInputDialog(self)
        i, okPressed = QInputDialog.getInt(dialog, "Size of sudoku", "Choose the size of sudoku", 3, 2, 100, 1)
        if okPressed:
            self.sudoku_size = i
        dialog.close()

    def init_field(self):
        for i in range(self.sudoku_size ** 2):
            if i % self.sudoku_size == 0:
                border_y = 20
            else:
                border_y = 10
            delta_y = 40 * i
            for j in range(self.sudoku_size ** 2):
                if j % self.sudoku_size == 0 and j != 0:
                    border_x = 10
                else:
                    border_x = 5
                delta_x = 40 * j
                self.text = QLineEdit(self)
                self.text.setText("0")
                all_text_box.append(self.text)
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
        string = ''
        for i in all_text_box:
            string += i.text()
        init_field_from_str_zero(string)
        print (string)
        print (input_sudoku_field)
        if isGood():
            start_solving()
            self.show_solved()
            self.info.setText("Successfully")
        else:
            self.info.setText("Unavailable to solve")

    def show_solved(self):
        result = ""
        capacity = len(input_sudoku_field)
        for i in range(capacity):
            for j in range(int(math.sqrt(math.sqrt(capacity * len(input_sudoku_field[0]))))):
                result += input_sudoku_field[i][j].__str__()
        for i in range(len(result)):
            all_text_box[i].setText(result[i])
        print(result)



def isGood():
    position = (0, 0)
    mini_row_count = len(input_sudoku_field)
    mini_row_capacity = len(input_sudoku_field[0])
    if not (isUnique(extract_row(position)) and isUnique(extract_square(position)) and isUnique(extract_column(position))):
        return False
    while position != (mini_row_count, mini_row_capacity):
        if position[1] != mini_row_capacity - 1:
            position = (position[0], position[1] + 1)
        else:
            position = (position[0] + 1, 0)
        if not (isUnique(extract_row(position)) and isUnique(extract_square(position)) and isUnique(extract_column(position))):
            return False
    return True

def isUnique(sets):
    return uniqueFlag

def init_field_from_str_zero(string):
    """В двумерный массив из строчки с нулями """
    dimension = int(math.sqrt(len(string)))
    mini_row_dimension = int(math.sqrt(dimension))
    num_pos_count = 0
    mini_row = []
    for i in string:
        if i != '\n':
            if num_pos_count != mini_row_dimension:
                mini_row.append(int(i))
                num_pos_count += 1
            else:
                input_sudoku_field.append(mini_row)
                num_pos_count = 0
                mini_row = []
                mini_row.append(int(i))
                num_pos_count += 1
    input_sudoku_field.append(mini_row)

def is_solved(field):
    """Метод, проверяющий решена ли судоку (нет свободных клеток)"""
    capacity = len(field)
    for i in range(capacity):
        for j in range(int(math.sqrt(math.sqrt(capacity * len(field[0]))))):
            if field[i][j] == 0:
                return False
    return True

def extract_row(position):
    """Возращает элементы строки по позиции элемента"""
    mini_row_capacity = len(input_sudoku_field[0])
    row = set()
    global uniqueFlag
    start_mini_row = position[0]
    while start_mini_row % mini_row_capacity != 0:
        start_mini_row -= 1
    for row_pos in range(start_mini_row, start_mini_row + mini_row_capacity, 1):
        for i in range(mini_row_capacity):
            number = input_sudoku_field[row_pos][i]
            if row.__contains__(number):
                uniqueFlag = False
            if number != 0:
                row.add(number)
    return row

def extract_column(position):
    """Возращает элементы столбца по позиции элемента"""
    mini_row_capacity = len(input_sudoku_field[0])
    column = set()
    global uniqueFlag
    # проверяет элементы сверху
    for i in range(position[0], -1, (-1) * mini_row_capacity):
        number = input_sudoku_field[i][position[1]]
        if column.__contains__(number):
            uniqueFlag=False
        if number != 0:
            column.add(input_sudoku_field[i][position[1]])

    # проверяет элементы снизу
    for i in range(position[0] + mini_row_capacity, len(input_sudoku_field), mini_row_capacity):
        number = input_sudoku_field[i][position[1]]
        if column.__contains__(number):
            uniqueFlag = False
        if number != 0:
            column.add(input_sudoku_field[i][position[1]])
    return column

def extract_square(position):
    """Возращает элементы квадрата по позиции элемента"""
    row_capacity = int(math.sqrt(len(input_sudoku_field) * len(input_sudoku_field[0])))
    mini_row_capacity = int(math.sqrt(row_capacity))
    square = set()
    global uniqueFlag
    starting_pos = position[0]

    starting_pos_list = []
    for i in range(0, len(input_sudoku_field), mini_row_capacity ** 2):
        for j in range(mini_row_capacity):
            starting_pos_list.append(i + j)

    while starting_pos not in starting_pos_list:
        starting_pos -= mini_row_capacity

    for row_pos in range(starting_pos, starting_pos + (2 * mini_row_capacity), mini_row_capacity):
        for i in range(mini_row_capacity):
            number = input_sudoku_field[row_pos][i]
            if square.__contains__(number):
                uniqueFlag=False
            if number != 0:
                square.add(number)
    return square

def get_available_numbers(position):
    """Получает на вход число из клетки и возращает лист возможных чисел"""
    dimension = int(math.sqrt(len(input_sudoku_field) * len(input_sudoku_field[0])))
    number = input_sudoku_field[position[0]][position[1]]
    all_numbers = set(i for i in range(1, dimension + 1))
    # print("Our position", position)

    # получаем строку, столбец и квадрат, содержащие элемент
    row = extract_row(position)
    # print('Row for this position', row)
    column = extract_column(position)
    # print('Column for this position', column)
    square = extract_square(position)
    # print('Square for this position', square)

    return (row | column | square) ^ all_numbers

def go_up_tree(position_from, position_to):
    """Проходит от и до заданных позиций, при этом обнуляя значения"""
    while not position_from == position_to:
        if position_from in all_empty:
            input_sudoku_field[position_from[0]][position_from[1]] = 0
        if position_from[1] != 0:
            position_from = (position_from[0], position_from[1] - 1)
        else:
            position_from = (position_from[0] - 1, 2)
    input_sudoku_field[position_from[0]][position_from[1]] = 0

def find_empty(position):
    """Находит пустую клетку после заданной position """
    mini_row_count = len(input_sudoku_field)
    mini_row_capacity = len(input_sudoku_field[0])
    if position != (mini_row_count, mini_row_capacity) and not is_solved(input_sudoku_field):
        while input_sudoku_field[position[0]][position[1]] != 0:
            if position[1] != mini_row_capacity - 1:
                position = (position[0], position[1] + 1)
            else:
                position = (position[0] + 1, 0)
        if position not in all_empty:
            all_empty.append(position)
        return position

current_node = Node((0, 0))
current_edge = Edge(current_node, current_node, -1)
next_node = Node((0, 0))
previous_edge_to_double = []
tree = Tree()

def start_solving():
    """Метод, решающий судоку"""
    current_node = Node(find_empty((0, 0)))  # первый пустой элемент
    next_node = current_node  # следующий элемент
    current_edge = Edge(current_node, current_node,-1)  # текущая ветвь, имеет значение -1 так как замыкается на корневом элементе

    # запускаем цикл решения судоку
    while not is_solved(input_sudoku_field):
        # восстанавилваем данные с предыдущего витка
        previous_node = current_node
        current_node = next_node
        # if current_node not in tree.all_nodes:
        #     tree.all_nodes.append(current_node)  # добавляем новую вершину в дерево

        # находим новый вариант для текущей пустой клетки
        all_variants = get_available_numbers(current_node.value)

        # если ветвь указывает на ребро, у которого хотя бы 2 варианта, то ...
        if len(all_variants) > 1:
            previous_edge_to_double.append(
                current_edge)  # ... добавляем ее в список ветвей, указывающих на ребра с неоднозначным выбором

            # если у ребра нет варинтов дальнейшего построения (неверное предположение в прошлом)
        if len(all_variants) == 0:
            destination_edge = previous_edge_to_double.pop()
            if len(destination_edge.To.all_edges) > 2:
                previous_edge_to_double.append(destination_edge)
            destination_node = destination_edge.To
            go_up_tree(current_node.value, destination_edge.To.value)
            current_node = destination_node
            current_node.all_edges.remove(current_node.all_edges[0])
            current_edge = current_node.all_edges[0]

            # когда мы вышли из цикла (сделали новый выбор узла и ветви), устанавливаем новые значения узла и ветви
            value_to_apply = current_edge.value
            position_to_apply = current_node.value

        else:  # если изначально не было проблемы с выбором варианта, то ...
            # записываем и "закольцовываем" новые ветви из текущего узла
            for edge_value in all_variants:
                current_node.add_edge(edge_value)

                # устанавлиаем новые значения узла и ветви
            current_edge = current_node.all_edges[0]
            value_to_apply = current_edge.value
            position_to_apply = current_node.value

            # применяем новые значения на поле
        input_sudoku_field[position_to_apply[0]][position_to_apply[1]] = value_to_apply
        # ищем следующее пустое место и записывем его как следующее
        next_node = Node(find_empty(current_node.value))
        if next_node.value is not None:
            current_edge.To = next_node
        else:
            break


    # print(input_sudoku_field)


input_text = ""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = App()
    sys.exit(app.exec_())