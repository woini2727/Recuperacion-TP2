import sys
import indexer as indx
import ranking as rank



def main(argv):
    ##--------------------------------------------------------------##
    ##             generar vocabulario y tabla de pesos             ##
    ##--------------------------------------------------------------##
    voc={}
    tabla_idf={}
    tabla_pesos={}
    voc=indx.index(argv)
    ndocs=indx.ndocs(argv)
    tabla_idf=indx.idf(ndocs)
    tabla_pesos=indx.calc_weights(voc,tabla_idf)
    print(tabla_idf)
    print(tabla_pesos)
    ##--------------------------------------------------------------##
    ##                          Rankear
    ##--------------------------------------------------------------##

    query   = input("Ingrese query: termino,termino,... \n")

    query_list=query.split(",")
    query_dicc={}
    for termino in query_list:
        if termino not in query_dicc:
           query_dicc[termino]=1
        else:
            value=query_dicc[termino]
            query_dicc[termino]+=1
    print(query_dicc)
    ranking=rank.calc_simi(tabla_pesos,tabla_idf,query_dicc,ndocs)
    print(ranking)



if __name__ == "__main__":
        main(sys.argv[1:])
