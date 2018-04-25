GTV - Get top verbs, please!


GTV is a static analysis tool for python code that catches verbs from functions name.

Example
From command line:

$ pytnon get_top_verbs.py 

--- . ---
total 7 files
7 trees generated
32 functions extracted
1 verbs extracted
total 1 words, 1 unique
('get', 19) 1


From python code:

>>> import get_top_verbs
>>> get_top_verbs.get_top_verbs_in_path('.')

--- . ---
total 7 files
7 trees generated
32 functions extracted
1 verbs extracted
total 1 words, 1 unique
('get', 19) 1


Installation
With pip:

pip install git+https://github.com/PyExplorer/get_top_verbs.git
Or just clone the project and install the requirements:

$ git clone https://github.com/PyExplorer/get_top_verbs.git
$ cd get_top_verbs
$ pip install -r requirements.txt

Docs
to be continue...

Contributing
To contribute, pick an issue to work on and leave a comment saying that you've taken the issue. Don't forget to mention when you want to submit the pull request.

Launch tests
python -m pytest
