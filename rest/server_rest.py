from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB = '../spotify.sqlite'

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    conn.close()
    return (dict(row) for row in rows) if not one else dict(rows[0]) if rows else {}

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    data = list(query_db("SELECT * FROM Usuario"))
    return jsonify(data)

@app.route('/musicas', methods=['GET'])
def listar_musicas():
    data = list(query_db("SELECT * FROM Musica"))
    return jsonify(data)

@app.route('/playlists/usuario/<int:id_usuario>', methods=['GET'])
def playlists_usuario(id_usuario):
    query = "SELECT * FROM Playlist WHERE id_usuario = ?"
    data = list(query_db(query, (id_usuario,)))
    return jsonify(data)

@app.route('/musicas/playlist/<int:id_playlist>', methods=['GET'])
def musicas_playlist(id_playlist):
    query = """
        SELECT Musica.* FROM Musica
        JOIN Playlist_Musica ON Musica.id = Playlist_Musica.id_musica
        WHERE Playlist_Musica.id_playlist = ?
    """
    data = list(query_db(query, (id_playlist,)))
    return jsonify(data)

@app.route('/playlists/musica/<int:id_musica>', methods=['GET'])
def playlists_musica(id_musica):
    query = """
        SELECT Playlist.* FROM Playlist
        JOIN Playlist_Musica ON Playlist.id = Playlist_Musica.id_playlist
        WHERE Playlist_Musica.id_musica = ?
    """
    data = list(query_db(query, (id_musica,)))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
