import unittest
from unittest import mock

import catch_verbs


class TestDclnt(unittest.TestCase):

    def setUp(self):
        self.path = './test/django'
        self.tree_template = """
def main():
    pass
def get_something(param):
    pass
def do_something(param):
    pass
if __name__ == 'main':
    main()
"""

    def test_flat(self):
        self.assertEqual(catch_verbs.flat([(1, 2), (3, 4)]), [1, 2, 3, 4])

    def test_check_is_verb_with_ntlk(self):
        self.assertEqual(catch_verbs.check_is_verb_with_ntlk('get'), True)
        self.assertEqual(catch_verbs.check_is_verb_with_ntlk('set'), False)

    def test_is_function_name_valid(self):
        self.assertEqual(catch_verbs.is_function_name_valid('get'), True)
        self.assertEqual(catch_verbs.is_function_name_valid('__main__'), False)

    @mock.patch('catch_verbs.os_walk')
    def test_get_filenames_with_ext_in_path(self, mocked_os_walk):
        mocked_os_walk.return_value = [
            ['./test/django', ['dir_2', 'dir_1'], ['file_1.py', 'file_2.py']],
            ['./test/django/dir_2', [], ['file_5.py', 'file_4.py']],
            ['./test/django/dir_1', [], ['file_3.py']]
        ]
        self.assertEqual(
            catch_verbs.get_filenames_with_ext_in_path(self.path),
            [
                './test/django/file_1.py',
                './test/django/file_2.py',
                './test/django/dir_2/file_5.py',
                './test/django/dir_2/file_4.py',
                './test/django/dir_1/file_3.py'
            ]
        )

    @mock.patch('catch_verbs.os_walk')
    def test_get_filenames_with_ext_in_path_with_bad_path(self, mocked_os_walk):
        mocked_os_walk.return_value = []
        self.assertEqual(
            catch_verbs.get_filenames_with_ext_in_path('-'), []
        )

    @mock.patch('catch_verbs.get_tree')
    def test_get_trees(self, mocked_get_tree):
        mocked_get_tree.return_value = [
            catch_verbs.ast.parse(self.tree_template)
        ]
        self.assertEqual(len(catch_verbs.get_trees([
            '1.py', '2.py', '3.py'
        ])), 3)

    def test_get_trees_with_bad_path(self):
        self.assertEqual(len(catch_verbs.get_trees([])), 0)

    def test_get_verbs_from_function_name(self):
        self.assertEqual(catch_verbs.get_verbs_from_function_name('main'), [])
        self.assertEqual(
            catch_verbs.get_verbs_from_function_name('do_something'), ['do']
        )
        self.assertEqual(
            catch_verbs.get_verbs_from_function_name('get_something'), ['get']
        )

    @mock.patch('catch_verbs.get_trees')
    def test_get_functions_from_trees(self, mocked_get_trees):
        mocked_get_trees.return_value = [
            catch_verbs.ast.parse(self.tree_template)
        ]
        trees = catch_verbs.get_trees([])
        self.assertEqual(
            catch_verbs.get_functions_from_trees(trees),
            ['main', 'get_something', 'do_something']
        )

    def test_get_functions_names_from_functions(self):
        self.assertEqual(
            catch_verbs.get_valid_functions_names_from_functions(
                ['get_something', '__main__']
            ),
            ['get_something']
        )

    def test_most_common_words(self):
        pass

    @mock.patch('catch_verbs.get_valid_functions_names_from_functions')
    def test_get_top_verbs_in_path(
            self,
            mocked_get_valid_functions_names_from_functions
    ):
        mocked_get_valid_functions_names_from_functions.return_value = [
            'get_something', 'do_something'
        ]
        self.assertCountEqual(
            catch_verbs.get_verbs_in_path(self.path),
            ['get', 'do']
        )

    @mock.patch('catch_verbs.get_verbs_in_path')
    def test_get_top_verbs_from_dirs(self, mocked_get_verbs_in_path):
        mocked_get_verbs_in_path.return_value = ['get', 'do']
        dirs = ['1', '2']
        self.assertCountEqual(
            catch_verbs.get_verbs_from_dirs(dirs),
            ['get', 'get', 'do', 'do']
        )


if __name__ == "__main__":
    unittest.main()
