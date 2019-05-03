import sys
import os.path
import glob
import errno
import tokenizer

def main(argv):
    ##------------------------------------------------------------------------##
    #                     vars for Estadisticas.txt
    ##------------------------------------------------------------------------##
    cant_doc = 0
    cant_tokens = 0
    cant_terminos = 0
    menor_token=10000
    menor_terms=10000
    mayor_token=0
    mayor_terms=0
    once_terms=[]
    lista_vacias=[]
    dicc_frec_menor = {}
    dicc_frec_mayor = {}
    ##------------------------------------------------------------------------##
    ##                                Read Params
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
    ##SOLO PARA EJ 4
    ##path = argv[0]+'/*.txt'
    ##SOLO PARA EJ 5
    path = argv[0] + '/*.ALL'
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
                ##lista_tokens = tokenizer.stemming_tokenizar(lista_tokens, "snowball", "spanish")
                lista_tokens = tokenizer.stemming_tokenizar(lista_tokens, "lancaster", "")
                #lista_tokens = tokenizer.stemming_tokenizar(lista_tokens, "porter", "")

                cant_tokens += len(lista_tokens)
                ##-------------------Conteo de terminos------------------------###
                if len(lista_tokens) < menor_terms:
                    menor_terms = len(lista_tokens)
                if len(lista_tokens) > mayor_terms:
                    mayor_terms = len(lista_tokens)
                ##-------------------------------------------------------------###

                ##-------------Quitar palabras vacias---------------------------##
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

                ##-------------------Conteo de tokens------------------------###
                cant_tokens_doc = len(terminos_archivo_actual)
                if cant_tokens_doc < menor_token:
                    menor_token = cant_tokens_doc
                if cant_tokens_doc > mayor_token:
                    mayor_token = cant_tokens_doc

                terminos_archivo_actual.clear()
                ##-------------------------------------------------------------###


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


    #------long promedio de los terminos------#
    for key in dicc:
        long_termino += len(key)
    long_prom_term = long_termino // len(dicc)

    ##---------------------generar estadística.txt-----------------##

    try:
        with open("estadisticas.txt", mode="w", encoding="UTF-8") as estadisticas:
            estadisticas.write(str(cant_doc) + "\n" +str(cant_tokens)+"\t"+str(cant_terminos)+"\n"+str(prom_tokens) +"\t"+str(prom_terminos)+"\n"+str(long_prom_term)+"\n"+str(menor_token)+"\t"+str(menor_terms)+"\t"+str(mayor_token)+"\t"+str(mayor_terms)+"\t"+"\n"+str(len(once_terms)))

    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
    ##-------------------generar Frecuencia.txt--------------------##

    with open("frecuencia.txt", mode="w", encoding="UTF-8") as frecuencia:

        ordered_terms = sorted(dicc, key=dicc.get, reverse=True)
        for token in ordered_terms[:10]:
            df, cf = dicc[token]
            frecuencia.write(str(token)+'\t'+str(cf)+"\n")

        ordered_terms = sorted(dicc, key=dicc.get)
        for token in ordered_terms[:10]:
            df, cf = dicc[token]
            frecuencia.write(str(token) + '\t' + str(cf) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])