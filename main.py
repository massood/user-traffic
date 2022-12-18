#!/usr/bin/env python

from datetime import datetime
from uuid import UUID

from flask import Flask, render_template
from hurry.filesize import size
from khayyam import JalaliDatetime

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

    if row['expiry_time'] and int(row['expiry_time']):
        xe = datetime.fromtimestamp(int(row['expiry_time']) / 1000)
        xf = JalaliDatetime(xe)
        exp = f"{xe.strftime('%Y-%m-%d')} ({xf.strftime('%N/%R/%D')})"
    else:
        exp = ''
    consumed = row['down'] + row['up']
    finished = consumed >= row['total']

    rows = {
        'Total traffic': size(row['total'], units),
        'Consumed': size(consumed, units),
        'Remaining': size(row['total'] - consumed, units),
        'Percent': f"{consumed / row['total'] * 100.0:.1f} %",
        'Expires on': exp,
        'Finished': 'Yes' if finished else 'No',
    }
    if finished:
        color = '#f00'
    else:
        color = '#0a0'
    return render_template('stat.html', rows=rows, color=color)
