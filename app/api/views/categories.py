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
    """ Create new category and return the new category object """
    public_id = get_jwt_identity()
    name = request.form['name']
    name_cap = cap_sentence(name)

    if name:

        if is_html(name):
            return jsonify(
                {'error': 'Html and script injection is not allowed!'}
            ), 422

        try:
            new_category = Category(name=name, user_id=public_id)
            db.session.add(new_category)
            db.session.commit()

        except IntegrityError:
            return jsonify(
                {'error': 'Category named %s already exists!' % name_cap}
            ), 422

        except SQLAlchemyError:
            return jsonify({'error': 'Some problem occurred!'}), 400

        new_category_schema = CategorySchema()
        output = new_category_schema.dump(new_category).data
        resp = make_response(jsonify(
            {
                'category': output,
                'success': 'Category named %s has been created!' % name_cap
            }
        ), 201)
        resp.headers['Location'] = (
            'http://localhost:5000/categories/' + str(new_category.id)
        )

        return resp

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
    """
    ids = []
    names = []
    user_ids = []
    args = []
    count = None

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

    try:
        categories = query.limit(count).all()
        if len(categories) == 0:
            return jsonify({'error': 'No results found!'}), 404

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    category_schema = CategorySchema(many=True)
    output = category_schema.dump(categories).data

    return jsonify(
        {'num_results': str(len(output)), 'categories': output}
    ), 200


@api.route('/categories/<int:id>', methods=['GET'])
def get_one_category(id):
    """ Return single category as an object """
    query = Category.query.filter_by(id=id)

    try:
        category = query.one()

    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    category_schema = CategorySchema()
    output = category_schema.dump(category).data

    return jsonify({'category': output}), 200


@api.route('/categories/<int:id>', methods=['PUT'])
@jwt_required
def edit_one_category(id):
    """ Edit single item """
    public_id = get_jwt_identity()
    query = Category.query.filter_by(
            id=id,
            user_id=public_id
    )

    try:
        category = query.one()

    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    name = request.form['name']
    nameCap = cap_sentence(name)

    if name:

        if is_html(name):
            return jsonify(
                {'error': 'Html and script injection is not allowed!'}
            ), 422

        try:
            category.name = name
            db.session.commit()

        except IntegrityError:
            return jsonify(
                {'error': 'Category named %s already exists!' % nameCap}
            ), 422

        except SQLAlchemyError:
            return jsonify({'error': 'Some problem occurred!'}), 400

        return jsonify(
            {'success': 'The category named %s has been updated!' % nameCap}
        ), 200

    return jsonify({'error': 'Missing data!'}), 400


@api.route('/categories/<int:id>', methods=['DELETE'])
@jwt_required
def delete_one_category(id):
    """ Delete single category """
    public_id = get_jwt_identity()
    query = Category.query.filter_by(id=id, user_id=public_id)

    try:
        category = query.one()
        name = category.name
        nameCap = cap_sentence(name)

    except NoResultFound:
        return jsonify({'error': 'No result found!'}), 404

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    try:
        db.session.delete(category)
        db.session.commit()

    except SQLAlchemyError:
        return jsonify({'error': 'Some problem occurred!'}), 400

    return jsonify(
        {'success': 'The category named %s has been deleted!' % nameCap}
    ), 200
