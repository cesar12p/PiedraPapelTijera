import webapp2
#3 metodo
import os
import jinja2
import random

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), "templates")),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)
def render_str(template, **params):
    t = JINJA_ENVIRONMENT.get_template(template)
    return t.render(params)
class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
class MainPage(Handler):
    def get(self):
        self.render("index.html")

    def post(self):
        usuario = self.request.get('user')
        intent = self.request.get('intentos')
        intentUsu = self.request.get('intentoUsu')
        intentPC = self.request.get('intentoPC')
        self.render("Bienvenido.html", usuario=usuario,
                    intent=intent, intentUsu=intentUsu, intentPC=intentPC)
class JugarPage(Handler):
    def post(self):
        usuario = self.request.get('nombre')
        intent = self.request.get('intentos')
        intentUsu = self.request.get('intentoUsu')
        intentPC = self.request.get('intentoPC')
        self.render("Juego.html", usuario=usuario, intent=intent, intentUsu=intentUsu, intentPC=intentPC)
class JugarPage2(Handler):
    def post(self):
        usuario = self.request.get('nombre')
        resp = self.request.get('respuesta')
        intent = self.request.get('intentos')
        intentUsu = self.request.get('intentoUsu')
        intentPC = self.request.get('intentoPC')
        cont = int(intent)
        intent = cont+1
        PC = random.choice(["a", "b", "c"])
        if resp.lower() == PC:
            resultado = "empate"
            fondo = "dark"
            tema = "secondary"
            if PC == "a":
                resp = "piedra"
                PC = "piedraPC"
            elif PC == "b":
                resp = "papel"
                PC = "papelPC"
            else:
                resp = "tijera"
                PC = "tijeraPC"

        elif resp.lower() == "a" and PC == "b":
            resultado = "perder"
            fondo = "danger"
            tema = "danger"
            resp = "piedra"
            PC = "papelPC"
            cont2= int(intentPC)
            intentPC=cont2+1
        elif resp.lower() == "a" and PC == "c":
            resultado = "ganar"
            fondo = "success"
            tema = "success"
            resp = "piedra"
            PC = "tijeraPC"
            cont1= int(intentUsu)
            intentUsu=cont1+1
        elif resp.lower() == "c" and PC == "a":
            resultado = "perder"
            fondo = "danger"
            tema = "danger"
            resp = "tijera"
            PC = "piedraPC"
            cont2= int(intentPC)
            intentPC=cont2+1
        elif (resp.lower() == "c" and PC == "b"):
            resultado = "ganar"
            fondo = "success"
            tema = "success"
            resp = "tijera"
            PC = "papelPC"
            cont1= int(intentUsu)
            intentUsu=cont1+1
        elif (resp.lower() == "b" and PC == "a"):
            resultado = "ganar"
            fondo = "success"
            tema = "success"
            resp = "papel"
            PC = "piedraPC"
            cont1= int(intentUsu)
            intentUsu=cont1+1
        elif (resp.lower() == "b" and PC == "c"):
            resultado = "perder"
            fondo = "danger"
            tema = "danger"
            resp = "papel"
            PC = "tijeraPC"
            cont2= int(intentPC)
            intentPC=cont2+1
        if (intentUsu==2 or intentPC==2):
            if intentUsu==2:
                copa="copa"
            else:
                copa="copa2"
            self.render("final.html",usuario=usuario, resp=resp, PC=PC,resultado=resultado, fondo=fondo, tema=tema,intent=intent,intentUsu=intentUsu, intentPC=intentPC, copa=copa)
        else:
            self.render("Juego2.html", usuario=usuario, resp=resp, PC=PC,resultado=resultado, fondo=fondo, tema=tema, intent=intent, intentUsu=intentUsu, intentPC=intentPC)
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/click_login', MainPage),
                               ('/click_jugar', JugarPage),
                               ('/click_jugar2', JugarPage2)
                               ], debug=True)
