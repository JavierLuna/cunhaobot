import random
import unicodedata
from typing import Tuple
from copy import deepcopy

thumbs = [
    "https://cdn.20m.es/img2/recortes/2018/02/06/632781-600-338.jpg",
    "https://i.blogs.es/c60c05/quien-javier/450_1000.jpg",
    "https://media-cdn.tripadvisor.com/media/photo-s/0f/f9/86/eb/junto-a-mi-cunado-compartiendo.jpg",
    "https://img.elcomercio.pe/files/ec_article_videogalleria/uploads/2018/06/18/5b27a6c5c9c49.jpeg",
    "https://fotos.perfil.com/2016/10/26/1026claudiominnicellig.jpg",
    "https://www.ecestaticos.com/imagestatic/clipping/7f5/900/7f59009441d3cf042f374f50756f3c5b/tu-cunado-ese-que-dice-que-escribe.jpg?mtime=1456847457",
    "https://s4.eestatic.com/2017/05/05/reportajes/entrevistas/VOX-Santiago_Abascal-Entrevistas_213740088_33819883_1024x576.jpg",
    "https://i.ytimg.com/vi/NyOwsYAPzTE/hqdefault.jpg",
    "https://pbs.twimg.com/media/DFRYYkRXgAIGOjI.jpg",
    "http://www.eluniversalqueretaro.mx/sites/default/files/styles/f03-651x400/public/2018/04/06/q8-20.jpg.jpg?itok=G2zZUM1c",
    "https://static3.elcomercio.es/www/pre2017/multimedia/noticias/201703/26/media/22940314.jpg",
]


def get_thumb():
    return random.choice(thumbs)


def random_combination(iterable: str, r: int) -> Tuple[str]:
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)


def remove_empty_from_dict(di):
    d = deepcopy(di)
    if type(d) is dict:
        return dict((k, remove_empty_from_dict(v)) for k, v in d.items() if v and remove_empty_from_dict(v))
    elif type(d) is list:
        return [remove_empty_from_dict(v) for v in d if v and remove_empty_from_dict(v)]
    else:
        return d


def normalize_str(s):
    """Returns a version of s without accents or specials characters such as ñ and lower-cased"""
    without_accents = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return without_accents.lower()


def improve_punctuation(s):
    """Returns a version of s capitalized if the first character is a letter and a trailling dot if neccesary"""
    if s[0].isalpha():
        s = s[0].upper() + s[1:]
    else:
        s = s[0] + s[1].upper() + s[2:]

    if s[-1].isalpha():
        s += "."

    return s
