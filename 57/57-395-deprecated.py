import os.path
from flask import Flask, render_template, request
import logging
import requests


app = Flask(__name__)


class Post:
    def __init__(self, post_id, title, subtitle, body):
        self.id = post_id
        self.title = title
        self.subtitle = subtitle
        self.body = body


def get_posts() -> list[Post]:
    def __make_req():
        try:
            resp = requests.get(url=POST_URL)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as req_err:
            logging.error(f'Request error: {req_err}')
        except Exception as err:
            logging.error(f'Unexpected error: {err}')
        return {}

    def __resp_to_obj() -> list[Post]:
        posts = __make_req()
        post_objs = []
        for post in posts:
            post_obj  = Post(post.get('id', 'N/A'), post.get('title', 'N/A'), post.get('subtitle', 'N/A'), post.get('body', 'N/A'))
            post_objs.append(post_obj)

        return post_objs

    return __resp_to_obj()


@app.route('/', methods=['GET'])
def show_all_posts():
    return render_template('index.html', posts=post_objs)


@app.route('/<int:index>', methods=['GET'])
def show_post(index: int):
    post = next((post for post in post_objs if post.id == index), None)

    if not post:
        logging.warning(f'Post with index -> {index} not found')
        return 'Post not found', 404

    return render_template('read_post.html', post=post)


@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        logging.info(data)
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


def setup_logging():
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s -> %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )


if __name__ == '__main__':
    setup_logging()
    POST_URL = 'https://api.npoint.io/b4169bb256b2250da79c'

    post_objs = get_posts()
    if not post_objs:
        logging.warning('No posts retrieved')

    app.run(debug=True)

    """
    https://www.npoint.io/docs/b4169bb256b2250da79c
    """

