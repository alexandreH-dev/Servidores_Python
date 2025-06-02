import sqlite3
import grpc
from concurrent import futures
import spotify_pb2
import spotify_pb2_grpc

def conectar():
    return sqlite3.connect("../spotify.sqlite")

class SpotifyService(spotify_pb2_grpc.SpotifyServiceServicer):
    def ListarUsuarios(self, request, context):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM Usuario")
        usuarios = [spotify_pb2.Usuario(id=row[0], nome=row[1], idade=row[2]) for row in cur.fetchall()]
        con.close()
        return spotify_pb2.UsuariosResponse(usuarios=usuarios)

    def ListarMusicas(self, request, context):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM Musica")
        musicas = [spotify_pb2.Musica(id=row[0], nome=row[1], artista=row[2]) for row in cur.fetchall()]
        con.close()
        return spotify_pb2.MusicasResponse(musicas=musicas)

    def ListarPlaylistsPorUsuario(self, request, context):
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM Playlist WHERE id_usuario = ?", (request.usuario_id,))
        playlists = [spotify_pb2.Playlist(id=row[0], nome=row[1], usuario_id=row[2]) for row in cur.fetchall()]
        con.close()
        return spotify_pb2.PlaylistsResponse(playlists=playlists)

    def ListarMusicasPorPlaylist(self, request, context):
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT m.id, m.nome, m.artista 
            FROM Musica m
            JOIN Playlist_Musica pm ON m.ID = pm.id_musica
            WHERE pm.id_playlist = ?
        """, (request.playlist_id,))
        musicas = [spotify_pb2.Musica(id=row[0], nome=row[1], artista=row[2]) for row in cur.fetchall()]
        con.close()
        return spotify_pb2.MusicasResponse(musicas=musicas)

    def ListarPlaylistsPorMusica(self, request, _):
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            SELECT p.id, p.nome, p.id_usuario 
            FROM Playlist p
            JOIN Playlist_Musica pm ON p.ID = pm.id_playlist
            WHERE pm.id_musica = ?
        """, (request.musica_id,))
        playlists = [spotify_pb2.Playlist(id=row[0], nome=row[1], usuario_id=row[2]) for row in cur.fetchall()]
        con.close()
        return spotify_pb2.PlaylistsResponse(playlists=playlists)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    spotify_pb2_grpc.add_SpotifyServiceServicer_to_server(SpotifyService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor gRPC em execução na porta 50051...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
