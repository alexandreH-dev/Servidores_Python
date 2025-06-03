from locust import HttpUser, task, between

class SpotifyRestUser(HttpUser):
    wait_time = between(1, 3)  # tempo de espera entre as requisições de um usuário

    @task
    def listar_usuarios(self):
        self.client.get("/usuarios")

    @task
    def listar_musicas(self):
        self.client.get("/musicas")

    @task
    def listar_playlists_usuario(self):
        self.client.get("/playlists/usuario/1")  # ajuste o ID conforme necessário

    @task
    def listar_musicas_playlist(self):
        self.client.get("/musicas/playlist/1")  # ajuste o ID conforme necessário

    @task
    def listar_playlists_musica(self):
        self.client.get("/playlists/musica/1")  # ajuste o ID conforme necessário
