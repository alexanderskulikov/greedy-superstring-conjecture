import string_methods as st
import unittest


class TestStringMethods(unittest.TestCase):
    def test_overlap_short(self):
        for (first, second, length) in [
            ("a", "a", 1),
            ("a", "b", 0),
            ("ab", "ba", 1),
            ("aba", "bab", 2),
            ("aba", "aba", 3),
            ("abb", "bab", 1),
            ("abb", "aba", 0),
            ("abc", "bca", 2),
        ]:
            self.assertEquals(st.overlap(first, second), length)

    def test_overlap_medium(self):
        for length in [10, 100, 1000, 10000]:
            first_string = "a" * length + "b" * length
            second_string = "b" * length + "a" * length
            self.assertEquals(st.overlap(first_string, second_string), length)


if __name__ == '__main__':
    unittest.main()
