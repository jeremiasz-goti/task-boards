from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# --- APP CONFIG
app = Flask(__name__)
DATABASE_URL = 'sqlite:///task-boards.db'
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MARSHMALLOW
mm = Marshmallow(app)

# --- BASIC MODELS

class Board(db.Model):
    boardId = db.Column(db.Integer, primary_key=True)
    boardName = db.Column(db.String(100))

    def __init__(self, boardName):
        self.boardName = boardName

# --- SCHEMAS

class boardSchema(mm.Schema):
    class Meta:
        fields = ['boardId', 'boardName']

board_schema = boardSchema()
boards_schema = boardSchema(many=True)

# --- ROUTINGS

# Add board
@app.route('/api/board', methods=['POST'])
def addBoard():
    name = request.get_json()['boardName']
    newBoard = Board(boardName=name)
    db.session.add(newBoard)
    db.session.commit()
    return board_schema.jsonify(newBoard)

# Edit board
@app.route('/api/board/<id>', methods=['PUT'])
def editBoard(id):
    board = Board.query.get(id)
    name = request.get_json()['boardName']
    board.boardName = name
    db.session.commit()
    return board_schema.jsonify(board)

# Get all boards
@app.route('/api/board', methods=['GET'])
def getAllBoards():
    allBoards = Board.query.all()
    result = boards_schema.dump(allBoards)
    return jsonify(result)

# Get single board
@app.route('/api/board/<id>', methods=['GET'])
def getSingleBoard(id):
    singleBoard = Board.query.get(id)
    return board_schema.jsonify(singleBoard)

# Delete board
@app.route('/api/board/<id>', methods=['DELETE'])
def deleteBoard(id):
    board = Board.query.get(id)
    db.session.delete(board)
    db.session.commit()
    return board_schema.jsonify(board)


if __name__ == '__main__':
    app.run(debug=True)