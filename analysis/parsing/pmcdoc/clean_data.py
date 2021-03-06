# -*- coding: utf-8 -*-
#
# Clean the data, and delete invalid file
#
import re
import nltk
nltk.data.path.append("/nltk")
import logging

import sys
sys.path.insert(0, 'util/')
import opfiles
import readwrite

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)


def remove_newline(line):
    return filter(lambda x: x != "", re.split("\n", line))


def remove_blank(line):
    return filter(lambda x: x != "", re.split(" ", line))


def cleaning(content, threashold=0.85):
    # remove [...]
    compile = re.compile("\[.*?\]", re.S)
    draft = re.sub(compile, "", content)
    # remove (...)
    compile = re.compile("\(.*?\)", re.S)
    draft = re.sub(compile, "", draft)
    # remove newline
    test = re.sub("\n", " ", draft)
    # take sentence
    sentences = nltk.sent_tokenize(test)
    # filter sentence
    valid_sentences = []
    for s in sentences:
        if 1.0 * len(re.sub("\d", "", s)) / len(s) > threashold:
            # remove non-word character
            t = re.sub("\W", " ", s)
            # remove blank
            t = remove_blank(t)
            # rebuild to sentence
            rebuild = " ".join(t)
            valid_sentences.append(rebuild)
    return valid_sentences


def format_file(data):
    abstract = "".join(data["abstract"])
    body = "".join(data["body"])
    abstract = cleaning(abstract)
    body = cleaning(body)
    return {
        "pmc_id": data["pmc_id"],
        "abstract": abstract,
        "body": body
    }


def append_to_smallfile(data, o):
    files = opfiles.list_files(o)
    len_of_o = len(files)
    if opfiles.get_file_size(o + str(len_of_o - 1)) / 1024.0 < 30:
        out_path = o + "0" if len_of_o == 0 else o + str(len_of_o - 1)
    else:
        out_path = o + str(len_of_o)
    out_string = ("...".join(data) + "\n").lower()
    readwrite.write_to_txt(out_string, out_path, type="a")


def append_to_bigfile(path, data, o):
    doc_id = re.sub("\D+", "", path)
    out_string = (doc_id + "::" + "...".join(data) + "\n").lower()
    readwrite.write_to_txt(out_string, o, type="a")


def main(in_path):
    paths = opfiles.list_files(in_path + "parsed/")
    opfiles.mkdir(in_path + "parsed_all/abstract/")
    opfiles.mkdir(in_path + "parsed_all/doc/")
    opfiles.delete_file(in_path + "parsed_all/all_in_one")

    logging.info('Start Cleaning...')
    for p in paths:
        logging.info('Cleaning document from the following path: ' + p)
        sdata, is_valid = opfiles.filter_by_file_size(p, in_size=10)
        if not is_valid:
            opfiles.delete_file(p)
            continue
        formated = format_file(sdata)
        readwrite.write_to_json(formated, p)
        # logging.info('Write document to following path...')
        append_to_smallfile(formated["abstract"],
                            in_path + "parsed_all/abstract/")
        append_to_smallfile(formated["body"],
                            in_path + "parsed_all/doc/")
        append_to_bigfile(p, formated["body"],
                          in_path + "parsed_all/all_in_one")


if __name__ == '__main__':
    data_in_path = "data/"
    main(data_in_path)
