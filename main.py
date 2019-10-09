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
            resultado = "/static/img/empate.png"
            fondo = "alert-dark"
            tema = "bg-secondary"
            if PC == "a":
                resp = "/static/img/piedra.png"
                PC = "/static/img/piedraPC.png"
            elif PC == "b":
                resp = "/static/img/papel.png"
                PC = "/static/img/papelPC.png"
            else:
                resp = "/static/img/tijera.png"
                PC = "/static/img/tijeraPC.png"

        elif resp.lower() == "a" and PC == "b":
            resultado = "/static/img/perder.png"
            fondo = "alert-danger"
            tema = "bg-danger"
            resp = "/static/img/piedra.png"
            PC = "/static/img/papelPC.png"
            cont2= int(intentPC)
            intentPC=cont2+1
        elif resp.lower() == "a" and PC == "c":
            resultado = "/static/img/ganar.png"
            fondo = "alert-success"
            tema = "bg-success"
            resp = "/static/img/piedra.png"
            PC = "/static/img/tijeraPC.png"
            cont1= int(intentUsu)
            intentUsu=cont1+1
        elif resp.lower() == "c" and PC == "a":
            resultado = "/static/img/perder.png"
            fondo = "alert-danger"
            tema = "bg-danger"
            resp = "/static/img/tijera.png"
            PC = "/static/img/piedraPC.png"
            cont2= int(intentPC)
            intentPC=cont2+1
        elif (resp.lower() == "c" and PC == "b"):
            resultado = "/static/img/ganar.png"
            fondo = "alert-success"
            tema = "bg-success"
            resp = "/static/img/tijera.png"
            PC = "/static/img/papelPC.png"
            cont1= int(intentUsu)
            intentUsu=cont1+1
        elif (resp.lower() == "b" and PC == "a"):
            resultado = "/static/img/ganar.png"
            fondo = "alert-success"
            tema = "bg-success"
            resp = "/static/img/papel.png"
            PC = "/static/img/piedraPC.png"
            cont1= int(intentUsu)
            intentUsu=cont1+1
        elif (resp.lower() == "b" and PC == "c"):
            resultado = "/static/img/perder.png"
            fondo = "alert-danger"
            tema = "bg-danger"
            resp = "/static/img/papel.png"
            PC = "/static/img/tijeraPC.png"
            cont2= int(intentPC)
            intentPC=cont2+1
        
        if (intentUsu==2 or intentPC==2):
            self.render("final.html",usuario=usuario, resp=resp, PC=PC,resultado=resultado, fondo=fondo, tema=tema,intent=intent,intentUsu=intentUsu, intentPC=intentPC)
        else:
            self.render("Juego2.html", usuario=usuario, resp=resp, PC=PC,resultado=resultado, fondo=fondo, tema=tema, intent=intent, intentUsu=intentUsu, intentPC=intentPC)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/click_login', MainPage),
                               ('/click_jugar', JugarPage),
                               ('/click_jugar2', JugarPage2)
                               ], debug=True)
