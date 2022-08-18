import http
from http.server import HTTPServer, BaseHTTPRequestHandler
from lib2to3.pytree import Base
import time
import RPi.GPIO as GPIO


HOST = "192.168.1.30"
PORT = 9999

magState = "Off"

def setupGPIO():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)

  GPIO.setup(18, GPIO.OUT)


def setState(s):
  global magState 
  magState = s


class NeuralHTTP(BaseHTTPRequestHandler):


  def do_GET(self):
    html = '''
      <!DOCTYPE html>
      <html lang="en">
      <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
      <style>
        html {{
          background-color: aqua;
          }}
      </style>
      </head>
      <body>
        <h1>
          Magnet Controler
        </h1>
        <form action="/" method="POST">
          Magnet state = {} <br>
          <input type="submit" name="submit" value="On">
          <input type="submit" name="submit" value="Off">
        </form>
        </body>
        </html>
    '''
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    
    self.wfile.write(bytes(html.format(magState), "utf-8"))

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length).decode("utf-8")
    print(post_data)
    post_data = post_data.split("=")[1]

    setupGPIO()

    if post_data == "On":
      setState("On")
      GPIO.output(18, GPIO.HIGH)
    else:
      setState("Off")
      GPIO.output(18, GPIO.LOW)
    
    self._redirect('/')

  def _redirect(self, path):
    self.send_response(303)
    self.send_header('Content-type', 'text/html')
    self.send_header('Location', path)
    self.end_headers()




    




if __name__ == '__main__':
    http_server = HTTPServer((HOST, PORT), NeuralHTTP)
    print("Server Starts - %s:%s" % (HOST, PORT))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()