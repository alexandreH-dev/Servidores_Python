# pip install zeep
from zeep import Client

# URL do WSDL do servidor
wsdl = "http://localhost:8000/soap?wsdl"
client = Client(wsdl=wsdl)

def menu():
    while True:
        print("\n--- CLIENTE SOAP - STREAMING DE MÚSICAS ---")
        print("1 - Listar todos os usuários")
        print("2 - Listar todas as músicas")
        print("3 - Listar playlists de um usuário")
        print("4 - Listar músicas de uma playlist")
        print("5 - Listar playlists que contêm uma música")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            usuarios = client.service.listar_usuarios()
            print("\nUsuários:")
            for u in usuarios:
                print(u)

        elif opcao == "2":
            musicas = client.service.listar_musicas()
            print("\nMúsicas:")
            for m in musicas:
                print(m)

        elif opcao == "3":
            id_usuario = int(input("Digite o ID do usuário: "))
            playlists = client.service.listar_playlists_usuario(id_usuario)
            print(f"\nPlaylists do usuário {id_usuario}:")
            for p in playlists:
                print(p)

        elif opcao == "4":
            id_playlist = int(input("Digite o ID da playlist: "))
            musicas = client.service.listar_musicas_playlist(id_playlist)
            print(f"\nMúsicas da playlist {id_playlist}:")
            for m in musicas:
                print(m)

        elif opcao == "5":
            id_musica = int(input("Digite o ID da música: "))
            playlists = client.service.listar_playlists_musica(id_musica)
            print(f"\nPlaylists que contêm a música {id_musica}:")
            for p in playlists:
                print(p)

        elif opcao == "0":
            print("Encerrando cliente.")
            break

        else:
            print("Opção inválida.")

# Executar o menu
menu()
