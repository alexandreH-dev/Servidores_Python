import grpc
import spotify_pb2
import spotify_pb2_grpc

def menu():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = spotify_pb2_grpc.SpotifyServiceStub(channel)

        while True:
            print("\n--- CLIENTE gRPC - STREAMING DE MÚSICAS ---")
            print("1 - Listar todos os usuários")
            print("2 - Listar todas as músicas")
            print("3 - Listar playlists de um usuário")
            print("4 - Listar músicas de uma playlist")
            print("5 - Listar playlists que contêm uma música")
            print("0 - Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                resposta = stub.ListarUsuarios(spotify_pb2.Empty())
                for u in resposta.usuarios:
                    print(f"ID: {u.id}, Nome: {u.nome}, Idade: {u.idade}")

            elif opcao == "2":
                resposta = stub.ListarMusicas(spotify_pb2.Empty())
                for m in resposta.musicas:
                    print(f"ID: {m.id}, Nome: {m.nome}, Artista: {m.artista}")

            elif opcao == "3":
                id_usuario = int(input("ID do usuário: "))
                resposta = stub.ListarPlaylistsPorUsuario(spotify_pb2.UsuarioRequest(usuario_id=id_usuario))
                for p in resposta.playlists:
                    print(f"ID: {p.id}, Nome: {p.nome}")

            elif opcao == "4":
                id_playlist = int(input("ID da playlist: "))
                resposta = stub.ListarMusicasPorPlaylist(spotify_pb2.PlaylistRequest(playlist_id=id_playlist))
                for m in resposta.musicas:
                    print(f"ID: {m.id}, Nome: {m.nome}, Artista: {m.artista}")

            elif opcao == "5":
                id_musica = int(input("ID da música: "))
                resposta = stub.ListarPlaylistsPorMusica(spotify_pb2.MusicaRequest(musica_id=id_musica))
                for p in resposta.playlists:
                    print(f"ID: {p.id}, Nome: {p.nome}")

            elif opcao == "0":
                print("Encerrando cliente...")
                break

            else:
                print("Opção inválida!")

if __name__ == "__main__":
    menu()
