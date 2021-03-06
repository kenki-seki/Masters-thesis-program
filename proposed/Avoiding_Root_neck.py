import time
import random
import math
import networkx as nx
import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt
from numpy.random import poisson #use_poisson
import myfunc

av_suvtime = 180.0
if __name__ == '__main__':

    t1 = time.time()
    graph = myfunc.add_node_and_edge()
    t2 = time.time()
    link = myfunc.link_init()
    outbreak = 0
    call_loss = 0
    lam = 100

    #以下、ループ処理
    while outbreak <= 100000:
        outbreak +=1
        start, goal = myfunc.define_passroot()
        print ("from:"+ str(start) +" to:"+ str(goal), end=" ")
        #passnodeはlist型
        passnode = nx.dijkstra_path(graph, str(start), str(goal))
        print (passnode, end="")
        print(len(passnode))
        #経由ノードから経由エッジを取得
        edge_list = [0 for i in range(len(passnode)-1)]
        for i in range(len(passnode)-1):
            for j in range(len(link)):
                if (link[j][0].conection1 == int(passnode[i]) and link[j][0].conection2 == int(passnode[i + 1])):
                    edge_list[i] = j
                    continue
                elif(link[j][0].conection1 == int(passnode[i + 1]) and link[j][0].conection2 == int(passnode[i])):
                    edge_list[i] = j
                    continue
        print(edge_list)
        '''
        print (nx.dijkstra_path_length(graph, str(start), str(goal)))
        '''
        slot, surv_time = myfunc.define_pass_condition(nx.dijkstra_path_length(graph, str(start), str(goal)), av_suvtime)
        print('seizon' + str(surv_time))
        #収容可否確認
        sum_link_status = [0 for i in range(100)]
        for i in range(len(edge_list)):
            use_link = edge_list[i]
            for j in range(100):
                sum_link_status[j] += link[use_link][j].conection_number
        #呼損
        #パス収容
        available_slot = 0
        avoid = [0 for i in range(slot)]
        for i in range(len(sum_link_status)):
            if sum_link_status[i] == 0:
                print("avoid:" + str(avoid))
                print(i)
                avoid[available_slot] = i
                available_slot +=1
                if available_slot == slot:
                    available = 1
                    break
            else:
                available_slot = 0
                available = 0

        print (available_slot)
        print (avoid)
        if available == 1:
            for i in range(len(edge_list)):
                for j in range(len(avoid)):
                    link[int(edge_list[i])][avoid[j]].conection_number = outbreak
                    link[int(edge_list[i])][avoid[j]].suvtime = surv_time
                    link[int(edge_list[i])][avoid[j]].start = start
                    link[int(edge_list[i])][avoid[j]].goal = goal
        else:
            print(outbreak)
            call_loss += 1
            print("call_loss:" + str(call_loss))

        #時間を進める
        foword = np.random.exponential(1/lam)
        for i in range(len(link)):
            for j in range(100):
                if link[i][j].suvtime > 0.0:
                    link[i][j].suvtime -= foword
                    if link[i][j].suvtime < 0:
                        print("syokika")
                        link[i][j].conection_number = 0
                        link[i][j].suvtime = 0
                        link[i][j].start = 0.0
                        link[i][j].goal = 0
        print(foword)
        #表示がヤバイデバッグ用
        # if available == 1:
        #     for i in range(len(edge_list)):
        #         print('conection_number:' + str(outbreak))
        #         print('link' + str(edge_list[i]))
        #         for j in range(100):
        #             print("(" + str(link[edge_list[i]][j].start) + ", " + str(link[edge_list[i]][j].goal) + ", " + str(link[edge_list[i]][j].conection_number) + ")", end=", ")

        print("slot = " + str(slot) + ", survival = " + str(surv_time) + ", next_breaktime = " + str(myfunc.next_node_event(0.01)))

    t3 = time.time()

    elapsed_time = t2-t1
    print(f"経過時間：{elapsed_time}")
    elapsed_time = t3-t2
    print(f"経過時間：{elapsed_time}")

    # レイアウトの取得

    pos = nx.spring_layout(graph)

    # 可視化

    plt.figure(figsize=(12, 12))
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_nodes(graph, pos, font_size=16)
    nx.draw_networkx_labels(graph, pos, font_size=16, font_color="b")
    plt.axis('off')
    plt.show()
