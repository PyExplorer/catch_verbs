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


def get_trees(path, with_filenames=False, with_file_content=False):
    filenames = []
    trees = []
    for dirname, dirs, files in os_walk(path, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os_path.join(dirname, file))
                if len(filenames) == 100:
                    break
    print('total %s files' % (len(filenames), ))
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

    print('trees generated')
    return trees


def get_verbs_from_function_name(function_name):
    res = []
    for word in function_name.split('_'):
        if not check_is_verb_with_ntlk(word):
            continue
        res.append(word)
    return res


def get_functions_names_from_trees(trees):
    functions = []
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue
            functions.append(node.name.lower())

    functions_names = []
    for func in flat([functions]):
        if not (func.startswith('__') and func.endswith('__')):
            functions_names.append(func)

    return functions_names


def get_top_verbs_in_path(path, top_size=10):
    trees = get_trees(path)
    functions_names = get_functions_names_from_trees(trees)

    print('functions extracted')
    verbs = flat(
        [get_verbs_from_function_name(function_name) for function_name in functions_names])
    return collections.Counter(verbs).most_common(top_size)


def main():
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    words = []
    for project in projects:
        path = os_path.join('.', project)
        words.extend(get_top_verbs_in_path(path))

    print(
        'total %s words, %s unique' % (
            len(words),
            len(set(words))
        )
    )

    top_size = 200
    for word, occurence in collections.Counter(words).most_common(top_size):
        print(word, occurence)


if __name__ == '__main__':
    main()
