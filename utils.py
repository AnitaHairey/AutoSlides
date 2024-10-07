import os, sys
import re
from markdown_it import MarkdownIt
import fitz
from PIL import Image
import io

def read_file(path):
    with open(path, 'r') as f:
        res = f.read()
    return res

def add_symbol(content):
    return f'~~~\n{content}\n~~~'

def add_short_symbol(content):
    return f'`{content}`'

def add_content(name, content):
    return f'The content of file {add_short_symbol(name)} is {add_symbol(content)}.\n'

def remove_comment(content):
    res = re.sub('%[^\n]*\n', '', content)
    return res

def parse_summary(raw_text, title=None):
    refined_text = re.sub('```', '\n```', raw_text)
    md = MarkdownIt()
    tokens = md.parse(refined_text)

    try:
        title = tokens[1].children[0].content
        title = title.replace('Title:', '').strip()
    except:
        title = '[Title]'

    tokens = [token for token in tokens if token.type == 'fence']
    token_tuples = [(token.info, token.content) for token in tokens]
    contents = [tp for tp in token_tuples if 'number' not in tp[0] and 'Title' not in tp[0]]
    try:
        number_tuple = [tp for tp in token_tuples if 'number' in tp[0]][0]
        slide_number = int(re.findall('[\d]+', number_tuple[0])[0])
    except:
        slide_number = len(contents)

    return slide_number, title, contents


def parse_figures(raw_text, repo_path):
    refined_text = re.sub('```', '\n```', raw_text)
    md = MarkdownIt()
    tokens = md.parse(refined_text)
    tokens = [token for token in tokens if token.type == 'fence']
    tokens = [token.content for token in tokens]
    def split_figure(content: str):
        try:
            lines = content.splitlines()
            path = [line for line in lines if 'Path' in line][0]
            desc = [line for line in lines if 'Desc' in line][0]
            path = path.replace('Path: ', '').strip()
            desc = desc.replace('Description: ', '').strip()
            if path.endswith('.pdf'):
                try:
                    pix = fitz.open(os.path.join(repo_path, path)).load_page(0).get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    factor = min(1000 / img.width, 800 / img.height)
                    img.resize((int(img.width * factor), int(img.height * factor)))
                    path = f'{path}.png'
                    img.save(os.path.join(repo_path, path))
                except:
                    print('fail again!')
                    return None
            suffix = path.split('.')[-1]
            if suffix in ['png', 'jpg', 'jpeg']:
                return path, desc
            else:
                return None
        except:
            return None

    figures = [split_figure(token) for token in tokens]
    figures = [fig for fig in figures if fig is not None]
    return figures
