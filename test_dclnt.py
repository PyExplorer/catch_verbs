# -*- coding: utf-8 -*-

import unittest

import dclnt


class TestDclnt(unittest.TestCase):

    def setUp(self):
        self.path = './test/django'

    def test_flat(self):
        self.assertEqual(dclnt.flat([(1, 2), (3, 4)]), [1, 2, 3, 4])

    def test_check_is_verb_with_ntlk(self):
        self.assertEqual(dclnt.check_is_verb_with_ntlk('get'), True)
        self.assertEqual(dclnt.check_is_verb_with_ntlk('set'), False)

    def test_is_function_name_valid(self):
        self.assertEqual(dclnt.is_function_name_valid('get'), True)
        self.assertEqual(dclnt.is_function_name_valid('__main__'), False)

    def test_get_filenames_with_ext_in_path(self):
        self.assertEqual(
            dclnt.get_filenames_with_ext_in_path(self.path),
            [
                './test/django/file_1.py',
                './test/django/file_2.py',
                './test/django/dir_2/file_5.py',
                './test/django/dir_2/file_4.py',
                './test/django/dir_1/file_3.py'
            ]
        )

    def test_get_filenames_with_ext_in_path_with_bad_path(self):
        self.assertEqual(
            dclnt.get_filenames_with_ext_in_path('-'), []
        )

    def test_get_trees(self):
        self.assertEqual(len(dclnt.get_trees(self.path)), 5)
        self.assertEqual(
            all([
                isinstance(t, dclnt.ast.Module) for t in
                dclnt.get_trees(self.path)
            ]),
            True
        )

    def test_get_trees_with_bad_path(self):
        self.assertEqual(len(dclnt.get_trees('-')), 0)

    def test_get_verbs_from_function_name(self):
        self.assertEqual(dclnt.get_verbs_from_function_name('main'), [])
        self.assertEqual(
            dclnt.get_verbs_from_function_name('do_something'), ['do']
        )
        self.assertEqual(
            dclnt.get_verbs_from_function_name('get_something'), ['get']
        )

    def test_get_functions_from_trees(self):
        trees = dclnt.get_trees(self.path)
        self.assertEqual(
            dclnt.get_functions_from_trees(trees), ['main', 'get_something']
        )

    def test_get_functions_names_from_functions(self):
        self.assertEqual(
            dclnt.get_valid_functions_names_from_functions(
                ['get_something', '__main__']
            ),
            ['get_something']
        )

    def test_most_common_words(self):
        pass

    def test_get_top_verbs_in_path(self):
        self.assertCountEqual(
            dclnt.get_top_verbs_in_path(self.path),
            [('get', 1)]
        )

    def test_get_top_verbs_from_projects(self):
        projects = [
            'django',
            'flask'
        ]
        self.assertCountEqual(
            dclnt.get_top_verbs_from_projects(projects),
            [('get', 4), ('do', 1)]
        )


if __name__ == "__main__":
    unittest.main()
