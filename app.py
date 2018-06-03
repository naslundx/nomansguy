import flask
import random

app = flask.Flask(__name__)
random.seed()

# More puns
# Get the CSS file locally and clean up
# Add background image (space theme?)
# Write about section


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
