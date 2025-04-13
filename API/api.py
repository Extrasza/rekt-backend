from datetime import datetime
from flask_openapi3 import Info, Tag, OpenAPI
from flask import request, jsonify
import sqlite3
from flask_cors import CORS
from models import GameInput, DeleteGameRequest, GameStatusUpdate, GameQuery

info = Info(title="REKT Game API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#Tag para o Swagger.
game_tag = Tag(name="Jogos", description="Manipulação de Jogos de um usuário")

def get_db_connection():
    conn = sqlite3.connect('rekt.db')
    conn.row_factory = sqlite3.Row
    return conn

#Criação da tabela base no banco de dados.
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            game_name TEXT NOT NULL,
            is_finished BOOLEAN,
            started_at TEXT,  -- Data de início
            finished_at TEXT,  -- Data de finalização
            UNIQUE(username, game_name)  -- Garante que o par (username, game_name) seja único
        )
    ''')

    conn.commit()
    conn.close()

create_table()


# Endpoint de inserção de um jogo para um usuário no DB.
@app.post("/games",tags=[game_tag],summary="Insere um jogo no registro de um usuário.", responses={
    201: {
        "description": "Jogo adicionado com sucesso.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Jogo adicionado com sucesso!"
                }
            }
        }
    }
})
def add_game(body: GameInput):
    username = body.username
    game_name = body.game_name
    is_finished = body.is_finished
    started_at = datetime.now()

    if not username or not game_name or not started_at:
        return jsonify({"error": "Campos obrigatórios faltando: Usuário, Nome do Jogo"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO games (username, game_name, is_finished, started_at)
        VALUES (?, ?, ?, ?)
    ''', (username, game_name, is_finished, started_at))
    conn.commit()
    conn.close()

    return jsonify({"message": "Jogo adicionado com sucesso!"}), 201

@app.get("/games", tags=[game_tag], summary="Lista todos os jogos de um usuário.", responses={
    200: {
        "description": "Lista de jogos do usuário.",
        "content": {
            "application/json": {
                "example": [
                    {
                        "id": 1,
                        "username": "Joao",
                        "game_name": "The Legend of Zelda",
                        "is_finished": False
                    }
                ]
            }
        }
    },
    400: {
        "description": "Parâmetro 'username' ausente.",
        "content": {
            "application/json": {
                "example": {
                    "error": "Parâmetro 'username' é obrigatório."
                }
            }
        }
    }
})
@app.get("/games", tags=[game_tag], summary="Lista todos os jogos de um usuário.")
def get_games(query: GameQuery):
    username = query.username

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM games WHERE username = ?', (username,))
    games = cursor.fetchall()
    conn.close()

    return jsonify([dict(game) for game in games]), 200

# Endpoint de deleção de jogos para um usuário específico.
@app.delete("/games", tags=[game_tag], summary="Remove um jogo da lista do usuário.", responses={
    200: {
        "description": "Jogo removido com sucesso.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Jogo removido com sucesso!"
                }
            }
        }
    }
})
def delete_game(body: DeleteGameRequest):
    game_name = body.game_name
    username = body.username

    if not game_name or not username:
        return jsonify({"message": "Nome do jogo e nome de usuário são necessários!"}), 400

    print(f"Attempting to delete game: {game_name} for user: {username}")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM games WHERE game_name = ? AND username = ?
    ''', (game_name, username))
    game = cursor.fetchone()

    if game is None:
        conn.close()
        return jsonify({"message": "Jogo não encontrado para o usuário!"}), 404

    cursor.execute('''
        DELETE FROM games WHERE game_name = ? AND username = ?
    ''', (game_name, username))
    conn.commit()
    conn.close()

    return jsonify({"message": "Jogo removido com sucesso!"})

# Endpoint de atualização de data e estado de um jogo de um usuário.
@app.put("/games", tags=[game_tag], summary="Atualiza o estado jogo adicionando data de finalização.", responses={
    200: {
        "description": "Status do jogo atualizado com sucesso.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Status do jogo atualizado com sucesso!"
                }
            }
        }
    }
})
def update_game_status(body: GameStatusUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT is_finished FROM games WHERE game_name = ? AND username = ?
    ''', (body.game_name, body.username))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return jsonify({"message": "Jogo não encontrado para o usuário!"}), 404

    new_status = not result[0] 
    finished_at = datetime.now()
    cursor.execute('''
        UPDATE games SET is_finished = ?, finished_at = ? WHERE game_name = ? AND username = ?
    ''', (new_status, finished_at, body.game_name, body.username))
    conn.commit()
    conn.close()

    return jsonify({"message": "Status do jogo atualizado com sucesso!"}), 200

# Main Function
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
