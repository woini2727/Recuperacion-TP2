import math

def calc_simi(tabla_pesos,tabla_idf,query,ndocs):
    ranking={}
    sim=0
    for i in range(1,ndocs+1):

        prod_escal=prod_escalar(i,query,tabla_idf,tabla_pesos)
        print("prod_E",prod_escal)
        normaq=norma_q(query,tabla_idf)
        print("NorQ",normaq)
        normad=norma_d(i,query,tabla_pesos)
        print("NorD",normad)
        if normad != 0:
            sim=prod_escal/(normad*normaq)

        ranking[i]=sim
        sim = 0

    return ranking

def norma_q(query,tabla_idf):
    pesos_q=0
    for termino in query.keys():
        if termino in tabla_idf.keys():
            idf = tabla_idf[termino]
            pesos_q += pow(idf * (1 + math.log(query[termino], 2)),2)
    pesos_q=math.sqrt(pesos_q)
    return  pesos_q

def norma_d(iddoc,query,tabla_pesos):
    normad=0
    for termino in query.keys():
        if termino in tabla_pesos.keys():
           dicc_doc=tabla_pesos[termino]
           if iddoc in dicc_doc:
              normad+=pow(dicc_doc[iddoc],2)

    normad=math.sqrt(normad)

    return normad
def prod_escalar(iddoc,query,tabla_idf,tabla_pesos):
    producto=0
    for termino in query.keys():
        if termino in tabla_pesos.keys():
           dicc_doc = tabla_pesos[termino]
           idf= tabla_idf[termino]
           if iddoc in dicc_doc:
                producto+=idf * (1 + math.log(query[termino], 2))*dicc_doc[iddoc]
    return producto