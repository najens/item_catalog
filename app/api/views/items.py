from app import db
from flask import request, jsonify, make_response
from app.models import Item, ItemSchema
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.api import api
from app.api.functions import is_html, cap_sentence


@api.route('/items', methods=['POST'])
@jwt_required
def create_new_item():
    """
    Create new item and return the new item object.
    This is a protected endpoint and requires valid jwt token.
    """
    # Get user id from jwt token
    public_id = get_jwt_identity()
    # Get item attributes from form
    name = request.form['name']
    nameCap = cap_sentence(name)
    description = request.form['description']
    category = request.form['category']

    # Check if all form fields, are not empty
    if name and category and description:

        # Check if any fields contain html or javascript
        if is_html(name) or is_html(category) or is_html(description):
            return jsonify(
                {'error': 'Html and script injection is not allowed!'}
            ), 422

        # Try to add new item to database
        try:
            new_item = Item(
                name=name,
                description=description,
                category_name=category,
                user_id=public_id
            )
            db.session.add(new_item)
            db.session.commit()

        # If name already exists, return error
        except IntegrityError:
            return jsonify(
                {'error': 'Item named %s already exists!' % nameCap}
            ), 422

        # If some other sqlalchemy error is thrown, return error
        except SQLAlchemyError:
            return jsonify({'error': 'Some problem occurred!'}), 400

        # If item successfully added, return object with success message
        new_item_schema = ItemSchema()
        output = new_item_schema.dump(new_item).data
        resp = make_response(jsonify(
            {
                'item': output,
                'success': 'Item named %s has been created!' % nameCap
            }
        ), 201)
        resp.headers['Location'] = (
            'http://localhost:5000/items/' + str(new_item.id)
        )
        return resp

    # If any fields are empty, return error
    return jsonify({'error': 'missing parameters'}), 400


@api.route('/items', methods=['GET'])
@jwt_optional
def get_all_items():
    """
    Return all items as a list of objects. Add query parameters
    to filter, order, and limit results. All query parameters follow
    the '?' after the URI and are seperated by the '&' symbol.
        - To limit results returned add 'count=value'
        - To filter by id add 'id=value'
        - To filter by names add 'name=value1,value2,...'
        - To filter by user id add 'user_id=value'
        - To filter by category name add 'category=value1,value2,...'
        - To sort results add 'sort=value1+asc,value2+desc'
            Ex. Sort all results by category name in ascending order
                /items?category=basketball&sort=name+asc

    This is a public non-protected endpoint.
    """
    # Setup empty argument arrays
    ids = []
    names = []
    users = []
    categories = []
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

        if 'user' in params:
            users = params['user'].split(',')

        if 'category' in params:
            categories = params['category'].split(',')

        if 'sort' in params:
            sort_list = params['sort'].split(',')
            for item in sort_list:
                if item == 'id desc':
                    item = Item.id.desc()
                    args.append(item)
                if item == 'id asc':
                    item = Item.id.asc()
                    args.append(item)
                if item == 'name desc':
                    item = Item.name.desc()
                    args.append(item)
                if item == 'name asc':
                    item = Item.name.asc()
                    args.append(item)
                if item == 'user desc':
                    item = Item.user_id.desc()
                    args.append(item)
                if item == 'user asc':
                    item = Item.user_id.asc()
                    args.append(item)
                if item == 'category asc':
                    item = Item.category_name.asc()
                    args.append(item)
                if item == 'category desc':
                    item = Item.category_name.desc()
                    args.append(item)

    # Setup query with all filters included
    query = Item.query.filter(
        db.and_(
            db.or_(
                Item.name == name for name in names
            ),
            db.or_(
                Item.id == id for id in ids
            ),
            db.or_(
                Item.user_id == user for user in users
            ),
            db.or_(
                Item.category_name == category for category in categories
            )
        )
    ).order_by(*args)

    # Try to get all results or filtered results from database
    try:
        items = query.limit(count).all()

        # If query returns no items, return error
        if len(items) == 0:
            return jsonify({'error': 'No results found!'}), 404

    # If some sqlalchemy error is thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # If query successful, return array of item objects
    item_schema = ItemSchema(many=True)
    output = item_schema.dump(items).data

    return jsonify(
        {'num_results': str(len(output)), 'items': output}
    ), 200


@api.route('/items/<int:id>', methods=['GET'])
@jwt_optional
def get_one_item(id):
    """
    Return single item as an object.
    This is a public non-protected endpoint.
    """
    # Setup query
    query = Item.query.filter_by(id=id)

    # Try to get item from database
    try:
        item = query.one()

    # If no result found, return error
    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    # If some other sqlalchemy error thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # If query successful, return item object
    item_schema = ItemSchema()
    output = item_schema.dump(item).data

    return jsonify({'item': output}), 200


@api.route('/items/<int:id>', methods=['PUT'])
@jwt_required
def edit_one_item(id):
    """
    Edit single item.
    This is a protected endpoint and requires valid jwt token.
    """
    # Get user id from jwt token
    public_id = get_jwt_identity()

    # Get item attributes from form fields
    name = request.form['name']
    nameCap = cap_sentence(name)
    description = request.form['description']
    category = request.form['category']

    # Setup query
    query = Item.query.filter_by(id=id, user_id=public_id)

    # Try to get item from database
    try:
        item = query.one()

    # If no result found, return error
    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    # If some other sqlalchemy error thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # Try to update item in database
    try:

        # Check if name field is not empty
        if name:

            # Check if name field contains html or javascript
            if is_html(name):
                return jsonify(
                    {'error': 'Html and script injection is not allowed!'}
                ), 422

            # Update item name
            item.name = name

        # Check if description field is not empty
        if description:

            # Check if description field cotains html or javascript
            if is_html(description):
                return jsonify(
                    {'error': 'Html and script injection is not allowed!'}
                ), 422

            # Update description
            item.description = description

        # Check if category field is not empty
        if category:

            # Check if category field contains html or javascript
            if is_html(category):
                return jsonify(
                    {'error': 'Html and script injection is not allowed!'}
                ), 422

            # Update category
            item.category_name = category

        # Commit changes to database
        db.session.commit()

    # If name already exists, return error
    except IntegrityError:
        return jsonify(
            {'error': 'Item named %s already exists!' % nameCap}
        ), 422

    # If some other sqlalchemy error thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # If item successfully updated, return success
    return jsonify(
        {'success': 'Item named %s has been updated!' % nameCap}
    ), 200


@api.route('/items/<int:id>', methods=['DELETE'])
@jwt_required
def delete_one_item(id):
    """
    Delete single item.
    This is a protected endpoint and requires valid jwt token.
    """
    # Get user id from jwt token
    public_id = get_jwt_identity()

    # Setup query
    query = Item.query.filter_by(id=id, user_id=public_id)

    # Try to get item from database
    try:
        item = query.one()

        # Get name from item object
        name = item.name
        nameCap = cap_sentence(name)

    # If no result found, return error
    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    # If some other sqlalchemy error thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # Try to delete item in database
    try:
        db.session.delete(item)
        db.session.commit()

    # If some sqlalchemy error thrown, return error
    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    # If item successfully deleted, return success
    return jsonify(
        {'success': 'Item named %s been deleted!' % nameCap}
    ), 200
