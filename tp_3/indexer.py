import os.path
import sys
import glob
import errno
import tokenizer
import json
import math

def ndocs(argv):
    if not os.path.isdir(argv[0]):
            print(argv[0], " No es un directorio ")
            sys.exit(2)

    path = argv[0] + '/*.txt'
    files = glob.glob(path)
    vocabulario = {}
    cont_doc=0
    for name in files:
        cont_doc+=1
    return cont_doc

def index(argv):
    if not os.path.isdir(argv[0]):
            print(argv[0], " No es un directorio ")
            sys.exit(2)

    path = argv[0] + '/*.txt'
    files = glob.glob(path)
    vocabulario = {}
    cont_doc=0
    for name in files:
        cont_doc+=1
        try:
            with open(name, encoding="utf-8", errors="ignore") as f:
                filedata = f.read()
                lista_tokens = tokenizer.tokenizar(filedata)
                ##print(lista_tokens)
                for token in lista_tokens:
                    if token in vocabulario.keys():
                       doc_dic=vocabulario[token]
                       if cont_doc in doc_dic.keys():
                          tf=doc_dic[cont_doc]
                          doc_dic[cont_doc]= tf+1
                       else:
                          doc_dic[cont_doc]=1
                    if token not in vocabulario.keys():
                       doc_dic={}
                       doc_dic[cont_doc]=1
                       vocabulario[token]=doc_dic



        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise
    ##print(vocabulario)
    with open("tf_table.txt", encoding="utf-8", errors="ignore",mode="w") as tabla_tf:
        ##vocabulario = {'vocabulario': vocabulario}
        tabla_tf.write(json.dumps(vocabulario))

    return vocabulario
def idf(ndocs):
    datastore={}
    tabla_idf={}
    with open("tf_table.txt", encoding="utf-8", errors="ignore",mode="r") as tabla_tf:
        datastore = json.load(tabla_tf)

    for key in datastore.keys():
        cont_doc=0
        dicc=datastore[key]
        for k in dicc:
            cont_doc+=1
            tabla_idf[key]=round(math.log(ndocs/cont_doc,2),4)


    return tabla_idf

def calc_weights(vocabulario,tabla_idf):
    tabla_pesos={}
    with open("tf_table.txt", encoding="utf-8", errors="ignore", mode="r") as tabla_tf:
        datastore = json.load(tabla_tf)
    dicc={}
    for key in vocabulario.keys():
        idf=tabla_idf[key]
        dicc=vocabulario[key]

        for key in dicc.keys():
            value=dicc[key]
            dicc[key]=(1+math.log(value,2))*idf

    tabla_pesos=vocabulario
    ##print(tabla_pesos)
    return tabla_pesos