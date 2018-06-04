import flask
import random

app = flask.Flask(__name__)
random.seed()

# Write about section with Daniel
# Link to exact line?


def get_data():
    with open('static/puns.txt') as f:
        contents = f.readlines()
        index = random.randint(0, len(contents) - 1)
        data = contents[index].split(',')
        return data[0].strip(), data[1].strip()


@app.route('/')
def hello_world():
    pun, desc = get_data()
    rendered = flask.render_template('index.html', pun=pun, desc=desc)
    return rendered


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
