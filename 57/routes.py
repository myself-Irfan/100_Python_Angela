import logging
from flask import Blueprint, request, jsonify, render_template
from marshmallow.exceptions import ValidationError

from model import Post, db
from schemas import PostSchema


main = Blueprint('main', __name__)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

# api

@main.route('/api/get', methods=['GET'])
def get_post():
    """
    API to get all posts or a specific post by ID (via query param).
    """
    def __get_post_id(post_id: int):
        try:
            post = Post.query.get(post_id)
        except Exception as err:
            logging.error(f'Error querying post with id-{post_id}: {str(err)}')
            return {'error': f'Error fetching post with id: {post_id}'}, 500
        else:
            if not post:
                return {'message': f'No post found with id-{post_id}'}, 404

            return post_schema.dump(post), 200

    def __get_all_posts():
        try:
            all_posts = Post.query.all()
        except Exception as err:
            logging.error(f'Error querying post: {str(err)}')
            return {'error': 'Error fetching posts'}, 500
        else:
            if not all_posts:
                return {'message': 'No post found'}, 404

            return posts_schema.dump(all_posts), 200


    try:
        post_id = request.args.get('id', type=int)

        if post_id:
            response, code = __get_post_id(post_id)
        else:
            response, code = __get_all_posts()

        return jsonify(response), code
    except Exception as err:
        logging.error(f'Error while fetching post: {str(err)}')
        return jsonify({'error': 'Error occurred while fetching posts'}), 500

@main.route('/api/post', methods=['POST'])
def create_post():
    """
    create a new post
    """
    try:
        data = post_schema.load(request.json)
        new_post = Post(**data)

        db.session.add(new_post)
        db.session.commit()
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as err:
        db.session.rollback()
        logging.error(f'An error occurred while creating post: {str(err)}')
        return jsonify({'error': 'An error occurred while creating post'}), 500
    else:
        return jsonify({'message': f'Post created successfully: id-{new_post.id}'})

@main.route('/api/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id: int):
    try:
        post = Post.query.get(post_id)

        if not post:
            return jsonify({'error': f'No post found with id-{post_id}'}), 404

        db.session.delete(post)
        db.session.commit()

    except Exception as err:
        db.session.rollback()
        logging.error(f'Error while deleting post with id-{post_id}: {str(err)}')
        return jsonify({'error': f'An error occurred while deleting post with id-{post_id}'}), 500
    else:
        return jsonify({'message': 'Post deleted successfully'}), 200

@main.route('/api/update/<int:post_id>', methods=['PUT', 'PATCH'])
def update_post(post_id: int):
    try:
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'message': f'No post found with id-{post_id}'}), 404

        data = request.json

        if not data:
            return jsonify({'message': 'No data provided'}), 400

        validated_data = post_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(post, key, value)

        db.session.commit()
    except ValidationError as val_err:
        return jsonify({'error': val_err.messages}), 400
    except Exception as db_err:
        db.session.rollback()
        logging.error(f'Failed to update post-{post_id}: {str(db_err)}')
        return jsonify({'error': 'Error updating Post'}), 500
    else:
        logging.info(f'Updated fields for post-{post_id}: {list(validated_data.keys())}')
        return jsonify({'message': 'Post updated successfully'}), 200

# template

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_post')
def write_blogpost():
    return render_template('create_post.html')

@main.route('/read_post/<int:post_id>')
def read_post(post_id: int):
    return render_template('read_post.html', post_id=post_id)