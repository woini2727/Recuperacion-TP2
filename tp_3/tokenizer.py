import re, string
from typing import List
from nltk.stem import SnowballStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import PorterStemmer

import unidecode
LONG_MIN=3
LONG_MAX=20
ACRONYMS_ABBREVIATIONS_REGEX = r"([A-Z]([a-zA-Z]*)\.)+"
URL_REGEX = r"(?i)\b((?:https?:(?:/{1,10}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:.,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"
MAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
NAME_REGEX = r"[A-Z][a-záéóúí]+( [A-Z][a-záéóúí]+)+"
NUMBER_REGEX = r"(?<![a-zA-Z])\d+((\.|,)\d+)?(?![a-zA-Z])"
CHEMICAL_REGEX=r"[A-Z]+[a-z]*[A-Z]*[a-z]*\d+|[A-Z]+[a-z]*[A-Z]+"


def sacar_palabras_vacias(lista_tokens,lista_vacias):
    lista_n_tokens=[]
    for token in lista_tokens:
        if token not in lista_vacias:
            lista_n_tokens.append(token)
    return lista_n_tokens

def remove_digits(lista_palabras):
    lista_palabras2=[]
    for palabra in lista_palabras:
        palabra_n=re.sub("\d+", " ", palabra)
        lista_palabras2.append(palabra_n)
    return lista_palabras2

def remove_punctuation ( text ):
    text = text.replace("\n", " ")
    text = text.lower()
    text = unidecode.unidecode(text)
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

def remove_chemical_exp(text):

    return re.sub(CHEMICAL_REGEX ,'', text)

def tokenizar(filedata):
    ##filedata = remove_chemical_exp(filedata)
    filedata=remove_punctuation(filedata)
    lista_palabras = filedata.split(" ")
    lista_palabras = remove_digits(lista_palabras)
    return [palabra for palabra in lista_palabras if not len(palabra)<LONG_MIN or  len(palabra)>LONG_MAX ]

def stemming_tokenizar(lista_tokens, stemmer, lenguage):
    if stemmer=="snowball":
        stemr=SnowballStemmer(lenguage)
        lista_tokens = [stemr.stem(x) for x in lista_tokens]
    if stemmer=="lancaster":
        stemr=LancasterStemmer()
        lista_tokens = [stemr.stem(x) for x in lista_tokens]
    if stemmer=="porter":
        stemr=PorterStemmer()
        lista_tokens= [stemr.stem(x) for x in lista_tokens]
    return lista_tokens

def get_abreviaturas(string: str) -> List[str]:
    return get_list_byregex(string, ACRONYMS_ABBREVIATIONS_REGEX)

def get_mails_and_urls(string: str) -> List[str]:
    tokens = get_list_byregex(string, MAIL_REGEX)
    tokens.extend(get_list_byregex(string, URL_REGEX))
    return tokens

def get_names(string: str) -> List[str]:
    return get_list_byregex(string, NAME_REGEX)

def get_numeros (string: str) -> List[str]:
    return get_list_byregex(string, NUMBER_REGEX)

def get_chemical_expressions(string: str) -> List[str]:
    return get_list_byregex(string,CHEMICAL_REGEX)

def get_list_byregex(string: str, rule: str) -> List[str]:
    tokens = []
    for match in re.finditer(rule, string):
        token = match.group(0)
        if LONG_MIN <= len(token) <= LONG_MAX:
            tokens.append(token)
    return tokens

