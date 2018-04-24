# -*- coding: utf-8 -*-

import unittest
import dclnt


class TestDclnt(unittest.TestCase):

    def setUp(self):
        self.path = './test/django'

    def test_check_is_verb_with_ntlk(self):
        self.assertEqual(dclnt.check_is_verb_with_ntlk('main'), False)
        self.assertEqual(dclnt.check_is_verb_with_ntlk('do'), True)

    def test_get_trees(self):
        pass

    def test_get_verbs_from_function_name(self):
        self.assertEqual(dclnt.get_verbs_from_function_name('main'), [])
        self.assertEqual(
            dclnt.get_verbs_from_function_name('do_something'), ['do']
        )
        self.assertEqual(
            dclnt.get_verbs_from_function_name('get_something'), ['get']
        )

    def test_get_top_verbs_in_path(self):
        self.assertCountEqual(
            dclnt.get_top_verbs_in_path(self.path),
            [('get', 1)]
        )


if __name__ == "__main__":
    unittest.main()