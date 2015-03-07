#!/usr/bin/python

import webapp
import urllib
import socket


class contentApp (webapp.webApp):

    urls_cortas = {}
    cortas_urls = {}
    urlcorta = -1

    def parse(self, request):
        metodo = request.split(' ', 2)[0]
        recurso = request.split(' ', 2)[1]
        if metodo == "POST":
            cuerpo = request.split('\r\n\r\n', 1)[1].split('=')[1]
            cuerpo = cuerpo.replace('+', ' ')
        else:
            cuerpo = ""
        return (metodo, recurso, cuerpo)

    def process(self, resourceName):
        metodo, recurso, cuerpo = resourceName
        formulario = ('<form action="" method="POST">Solicita tu URL corta:'
                    + '<input type="text" name="nombre" value="" /><br/>'
                    + '<input type="submit" value="Enviar" /></form>')
        if metodo == "POST":
            if cuerpo == "":
                httpCode = "404 Not Found"
                htmlBody = ("<html><body>No se introdujo URL" +
                            "</body></html>")
                return (httpCode, htmlBody)
            elif cuerpo.find("http") == -1:
                cuerpo = "http://" + cuerpo
            else:
                cuerpo = (cuerpo.split("%3A%2F%2F")[0] + "://" +
                          cuerpo.split("%3A%2F%2F")[1])
            if cuerpo in self.urls_cortas:
                urlcorta = self.urls_cortas[cuerpo]
            else:
                self.urlcorta = self.urlcorta + 1
                urlcorta = self.urlcorta
                self.urls_cortas[cuerpo] = urlcorta
                self.cortas_urls[urlcorta] = cuerpo

            httpCode = "200 OK"
            htmlBody = ("<html><body>" +
                        "<h1>URL original y acortada:</h1>" +
                        "<a href=" + cuerpo + ">" + cuerpo + "</href></br>" +
                        "<a href=" + str(urlcorta) + ">" +
                        str(urlcorta) + "</href></body></html>")
        elif metodo == "GET":
            if recurso == '/':
                httpCode = "200 OK"
                htmlBody = ("<html><body>" + str(self.urls_cortas) +
                            formulario + "</body></html>")
            else:
                urlcorta = int(recurso.split('/')[1])
                if urlcorta in self.cortas_urls:
                    httpCode = ("301 Moved Permanently\nLocation: " +
                                self.cortas_urls[urlcorta])
                    htmlBody = "<html><body>Redirigiendo...</body></html>"
                else:
                    httpCode = "404 Not Found"
                    htmlBody = ("<html><body>Not Found"
                        + formulario + "</body></html>")
        else:
            httpCode = "404 Not Found"
            htmlBody = "<html><body>Metodo no entendido</body></html>"

        return (httpCode, htmlBody)

if __name__ == "__main__":
    try:
        testWebApp = contentApp(socket.gethostname(), 1234)
    except KeyboardInterrupt:
        print "\n\nFinalizando servidor...\n\n"
