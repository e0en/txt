#!/usr/bin/env python
import hashlib
import sqlite3
import time

from jinja2 import Template
from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Sanic, response
from sanic.exceptions import NotFound
import mistune


FILENAME_PREFIX = 'txt'
conn = sqlite3.connect(f'{FILENAME_PREFIX}.db')

app = Sanic(__name__)
app.static('/s', f'./static')


markdown = mistune.Markdown()

template_env = Environment(
    loader=PackageLoader(__name__, '.'),
    enable_async=True,
)

read_template = template_env.get_template('read.html')
edit_template = template_env.get_template('edit.html')


def add_doc(doc_id, content):
    timestamp = time.time()
    query = 'INSERT INTO documents (id, content, created_at) VALUES (?,?,?)'
    c = conn.cursor()
    c.execute(query, (doc_id, content, timestamp))
    conn.commit()


def doc_id_in_db(doc_id):
    query = 'SELECT count(1) from documents WHERE id=?'
    c = conn.cursor()
    c.execute(query, (doc_id, ))
    r = c.fetchone()
    return r is not None and r[0] > 0


def generate_doc_id(content):
    full_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    len_hash = len(full_hash)
    for i in range(4, len_hash):
        doc_id = full_hash[:i]
        if not doc_id_in_db(doc_id):
            return doc_id


def init_db():
    with open(f'{FILENAME_PREFIX}.sql') as fp:
        c = conn.cursor()
        for q in fp.readlines():
            c.execute(q)
        conn.commit()


@app.exception(NotFound)
def ignore_file_not_found(request, exception: NotFound):
    url = app.url_for('show', doc_id=exception.relative_url)
    return response.redirect(url)


@app.route('/document.json', methods=['POST'])
async def save(request):
    content = request.form['content'][0]

    doc_id = generate_doc_id(content)

    if doc_id:
        add_doc(doc_id, content)
        url = app.url_for('show', doc_id=doc_id)
        return response.redirect(url)
    else:
        return response.json({'status': 'error'})


@app.route('/<doc_id>', methods=['GET'])
async def show(request, doc_id):
    c = conn.cursor()
    query = ('SELECT content FROM documents WHERE id=?')
    c.execute(query, (doc_id, ))
    r = c.fetchone()

    if r:
        content = markdown(r[0])
        html = await read_template.render_async(content=content)
        return response.html(html)
    else:
        url = app.url_for('index')
        return response.redirect(url)


@app.route('/', methods=['GET'])
async def index(request):
    html = await edit_template.render_async(url_for=app.url_for)
    return response.html(html)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8002)
