import unittest
import sudoku


class TestRoom (unittest.TestCase):
    def test_remove_blank(self):
        string = "2 4  5 6"
        result = sudoku.remove_blanks(string)
        self.assertEqual(sudoku.remove_blanks(result),"2456")

    def test_get_shifts_num(self):
        string = "1 2\n 4 3 \n 2 3"
        result = sudoku.get_num_of_shifts_and_transform(string)
        self.assertEqual(result, 2)

    def test_is_good(self):
        field = [[1,3],[3,0],[0,2],[0,0],[0,0],[2,0],[0,4],[3,1]]
        result = sudoku.is_good(field)
        self.assertEqual(result,False)

    def test_init_from_str(self):
        string = "1 3 4 2 4 2 1 3 3 1 2 4 2 0 3 1"
        field = sudoku.init_field_from_str_zero(string)
        self.assertEqual(field,[[1,3],[4,2],[4,2],[1,3],[3,1],[2,4],[2,0],[3,1]])

    def test_solved(self):
        field = [[1,3],[4,2],[4,2],[1,3],[3,1],[2,4],[2,0],[3,1]]
        result = sudoku.is_solved(field)
        self.assertEqual(result,False)
