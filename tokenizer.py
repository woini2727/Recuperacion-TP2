import re, string
LONG_MIN=2
LONG_MAX=20

def replacelist (lista_palabras):
    lista_palabras=[p.replace ("\n",'') for p in lista_palabras]
    return lista_palabras

def remove_punctuation ( text ):
    text = text.replace("\n", "")
    text = text.lower()
    return re.sub('[%s]' % re.escape(string.punctuation), '', text)


def split(filedata,delim):
    #lista_palabras=filedata.split(delim)
    lista_palabras=remove_punctuation(filedata)
    lista_palabras = lista_palabras.split(delim)

    for palabra in lista_palabras:
        if len(palabra)<LONG_MIN or  len(palabra)>LONG_MAX:
            lista_palabras.remove(palabra)


    # lista_palabras = lista_palabras.split(delim)
    return lista_palabras
