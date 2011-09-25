from __future__ import with_statement
import unittest
import calculate
from datetime import datetime, date
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class BaseTest(unittest.TestCase):
    
    def setUp(self):
        pass


class CalculateTest(BaseTest):
    
    def test_adjusted_monthly_value(self):
        self.assertEqual(
            calculate.adjusted_monthly_value(10, datetime(2009, 4, 1, 0, 10, 10)),
            10.0
        )
        self.assertEqual(
            calculate.adjusted_monthly_value(10, datetime(2009, 2, 17)),
            10.714285714285714
        )
        self.assertEqual(
            calculate.adjusted_monthly_value(10, date(2009, 12, 31)),
            9.67741935483871
        )
        with self.assertRaises(TypeError):
            calculate.adjusted_monthly_value('a', date(2009, 12, 31))
        with self.assertRaises(TypeError):
            calculate.adjusted_monthly_value(10, '2010-01-01')
        with self.assertRaises(TypeError):
            calculate.adjusted_monthly_value(10, 2)
    
    def test_benfords_law(self):
        self.assertEqual(
            calculate.benfords_law([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], verbose=False),
            -0.863801937698704
        )
        self.assertEqual(
            calculate.benfords_law([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], method="last_digit", verbose=False),
            0
        )
        with self.assertRaises(ValueError):
            calculate.benfords_law([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], method='magic')
        with self.assertRaises(TypeError):
            calculate.benfords_law(10.0)
    
    def test_competition_rank(self):
        dict_list = [
            {'name': 'Joan', 'value': 1},
            {'name': 'Jane', 'value': 2},
            {'name': 'Mary', 'value': 2},
            {'name': 'Josh', 'value': 3},
        ]
        self.assertEqual(
            calculate.competition_rank(dict_list, dict_list[0], 'value', 'desc'),
            4
        )
        self.assertEqual(
            calculate.competition_rank(dict_list, dict_list[1], 'value', 'desc'),
            2
        )
        self.assertEqual(
            calculate.competition_rank(dict_list, dict_list[2], 'value', 'desc'),
            2
        )
        self.assertEqual(
            calculate.competition_rank(dict_list, dict_list[3], 'value', 'desc'),
            1
        )
        class Dummy:
            def __init__(self, **entries): 
                self.__dict__.update(entries)
        obj_list = [Dummy(**d) for d in dict_list]
        self.assertEqual(
            calculate.competition_rank(obj_list, obj_list[0], 'value', 'asc'),
            1
        )
        self.assertEqual(
            calculate.competition_rank(obj_list, obj_list[1], 'value', 'asc'),
            2
        )
        self.assertEqual(
            calculate.competition_rank(obj_list, obj_list[2], 'value', 'asc'),
            2
        )
        self.assertEqual(
            calculate.competition_rank(obj_list, obj_list[3], 'value', 'asc'),
            4
        )
    
    def test_date_range(self):
        dr = calculate.date_range(datetime(2009,1,1, 12, 31, 00), date(2009,1,3))
        self.assertEqual(list(dr), [date(2009, 1, 1), date(2009, 1, 2),
            date(2009, 1, 3)])
        with self.assertRaises(ValueError):
            calculate.date_range(date(2011,1,1), date(2010,12,31))
    
    def test_decile(self):
        # Waiting on the percentile test to do this one
        pass
    
    def test_elfi(self):
        self.assertEqual(
            calculate.elfi([0.2, 0.5, 0.05, 0.25]),
            0.64500000000000002
        )
        self.assertEqual(calculate.elfi([1]), 0)
        self.assertEqual(calculate.elfi([0.5, 0.5]), 0.5)
        with self.assertRaises(ValueError):
            calculate.elfi(['a', 0.2, 3])
    
    def test_mean(self):
        self.assertEqual(calculate.mean([1,2,3]), 2.0)
        self.assertEqual(calculate.mean([1, 99]), 50.0)
        self.assertEqual(calculate.mean([2,3,3]), 2.6666666666666665)
        with self.assertRaises(ValueError):
            calculate.elfi(['a', 0.2, 3])
    
    def test_mean_center(self):
        dict_list = [
            {
                'name': 'The Los Angeles Times',
                'point': Point(-118.24551701545715, 34.05252608491458, srid=4326)
            },
            {
                'name': 'The Higgins Building',
                'point': Point(-118.245015, 34.051007, srid=4326)
            },
            {
                'name': 'Los Angeles City Hall',
                'point': Point(-118.24301719665527, 34.05357499274671, srid=4326)
            },
        ]
        self.assertEqual(type(calculate.mean_center(dict_list)), Point)
        self.assertEqual(
            calculate.mean_center(dict_list).wkt,
            'POINT (-118.2445164040374692 34.0523693592204282)'
        )
        class FakePoint(models.Model):
            name = models.TextField()
            point = models.PointField(srid=4326)
        obj_list = [FakePoint(**d) for d in dict_list]
        self.assertEqual(type(calculate.mean_center(obj_list)), Point)
        self.assertEqual(
            calculate.mean_center(obj_list).wkt,
            'POINT (-118.2445164040374692 34.0523693592204282)'
        )

if __name__ == '__main__':
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    