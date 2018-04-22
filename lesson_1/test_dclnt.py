# -*- coding: utf-8 -*-

import unittest
import dclnt


class TestDclnt(unittest.TestCase):

    def test_flat(self):
        self.assertEqual(dclnt.flat([(1, 2), (3, 4)]), [1, 2, 3, 4])

    def test_is_verb(self):
        self.assertEqual(dclnt.is_verb('main'), False)
        self.assertEqual(dclnt.is_verb('do'), True)

    def test_get_trees(self):
        pass

    def test_get_all_names(self):
        trees = dclnt.get_trees('./django')
        tree = trees[1]
        self.assertEqual(dclnt.get_all_names(tree), ['__name__', 'main'])

    def test_get_verbs_from_function_name(self):
        self.assertEqual(dclnt.get_verbs_from_function_name('main'), [])
        self.assertEqual(
            dclnt.get_verbs_from_function_name('do_something'), ['do']
        )
        self.assertEqual(
            dclnt.get_verbs_from_function_name('get_something'), ['get']
        )

    def test_get_all_names_in_path(self):
        self.assertEqual(
            dclnt.get_all_names_in_path('./django'),
            ['main']
        )








    def test_get_functions_names_from_trees(self):
        trees = dclnt.get_trees('./django')
        self.assertEqual(
            dclnt.get_functions_names_from_trees(trees),
            ['main', 'get_something']
        )



    def test_get_top_verbs_in_path(self):
        self.assertCountEqual(
            dclnt.get_top_verbs_in_path('./django'),
            [('get', 1)]
        )

    def test_get_top_functions_names_in_path(self):
        self.assertCountEqual(
            dclnt.get_top_functions_names_in_path('./django'),
            [('main', 1), ('get_something', 1)]
        )


if __name__ == "__main__":
    unittest.main()