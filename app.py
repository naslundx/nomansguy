import flask
import random
import argparse
import pymongo
import os

ALL_PUNS = open('static/puns.txt').readlines()
app = flask.Flask(__name__)
print(app.config['SEND_FILE_MAX_AGE_DEFAULT'])
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 604800
print(app.config['SEND_FILE_MAX_AGE_DEFAULT'])
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
    return data[0].strip(), data[1].strip(), index


def get_db_uri():
    try:
        pw = os.environ['DB_PASSWORD']
    except KeyError:
        try:
            pw = open('database.txt').readlines()[0].strip()
        except IOError:
            pw = ''

    return f'mongodb://nomansski:{pw}@ds247290.mlab.com:47290/naslundx-nomansski'


def add_to_db(title, desc):
    try:
        uri = get_db_uri()
        client = pymongo.MongoClient(uri)
        db = client['naslundx-nomansski']
        result = db.posts.insert_one({'title': title, 'desc': desc}).inserted_id
        client.close()
        return result
    except Exception:
        return None


def validate_add(title, desc):
    return 0 < len(title) < 128 and 0 <= len(desc) < 128


@app.route('/add', methods=['POST'])
def add_post():
    title = flask.request.form['title'].strip()
    desc = flask.request.form['desc'].strip()

    msg = 'Oops! Something went wrong. Please try again!'

    if validate_add(title, desc) and add_to_db(title, desc):
        msg = 'Thank you for the "' + title + '" suggestion! It will be reviewed and, if accepted, added to the list.'
    
    rendered = flask.render_template('add.html', msg=msg)
    return rendered


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def main(path):
    if path == 'add':
        rendered = flask.render_template('add.html')
    else:
        index = try_parse_int(path)
        pun, desc, line = get_data(index)
        rendered = flask.render_template('index.html', pun=pun, desc=desc, index="%04d" % line)
    
    return rendered


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true', help="Debug mode")
    args = parser.parse_args()
    app.run(debug=args.debug, use_reloader=args.debug)
