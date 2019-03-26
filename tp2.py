import sys
import os.path
import glob
import errno
import tokenizer
#from palabra import Palabra

def main(argv):

    ##--variables para Estadisticas.txt--##
    cant_doc = 0
    cant_tokens = 0
    cant_terminos = 0
    prom_tokens=0
    prom_terminos=0
    long_prom_term=0
    menor_token=100
    menor_terms=100
    mayor_token=0
    mayor_terms=0
    once_terms=[]
    lista_vacias=[]
    dicc_frec_menor = {}
    dicc_frec_mayor = {}
    ##------------------------------------------------------------------------##

    if not os.path.isdir(argv[0]) :
       print(argv[0] ," No es un directorio " )
       sys.exit(2)

    if len(argv)==2 :
        if not os.path.isfile(argv[1]):
            print(argv[1], "No es un archivos")
            sys.exit(2)
        else:

            with open(argv[1], encoding="UTF-8") as stop_words:
                filedata = stop_words.read()
                lista_vacias=filedata.split("\n")
                #print(lista_pvacias)

    ##------------------------------------------------------------------------##
    ##                                Read Colleción
    ##------------------------------------------------------------------------##
    ##
    path = argv[0]+'/*.txt'
    files = glob.glob(path)
    lista_terminos = []
    dicc={}
    for name in files:
        cant_doc+=1
        tokens_sin_rep =[]
        try:
            with open(name, encoding="ISO-8859-1") as f:
                pass
                filedata = f.read()
                lista_tokens=tokenizer.tokenizar(filedata)
                cant_tokens += len(lista_tokens)
                cant_tokens_doc=len(lista_tokens)

                if cant_tokens_doc<menor_token:
                    menor_token=cant_tokens_doc
                if cant_tokens_doc>mayor_token:
                    mayor_token=cant_tokens_doc
                ##---si se pasó por parámetro se quitan las palabras vacias-----##
                if lista_vacias:
                    lista_tokens=tokenizer.sacar_palabras_vacias(lista_tokens,lista_vacias)
                ##--------------------------------------------------------------##
                if len(lista_tokens) < menor_terms:
                    menor_terms = len(lista_tokens)
                if len(lista_tokens) > mayor_terms:
                    mayor_terms = len(lista_tokens)

                for token in lista_tokens:
                    if  token not in lista_terminos:
                        lista_terminos.append(token)
                        dicc[token]=1,1
                        tokens_sin_rep.append(token)
                    elif token not in tokens_sin_rep:
                        df,cf = dicc[token]
                        dicc[token]=df+1,cf+1
                        tokens_sin_rep.append(token)
                    else:
                        df, cf = dicc[token]
                        dicc[token]=df,cf+1
        except IOError as exc:
            if exc.errno != errno.EISDIR:
                raise

    ##------------generar terminos-------------##
    try:
        with open("terminos.txt", mode="w", encoding="UTF-8") as terminos:
            ordered_terms = sorted(dicc, key=dicc.get, reverse=True)
            for token in ordered_terms:
                df, cf = dicc[token]
                if cf==1:
                    once_terms.append(token)
                terminos.write(token + "\t" + str(cf) + "\t" + str(df) + "\n")

    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
    cant_terminos+=len(dicc)
    prom_tokens=cant_tokens//cant_doc
    prom_terminos=cant_terminos//cant_doc
    long_termino=0
    frec_menor=cant_doc
    frec_mayor=0

    for key in dicc:
        ##--saco la frecuencia--##
        df,cf=dicc[key]
        if df <= frec_menor:
            frec_menor=df
        if df >= frec_mayor:
            frec_mayor=df
        ##----------------------##
        long_termino+=len(key)
    long_prom_term=long_termino//len(dicc)


    """"while not len(dicc_frec_menor)==10 and not len(dicc_frec_mayor)>=10:
        for token in dicc:
            df, cf = dicc[token]
            if df==frec_menor:
                dicc_frec_menor[token]=cf
            if df==frec_mayor:
                dicc_frec_mayor[token]=cf
        if len(dicc_frec_menor)<10:
            frec_menor+=1
        if len(dicc_frec_mayor)<10:
            frec_mayor+=1 """
    for token in dicc:
        df, cf = dicc[token]
        if df == frec_menor:
            dicc_frec_menor[token] = cf
        if df == frec_mayor:
            dicc_frec_mayor[token] = cf

    ##for key in dicc_frec_mayor:
      ##  print(key)
    ##for key in dicc_frec_menor:
      ##  print(key)
    ##------------generar estadística.txt--------------##
    ##print("cantidad de docs: "+ str(cant_doc))
    ##print("cantidad de tokens y terminos extraidos"+ str(cant_tokens)+" "+str(cant_terminos))
    ##print("prom term y tokens de los docs "+str(prom_terminos) +" "+str(prom_tokens) )
    ##print("Largo prom de un term "+str(long_prom_term))
    ##print("menor tok "+str(menor_token)+" menor terms "+str(menor_terms)+" mayor tok "+str(mayor_token)+" mayor terms"+str(mayor_terms))
    #print("cant term once "+str(len(once_terms)))
    try:
        with open("estadisticas.txt", mode="w", encoding="UTF-8") as estadisticas:
            estadisticas.write(str(cant_doc) + "\n" +str(cant_tokens)+"\t"+str(cant_terminos)+"\n"+str(prom_tokens) +"\t"+str(prom_terminos)+"\n"+str(long_prom_term)+"\n"+str(menor_token)+"\t"+str(menor_terms)+"\t"+str(mayor_token)+"\t"+str(mayor_terms)+"\t"+"\n"+str(len(once_terms)))


    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
    ##------------generar Frecuencia.txt--------------##
    ##print(dicc_frec_menor)

    with open("frecuencia.txt", mode="w", encoding="UTF-8") as frecuencia:
        contvueltas = 0
        for value in dicc_frec_menor :
            contvueltas+=1
            cf=dicc_frec_menor[value]
            frecuencia.write(str(value)+'\t'+str(cf)+"\n")
            if contvueltas==10:
                break
        contvueltas = 0
        for value in dicc_frec_mayor :
            contvueltas+=1
            cf=dicc_frec_mayor[value]
            frecuencia.write(str(value)+'\t'+str(cf)+"\n")
            if contvueltas==10:
                break


if __name__ == "__main__":
    main(sys.argv[1:])