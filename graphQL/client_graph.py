import requests

URL = "http://localhost:4000/graphql"

def query(q, variables=None):
    r = requests.post(URL, json={'query': q, 'variables': variables})
    print(r.json())

# Exemplos
query_usuarios = """
query {
  usuarios {
    id
    nome
    idade
  }
}
"""

query_musicas = """
query {
  musicas {
    id
    nome
    artista
  }
}
"""

query_playlists_usuario = """
query ($id: Int!) {
  playlistsUsuario(usuarioId: $id) {
    id
    nome
  }
}
"""

query_musicas_playlist = """
query ($id: Int!) {
  musicasPlaylist(playlistId: $id) {
    id
    nome
  }
}
"""

query_playlists_musica = """
query ($id: Int!) {
  playlistsMusica(musicaId: $id) {
    id
    nome
  }
}
"""

# Interface simples
while True:
    print("\n--- CLIENTE GRAPHQL ---")
    print("1 - Listar usuários")
    print("2 - Listar músicas")
    print("3 - Playlists de um usuário")
    print("4 - Músicas de uma playlist")
    print("5 - Playlists com uma música")
    print("0 - Sair")

    op = input("Escolha: ")

    if op == "1":
        query(query_usuarios)
    elif op == "2":
        query(query_musicas)
    elif op == "3":
        uid = int(input("ID do usuário: "))
        query(query_playlists_usuario, {"id": uid})
    elif op == "4":
        pid = int(input("ID da playlist: "))
        query(query_musicas_playlist, {"id": pid})
    elif op == "5":
        mid = int(input("ID da música: "))
        query(query_playlists_musica, {"id": mid})
    elif op == "0":
        break
