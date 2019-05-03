import numpy as np
import matplotlib.pyplot as plt
import sys
import os.path
import glob
import errno
import re, string
from typing import List
from langdetect import detect
import unidecode


def remove_punctuation ( text ):
    text = text.replace("\n", " ")
    text = text.lower()
    text = unidecode.unidecode(text)
    return re.sub('[%s]' % re.escape(string.punctuation), '', text)

def remove_digits(lista_palabras):
    lista_palabras2=[]
    for palabra in lista_palabras:
        palabra_n=re.sub("\d+", " ", palabra)
        lista_palabras2.append(palabra_n)
    return lista_palabras2

def main(argv):
    abecedario=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    dist_eng_wiki=[8.2,1.5,2.8,4.3,12.7,2.2,2,6,7,0.2,0.8,4,2.4,6.8,7.5,1.9,0.1,6,6.3,9,2.8,1,2.4,0.2,2,0.1]
    dist_fr_wiki=[94,10,26,34,16,1,10,8,84,9,0,53,32,71,51,27,11,65,79,73,62,22,0,3,2,3]
    dist_it_wiki=[11.74,0.92,4.50,3.73,11.79,0,0,0.95,1.64,1.54,11.28,6.51,2.51,6.88,9.83,3.05,0.51,6.37,4.98,5.62,3.01,2.10 ,0,0,0,0.49]
    dist_eng=[]
    dist_fr=[]
    dist_it=[]

    dicc_global_uni={}
    dicc_global_bi={}
    dist=[]
##------------------------------------------------------------------------##
##                                Training
##------------------------------------------------------------------------##
    if not os.path.isdir(argv[0]):
        print(argv[0], " No es un directorio ")
        sys.exit(2)

    path = argv[0] + '/*.*'
    files = glob.glob(path)

    for name in files:
        try:
            dicc_distro = {}
            dicc_distro_bi={}
            with open(name, encoding="utf-8", errors="ignore") as f:
                filedata = f.read()
                filedata = remove_punctuation(filedata)
                lista_palabras = filedata.split(" ")
                lista_palabras=remove_digits(lista_palabras)

                ##---------------      Para Unigramas     ------------------##
                for palabra in lista_palabras:
                    for i in range(len(palabra)):
                        if palabra[i] in palabra and palabra[i]!=" ":
                            if palabra[i] in dicc_distro:
                                cant=dicc_distro[palabra[i]]
                                dicc_distro[palabra[i]]=cant+1
                            else:
                                dicc_distro[palabra[i]] = 1

                dicc_global_uni[name[36:]]=dicc_distro
                ##print(dicc_global_uni)

                ##---------------      Para Bigramas     ------------------## contar total de values bi/totalv= PROB
                for palabra in lista_palabras:
                    for i in range(len(palabra)):
                        if palabra[i:i+2] in palabra:
                            if palabra[i:i+2] in dicc_distro_bi:
                                cant=dicc_distro_bi[palabra[i:i+2]]
                                dicc_distro_bi[palabra[i:i+2]]=cant+1
                            else:
                                dicc_distro_bi[palabra[i:i+2]] = 1

                dicc_global_bi[name[36:]]=dicc_distro_bi
                ##print(dicc_global_bi)



        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise

