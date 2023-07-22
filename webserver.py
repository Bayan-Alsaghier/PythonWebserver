import cgi
import webbrowser
import threading
from datetime import datetime, date
from tkinter.ttk import Label
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
try:
    import tkinter.scrolledtext as tkscrolledtext
except ImportError:
    import ScrolledText as tkscrolledtext
try:
    import tkinter.filedialog as tkfiledialog
except ImportError:
    import tkFileDialog as tkfiledialog
try:
    import http.server as httpserver
except ImportError:
    import SimpleHTTPServer as httpserver
try:
    import socketserver as socketserver
except ImportError:
    import SocketServer as socketserver
try:
    import _thread as thread
except ImportError:
    import thread as thread

adding_list = []
"""
This class is developed to communicate with the HTTP request handler. The class contains GET, and POST methods 
and two methods that manage the threading messages to demonstrate the communication stream between server and client 
"""
class MyTCPClientHandler(httpserver.SimpleHTTPRequestHandler):
    """
    get_print_confimation_message(self) a method that prints a threading messages
     to illustrate request streaming when the client call the GET method
    """
    def get_print_confimation_message(self):
        print("Send one request to {}".format(self.client_address[0]))
        print("GET HTTP/1.1")
        print("Thread Name:{}".format(threading.current_thread().name))
        m1 = "Receive one request from {}\n".format(self.client_address[0])
        m2 = "GET HTTP/1.1\n"
        m3 = "Thread Name:{}\n".format(threading.current_thread().name)
        info_message = m1 + m2 + m3
        root = tk.Tk()
        root.geometry('300x100')
        root.title('Connection State')
        label = Label(root, text=info_message)
        label.pack(ipadx=10, ipady=10)
        root.mainloop()
    """
    post_print_confimation_message(self) a method that prints a threading messages
     to illustrate request streaming when the client make a POST request.
    """
    def post_print_confimation_message(self):
        print("Send one request from {}".format(self.client_address[0]))
        print("POST HTTP/1.1")
        print("Thread Name:{}".format(threading.current_thread().name))

    def do_GET(self):
        if self.path.endswith('/home'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            home_page = '<html><body> ' \
                        '<h1> This is a test of GET method using HTTP protocol </h1>' \
                        '<h2> Please go to link : <a href ="home/testpost"> Click Here </a> to test POST method '
            for action in adding_list:
                home_page += action
                home_page += '<br>'
            home_page += '</body></html>'
            self.wfile.write(home_page.encode())
            self.get_print_confimation_message()

        if self.path.endswith('/testpost'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            new_page = '<html><body> ' \
                       '<h1> Test post method using form below</h1>' \
                       '<form method ="POST" enctype = "multipart/form-data" action ="/home/formresult"> ' \
                       '<input name = "add" type = "text" placeholder = "Enter text here">' \
                       '<input type="submit" value="Add">' \
                       '</form>' \
                       '</body></html>'
            self.wfile.write(new_page.encode())
            self.get_print_confimation_message()

        if self.path.endswith('/formresult'):
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            form_result = '<html><body> ' \
                          '<h1> Your POST form result </h1> <br>'
            for action in adding_list:
                form_result += action
                form_result += '<br>'
            form_result += '</body></html>'
            self.wfile.write(form_result.encode())
            self.get_print_confimation_message()

    def do_POST(self):
        self.post_print_confimation_message()
        if self.path.endswith('/formresult'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_submit = fields.get('add')
                adding_list.append(new_submit[0])
            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/formresult')
            self.end_headers()


class Application(tk.Frame):
    def start_server(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()
        d2 = today.strftime("%B%d,%Y")
        thread.start_new_thread(st_server, ())
        self.start.config(state='disabled')
        self.text.insert('end', "Server running on PORT: {}\n127.0.0.1 on [{} {}]".format(PORT, d2, current_time))

    def go_home(self):
        webbrowser.open_new_tab("http://localhost:8000/home")

    def go_post(self):
        webbrowser.open_new_tab("http://localhost:8000/home/testpost")

    def createWidgets(self):
        """create GUI Tkinter"""
        # start server
        self.start = tk.Button(self)
        self.start["text"] = "Start server"
        self.start["fg"] = "green"
        self.start["command"] = self.start_server
        self.start.pack({"side": "top", "fill": "x"})

        # GET method
        self.g = tk.Button(self)
        self.g["text"] = "GET method"
        self.g["fg"] = "orange"
        self.g["command"] = self.go_home
        self.g.pack({"side": "top", "fill": "x"})

        # POST method
        self.post = tk.Button(self)
        self.post["text"] = "POST method"
        self.post["fg"] = "blue"
        self.post["command"] = self.go_post
        self.post.pack({"side": "top", "fill": "x"})

        # exit
        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "End"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.pack({"side": "top", "fill": "x"})

        # Information
        self.lab = tk.Label(self, text="Informationen")
        self.lab.pack({"side": "top"})

        self.text = tkscrolledtext.ScrolledText(self)
        self.text["width"] = 40
        self.text["height"] = 5
        self.text.pack({"side": "left"})

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack(expand='yes')
        self.createWidgets()


def main():
    root = tk.Tk()
    root.title("HTTP Server")
    app = Application(master=root)
    app.mainloop()


PORT = 8000
ServerAddress = ("192.168.56.1", PORT)
TCPServerInstance = socketserver.ThreadingTCPServer(ServerAddress, MyTCPClientHandler)


def st_server():
    """Start server"""
    while True:
        TCPServerInstance.handle_request()


if __name__ == '__main__':
    main()
