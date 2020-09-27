import socket
from flask import Flask, render_template, request, redirect, url_for


def con():
      global sock
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_address = ('localhost', 9991)
      print('connecting to {} port {}'.format(*server_address))
      sock.connect(server_address)


def send(item):
      message = bytes(item, 'utf-8')
      sock.send(message)
      exists = recieve()
      return exists


def recieve():
      while True:
            data = sock.recv(1024)
            return str(data, 'utf-8')


def close():
      sock.send(bytes("exit", 'utf-8'))
      sock.close()


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def grocery():
      try:
            close()
      except:
            pass
      con()
      if request.method == 'POST':
            grocery_item = request.form['grocery_item']
            response = send(grocery_item)
            if response == "true":
                  return redirect('/quantity')
            else:
                  return render_template("grocery.html", message="OOPS..Item not found.")
      else:
            return render_template("grocery.html")


@app.route('/quantity', methods=['POST', 'GET'])
def amount():
      if request.method == 'POST':
            quantity_item = request.form['quantity_item']
            response = send(quantity_item)
            if(response=='true'):
                  return redirect('/want')
            else:
                  return render_template("quantity.html", message="Not entered")
      else:
            return render_template("quantity.html")


@app.route('/want', methods=['POST', 'GET'])
def nextitem():
      if request.method == 'POST':
            answer = request.form['answer']
            response = send(answer)
            if response == "true":
                  return redirect('/')
            else:
                  close()
                  f = open("prices.txt", 'r')
                  line = f.readlines()
                  amount = 0
                  for word in line:
                        amount = amount + int(word)
                  return render_template("thank.html", message="Your Total Purchase Amount:" + str(amount))

      else:

            return render_template("more.html")


if __name__ == "__main__":
      app.run(debug=True)
