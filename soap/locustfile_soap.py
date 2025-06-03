from locust import HttpUser, task, between

SOAP_HEADERS = {
    "Content-Type": "text/xml; charset=utf-8",
    "SOAPAction": ""
}

class SOAPUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    @task(1)
    def listar_usuarios(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:spy="spyne.streaming.soap">
           <soapenv:Header/>
           <soapenv:Body>
              <spy:listar_usuarios/>
           </soapenv:Body>
        </soapenv:Envelope>"""
        self.client.post("/soap", data=xml, headers=SOAP_HEADERS, name="listar_usuarios")

    @task(1)
    def listar_musicas(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:spy="spyne.streaming.soap">
           <soapenv:Header/>
           <soapenv:Body>
              <spy:listar_musicas/>
           </soapenv:Body>
        </soapenv:Envelope>"""
        self.client.post("/soap", data=xml, headers=SOAP_HEADERS, name="listar_musicas")

    @task(1)
    def listar_playlists_usuario(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:spy="spyne.streaming.soap">
           <soapenv:Header/>
           <soapenv:Body>
              <spy:listar_playlists_usuario>
                 <spy:usuario_id>1</spy:usuario_id>
              </spy:listar_playlists_usuario>
           </soapenv:Body>
        </soapenv:Envelope>"""
        self.client.post("/soap", data=xml, headers=SOAP_HEADERS, name="listar_playlists_usuario")

    @task(1)
    def listar_musicas_playlist(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:spy="spyne.streaming.soap">
           <soapenv:Header/>
           <soapenv:Body>
              <spy:listar_musicas_playlist>
                 <spy:playlist_id>1</spy:playlist_id>
              </spy:listar_musicas_playlist>
           </soapenv:Body>
        </soapenv:Envelope>"""
        self.client.post("/soap", data=xml, headers=SOAP_HEADERS, name="listar_musicas_playlist")

    @task(1)
    def listar_playlists_musica(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:spy="spyne.streaming.soap">
           <soapenv:Header/>
           <soapenv:Body>
              <spy:listar_playlists_musica>
                 <spy:musica_id>1</spy:musica_id>
              </spy:listar_playlists_musica>
           </soapenv:Body>
        </soapenv:Envelope>"""
        self.client.post("/soap", data=xml, headers=SOAP_HEADERS, name="listar_playlists_musica")
