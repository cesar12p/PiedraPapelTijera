import webapp2
#3 metodo
import os
import jinja2
import random
import logging
from google.appengine.ext import ndb
from webapp2_extras import sessions
intent = 0
userg=""
intentUsu = 0
intentPC = 0
resp = ""
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
template_values={}
class Objeto_Usuario(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    ganadas = ndb.IntegerProperty()
    perdidas = ndb.IntegerProperty()


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def render(self, template, **kw):
		self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)



class MainPage(Handler):
    def get(self):
        fondo="bg-info"
        msg=""
        self.render("index.html",fondo=fondo, error=msg)
        global intent
        intent = 0
        global intentUsu
        intentUsu = 0
        global intentPC
        intentPC = 0
        global resp
        resp = ""

    def post(self):
        global template_values
        user = self.request.get('user')
        pw = self.request.get('contra')
        logging.info('Checking user='+ str(user) + 'pw='+ str(pw))
        msg = ''
        fondo="bg-warning"
        if pw == '' or user == '':
            msg = "Error Ingresa tu usuario y password"
            self.render("index.html", error=msg ,fondo=fondo)
        else:
            consulta=Objeto_Usuario.query(ndb.AND(Objeto_Usuario.username==user, Objeto_Usuario.password==pw )).get()
            if consulta is not None:
                logging.info('POST consulta=' + str(consulta))
                #Vinculo el usuario obtenido de mi datastore con mi sesion.
                self.session['user'] = consulta.username
                logging.info("%s just logged in" % user)
                global userg
                userg=user
                template_values={
                    'user':self.session['user']
                }
                self.render("Bienvenido.html", user=template_values)
            else:
                logging.info('POST consulta=' + str(consulta))
                fondo="bg-danger"
                msg = 'El usuario o el password son Incorectos  Intenta de nuevo'
                self.render("index.html", error=msg, fondo=fondo)

class JugarPage(Handler):
    def post(self):
        global template_values
        self.render("Juego.html",user=template_values)

class Registrar(Handler):
    def get(self):
        fondo="bg-dark"
        self.render("Registro.html",fondo=fondo)

    def post(self):
        user = self.request.get('user')
        pw = self.request.get('contra')
        cuenta = Objeto_Usuario(username=user, password = pw, ganadas=0, perdidas=0)
        cuentakey = cuenta.put()
        cuenta_user=cuentakey.get()
        if cuenta_user == cuenta:
            msj = "Fuiste registrado con exito"
            fondo="bg-success"
            self.render("Registro.html",fondo=fondo, msj=msj)
class Salir(Handler):
    def get(self):
        if self.session.get('user'):
            logging.info("%s bye")
            msg ="Cerraste sesion"
            fondo="bg-secondary"
            self.render("index.html", error=msg ,fondo=fondo)
            del self.session['user']

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}


class JugarPage2(Handler):
    def post(self):
        global template_values
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
            consulta = Objeto_Usuario.query(Objeto_Usuario.username==userg).get()
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
            self.render("final.html", resp=resp, PC=PC,resultado=resultado, fondo=fondo, tema=tema,intent=intent,intentUsu=intentUsu, intentPC=intentPC, copa=copa,user=template_values)
        else:
            self.render("Juego2.html", resp=resp, PC=PC,resultado=resultado, fondo=fondo, tema=tema, intent=intent, intentUsu=intentUsu, intentPC=intentPC,user=template_values)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/click_login', MainPage),
                               ('/click_jugar', JugarPage),
                               ('/click_jugar2', JugarPage2),
                               ('/registrame',Registrar),
                               ('/salir',Salir)
                               ], debug=True, config=config)
