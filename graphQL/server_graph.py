from flask import Flask, request, jsonify
from graphene import ObjectType, String, Int, List, Schema
import sqlite3

app = Flask(__name__)
DB = '../spotify.sqlite'

def query_db(query, args=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Tipos GraphQL
class Usuario(ObjectType):
    id = Int()
    nome = String()
    idade = Int()

class Musica(ObjectType):
    id = Int()
    nome = String()
    artista = String()

class Playlist(ObjectType):
    id = Int()
    nome = String()
    id_usuario = Int()

# Queries
class Query(ObjectType):
    usuarios = List(Usuario)
    musicas = List(Musica)
    playlists_usuario = List(Playlist, usuario_id=Int(required=True))
    musicas_playlist = List(Musica, playlist_id=Int(required=True))
    playlists_musica = List(Playlist, musica_id=Int(required=True))

    def resolve_usuarios(root, _):
        return query_db("SELECT * FROM Usuario")

    def resolve_musicas(root, _):
        return query_db("SELECT * FROM Musica")

    def resolve_playlists_usuario(root, _, usuario_id):
        return query_db("SELECT * FROM Playlist WHERE id_usuario = ?", (usuario_id,))

    def resolve_musicas_playlist(root, _, playlist_id):
        return query_db("""
            SELECT Musica.* FROM Musica
            JOIN Playlist_Musica ON Musica.id = Playlist_Musica.id_musica
            WHERE Playlist_Musica.id_playlist = ?
        """, (playlist_id,))

    def resolve_playlists_musica(root, _, musica_id):
        return query_db("""
            SELECT Playlist.* FROM Playlist
            JOIN Playlist_Musica ON Playlist.id = Playlist_Musica.id_playlist
            WHERE Playlist_Musica.id_musica = ?
        """, (musica_id,))

schema = Schema(query=Query)

@app.route("/graphql", methods=["POST"])
def graphql_post():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Requisição inválida"}), 400

    result = schema.execute(data["query"], variables=data.get("variables"))
    return jsonify(result.data if not result.errors else {"errors": [str(e) for e in result.errors]})

@app.route("/", methods=["GET"])
def hello():
    return "Servidor GraphQL rodando! Use POST em /graphql com uma query."

if __name__ == "__main__":
    app.run(debug=True, port=4000)
