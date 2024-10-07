from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

# initialize the app
app = Flask(__name__)

# configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# configure extensions
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


# routes
# GET /messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()

    # Ensures messages is not None and contains data
    if messages is None or len(messages) == 0:
        return make_response(jsonify([]), 200)

    messages_serialized = [message.to_dict() for message in messages]
    return make_response(jsonify(messages_serialized), 200)


# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     return ''

# POST /messages
@app.route('/messages', methods = ['POST'])
def create_message():
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.to_dict()), 201

# PATCH/message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict()), 200

# DELETE/message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return '', 204

# Helper function to convert a message object to dict
def to_dict(self):
    return {
        "id": self.id,
        "body": self.body,
        "username": self.username,
        "created_at": self.created_at,
        "updated_at": self.updated_at
    }

Message.to_dict = to_dict

if __name__ == '__main__':
    app.run(port=5555)

