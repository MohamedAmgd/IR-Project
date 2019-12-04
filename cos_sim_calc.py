import collections
import math


def char_counter(text, char):
    count = 0
    for i in text:
        if i == char:
            count += 1
    return count


def char_dic_from_file(path):
    with open(path) as file:
        text = file.read()
        dic = char_dic(text.replace(".txt", ""))
    return dic


def char_dic(input_text):
    if input_text == "":
        return None
    dic = {}
    text = input_text.casefold().swapcase().replace(' ', '')
    for i in range(65, 91):
        x = char_counter(text, chr(i))
        if x == 0:
            continue
        dic[chr(i)] = x
    return dic


def tf_dic_from_char_dic(dic):
    max_num = 0
    result = {}
    for i in dic:
        if dic[i] > max_num:
            max_num = dic[i]
    for i in dic:
        result[i] = dic[i] / max_num
    return result


def idf_dic(list_doc):
    result = {}
    for i in range(65, 91):
        x = 0
        for j in list_doc:
            if chr(i) in j:
                x += 1
        if x == 0:
            continue
        result[chr(i)] = math.log2(6 / x)
    return result


def tf_idf(tf_dic, idf):
    result = {}
    for i in idf:
        if i not in tf_dic:
            tf = 0
        else:
            tf = tf_dic[i]
        result[i] = tf * idf[i]
    return result


def cos_sim(tf_idf_doc, tf_idf_q):
    numerator = 0
    sum_doc_square = 0
    sum_q_square = 0
    for i in tf_idf_q:
        numerator += tf_idf_q[i] * tf_idf_doc[i]
        sum_doc_square += tf_idf_doc[i] * tf_idf_doc[i]
        sum_q_square += tf_idf_q[i] * tf_idf_q[i]
    denominator = math.sqrt(sum_q_square * sum_doc_square)
    return numerator / denominator


def calc_result(query, list_path):
    list_doc = [char_dic(query)]
    if len(list_path) != 0:
        for i in list_path:
            x = char_dic_from_file(i)
            if x is not None:
                list_doc.append(x)
    tf_list = []
    for i in list_doc:
        tf_list.append(tf_dic_from_char_dic(i))
    idf = idf_dic(list_doc)
    result = {}
    for i in range(1, len(tf_list)):
        result[list_path[i-1]] = cos_sim(tf_idf(tf_list[i], idf),
                                         tf_idf(tf_list[0], idf))
    return result


if __name__ == '__main__':
    l = ["d1.txt", "d2.txt", "d3.txt", "d4.txt", "d5.txt"]
    print(calc_result("z z z z z z z", l))
