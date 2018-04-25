# -*- coding: utf-8 -*-

import unittest

import get_top_verbs


class TestDclnt(unittest.TestCase):

    def setUp(self):
        self.path = './test/django'

    def test_flat(self):
        self.assertEqual(get_top_verbs.flat([(1, 2), (3, 4)]), [1, 2, 3, 4])

    def test_check_is_verb_with_ntlk(self):
        self.assertEqual(get_top_verbs.check_is_verb_with_ntlk('get'), True)
        self.assertEqual(get_top_verbs.check_is_verb_with_ntlk('set'), False)

    def test_is_function_name_valid(self):
        self.assertEqual(get_top_verbs.is_function_name_valid('get'), True)
        self.assertEqual(get_top_verbs.is_function_name_valid('__main__'), False)

    def test_get_filenames_with_ext_in_path(self):
        self.assertEqual(
            get_top_verbs.get_filenames_with_ext_in_path(self.path),
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
            get_top_verbs.get_filenames_with_ext_in_path('-'), []
        )

    def test_get_trees(self):
        self.assertEqual(len(get_top_verbs.get_trees(self.path)), 5)
        self.assertEqual(
            all([
                isinstance(t, get_top_verbs.ast.Module) for t in
                get_top_verbs.get_trees(self.path)
            ]),
            True
        )

    def test_get_trees_with_bad_path(self):
        self.assertEqual(len(get_top_verbs.get_trees('-')), 0)

    def test_get_verbs_from_function_name(self):
        self.assertEqual(get_top_verbs.get_verbs_from_function_name('main'), [])
        self.assertEqual(
            get_top_verbs.get_verbs_from_function_name('do_something'), ['do']
        )
        self.assertEqual(
            get_top_verbs.get_verbs_from_function_name('get_something'), ['get']
        )

    def test_get_functions_from_trees(self):
        trees = get_top_verbs.get_trees(self.path)
        self.assertEqual(
            get_top_verbs.get_functions_from_trees(trees),
            ['main', 'get_something', 'do_something']
        )

    def test_get_functions_names_from_functions(self):
        self.assertEqual(
            get_top_verbs.get_valid_functions_names_from_functions(
                ['get_something', '__main__']
            ),
            ['get_something']
        )

    def test_most_common_words(self):
        pass

    def test_get_top_verbs_in_path(self):
        self.assertCountEqual(
            get_top_verbs.get_top_verbs_in_path(self.path),
            [('get', 1), ('do', 1)]
        )

    def test_get_top_verbs_from_dirs(self):
        dirs = [
            'test/django',
            'test/flask'
        ]
        self.assertCountEqual(
            get_top_verbs.get_top_verbs_from_dirs(dirs),
            [('get', 1), ('do', 1)]
        )


if __name__ == "__main__":
    unittest.main()
