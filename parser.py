from grab import Grab
from grab.error import DataNotFound
import config
import re

class URLExeption(Exception):
    pass

class WebExeption(Exception):
    pass

def get_course_info(message):
    g,course_id = check_url(message)

    try:
        name = g.doc.select('//title').text()
        mem,space = g.doc.rex_text(
            '<p><strong>Записалось / всего мест</strong><br />.*\n(.*)</p>').split(' / ')
    except DataNotFound:
        raise WebExeption
    mem = int(mem)
    space = int(space)

    return course_id, name, mem, space

def check_url(message):
    course_id = parse_url(message)
    g = Grab()
    g.go(config.mfk_url+str(course_id))
    if g.doc.code == 200:
        return g, course_id
    else:
        raise WebExeption

def parse_url(message):
    try:
        course_id = re.search(r'\d+$', message).group(0)
        return course_id
    except AttributeError:
        raise URLExeption("Exeption in parse_url")
