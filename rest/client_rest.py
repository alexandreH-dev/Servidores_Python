import requests

BASE = "http://localhost:5000"

def menu():
    while True:
        print("\n--- CLIENTE REST - STREAMING DE MÚSICAS ---")
        print("1 - Listar todos os usuários")
        print("2 - Listar todas as músicas")
        print("3 - Listar playlists de um usuário")
        print("4 - Listar músicas de uma playlist")
        print("5 - Listar playlists que contêm uma música")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            r = requests.get(f"{BASE}/usuarios")
            print(r.json())

        elif opcao == "2":
            r = requests.get(f"{BASE}/musicas")
            print(r.json())

        elif opcao == "3":
            id_usuario = input("ID do usuário: ")
            r = requests.get(f"{BASE}/playlists/usuario/{id_usuario}")
            print(r.json())

        elif opcao == "4":
            id_playlist = input("ID da playlist: ")
            r = requests.get(f"{BASE}/musicas/playlist/{id_playlist}")
            print(r.json())

        elif opcao == "5":
            id_musica = input("ID da música: ")
            r = requests.get(f"{BASE}/playlists/musica/{id_musica}")
            print(r.json())

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")

menu()
