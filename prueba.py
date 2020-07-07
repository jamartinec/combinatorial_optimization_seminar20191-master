# parallel.py

#from tests.test_caminos import *
#from tests.test_path_packing import *

#from tests.test_flows import *
#from tests.test_knapsack import *
#from tests.test_fourier_motzkin import *
from tests.test_shortest_path import *


import sys
import time

def main():
 
   start = time.time()
   #test_DFS() #tiene problema
   #test_dfs_iterative()
   #test_blocking_collection()
   #test_caminos_simples_st_prioritize_minlenFIFO()
   #test_reverse_blocking_collection()
   #test_menger_path_cut_speedup()
   #test_blocking_flow() #esto tiene problema
   #test_augmenting_along_flows()
   #test_kp_recursive()
   #test_kp_dynamicp()
   #test_f_m()
   #test_Dijkstra()
   #test_Bidirectional_Dijkstra()
   #test_SPPTW_basic_B()
   #test_SPPTW_basic()
   #test_spptw_desrochers1988_imp1()
   #test_spptw_desrochers1988_imp2()
   test_spptw_desrochers1988_imp3()
   end = time.time()
   print(end-start)

if __name__ == '__main__':
    main()



