from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))
#
# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.1.3'
DESCRIPTION = 'A sorted multiset can store multiple values in sorted order unlike a normal set'
LONG_DESCRIPTION = """
Used a balanced binary search to implement this  one in which will work like max heap and min heap
with extra operation like searching in the list in just O(Log N) operations.
1)A orderdmultiset is a module which has same behavior like cpp multiset.



2)it is most important for cosing community which help to grow python in coding community.

3)it has various functions like appending an element, erasing an element,searching an element,
poping out an element from left and poopoing out an element from right all operations done in O(log n) times.

4)we can make a ascending multiset as well as descending multiset via providing a parameter in object reverse=True for descending.

- How to create multiset :-->
    For asceding multiset:->
        var_name=sortedmultiset.orderdmultiset(reverse=False)#--->To create an object of ascending sorted multiset .
        -reverse=False is optional for ascending multiset it is bydefault parameter.
    For descending multiset:->
        var_name=sortedmultiset.orderdmultiset(reverse=True)#--->To create an object of descending sorted multiset.
        -reverse=True is required while creating descending multiset.
-Functions :-->
    var_name.append(element:int)#---> To add an element in  O(log n).
    var_name.search(element:int)#--->To search an element in O(log n).
    var_name.erase(element:int)#--->To delete an element in O(log n).
    var_name.popleft()#--------> To delete the First/Leftmost most element in O(log n).
    var_name.popright()#--------> To delete the Last/Rightmost most element in O(log n).

-To access all the stored elements u can use following syntax:-->
    var_name.multiset---> A list where all the element are stored.
"""

# Setting up
setup(
    name="sortedmultiset",
    version=VERSION,
    author="Rushikesh Sunil Kotkar",
    author_email="<rshksh019@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'multiset'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        # "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)