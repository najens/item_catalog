from app import db
from flask import request, jsonify, make_response
from app.models import Item, ItemSchema
from flask_jwt_extended import jwt_required, jwt_optional, get_jwt_identity
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.api import api
from app.api.functions import is_html


@api.route('/items', methods=['POST'])
@jwt_required
def create_new_item():
    """ Create new item and return the new item object """
    public_id = get_jwt_identity()
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    if name and category and description:

        if is_html(name) or is_html(category) or is_html(description):
            return jsonify(
                {'error': 'Html and script injection is not allowed!'}
            ), 422

        try:
            new_item = Item(
                name=name,
                description=description,
                category_name=category,
                user_id=public_id
            )
            db.session.add(new_item)
            db.session.commit()

        except IntegrityError:
            return jsonify(
                {'error': 'Item named %s already exists!' % name}
            ), 422

        except SQLAlchemyError:
            return jsonify({'error': 'Some problem occurred!'}), 400

        new_item_schema = ItemSchema()
        output = new_item_schema.dump(new_item).data
        resp = make_response(jsonify(
            {
                'item': output,
                'success': 'Item named %s has been created!' % name
            }
        ), 201)
        resp.headers['Location'] = (
            'http://localhost:5000/items/' + str(new_item.id)
        )
        return resp

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
        - To sort results add 'sort=value1+asc, value2+desc'
            Ex. Sort all results by category name in ascending order
                /catalog/categories?name=basketball&sort=name+asc
    """
    ids = []
    names = []
    users = []
    categories = []
    args = []
    count = None
    items = Item.query.all()
    item_schema = ItemSchema(many=True)
    output = item_schema.dump(items).data

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

    try:
        items = query.limit(count).all()
        if len(items) == 0:
            return jsonify({'error': 'No results found!'}), 404

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    item_schema = ItemSchema(many=True)
    output = item_schema.dump(items).data

    return jsonify(
        {'num_results': str(len(output)), 'items': output}
    ), 200


@api.route('/items/<int:id>', methods=['GET'])
@jwt_optional
def get_one_item(id):
    """ Return single item as an object """
    query = Item.query.filter_by(id=id)

    try:
        item = query.one()

    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    item_schema = ItemSchema()
    output = item_schema.dump(item).data

    return jsonify({'item': output}), 200


@api.route('/items/<int:id>', methods=['PUT'])
@jwt_required
def edit_one_item(id):
    """ Edit single item """
    public_id = get_jwt_identity()
    query = Item.query.filter_by(id=id, user_id=public_id)

    try:
        item = query.one()

    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    try:

        name = request.form['name']
        description = request.form['description']
        category = request.form['category']

        if name:

            if is_html(name):
                return jsonify(
                    {'error': 'Html and script injection is not allowed!'}
                ), 422

            item.name = name

        if description:

            if is_html(description):
                return jsonify(
                    {'error': 'Html and script injection is not allowed!'}
                ), 422

            item.description = description

        if category:

            if is_html(category):
                return jsonify(
                    {'error': 'Html and script injection is not allowed!'}
                ), 422

            item.category_name = category

        db.session.commit()

    except IntegrityError:
        return jsonify(
            {'error': 'Item named %s already exists!' % name}
        ), 422

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    return jsonify(
        {'success': 'Item named %s has been updated!' % name}
    ), 200


@api.route('/items/<int:id>', methods=['DELETE'])
@jwt_required
def delete_one_item(id):
    """ Delete single item """
    public_id = get_jwt_identity()
    query = Item.query.filter_by(id=id, user_id=public_id)

    try:
        item = query.one()

    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    try:
        db.session.delete(item)
        db.session.commit()

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    return jsonify(
        {'success': 'Item named %s been deleted!' % item.name}
    ), 200
