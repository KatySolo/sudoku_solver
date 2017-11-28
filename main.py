import time
import sys

input_sudoku_field = []
all_empty = []

input_sudoku_string_easy = "009582160" \
                           "017096030" \
                           "568070902" \
                           "426105700" \
                           "700024013" \
                           "090760054" \
                           "600800401" \
                           "900013825" \
                           "801207300"
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
input_sudoku_string_hardcore_2="7700108000" \
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


def init_field_from_str_zero(string):
    """В двумерный массив из строчки с нулями """
    num_pos_count = 0
    mini_row = []
    for i in string:
        if num_pos_count != 3:
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
    """Метод, проверяющий решена ли судоку (нет свободных клеток плюс другие критерии)"""
    for i in range(27):
        for j in range(3):
            if field[i][j] == 0:
                empty_x = i
                empty_y = j
                return False
    return True


def extract_row(position):
    """Возращает элементы строки по позиции элемента"""
    row = set()
    start_mini_row = position[0]
    while start_mini_row % 3 != 0:
        start_mini_row -= 1
    for row_pos in range(start_mini_row, start_mini_row + 3, 1):
        for i in range(3):
            number = input_sudoku_field[row_pos][i]
            if number != 0:
                row.add(number)
    return row


def extract_column(position):
    """Возращает элементы столбца по позиции элемента"""
    column = set()
    for i in range(position[0], -1, -3):
        number = input_sudoku_field[i][position[1]]
        if number != 0:
            column.add(input_sudoku_field[i][position[1]])

    for i in range(position[0] + 3, 27, 3):
        number = input_sudoku_field[i][position[1]]
        if number != 0:
            column.add(input_sudoku_field[i][position[1]])
    return column


def extract_square(position):
    """Возращает элементы квадрата по позиции элемента"""
    square = set()
    start_mini_row = position[0]
    while (start_mini_row - 2) % 9 != 0 and (start_mini_row - 1) % 9 != 0 and start_mini_row % 9 != 0:
        start_mini_row -= 3
    for row_pos in range(start_mini_row, start_mini_row + 7, 3):
        for i in range(3):
            number = input_sudoku_field[row_pos][i]
            if number != 0:
                square.add(number)
    return square


def get_available_numbers(position):
    """Получает на вход число из клетки и возращает лист возможных чисел"""
    number = input_sudoku_field[position[0]][position[1]]
    all_numbers = set(i for i in range(1, 10))
    # print("Our position", position)

    # получаем строку, столбец и квадрат, содержащие элемент
    row = extract_row(position)
    # print('Row for this position', row)
    column = extract_column(position)
    # print('Column for this position', column)
    square = extract_square(position)
    # print('Square for this position', square)

    return (row | column | square) ^ all_numbers

def make_sudoku_beautiful (field):
    count = 0
    result=[]
    line =[]
    for i in field:
        if count % 3 == 2:
            line.append(i)
            result.append(line)
            line=[]
        else:
            line.append(i)
        count += 1
    return result

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
    if position != (26, 2) and not is_solved(input_sudoku_field):
        while input_sudoku_field[position[0]][position[1]] != 0:
            if position[1] != 2:
                position = (position[0], position[1] + 1)
            else:
                position = (position[0] + 1, 0)
        if position not in all_empty:
            all_empty.append(position)
        return position


current_node = Node((0, 0))
current_edge=Edge(current_node,current_node,-1)
next_node = Node((0, 0))
previous_edge_to_double = []
tree = Tree()

start = time.time()
# print(start)

input_text=""
if __name__ == '__main__':
    # инициализируем поле
    # input_path = sys.argv[1]
    # with open (input_path,'r') as f:
    #     input_text += f.read()
    init_field_from_str_zero(input_sudoku_string_easy)
    make_sudoku_beautiful(input_sudoku_field)
    # устанавливем начальные данные для корневого элемента
    current_node = Node(find_empty((0, 0)))  # первый пустой элемент
    next_node = current_node  # следующий элемент
    current_edge = Edge(current_node, current_node,-1)  # текущая ветвь, имеет значение -1 так как замыкается на корневом элементе
    # root = Node(find_empty((0,0)))

    # tree = Tree(root)

    # all_variants = get_available_numbers(current_node.value)
    # if len(all_variants) > 1:
    #     previous_edge_to_double.append(Edge(root,root,-1))
    # for edge_value in all_variants:
    #     current_node.add_edge(edge_value)
    # current_edge = current_node.all_edges[0]
    # value_to_apply = current_edge.value
    # position_to_apply = current_node.value
    # input_sudoku_field[position_to_apply[0]][position_to_apply[1]]=value_to_apply
    # next_node = Node (find_empty(current_node.value))
    # current_edge.To = next_node

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
        previous_edge_to_double.append(current_edge)  # ... добавляем ее в список ветвей, указывающих на ребра с неоднозначным выбором

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
finish = time.time()
# print(finish)
print(finish - start)
# print(len(all_empty))
beautiful_output= make_sudoku_beautiful(input_sudoku_field)
with open ('output.txt','w') as f:
    for i in beautiful_output:
        f.write(str(i))
        f.write('\n')

# print (len(tree.all_nodes))