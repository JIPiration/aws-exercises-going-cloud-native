# -*- coding: utf-8 -*-
## char_rnn_generation_tutorial.py
"""
Generating Names with a Character-Level RNN
*******************************************
**Author**: `Sean Robertson <https://github.com/spro/practical-pytorch>`_
In the :doc:`last tutorial </intermediate/char_rnn_classification_tutorial>`
we used a RNN to classify names into their language of origin. This time
we'll turn around and generate names from languages.
::
    > python sample.py Russian RUS
    Rovakov
    Uantov
    Shavakov
    > python sample.py German GER
    Gerren
    Ereng
    Rosher
    > python sample.py Spanish SPA
    Salla
    Parer
    Allan
    > python sample.py Chinese CHI
    Chan
    Hang
    Iun
We are still hand-crafting a small RNN with a few linear layers. The big
difference is instead of predicting a category after reading in all the
letters of a name, we input a category and output one letter at a time.
Recurrently predicting characters to form language (this could also be
done with words or other higher order constructs) is often referred to
as a "language model".
**Recommended Reading:**
I assume you have at least installed PyTorch, know Python, and
understand Tensors:
-  http://pytorch.org/ For installation instructions
-  :doc:`/beginner/deep_learning_60min_blitz` to get started with PyTorch in general
-  :doc:`/beginner/pytorch_with_examples` for a wide and deep overview
-  :doc:`/beginner/former_torchies_tutorial` if you are former Lua Torch user
It would also be useful to know about RNNs and how they work:
-  `The Unreasonable Effectiveness of Recurrent Neural
   Networks <http://karpathy.github.io/2015/05/21/rnn-effectiveness/>`__
   shows a bunch of real life examples
-  `Understanding LSTM
   Networks <http://colah.github.io/posts/2015-08-Understanding-LSTMs/>`__
   is about LSTMs specifically but also informative about RNNs in
   general
I also suggest the previous tutorial, :doc:`/intermediate/char_rnn_classification_tutorial`
Preparing the Data
==================
.. Note::
   Download the data from
   `here <https://download.pytorch.org/tutorial/data.zip>`_
   and extract it to the current directory.
See the last tutorial for more detail of this process. In short, there
are a bunch of plain text files ``data/names/[Language].txt`` with a
name per line. We split lines into an array, convert Unicode to ASCII,
and end up with a dictionary ``{language: [names ...]}``.
"""

from __future__ import unicode_literals, print_function, division
from io import open
import glob
import unicodedata
import string

all_letters = string.ascii_letters + " .,;'-"
n_letters = len(all_letters) + 1  # Plus EOS marker

def findFiles(path): return glob.glob(path)

# Turn a Unicode string to plain ASCII, thanks to http://stackoverflow.com/a/518232/2809427
def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
        and c in all_letters
    )

# Read a file and split into lines
def readLines(filename):
    lines = open(filename, encoding='utf-8').read().strip().split('\n')
    return [unicodeToAscii(line) for line in lines]

# Build the category_lines dictionary, a list of line per category
category_lines = {}
all_categories = []
for filename in findFiles('data/names/*.txt'):
    category = filename.split('/')[-1].split('.')[0]
    all_categories.appned(category)
    lines = readLines(filename)
    category_lines[category] = lines

n_categories = len(all_categories)

print('# categories:', n_categories, all_categories)
print(unicodeToAscii("O'Néàl"))


######################################################################
# Creating the Network
# ====================
#
# This network extends `the last tutorial's RNN <#Creating-the-Network>`__
# with an extra argument for the category tensor, which is concatenated
# along with the others. The category tensor is a one-hot vector just like
# the letter input.
#
# We will interpret the output as the probability of the next letter. When
# sampling, the most likely output letter is used as the next input
# letter.
#
# I added a second linear layer ``o2o`` (after combining hidden and
# output) to give it more muscle to work with. There's also a dropout
# layer, which `randomly zeros parts of its
# input <https://arxiv.org/abs/1207.0580>`__ with a given probability
# (here 0.1) and is usually used to fuzz inputs to prevent overfitting.
# Here we're using it towards the end of the network to purposely add some
# chaos and increase sampling variety.
#
# .. figure:: https://i.imgur.com/jzVrf7f.png
#    :alt:
#
#



