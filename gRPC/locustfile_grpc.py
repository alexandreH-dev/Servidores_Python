from locust import User, task, between
import grpc
import spotify_pb2
import spotify_pb2_grpc

class SpotifyClient:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = spotify_pb2_grpc.SpotifyServiceStub(self.channel)

    def listar_usuarios(self):
        return self.stub.ListarUsuarios(spotify_pb2.Empty())

    def listar_musicas(self):
        return self.stub.ListarMusicas(spotify_pb2.Empty())

    def listar_playlists_por_usuario(self, usuario_id=1):
        return self.stub.ListarPlaylistsPorUsuario(spotify_pb2.UsuarioRequest(usuario_id=usuario_id))

    def listar_musicas_por_playlist(self, playlist_id=1):
        return self.stub.ListarMusicasPorPlaylist(spotify_pb2.PlaylistRequest(playlist_id=playlist_id))

    def listar_playlists_por_musica(self, musica_id=1):
        return self.stub.ListarPlaylistsPorMusica(spotify_pb2.MusicaRequest(musica_id=musica_id))

class GrpcUser(User):
    wait_time = between(1, 2)
    host = "http://localhost:5051"

    def on_start(self):
        self.client = SpotifyClient()

    @task(1)
    def task_listar_usuarios(self):
        try:
            self.client.listar_usuarios()
        except grpc.RpcError as e:
            print(f"Erro listar_usuarios: {e}")

    @task(1)
    def task_listar_musicas(self):
        try:
            self.client.listar_musicas()
        except grpc.RpcError as e:
            print(f"Erro listar_musicas: {e}")

    @task(1)
    def task_listar_playlists_usuario(self):
        try:
            self.client.listar_playlists_por_usuario(usuario_id=1)
        except grpc.RpcError as e:
            print(f"Erro listar_playlists_usuario: {e}")

    @task(1)
    def task_listar_musicas_playlist(self):
        try:
            self.client.listar_musicas_por_playlist(playlist_id=1)
        except grpc.RpcError as e:
            print(f"Erro listar_musicas_playlist: {e}")

    @task(1)
    def task_listar_playlists_musica(self):
        try:
            self.client.listar_playlists_por_musica(musica_id=1)
        except grpc.RpcError as e:
            print(f"Erro listar_playlists_musica: {e}")
