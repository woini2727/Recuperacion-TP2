import sys
import os.path
import glob
import errno
import tokenizer

def main(argv):
    ##--variables para Estadisticas.txt--##
    cant_doc = 0
    cant_tokens = 0
    cant_terminos = 0
    prom_tokens=0
    prom_terminos=0
    long_prom_term=0
    menor_token=10000
    menor_terms=10000
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
            with open(name, encoding="utf-8",errors="ignore") as f:
                pass
                filedata = f.read()
                lista_tokens=tokenizer.tokenizar(filedata)

                cant_tokens += len(lista_tokens)

                if len(lista_tokens) < menor_terms:
                    menor_terms = len(lista_tokens)
                if len(lista_tokens) > mayor_terms:
                    mayor_terms = len(lista_tokens)
                ##---si se pasó por parámetro se quitan las palabras vacias-----##
                if lista_vacias:
                    lista_tokens=tokenizer.sacar_palabras_vacias(lista_tokens,lista_vacias)
                ##--------------------------------------------------------------##


                terminos_archivo_actual=[]
                for token in lista_tokens:
                    if  token not in lista_terminos:
                        lista_terminos.append(token)
                        terminos_archivo_actual.append(token)
                        dicc[token]=1,1
                        tokens_sin_rep.append(token)
                    elif token not in tokens_sin_rep:
                        df,cf = dicc[token]
                        dicc[token]=df+1,cf+1
                        tokens_sin_rep.append(token)
                        terminos_archivo_actual.append(token)
                    else:
                        df, cf = dicc[token]
                        dicc[token]=df,cf+1

                cant_tokens_doc = len(terminos_archivo_actual)
                if cant_tokens_doc < menor_token:
                    menor_token = cant_tokens_doc
                if cant_tokens_doc > mayor_token:
                    mayor_token = cant_tokens_doc

                terminos_archivo_actual.clear()


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
    cont_frec_menor=0
    cont_frec_mayor=0

    #---long de los terminos---#
    for key in dicc:
        long_termino += len(key)
    long_prom_term = long_termino // len(dicc)

    #listas de frec menores
    for key in dicc:
        df,cf=dicc[key]
        if df <= frec_menor:
            frec_menor=df
        if df >= frec_mayor:
            frec_mayor=df

    while cont_frec_menor < 10:
        for token in dicc:
            df, cf = dicc[token]
            if df == frec_menor:
                dicc_frec_menor[token] = cf
                cont_frec_menor+=1
        frec_menor=frec_menor+1


    while cont_frec_mayor < 10:
        for token in dicc:
            df, cf = dicc[token]
            if df == frec_mayor:
                dicc_frec_mayor[token] = cf
                cont_frec_mayor += 1
        frec_mayor = frec_mayor -1


    ##------------generar estadística.txt--------------##

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