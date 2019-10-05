import webapp2
#3 metodo
import os
import jinja2
import random

JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
extensions=["jinja2.ext.autoescape"],
autoescape=True
)

def render_str(template,**params):
    t = JINJA_ENVIRONMENT.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    def render(self,template, **kw):
        self.response.out.write(render_str(template,**kw))

    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

class MainPage(Handler):
    def get(self):
        self.render("index.html")

    def post(self):
        usuario=self.request.get('user')
        self.render("Bienvenido.html", usuario = usuario)

class JugarPage(Handler):
    def post(self):
        usuario=self.request.get('nombre')
        self.render("Juego.html" ,usuario = usuario)

class JugarPage2(Handler):
    def post(self):
        usuario=self.request.get('nombre')
        resp=self.request.get('respuesta')
        PC=random.choice(["a","b","c"])
        if resp.lower() == PC:
            resultado="Empate"
        elif resp.lower() == "a" and PC == "b":
            resultado="Has Perdio"
        elif resp.lower() ==  "a" and PC == "c":
            resultado="Has Ganado"
        elif resp.lower() == "c" and PC == "a":
            resultado="Has Perdido"
        elif (resp.lower() == "c" and PC == "b" ):
            resultado="Has Ganado"
        elif (resp.lower() == "b" and PC == "a"):
            resultado="Has Ganado"
        elif (resp.lower() == "b" and PC == "c"):
            resultado="Has Perdido"
        else:
            resultado="Caracter Invalido"

        self.render("Juego2.html" ,usuario = usuario, resp = resp, PC=PC, resultado=resultado)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/click_login',MainPage),
                               ('/click_jugar',JugarPage),
                               ('/click_jugar2',JugarPage2)
], debug=True)