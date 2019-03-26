import re, string
import unidecode
LONG_MIN=2
LONG_MAX=20

def sacar_palabras_vacias(lista_tokens,lista_vacias):
    lista_n_tokens=[]
    for token in lista_tokens:
        if token not in lista_vacias:
            lista_n_tokens.append(token)
    return lista_n_tokens

def replacelist (lista_palabras):
    lista_palabras=[p.replace ("\n",' ') for p in lista_palabras]
    return lista_palabras

def remove_punctuation ( text ):
    text = text.replace("\n", " ")
    text = text.lower()
    text = unidecode.unidecode(text)
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)


def tokenizar(filedata):
    #lista_palabras=filedata.split(delim)
    lista_palabras=remove_punctuation(filedata)
    lista_palabras = lista_palabras.split(" ")

    return [palabra for palabra in lista_palabras if not len(palabra)<LONG_MIN or  len(palabra)>LONG_MAX ]

