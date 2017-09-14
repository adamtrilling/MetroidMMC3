from flask import Flask, render_template, request, send_file
from generator import generate
from random import randint
from re import match
import os

app = Flask(__name__)


@app.route('/')
def homepage():
    default_seed = match(r'^0x([0-9a-f]+)L?$', hex(randint(0, 2**63))).group(1)
    return render_template('main.html', default_seed=default_seed)


@app.route('/randomize')
def randomize():
    seed = request.args.get('seed')

    if (match(r'^[0-9a-f]+$', seed) is None):
        return ("Bad Request", 400, [])

    if (os.path.isfile("work/metroid-{0}.nes".format(seed)) is not True):
        generate(seed)

    return send_file("../work/metroid-{0}.nes".format(seed),
                     'vnd.nintendo.nes.rom', True,
                     "metroid-{0}.nes".format(seed))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
