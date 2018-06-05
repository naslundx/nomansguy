import flask
import random
import argparse

ALL_PUNS = open('static/puns.txt').readlines()
app = flask.Flask(__name__)
random.seed()


def try_parse_int(string):
    try:
        return int(string)
    except ValueError:
        return None


def get_data(index=None):
    if not index:
        index = random.randint(0, len(ALL_PUNS) - 1)
    else:
        index = index % len(ALL_PUNS)

    data = ALL_PUNS[index].split(',')
    return data[0].strip(), data[1].strip()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    index = try_parse_int(path)
    pun, desc = get_data(index)
    rendered = flask.render_template('index.html', pun=pun, desc=desc)
    return rendered


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true', help="Debug mode")
    args = parser.parse_args()
    app.run(debug=args.debug, use_reloader=args.debug)
