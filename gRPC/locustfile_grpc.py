import grpc
import time
from locust import User, task, between

import spotify_pb2
import spotify_pb2_grpc

class GRPCUser(User):
    wait_time = between(1, 3)
    host = "localhost:50051"  # opcional, não usado no gRPC

    def on_start(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = spotify_pb2_grpc.SpotifyServiceStub(self.channel)

    def grpc_request(self, name, func, *args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            total_time = (time.time() - start_time) * 1000  # ms
            self.environment.events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                response_length=0,  # opcional, pode estimar o tamanho da resposta
                success=True,
            )
            return result
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            self.environment.events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=total_time,
                response_length=0,
                success=False,
                exception=e,
            )

    @task
    def listar_usuarios(self):
        request = spotify_pb2.Empty()
        response = self.grpc_request("ListarUsuarios", self.stub.ListarUsuarios, request)
        if response:
            print(f"ListarUsuarios: {len(response.usuarios)} usuários retornados.")

    @task
    def listar_musicas(self):
        request = spotify_pb2.Empty()
        response = self.grpc_request("ListarMusicas", self.stub.ListarMusicas, request)
        if response:
            print(f"ListarMusicas: {len(response.musicas)} músicas retornadas.")

    @task
    def listar_playlists_por_usuario(self):
        request = spotify_pb2.UsuarioRequest(usuario_id=1)
        response = self.grpc_request("ListarPlaylistsPorUsuario", self.stub.ListarPlaylistsPorUsuario, request)
        if response:
            print(f"ListarPlaylistsPorUsuario: {len(response.playlists)} playlists do usuário 1.")

    @task
    def listar_musicas_por_playlist(self):
        request = spotify_pb2.PlaylistRequest(playlist_id=1)
        response = self.grpc_request("ListarMusicasPorPlaylist", self.stub.ListarMusicasPorPlaylist, request)
        if response:
            print(f"ListarMusicasPorPlaylist: {len(response.musicas)} músicas na playlist 1.")

    @task
    def listar_playlists_por_musica(self):
        request = spotify_pb2.MusicaRequest(musica_id=1)
        response = self.grpc_request("ListarPlaylistsPorMusica", self.stub.ListarPlaylistsPorMusica, request)
        if response:
            print(f"ListarPlaylistsPorMusica: {len(response.playlists)} playlists com a música 1.")
