import os
import sys
import copy
from flask import Flask, jsonify, request, send_from_directory, render_template

# Locate game logic (prefer web/src, fallback to project src)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
WEB_SRC = os.path.join(os.path.dirname(__file__), 'src')
if os.path.exists(WEB_SRC):
    SRC = WEB_SRC
else:
    SRC = os.path.join(ROOT, 'src')

if SRC not in sys.path:
    sys.path.insert(0, SRC)

from src.board import Board
from src.move import Move
from src.square import Square

app = Flask(__name__, template_folder='templates', static_folder='static')

# In-memory single game instance (suitable for single-worker deployments)
GAME = {'board': Board(), 'next_player': 'white', 'history': []}


def _short_name(long_name):
    mapping = {'pawn': 'p', 'rook': 'r', 'knight': 'n', 'bishop': 'b', 'queen': 'q', 'king': 'k'}
    return mapping.get(long_name, long_name[:1])


def serialize_board(board):
    pieces = []
    for r in range(8):
        for c in range(8):
            sq = board.squares[r][c]
            if sq.has_piece():
                p = sq.piece
                pieces.append({'row': r, 'col': c, 'name': _short_name(p.name), 'color': 'w' if p.color == 'white' else 'b'})

    last = None
    if getattr(board, 'last_move', None):
        last = {
            'initial': {'row': board.last_move.initial.row, 'col': board.last_move.initial.col},
            'final': {'row': board.last_move.final.row, 'col': board.last_move.final.col}
        }

    return {'rows': 8, 'cols': 8, 'pieces': pieces, 'last_move': last}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/images/<path:filename>')
def static_images(filename):
    # Serve images from the project's `assets/images` so we don't need to duplicate large files.
    images_dir = os.path.abspath(os.path.join(ROOT, 'assets', 'images'))
    return send_from_directory(images_dir, filename)


@app.route('/api/state')
def api_state():
    board = GAME['board']
    return jsonify({'board': serialize_board(board), 'next_player': GAME['next_player']})


@app.route('/api/reset', methods=['POST'])
def api_reset():
    GAME['board'] = Board()
    GAME['next_player'] = 'white'
    return jsonify({'ok': True})


@app.route('/api/move', methods=['POST'])
def api_move():
    data = request.get_json() or {}
    try:
        ir = int(data.get('initial_row'))
        ic = int(data.get('initial_col'))
        fr = int(data.get('final_row'))
        fc = int(data.get('final_col'))
    except Exception:
        return jsonify({'ok': False, 'error': 'invalid payload'})

    board = GAME['board']

    if not Square.in_range(ir, ic, fr, fc):
        return jsonify({'ok': False, 'error': 'out of range'})

    sq = board.squares[ir][ic]
    if not sq.has_piece():
        return jsonify({'ok': False, 'error': 'no piece at initial'})

    piece = sq.piece
    if piece.color != GAME['next_player']:
        return jsonify({'ok': False, 'error': 'not your turn'})

    # calculate valid moves for this piece
    board.calc_moves(piece, ir, ic, bool=True)
    initial = Square(ir, ic)
    final_piece = board.squares[fr][fc].piece if board.squares[fr][fc].has_piece() else None
    final = Square(fr, fc, final_piece)
    move = Move(initial, final)

    if not board.valid_move(piece, move):
        return jsonify({'ok': False, 'error': 'invalid move'})

    # perform move
    # push snapshot for undo
    try:
        GAME['history'].append(copy.deepcopy(board))
    except Exception:
        # fallback: clear history if deepcopy fails
        GAME['history'] = []

    board.move(piece, move, testing=False)
    board.set_true_en_passant(piece)

    # toggle next player
    GAME['next_player'] = 'white' if GAME['next_player'] == 'black' else 'black'

    return jsonify({'ok': True, 'board': serialize_board(board), 'next_player': GAME['next_player']})


@app.route('/api/undo', methods=['POST'])
def api_undo():
    # restore last board snapshot
    if not GAME.get('history'):
        return jsonify({'ok': False, 'error': 'nothing to undo'})

    last_board = GAME['history'].pop()
    GAME['board'] = last_board
    # toggle back the player since a move was undone
    GAME['next_player'] = 'white' if GAME['next_player'] == 'black' else 'black'

    return jsonify({'ok': True, 'board': serialize_board(GAME['board']), 'next_player': GAME['next_player']})


if __name__ == '__main__':
    # Run without the reloader for predictable background starts from automation
    app.run(host='127.0.0.1', debug=False, port=int(os.environ.get('PORT', 5000)))
