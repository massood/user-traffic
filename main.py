#!/usr/bin/env python

from uuid import UUID

from flask import Flask, render_template
from hurry.filesize import size

import db

app = Flask(__name__)

units = [
    (1024 ** 5, ' PB'),
    (1024 ** 4, ' TB'),
    (1024 ** 3, ' GB'),
    (1024 ** 2, ' MB'),
    (1024 ** 1, ' KB'),
    (1024 ** 0, ' B'),
]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/stat/<uuid>', methods=['GET', 'POST'])
def stat(uuid):
    try:
        UUID(uuid)
    except ValueError:
        return render_template('stat.html', error=f'Invalid user id: {uuid}')

    row = db.get_inbounds_row(uuid)
    if row is None:
        return render_template('stat.html', error=f'No user found with this id: {uuid}')

    consumed = row['down'] + row['up']
    finished = consumed >= row['total']
    rows = {
        'Total traffic': size(row['total'], units),
        'Consumed': size(consumed, units),
        'Remaining': size(row['total'] - consumed, units),
        'Percent': f"{consumed / row['total'] * 100.0:.1f} %",
        'Finished': 'Yes' if finished else 'No',
    }
    if finished:
        color = '#f00'
    else:
        color = '#0a0'
    return render_template('stat.html', rows=rows, color=color)
