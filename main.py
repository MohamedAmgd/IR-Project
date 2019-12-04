import cos_sim_calc
import numpy as np
import math


def refer_to(file1_path, file2_path):
    with open(file1_path) as file:
        text = file.read()
        if file2_path.replace(".txt", "") in text:
            return 1
    return 0


def adj_calc(relevance_list):
    result = []
    for i in relevance_list:
        temp = []
        for j in relevance_list:
            if i == j:
                temp.append(0)
            else:
                temp.append(refer_to(i, j))
        result.append(temp)
        temp.clear
    return result


def HITS_algo(query, file_list):
    relevance_list = dict(filter(
        lambda x: x[1] > 0, cos_sim_calc.calc_result(query, file_list).items()))

    adj_list = adj_calc(relevance_list)
    adj = np.array(adj_list)
    hub = np.ones((len(relevance_list), 1))
    for i in range(20):
        auth = np.dot(np.transpose(adj), hub)
        hub = np.dot(adj, auth)
        norm_auth = np.linalg.norm(auth)
        auth = np.divide(auth, norm_auth)
        norm_hub = np.linalg.norm(hub)
        hub = np.divide(hub, norm_hub)
    auth_dic = {}
    hub_dic = {}
    count = 0
    for i in relevance_list:
        auth_dic[i] = auth[count][0]
        hub_dic[i] = hub[count][0]
        count += 1

    result = [dict(sorted(relevance_list.items(), key=lambda x: x[1], reverse=True)),
              dict(sorted(auth_dic.items(), key=lambda x: x[1], reverse=True)),
              dict(sorted(hub_dic.items(), key=lambda x: x[1], reverse=True))]
    return result


if __name__ == "__main__":
    paths_list = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt"]
    input_query = "A B C D E"
    print(HITS_algo(input_query, paths_list)[1])
