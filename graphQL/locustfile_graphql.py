from locust import HttpUser, task, between

class GraphQLUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:4000"

    @task(1)
    def listar_usuarios(self):
        query = {"query": "{ usuarios { id nome idade } }"}
        self.client.post("/graphql", json=query, name="usuarios")

    @task(1)
    def listar_musicas(self):
        query = {"query": "{ musicas { id nome artista } }"}
        self.client.post("/graphql", json=query, name="musicas")

    @task(1)
    def listar_playlists_usuario(self):
        query = {
            "query": """
                {
                    playlists_usuario(usuario_id: 1) {
                        id
                        nome
                        id_usuario
                    }
                }
            """
        }
        self.client.post("/graphql", json=query, name="playlists_usuario")

    @task(1)
    def listar_musicas_playlist(self):
        query = {
            "query": """
                {
                    musicas_playlist(playlist_id: 1) {
                        id
                        nome
                        artista
                    }
                }
            """
        }
        self.client.post("/graphql", json=query, name="musicas_playlist")

    @task(1)
    def listar_playlists_musica(self):
        query = {
            "query": """
                {
                    playlists_musica(musica_id: 1) {
                        id
                        nome
                        id_usuario
                    }
                }
            """
        }
        self.client.post("/graphql", json=query, name="playlists_musica")
