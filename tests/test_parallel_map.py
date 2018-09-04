"""Implements tests for parllel map module.
"""
from unittest import TestCase

from mpischedule.parallel_map import parallel_map


class TestParallelMap(TestCase):
    """Tests `parallel_map`
    """

    def test_map_results(self):
        """Applies map to range and verfies results
        """
        x = range(20)
        func = lambda x: x ** 2

        result = map(func, x)
        parallel_result = parallel_map(func, x)

        self.assertListEqual(result, parallel_result)
