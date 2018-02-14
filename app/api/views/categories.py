from app import db
from flask import request, jsonify, make_response
from app.models import Category, CategorySchema
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.api import api
from app.api.functions import is_html, cap_sentence


@api.route('/categories', methods=['POST'])
@jwt_required
def create_new_category():
    """
    Create new category and return the new category object.
    This is a protected endpoint and requires valid jwt token.
    """
    # Get user id from jwt token
    public_id = get_jwt_identity()

    # Get category name from name field
    name = request.form['name']
    name_cap = cap_sentence(name)

    # Check if name field is not empty
    if name:

        # Check if name field contains html or javascript
        if is_html(name):
            return jsonify(
                {'error': 'Html and script injection is not allowed!'}
            ), 422

        # Try to add new category to database
        try:
            new_category = Category(name=name, user_id=public_id)
            db.session.add(new_category)
            db.session.commit()

        # If category already exists, return error
        except IntegrityError:
            return jsonify(
                {'error': 'Category named %s already exists!' % name_cap}
            ), 422

        # If some other sqlalchemy error is thrown, return error
        except SQLAlchemyError:
            return jsonify({'error': 'Some problem occurred!'}), 400

        # If category successfully added, return object with success message
        new_category_schema = CategorySchema()
        output = new_category_schema.dump(new_category).data
        resp = make_response(jsonify(
            {
                'category': output,
                'success': 'Category named %s has been created!' % name_cap
            }
        ), 201)
        resp.headers['Location'] = (
            'http://localhost:5000/categories/%s' % str(new_category.id)
        )

        return resp

    # If name field is empty, return error
    return jsonify({'error': 'missing parameters'}), 400


@api.route('/categories', methods=['GET'])
def get_all_categories():
    """
    Return all categories as a list of objects. Add query parameters
    to filter, order, and limit results. All query parameters follow
    the '?' after the URI and are seperated by the '&' symbol.
        - To limit results returned add 'count=value'
        - To filter by id add 'id=value'
        - To filter by names add 'name=value1,value2,value3'
        - To filter by user id add 'user_id=value'
        - To sort results add 'sort=value1+asc, value2+desc'
            Ex. Sort all results by category name in ascending order
                /catalog/categories?name=basketball&sort=name+asc

    This is a public non-protected endpoint.
    """
    # Setup empty argument arrays
    ids = []
    names = []
    user_ids = []
    args = []
    count = None

    # If valid arguments in request, add them to argument array
    if request.args:
        params = request.args.to_dict()

        if 'count' in params:
            count = params['count']

        if 'id' in params:
            ids = params['id'].split(',')

        if 'name' in params:
            names = params['name'].split(',')

        if 'user_id' in params:
            user_ids = params['user_id'].split(',')

        if 'sort' in params:
            sort_list = params['sort'].split(',')
            for item in sort_list:
                if item == 'name desc':
                    item = Category.name.desc()
                    args.append(item)
                if item == 'name asc':
                    item = Category.name.asc()
                    args.append(item)
                if item == 'id desc':
                    item = Category.id.desc()
                    args.append(item)
                if item == 'id asc':
                    item = Category.id.asc()
                    args.append(item)
                if item == 'user_id desc':
                    item = Category.user_id.desc()
                    args.append(item)
                if item == 'user_id asc':
                    item = Category.user_id.asc()
                    args.append(item)

    # Setup query with all filters included
    query = Category.query.filter(
        db.and_(
            db.or_(
                Category.name == name for name in names
            ),
            db.or_(
                Category.id == id for id in ids
            ),
            db.or_(
                Category.user_id == user_id for user_id in user_ids
            )
        )
    ).order_by(*args)

    # Try to get all results or filtered results from database
    try:
        categories = query.limit(count).all()

        # If query returns no categories, return erorr
        if len(categories) == 0:
            return jsonify({'error': 'No results found!'}), 404

    # If a sqlalchemy error is thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # If query successful, return array of category objects
    category_schema = CategorySchema(many=True)
    output = category_schema.dump(categories).data

    return jsonify(
        {'num_results': str(len(output)), 'categories': output}
    ), 200


@api.route('/categories/<int:id>', methods=['GET'])
def get_one_category(id):
    """
    Return single category as an object.
    This is a public non-protected endpoint.
    """
    # Setup query
    query = Category.query.filter_by(id=id)

    # Try to get category from database
    try:
        category = query.one()

    # If no result found, return error
    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    # If some other sqlalchemy error is thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # If query successful, return category object
    category_schema = CategorySchema()
    output = category_schema.dump(category).data

    return jsonify({'category': output}), 200


@api.route('/categories/<int:id>', methods=['PUT'])
@jwt_required
def edit_one_category(id):
    """
    Edit single item.
    This is a protected endpoint and requires valid jwt token.
    """
    # Get user id from jwt token
    public_id = get_jwt_identity()

    # Get category name from name field
    name = request.form['name']
    nameCap = cap_sentence(name)

    # Check if name field is not empty
    if name:

        # Check if name field contains html or javascript
        if is_html(name):
            return jsonify(
                {'error': 'Html and script injection is not allowed!'}
            ), 422

        # Setup query
        query = Category.query.filter_by(
                id=id,
                user_id=public_id
        )

        # Try to get category from database
        try:
            category = query.one()

        # If no result found, return error
        except NoResultFound:
            return jsonify({'error': 'No result found!'}), 404

        # If some other sqlalchemy error is thrown, return error
        except SQLAlchemyError:
            return jsonify({'error': 'Some problem occurred!'}), 400

        # Try to update category in database
        try:
            category.name = name
            db.session.commit()

        # If category with name already exists, return error
        except IntegrityError:
            return jsonify(
                {'error': 'Category named %s already exists!' % nameCap}
            ), 422

        # If some other sqlalchemy error is thrown, return error
        except SQLAlchemyError:
            return jsonify({'error': 'Some problem occurred!'}), 400

        # If update successful, return success
        return jsonify(
            {'success': 'The category named %s has been updated!' % nameCap}
        ), 200

    # If name field is empty, return error
    return jsonify({'error': 'Missing data!'}), 400


@api.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required
def delete_one_category(id):
    """
    Delete single category.
    This is a protected endpoint and requires valid jwt token.
    """
    # Get user id from jwt token
    public_id = get_jwt_identity()

    # Setup query
    query = Category.query.filter_by(id=id, user_id=public_id)

    # Try to get category from database
    try:
        category = query.one()

        # Get name from category object
        name = category.name
        nameCap = cap_sentence(name)

    # If no result found, return error
    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    # If some other sqlalchemy error is thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # Try to delete category in database
    try:
        db.session.delete(category)
        db.session.commit()

    # If some sqlalchemy error thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # If delete successful, return success
    return jsonify(
        {'success': 'The category named %s has been deleted!' % nameCap}
    ), 200
