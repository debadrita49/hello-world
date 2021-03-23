import csv
import os
import re

import PyPDF2
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')


read_keyword = open('keywords', encoding='utf8')
keyword_file = read_keyword.read().lower()


def keyword_index(ip):
    key_words = list()
    words = ip.split()
    for ele in words:
        if ele not in key_words:
            key_words.append(ele)
    return key_words


keyword_set = list(keyword_index(keyword_file))
print(f'Keywords:\n{keyword_set}')
c = 0
docs = dict()
# print(f'Document Collection:')
for folder_name, sub_folders, files in os.walk(r"/home/debadrita/Documents/doc"):
    for file in files:
        pdf_read = PyPDF2.PdfFileReader(os.path.join(folder_name, file))
        num_pages = pdf_read.getNumPages()
        text = ""

        my_list = dict()
        for i in range(num_pages):
            my_pdf = pdf_read.getPage(i)
            text += my_pdf.extractText()

            my_list[file] = text.lower()
            stop_words = stopwords.words('english')
            tokens = re.sub("[^a-zA-Z]+", "", my_list[file]).split()
            my_list[file] = tokens

        docs[file] = my_list[file]
# print(docs)


idx = {}
d = 0
for pg in docs:
    d += 1
    for keyword in keyword_set:
        idx.setdefault(keyword, [])
        for word in docs[pg]:
            if keyword in word:
                if keyword not in idx:
                    idx[keyword].append(d)
                else:
                    idx[keyword].append(d)
            if not idx[keyword]:
                del idx[keyword]


for k in list(idx):
    final = idx[k]
    print(k, final)

p = 0
with open('pdf1_trial.csv', 'w') as index:
    write_ = csv.writer(index)
    for line in sorted(idx.keys()):
        p += 1
        write_.writerow([line] + idx[line])


with open('pdf2_trial.csv', 'w') as index:
    write_ = csv.writer(index)
    for line in sorted(idx.keys()):
        write_.writerow(''.join(format(my_int, 'x') for my_int in idx[line]))
#  '02x' use for numbers lower than 16



