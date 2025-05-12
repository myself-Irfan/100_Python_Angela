import logging
from flask import Blueprint, request, jsonify, render_template
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

from .model import Post, User, db
from .schemas import PostSchema


main = Blueprint('main', __name__, url_prefix='/')
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

# api

@main.route('/api/get', methods=['GET'])
@jwt_required()
def get_post():
    """
    API to get all posts or a specific post by ID (via query param).
    """
    def __get_post_id(post_id: int):
        try:
            post = Post.query.get(post_id)
        except Exception as err:
            logging.error(f'Error querying post with id-{post_id}: {str(err)}')
            return {
                'status': 'error',
                'message': f'Error fetching post with id: {post_id}'
            }, 500
        else:
            if not post:
                return {
                    'status': 'warning',
                    'message': f'No post found with id-{post_id}'
                }, 404

            return {
                'status': 'success',
                'message': 'Post fetched successfully',
                'data': post_schema.dump(post)
            }, 200

    def __get_all_posts():
        try:
            all_posts = Post.query.all()
        except Exception as err:
            logging.error(f'Error querying post: {str(err)}')
            return {
                'status': 'error',
                'message': 'Error fetching posts'
            }, 500
        else:
            if not all_posts:
                return {
                    'status': 'warning',
                    'message': 'No post found'
                }, 404

            return {
                'status': 'success',
                'message': 'Posts fetched successfully',
                'data': post_schema.dump(all_posts, many=True)
            }, 200

    try:
        user_id = get_jwt_identity()
        if not User.query.get(user_id):
            logging.warning(f'Failed to fetch user-{user_id} using current token')
            return jsonify({
                'status': 'warning',
                'message': 'User not found'
            }), 404

        post_id = request.args.get('id', type=int)

        if post_id:
            response, code = __get_post_id(post_id)
        else:
            response, code = __get_all_posts()

        return jsonify(response), code
    except Exception as err:
        logging.error(f'Error while fetching post: {str(err)}')
        return jsonify({
            'status': 'error',
            'message': 'Error occurred while fetching posts'
        }), 500

@main.route('/api/post', methods=['POST'])
@jwt_required()
def create_post():
    """
    create a new post
    """
    try:
        if not request.is_json:
            return jsonify({
                'status': 'warning',
                'message': 'Request must be JSON'
            }), 400

        user_id = get_jwt_identity()
        if not User.query.get(user_id):
            logging.warning(f'Failed to fetch user-{user_id} using current token')
            return jsonify({
                'status': 'warning',
                'message': 'User not found'
            }), 404

        data = post_schema.load(request.json)
        new_post = Post(
            title=data['title'],
            subtitle=data['subtitle'],
            body=data['body'],
            author_id=user_id
        )

        db.session.add(new_post)
        db.session.commit()
    except ValidationError as err:
        return jsonify({
            'status': 'error',
            'message': 'Validation error',
            'errors': err.messages
        }), 400
    except IntegrityError as integ_err:
        db.session.rollback()
        logging.error(f'Integrity Error: {integ_err}')
        return jsonify({
            'status': 'error',
            'message': f'Post with title-{request.json.get("title")} may already exist'
        }), 400
    except Exception as err:
        db.session.rollback()
        logging.error(f'An error occurred while creating post: {str(err)}')
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while creating post. Please try later.'
        }), 500
    else:
        return jsonify({
            'status': 'success',
            'message': f'Post created successfully: id-{new_post.id}'
        }), 201

@main.route('/api/delete/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id: int):
    try:
        user_id = get_jwt_identity()
        if not User.query.get(user_id):
            logging.warning(f'Failed to fetch user using current token')
            return jsonify({
                'status': 'warning',
                'message': 'User not found'
            }), 404

        post = Post.query.get(post_id)

        if not post:
            return jsonify({
                'status': 'warning',
                'message': f'No post found with id-{post_id}'
            }), 404
        if int(post.author_id) != int(user_id):
            logging.warning(f'Unauthorized delete attempt by: {user_id}')
            return jsonify({
                'status': 'warning',
                'message': f'User not authorized to delete post-{post_id}'
            }), 403

        db.session.delete(post)
        db.session.commit()

    except Exception as err:
        db.session.rollback()
        logging.error(f'Error while deleting post with id-{post_id}: {str(err)}')
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while deleting post with id-{post_id}'
        }), 500
    else:
        return jsonify({
            'status': 'success',
            'message': 'Post deleted successfully'
        }), 200

@main.route('/api/update/<int:post_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_post(post_id: int):
    try:
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Request must be JSON'
            }), 400

        user_id = get_jwt_identity()
        logging.info(f'Extracted user_id from JWT: {user_id}')
        if not User.query.get(user_id):
            logging.warning(f'Failed to fetch user using current token')
            return jsonify({
                'status': 'warning',
                'message': 'User not found'
            }), 404

        post = Post.query.get(post_id)
        if not post:
            return jsonify({
                'status': 'warning',
                'message': f'No post found with id-{post_id}'
            }), 404

        if int(post.author_id) != int(user_id):
            logging.warning(
                f'Unauthorized update attempt by user-{user_id} to update post-{post_id} owned by user-{post.author_id}')
            return jsonify({
                'status': 'warning',
                'message': f'User not authorized to update post-{post_id}'
            }), 403

        data = request.json

        if not data:
            return jsonify({
                'status': 'warning',
                'message': 'No data provided'
            }), 400

        validated_data = post_schema.load(data, partial=True)

        for key, value in validated_data.items():
            setattr(post, key, value)

        db.session.commit()
    except ValidationError as val_err:
        return jsonify({
            'status': 'warning',
            'message': 'Validation error',
            'error': val_err.messages
        }), 400
    except IntegrityError as integ_err:
        logging.error(f'Integrity error: {integ_err}')
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Post with title-{request.json.get("title")} may already exist'
        }), 400
    except Exception as db_err:
        db.session.rollback()
        logging.error(f'Failed to update post-{post_id}: {str(db_err)}')
        return jsonify({
            'status': 'error',
            'message': 'Error updating Post'
        }), 500
    else:
        logging.info(f'Updated fields for post-{post_id}: {list(validated_data.keys())}')
        return jsonify({
            'status': 'success',
            'message': f'Post-{post_id} updated successfully'
        }), 200

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

@main.route('/edit_post/<int:post_id>')
def edit_post(post_id: int):
    return render_template('edit_post.html', post_id=post_id)