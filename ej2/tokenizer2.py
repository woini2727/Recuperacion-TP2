import re, string
import unidecode
LONG_MIN=2
LONG_MAX=20
ACRONYMS_ABBREVIATIONS_REGEX = r"([A-Z]([a-zA-Z]*)\.)+"
URL_REGEX="/(((http|ftp|https):\/{2})+(([0-9a-z_-]+\.)+(aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mn|mn|mo|mp|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|nom|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ra|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw|arpa)(:[0-9]+)?((\/([~0-9a-zA-Z\#\+\%@\.\/_-]+))?(\?[0-9a-zA-Z\+\%@\/&\[\];=_-]+)?)?))\b/imuS"
MAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
NAME_REGEX = r"[A-Z][a-záéóúí]+( [A-Z][a-záéóúí]+)+"
NUMBER_REGEX = r"(?<![a-zA-Z])\d+((\.|,)\d+)?(?![a-zA-Z])"


def sacar_palabras_vacias(lista_tokens,lista_vacias):
    lista_n_tokens=[]
    for token in lista_tokens:
        if token not in lista_vacias:
            lista_n_tokens.append(token)
    return lista_n_tokens

def remove_punctuation ( text ):
    text = text.replace("\n", " ")
    text = text.lower()
    text = unidecode.unidecode(text)
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)


def tokenizar(filedata):
    lista_palabras=remove_punctuation(filedata)
    lista_palabras = lista_palabras.split(" ")
    return [palabra for palabra in lista_palabras if not len(palabra)<LONG_MIN or  len(palabra)>LONG_MAX ]

def get_abreviaturas(filedata):
    return extract_by_rule(filedata, ACRONYMS_ABBREVIATIONS_REGEX)

def get_mails_and_urls(string: str) -> [str]:
    tokens = extract_by_rule(string, MAIL_REGEX)
    tokens.extend(extract_by_rule(string, URL_REGEX))
    return tokens

def get_names(string: str) -> [str]:
    return extract_by_rule(string, NAME_REGEX)

def get_numeros(string: str) -> [str]:
    return extract_by_rule(string, NUMBER_REGEX)

def extract_by_rule(string: str, rule: str) -> [str]:
    tokens = []
    for match in re.finditer(rule, string):
        token = match.group(0)
        if LONG_MIN <= len(token) <= LONG_MAX:
            tokens.append(token)
    return tokens
