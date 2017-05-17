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

global to_user
global group_flag

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/auth/login', AuthLoginHandler),
            (r'/auth/logout', AuthLogoutHandler),
            (r'/chat/*', ChatHandler),
            (r'/chats*',MainHandler),
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
        return tornado.escape.utf8(username).decode('utf-8')

    def set_current_user(self, username):
        self.set_secure_cookie(self.cookie_username, tornado.escape.utf8(username))

    def clear_current_user(self):
        self.clear_cookie(self.cookie_username)


class MainHandler(BaseHandler):

    
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        global group_flag
        face_pics = ['cat.gif', 'fere.gif', 'lion.gif']
        img_name = random.choice(face_pics)
        global to_user
        try:
            print(self.get_argument("request_user"))
            #self.write("request message is "+self.get_argument("request_user"))
            to_user=self.get_argument("request_user")
            group_flag = False
        except:
            try:
                to_user=self.get_argument("request_group")
                group_flag = True
            except:
                to_user = 'bot'
                group_flag = False
        self.render('index.html', img_path=self.static_url('images/' + img_name),user_name=str(self.get_current_user()),user_list=db.get_user_list(),group_list=db.get_group_list())


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
    waiters = []
    messages = []
    
    def open(self, *args, **kwargs):#初期メッセージ送信
        global to_user
        global group_flag

        print("open")
        print(self)
        self.waiters.append([self,db.get_user_id_from_name(self.get_current_user())])
        self.messages=[]

        if(group_flag == False):

            for message in db.get_message(db.get_user_id_from_name(to_user),db.get_user_id_from_name(self.get_current_user())):
                #print(message)
                self.messages.append({'img_path': '/static/images/lion.gif', 'message': message[4] , 'to_user': db.get_user_name(message[1]) , 'from_user':db.get_user_name(message[2]) , 'my_name':self.get_current_user(), 'is_group':'False'})
            self.write_message({'messages': self.messages})
        else:
            for message in db.get_group_message(db.get_group_id_from_name(to_user)):
                #print(message)
                self.messages.append({'img_path': '/static/images/lion.gif', 'message': message[4] , 'to_user':db.get_group_name(message[1]) ,'from_user': db.get_user_name(message[2]), 'my_name':self.get_current_user() , 'is_group':'True'})
            self.write_message({'messages': self.messages})


    def on_message(self, message):#メーッセージ受信およびブロードキャスト
        global to_user
        global group_flag

        message = json.loads(message)
        print("on_message")
        print(message)
        print(self.get_current_user())
        if(group_flag==False):
            db.insert_message(db.get_user_id_from_name(message["to_user"]), db.get_user_id_from_name(self.get_current_user()), db.get_now_time(),message['message'], 0)
            #self.messages.append(message)
        else:
            db.insert_message(db.get_group_id_from_name(message["to_user"]), db.get_user_id_from_name(self.get_current_user()), db.get_now_time(),message['message'], 0)

        print(to_user)
        print(group_flag)
        print(self.waiters)
        for waiter in self.waiters:
            print(waiter)
            # if waiter[0] == self:
            #     continue
            # waiter[0].write_message({'img_path': message['img_path'], 'message': message['message'] , 'to_user': to_user ,'from_user':self.get_current_user() , 'my_name':self.get_current_user()})
            # print("Sended:"+waiter[1])
            if waiter[0] == self:
               continue
            if group_flag == False:
                print(db.get_user_id_from_name(to_user))
                if waiter[1] != db.get_user_id_from_name(message["to_user"]):
                    continue
                waiter[0].write_message({'img_path': message['img_path'], 'message': message['message'] , 'to_user': message["to_user"] ,'from_user':self.get_current_user() , 'my_name':self.get_current_user() , 'is_group':False})
            else:
                group_user_list = db.get_group_user_list(db.get_group_id_from_name(message["to_user"]))
                for number in group_user_list:
                    if waiter[1] == number:
                        waiter[0].write_message({'img_path': message['img_path'], 'message': message['message'] , 'to_user': message["to_user"] ,'from_user': self.get_current_user(), 'my_name':db.get_user_name(number) , 'is_group':'True'})
            
            print("send:"+waiter[1]+'\nmessage:'+message['message'])
            
    def on_close(self):
        self.waiters.remove([self,db.get_user_id_from_name(self.get_current_user())])


def main():
    tornado.options.parse_config_file(os.path.join(os.path.dirname(__file__), 'server.conf'))
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    logging.debug('run on port %d in %s mode' % (options.port, options.logging))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
