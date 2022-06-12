from flask import Flask, redirect, url_for
from mpd import MPDClient
import threading

app = Flask(__name__)

app.secret_key = 'piwo'

stopped = True
client = MPDClient()
client_lock = threading.Lock()
with client_lock:
   client.connect("localhost", 6600)
   client.update()

def reconnect():
    try:
        client.ping()
    except Exception:
        client.connect("localhost", 6600)
        client.update()

@app.route("/")
def homePage():
    reconnect()
    return '''
        <form action="/reload">
            <input type=submit value="previous" formaction="/previous">
            <input type=submit value="play" formaction="/play">
            <input type=submit value="next" formaction="/next">
            <input type=submit value="Volume Down" formaction="/volumedown">
            <input type=submit value="Volume Up" formaction="/volumeup">
        </form>   '''

#------- Current Song Actions ------#
@app.route("/reload")
def reload():
    return redirect(url_for("homePage"))

@app.route("/previous")
def previous():
    reconnect()
    client.previous()
    return redirect(url_for("homePage"))

@app.route("/next")
def next():
    reconnect()
    client.next()
    return redirect(url_for("homePage"))

@app.route("/play")
def playpause():
    global stopped
    if stopped == False:
        stopped = True
        reconnect()
        client.pause()
    elif stopped == True:
        stopped = False
        reconnect()
        client.play()
    return redirect(url_for("homePage"))

@app.route("/volumedown")
def volumedown():
    reconnect()
    volume = (int)(client.status()['volume'])
    if volume >= 10 :
        reconnect()
        client.setvol(volume - 10)
    return redirect(url_for("homePage"))

@app.route("/volumeup")
def volumeup():
    reconnect()
    volume = (int)(client.status()['volume'])
    if volume <= 90 :
        reconnect()
        client.setvol(volume + 10)
    return redirect(url_for("homePage"))


if __name__ == '__main__':
    app.run(debug=True, port=7777, host='0.0.0.0')