##------------------------------------------------------------------------##
##                               Compare Unigramas
##------------------------------------------------------------------------##

    with open("languageIdentificationData/solution", mode="r", encoding="utf-8", errors="ignore") as solution:
        with open("resultUnigramas", mode="w", encoding="utf-8", errors="ignore") as result_uni:
            with open("languageIdentificationData/test", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                for filedata in lines:
                    cor_mayor = 0
                    idioma_may = ""
                    for idioma in dicc_global_uni:    #por cada idioma
                        dicc=dicc_global_uni[idioma]
                        ordered_terms = sorted(dicc, key=dicc.get, reverse=False)   ####!!!!!!!!!
                        ordered_terms=[ dicc.get(e) for e in sorted(dicc.keys()) ]

                        dicc_test={ chr(i):0 for i in range(97,123) }
                        ##print (dicc_test)
                        distro_leng = []
                        for j in range(len(filedata)):    # por cada letra de la linea
                            if filedata[j] in dicc:       ## si la letra esta en el dicc de idioma
                                if filedata[j] in dicc_test:     ##si la letra esta en el test
                                    cant = dicc_test[filedata[j]]
                                    dicc_test[filedata[j]] = cant + 1
                                else:
                                    dicc_test[filedata[j]] = 1

                        ##print(dicc_test)
                        #distro_line = []
                        #keys_list=[]

                        test_values = [dicc_test.get(e) for e in sorted(dicc_test.keys())]
                        cor= np.corrcoef(ordered_terms, test_values)[0][1]
                        ##print(cor)
                        print("Correlacion de la frecuencia: ", idioma, cor)
                        if cor > cor_mayor:
                            cor_mayor = cor
                            idioma_may = idioma

                    ##print(filedata)
                    #print("Correlacion Mayor: ", cor_mayor)
                    #print(detect(filedata))
                    lang_det = detect(filedata)
                    result_uni.write(idioma_may)
                    result_uni.write(" \t")
                    result_uni.write(str(cor_mayor))
                    result_uni.write(" \t")
                    result_uni.write(lang_det)
                    line_sol = solution.readline()
                    result_uni.write(" \t")
                    result_uni.write(line_sol)
                    result_uni.write(" \n")


##------------------------------------------------------------------------##
##                               Compare Bigramas
##------------------------------------------------------------------------##
    with open("languageIdentificationData/solution", mode="r", encoding="utf-8", errors="ignore") as solution:
        with open("resultBigramas",mode="w", encoding="utf-8", errors="ignore") as result_bi:
            contt=0
            with open("languageIdentificationData/test", encoding="utf-8", errors="ignore") as f2:
                lines2 = f2.readlines()
                for filedata in lines2:
                    cor_mayor=0
                    idioma_may=""
                    for idioma in dicc_global_bi:  # por cada idioma
                        dicc = dicc_global_bi[idioma]
                        ordered_terms = sorted(dicc, key=dicc.get, reverse=False)  ####!!!!!!!!!
                        ordered_terms = [dicc.get(e) for e in sorted(dicc.keys())]
                        dicc_test={}
                        for key in dicc:
                            dicc_test[key]=0

                        distro_leng = []
                        for j in range(len(filedata)):  # por cada letra de la linea
                            if filedata[j:j+2] in dicc:  ## si la letra esta en el dicc de idioma
                                if filedata[j:j+2] in dicc_test:  ##si la letra esta en el test
                                    cant = dicc_test[filedata[j:j+2]]
                                    dicc_test[filedata[j:j+2]] = cant + 1


                        test_values = [dicc_test.get(e) for e in sorted(dicc_test.keys())]
                        ##conteo de freq
                        cor = np.corrcoef(ordered_terms, test_values)[0][1]

                        sumacant=0
                        for n in dicc:
                            cant=dicc[n]
                            sumacant+=cant

                        sumcant_test=0
                        for n in dicc_test:
                            cant=dicc[n]
                            sumcant_test+=cant
                        f_rel_idioma =[]
                        for n in ordered_terms:
                            f_rel_idioma.append(n/sumacant)
                        f_rel_linea=[]
                        for n in test_values:
                            f_rel_linea.append(n/sumcant_test)

                        cor_rel = np.corrcoef(f_rel_idioma, f_rel_linea)[0][1]
                        if cor_rel>cor_mayor:
                            cor_mayor=cor_rel
                            idioma_may=idioma

                        #print("Correlacion de la frecuencia_relativa : ", idioma, cor_rel)
                    contt += 1
                    print(contt)
                    print(filedata)
                    ##print("Correlacion Mayor: ",cor_mayor)
                    #print(detect(filedata))
                    lang_det=detect(filedata)
                    result_bi.write(idioma_may)
                    result_bi.write(" \t")
                    result_bi.write(str(cor_mayor))
                    result_bi.write(" \t")
                    result_bi.write(lang_det)
                    line_sol=solution.readline()
                    result_bi.write(" \t")
                    result_bi.write(line_sol)
                    result_bi.write(" \n")
                    ##print(filedata[0:2])


##---------------------------------

if __name__ == "__main__":
    main(sys.argv[1:])
