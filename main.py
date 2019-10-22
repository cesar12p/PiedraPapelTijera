import webapp2
#3 metodo
import os
import jinja2
import random
from google.appengine.ext import ndb
usuario =""
intent =0
intentUsu=0
intentPC=0
resp=""
password=""
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(
        os.path.dirname(__file__), "templates")),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)
class Objeto_Usuario(ndb.Model):
    usuario=ndb.StringProperty()
    password=ndb.StringProperty()
    ganadas=ndb.IntegerProperty()
    perdidas=ndb.IntegerProperty()
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
        global usuario 
        usuario=""
        global intent 
        intent=0
        global intentUsu
        intentUsu=0
        global intentPC
        intentPC=0
        global resp
        resp=""


    def post(self):
        global usuario
        usuario= self.request.get('user')
        global password
        password=self.request.get('contra')
        consulta = Objeto_Usuario.query(ndb.AND(Objeto_Usuario.usuario==usuario,Objeto_Usuario.password==password)).get()

        if consulta is None:
            obj=Objeto_Usuario()
            obj.usuario=usuario
            obj.password=password
            obj.ganadas=0
            obj.perdidas=0
            obj.put()
            self.render("Bienvenido.html", usuario=usuario)
        else:
            self.render("Bienvenido.html",usuario=usuario)
class JugarPage(Handler):
    def post(self):
        global usuario
        self.render("Juego.html", usuario=usuario)
class JugarPage2(Handler):
    def post(self):
        resp = self.request.get('respuesta')
        global intent
        global intentUsu
        global intentPC
        intent +=1
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
            intentPC +=1
        elif resp.lower() == "a" and PC == "c":
            resultado = "ganar"
            fondo = "success"
            tema = "success"
            resp = "piedra"
            PC = "tijeraPC"
            intentUsu +=1
        elif resp.lower() == "c" and PC == "a":
            resultado = "perder"
            fondo = "danger"
            tema = "danger"
            resp = "tijera"
            PC = "piedraPC"
            intentPC +=1
        elif (resp.lower() == "c" and PC == "b"):
            resultado = "ganar"
            fondo = "success"
            tema = "success"
            resp = "tijera"
            PC = "papelPC"
            intentUsu +=1
        elif (resp.lower() == "b" and PC == "a"):
            resultado = "ganar"
            fondo = "success"
            tema = "success"
            resp = "papel"
            PC = "piedraPC"
            intentUsu +=1
        elif (resp.lower() == "b" and PC == "c"):
            resultado = "perder"
            fondo = "danger"
            tema = "danger"
            resp = "papel"
            PC = "tijeraPC"
            intentPC +=1
        if (intentUsu==2 or intentPC==2):
            global usuario
            global password
            consulta = Objeto_Usuario.query(ndb.AND(Objeto_Usuario.usuario==usuario,Objeto_Usuario.password==password)).get()

            if intentUsu==2:
                copa="copa"
                if consulta is not None:
                    consulta.ganadas=consulta.ganadas+1
                    consulta.put()
            else:
                copa="copa2"
                if consulta is not None:
                    consulta.perdidas=consulta.perdidas+1
                    consulta.put()
            self.render("final.html", resp=resp, PC=PC,resultado=resultado, fondo=fondo, tema=tema,intent=intent,intentUsu=intentUsu, intentPC=intentPC, copa=copa)
        else:
            self.render("Juego2.html", resp=resp, PC=PC,resultado=resultado, fondo=fondo, tema=tema, intent=intent, intentUsu=intentUsu, intentPC=intentPC)
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/click_login', MainPage),
                               ('/click_jugar', JugarPage),
                               ('/click_jugar2', JugarPage2)
                               ], debug=True)
