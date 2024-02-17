#
#  Copyright 2014+ Carnegie Mellon University
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from flexneuart.config import STOPWORD_FILE
from flexneuart.io import open_with_default_enc


def read_stop_words(file_name=STOPWORD_FILE, lower_case=True):
    """Reads a list of stopwords from a file. By default the words
       are read from a standard repo location and are lowercased.

      :param file_name: a stopword file name
      :param lower_case:  a boolean flag indicating if lowercasing is needed.

      :return a list of stopwords
    """
    stop_words = []
    with open_with_default_enc(file_name) as f:
        for w in f:
            w = w.strip()
            if w:
                if lower_case:
                    w = w.lower()
                stop_words.append(w)

    return stop_words

