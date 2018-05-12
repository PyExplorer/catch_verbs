Catch verbs
==

Catch verbs is a static analysis tool for python code that catches verbs 
from functions name.

Example
--

**From command line:**

```
$ python3 catch_verbs.py 
```

```
--- . ---
total 7 files
7 trees generated
32 functions extracted
1 verbs extracted
total 1 words, 1 unique
('get', 19) 1
```

**From python code:**

```
>>> import catch_verbs
>>> catch_verbs.get_top_verbs_in_path('.')
```

```
--- . ---
total 7 files
7 trees generated
32 functions extracted
1 verbs extracted
total 1 words, 1 unique
('get', 19) 1
```

Requirements
--

- at least python 3.5
 

Installation
--

just clone the project and install the requirements:

```
$ git clone https://github.com/PyExplorer/catch_verbs.git
$ cd catch_verbs
$ pip3 install -r requirements.txt
```

Docs
--

The script has 3 option to run:


**-p (--path)** - path for searching *.py files (includung all subdirectories) 

**default:** '.' 

```
example: $ python3 catch_verbs.py -p './my_path'
```

**-d (--dirs)** - turn on filter by directories for searching from current path

It can be filled in config.json
  
**default:** 'django', 'flask', 'pyramid', 'reddit', 'requests', 'sqlalchemy'

```
example: $ python3 catch_verbs.py -p './my_path' -d
```

**-c (--config)** - Set the name and path for config

**default:** 'config.json' 

```
example: $ python3 catch_verbs.py -c './mydir/config.txt'
```

Contributing
--

To contribute, pick an issue to work on and leave a comment saying that you've taken the issue. Don't forget to mention when you want to submit the pull request.


Launch tests
--

*$ python3 -m unittest*
