import ast
import collections
from os import path as os_path
from os import walk as os_walk

from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    res = []
    for item in _list:
        res.extend(list(item))
    return res


def check_is_verb_with_ntlk(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def is_function_name_valid(func):
    return not (func.startswith('__') and func.endswith('__'))


def get_filenames_with_ext_in_path(path, ext='.py', max_size=100):
    filenames = []
    for dirname, dirs, files in os_walk(path, topdown=True):
        for file in files:
            if not file.endswith(ext):
                continue
            filenames.append(os_path.join(dirname, file))
            if len(filenames) == max_size:
                break

    print('total {} files'.format(len(filenames)))
    return filenames


def get_trees(path, with_filenames=False, with_file_content=False):
    filenames = get_filenames_with_ext_in_path(path)

    trees = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as opened_file:
            main_file_content = opened_file.read()
        try:
            tree = ast.parse(main_file_content)
        except SyntaxError as e:
            print(e)
            tree = None
        except Exception as e:
            print('Something went wrong %s' % (e,))
            tree = None

        if not tree:
            continue

        if not with_filenames:
            trees.append(tree)
            continue

        if with_file_content:
            trees.append((filename, main_file_content, tree))
            continue

        trees.append((filename, tree))

    print('{} trees generated'.format(len(trees)))
    return trees


def get_verbs_from_function_name(function_name):
    verbs = []
    for word in function_name.split('_'):
        if not check_is_verb_with_ntlk(word):
            continue
        verbs.append(word)
    return verbs


def get_functions_from_trees(trees):
    functions = []
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            functions.append(node.name.lower())
    return functions


def get_valid_functions_names_from_functions(functions):
    functions_names = []
    for func in functions:
        if is_function_name_valid(func):
            functions_names.append(func)
    return functions_names


def get_most_common_words(words, top_size=200):
    return collections.Counter(words).most_common(top_size)


def get_top_verbs_in_path(path, top_size=10):
    trees = get_trees(path)
    functions = get_functions_from_trees(trees)
    functions_names = get_valid_functions_names_from_functions(functions)
    print('{} functions extracted'.format(len(functions_names)))
    verbs = []
    for function_name in functions_names:
        verbs_from_function = get_verbs_from_function_name(function_name)
        verbs.extend(verbs_from_function)
    verbs = get_most_common_words(verbs, top_size)
    print('{} verbs extracted'.format(len(verbs)))

    return verbs


def get_top_verbs_from_projects(projects):
    verbs = []
    for project in projects:
        path = os_path.join('.', project)
        print('--- {} ---'.format(path))
        verbs.extend(get_top_verbs_in_path(path))
    return verbs


def print_results(results):
    for result in results:
        print(*result)


def main():
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    top_verbs = get_top_verbs_from_projects(projects)

    print('total {} words, {} unique'.format(
        len(top_verbs), len(set(top_verbs)))
    )

    most_common_words = get_most_common_words(top_verbs)

    print_results(most_common_words)


if __name__ == '__main__':
    main()
