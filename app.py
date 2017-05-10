import os
import logging
import json
import random
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.web import url
import tornado.escape
import tornado.options
from tornado.options import define, options

import db


define("username", default="user")
define("password", default="pass")

class MainHandler(tornado.web.RequestHandler):
    print("Hi2")
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        #self.write("Hello, <b>" + self.get_current_user() + "</b> <br> <a href=/auth/logout>Logout</a>")
        print("Hi")
        print(self.get_current_user())
        self.redirect('/chat')


class ChatHandler(tornado.websocket.WebSocketHandler):

    waiters = set()
    messages = []
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        face_pics = ['cat.gif', 'fere.gif', 'lion.gif']
        img_name = random.choice(face_pics)
        self.render('index.html', img_path=self.static_url('images/' + img_name))

    def open(self, *args, **kwargs):
        self.waiters.add(self)
        self.write_message({'messages': self.messages})

    def on_message(self, message):
        message = json.loads(message)
        self.messages.append(message)
        for waiter in self.waiters:
            if waiter == self:
                continue
            waiter.write_message({'img_path': message['img_path'], 'message': message['message']})

    def on_close(self):
        self.waiters.remove(self)



class BaseHandler(tornado.web.RequestHandler):
    print("BaseHandler")
    cookie_username = "username"

    def get_current_user(self):
        username = self.get_cookie(self.cookie_username)
        logging.debug('BaseHandler - username: %s' % username)
        if not username: return None
        return tornado.escape.utf8(username)

    def set_current_user(self, username):
        print("set_current_user")
        self.set_cookie(self.cookie_username, tornado.escape.utf8(username))

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)


class AuthLoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        # logging.debug("xsrf_cookie:" + self.get_argument("_xsrf", None))

        # self.check_xsrf_cookie()

        username = self.get_argument("username")
        password = self.get_argument("password")

        logging.debug('AuthLoginHandler:post %s %s' % (username, password))
        user_id = db.get_user_id(username,password)
        if user_id!=None:
            print(username)
            self.set_current_user(user_id)
            print(username)
            self.redirect('/')
        else:
            self.render("login_error.html")


class AuthLogoutHandler(BaseHandler):

    def get(self):
        #self.clear_current_user()
        self.redirect('/chat')


class Application(tornado.web.Application):

    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        handlers = [
        	url(r'/', MainHandler, name='index'),
            url(r'/chat', ChatHandler, name='chat'),
            url(r'/auth/login', AuthLoginHandler),
            url(r'/auth/logout', AuthLogoutHandler),
        ]
        setting = dict(
        	template_path = os.path.join(BASE_DIR, 'templates'),
            static_path = os.path.join(BASE_DIR, 'static'),
            login_url = "/auth/login",
            xsrf_cookies = False,
            # cookie_secret='gaofjawpoer940r34823842398429afadfi4iias',
            autoescape="xhtml_escape",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **setting)

if __name__ == '__main__':
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8008)
    tornado.ioloop.IOLoop.instance().start()