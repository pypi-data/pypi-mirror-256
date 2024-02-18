# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['embarrassment']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['pandas>=2,<3']

extras_require = \
{'docs': ['mkdocs>=1.5.3,<2.0.0',
          'mkdocs-material>=9.5.8,<10.0.0',
          'mkdocstrings[python]>=0.24.0,<0.25.0',
          'mkdocs-literate-nav>=0.6.1,<0.7.0',
          'mkdocs-gen-files>=0.5.0,<0.6.0',
          'mkdocs-section-index>=0.3.8,<0.4.0']}

setup_kwargs = {
    'name': 'embarrassment',
    'version': '0.1.0',
    'description': 'Convenience functions to work with pandas triple dataframes 🐼🐼🐼',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/embarrassment/raw/main/docs/logo.png" alt="kiez logo", width=200/>\n</p>\n<p align="center">\n<a href="https://github.com/dobraczka/embarrassment/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/embarrassment/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\nConvenience functions for pandas dataframes containing triples. Fun fact: a group of pandas (e.g. three) is commonly referred to as an [embarrassment](https://www.zmescience.com/feature-post/what-is-a-group-of-pandas-called-its-surprisingly-complicated/).\n\nThis library\'s main focus is to easily make commonly used functions available, when exploring [triples](https://en.wikipedia.org/wiki/Semantic_triple) stored in pandas dataframes. It is not meant to be an efficient graph analysis library.\n\nUsage\n=====\nYou can use a variety of convenience functions, let\'s create some simple example triples:\n```python\n>>> import pandas as pd\n>>> rel = pd.DataFrame([("e1","rel1","e2"), ("e3", "rel2", "e1")], columns=["head","relation","tail"])\n>>> attr = pd.DataFrame([("e1","attr1","lorem ipsum"), ("e2","attr2","dolor")], columns=["head","relation","tail"])\n```\nSearch in attribute triples:\n```python\n>>> from embarrassment import search\n>>> search(attr, "lorem ipsum")\n  head relation         tail\n0   e1    attr1  lorem ipsum\n>>> search(attr, "lorem", method="substring")\n  head relation         tail\n0   e1    attr1  lorem ipsum\n```\nSelect triples with a specific relation:\n```python\n>>> from embarrassment import select_rel\n>>> select_rel(rel, "rel1")\n  head relation tail\n0   e1     rel1   e2\n```\nPerform operations on the immediate neighbor(s) of an entity, e.g. get the attribute triples:\n```python\n>>> from embarrassment import neighbor_attr_triples\n>>> neighbor_attr_triples(rel, attr, "e1")\n  head relation   tail\n1   e2    attr2  dolor\n```\nOr just get the triples:\n```python\n>>> from embarrassment import neighbor_rel_triples\n>>> neighbor_rel_triples(rel, "e1")\n  head relation tail\n1   e3     rel2   e1\n0   e1     rel1   e2\n```\nBy default you get in- and out-links, but you can specify a direction:\n```python\n>>> neighbor_rel_triples(rel, "e1", in_out_both="in")\n  head relation tail\n1   e3     rel2   e1\n>>> neighbor_rel_triples(rel, "e1", in_out_both="out")\n  head relation tail\n0   e1     rel1   e2\n```\n\nUsing pandas\' [pipe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pipe.html) operator you can chain operations.\nLet\'s see a more elaborate example by loading a dataset from [sylloge](https://github.com/dobraczka/sylloge):\n\n```python\n>>> from sylloge import MovieGraphBenchmark\n>>> from embarrassment import clean, neighbor_attr_triples, search, select_rel\n>>> ds = MovieGraphBenchmark()\n>>> # clean attribute triples\n>>> cleaned_attr = clean(ds.attr_triples_left)\n>>> # find uri of James Tolkan\n>>> jt = search(cleaned_attr, query="James Tolkan")["head"].iloc[0]\n>>> # get neighbor triples\n>>> # and select triples with title and show values\n>>> title_rel = "https://www.scads.de/movieBenchmark/ontology/title"\n>>> neighbor_attr_triples(ds.rel_triples_left, cleaned_attr, jt).pipe(\n            select_rel, rel=title_rel\n        )["tail"]\n    )\n    12234    A Nero Wolfe Mystery\n    12282           Door to Death\n    12440          Die Like a Dog\n    12461        The Next Witness\n    Name: tail, dtype: object\n```\n\n\nInstallation\n============\nYou can install `embarrassment` via pip:\n```\npip install embarrassment\n```\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dobraczka/embarrassment',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
