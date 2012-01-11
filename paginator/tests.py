# -*- coding: utf-8 -*-
from django.utils import unittest
from paginator.utils import get_format_page_range


class PaginatorTest(unittest.TestCase):
    cases = [
            (1, 10, [1, 2, 3, None, 10]),
            (3, 10, [1, 2, 3, 4, None, 10]),
            (4, 10, [1, 2, 3, 4, 5, None, 10]),
            (10, 10, [1, None, 8, 9, 10]),
            (6, 10, [1, None, 5, 6, 7, None, 10]),
            (5, 20, [1, None, 4, 5, 6, None, 20]),
            (18, 20, [1, None, 17, 18, 19, 20]),
            (17, 20, [1, None, 16, 17, 18, 19, 20]),
            (16, 20, [1, None, 15, 16, 17, None, 20]),
            (15, 20, [1, None, 14, 15, 16, None, 20]),
            (20, 50, [1, None, 19, 20, 21, None, 50]),
            ]

    def test_simple(self):
        for num_page, pages_range, result in self.cases:
            test_result = get_format_page_range(num_page, pages_range)
            assert(test_result == result, "%s != %s (%s)" % (test_result, result, num_page))
