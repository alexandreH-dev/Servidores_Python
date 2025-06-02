# pip install spyne lxml werkzeug
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import sqlite3

def executar_consulta(query, params=()):
    con = sqlite3.connect("../spotify.sqlite")
    cur = con.cursor()
    cur.execute(query, params)
    resultados = cur.fetchall()
    con.close()
    return resultados

class StreamingService(ServiceBase):

    @rpc(_returns=Iterable(Unicode))
    def listar_usuarios(ctx):
        resultados = executar_consulta("SELECT * FROM Usuario")
        return [str(r) for r in resultados]

    @rpc(_returns=Iterable(Unicode))
    def listar_musicas(ctx):
        resultados = executar_consulta("SELECT * FROM Musica")
        return [str(r) for r in resultados]

    @rpc(Integer, _returns=Iterable(Unicode))
    def listar_playlists_usuario(ctx, usuario_id):
        query = "SELECT * FROM Playlist WHERE id_usuario = ?"
        resultados = executar_consulta(query, (usuario_id,))
        return [str(r) for r in resultados]

    @rpc(Integer, _returns=Iterable(Unicode))
    def listar_musicas_playlist(ctx, playlist_id):
        query = """
            SELECT m.ID, m.Nome, m.Artista
            FROM Musica m
            JOIN Playlist_Musica pm ON m.ID = pm.id_musica
            WHERE pm.id_playlist = ?
        """
        resultados = executar_consulta(query, (playlist_id,))
        return [str(r) for r in resultados]

    @rpc(Integer, _returns=Iterable(Unicode))
    def listar_playlists_musica(ctx, musica_id):
        query = """
            SELECT p.ID, p.Nome, p.id_usuario
            FROM Playlist p
            JOIN Playlist_Musica pm ON p.ID = pm.id_playlist
            WHERE pm.id_musica = ?
        """
        resultados = executar_consulta(query, (musica_id,))
        return [str(r) for r in resultados]

# Aplicação SOAP
application = Application(
    [StreamingService],
    tns="spyne.streaming.soap",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Servidor WSGI
from werkzeug.serving import run_simple
wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    print("Servidor SOAP rodando em http://localhost:8000/soap")
    run_simple("localhost", 8000, wsgi_app)
