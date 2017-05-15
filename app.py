# -*- coding: utf-8 -*-

'''
    User: ogata
    Date: 5/31/12
    Time: 2:10 PM
'''
__author__ = 'ogata'
import json
import random
import tornado.ioloop
import tornado.web
import tornado.escape
import tornado.options
from tornado.options import define, options
import tornado.websocket
from tornado.web import url
import os
import logging
import db

define("port", default=5000, type=int)
define("username", default="user")
define("password", default="pass")



class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/auth/login', AuthLoginHandler),
            (r'/auth/logout', AuthLogoutHandler),
            (r'/chat/*', ChatHandler),
        ]
        settings = dict(
            cookie_secret='gaofjawpoer940r34823842398429afadfi4iias',
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            login_url="/auth/login",
            xsrf_cookies=True,
            autoescape="xhtml_escape",
            debug=True,
            )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.websocket.WebSocketHandler):
    #tornado.web.RequestHandler,
    cookie_username = "username"

    def get_current_user(self):
        username = self.get_secure_cookie(self.cookie_username)
        logging.debug('BaseHandler - username: %s' % username)
        if not username: return None
        return tornado.escape.utf8(username)

    def set_current_user(self, username):
        self.set_secure_cookie(self.cookie_username, tornado.escape.utf8(username))

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        #self.write("Hello, <b>" + str(self.get_current_user()) + "</b> <br> <a href=/auth/logout>Logout</a>")
        face_pics = ['cat.gif', 'fere.gif', 'lion.gif']
        img_name = random.choice(face_pics)
        self.render('index.html', img_path=self.static_url('images/' + img_name),user_name=self.get_current_user(),user_list=db.get_user_list(),group_list=db.get_group_list())


class AuthLoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        logging.debug("xsrf_cookie:" + self.get_argument("_xsrf", None))

        self.check_xsrf_cookie()

        username = self.get_argument("username")
        password = self.get_argument("password")

        logging.debug('AuthLoginHandler:post %s %s' % (username, password))
        user_id = db.get_user_id(username,password)
        if user_id!=None:
            self.set_current_user(username)
            self.redirect('/')
        else:
            self.render("login_error.html")


class AuthLogoutHandler(BaseHandler):

    def get(self):
        self.clear_current_user()
        self.redirect('/')


class ChatHandler(BaseHandler):
    waiters = set()
    messages = []
    user_list = []
    def get(self, *args, **kwargs):
        face_pics = ['cat.gif', 'fere.gif', 'lion.gif']
        img_name = random.choice(face_pics)
        print(self.get_argument("request_user"))
        self.write("request message is "+self.get_argument("request_user"))
        self.render('index.html', img_path=self.static_url('images/' + img_name),user_name=str(self.get_current_user()),user_list=db.get_user_list(),group_list=db.get_group_list())


    def open(self, *args, **kwargs):
        print("open")
        print(self)
        self.user_list.append([self.get_current_user(),self])

        self.waiters.add(self)
        self.write_message({'messages': self.messages})
        print(self.user_list)

    def on_message(self, message):
        message = json.loads(message)
        print("on_message")
        print(message)
        self.messages.append(message)

        for waiter in self.waiters:
            if waiter == self:
                None
            #    continue
            waiter.write_message({'img_path': message['img_path'], 'message': message['message']})
            #db.insert_massage(get_current_user(),massage['message'])

    def on_close(self):
        self.waiters.remove(self)


def main():
    tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__), 'server.conf'))
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.debug('run on port %d in %s mode' % (options.port, options.logging))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
