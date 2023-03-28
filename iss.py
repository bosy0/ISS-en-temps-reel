import requests 
import turtle
from time import strftime, sleep
from requests.exceptions import ConnectionError
import os


courant = os.path.dirname(__file__)


def personnes():
    
    # pour vérifier la connexion internet
    test_connexion()
    
    url = 'http://api.open-notify.org/astros.json'
    reponse = requests.get(url)
    data = reponse.json()
    
    
    # si le site envoie un message d'erreur
    assert data['message'] == 'success', 'Le site de l\'ISS affiche un message d\'erreur.'
    
    
    txt = 'Les personnes stationnant à l\'ISS sont :\n'
    
    for i in range(data['number']) :
        if data['people'][i]['craft'] == 'ISS' :
            txt += '- ' + data['people'][i]['name'] + '\n'
            
    print(txt)
    return 





def position() :
    
    test_connexion()

    url = 'http://api.open-notify.org/iss-now.json'
    reponse = requests.get(url)
    data = reponse.json()
    
    assert data['message'] == 'success', 'Le site de l\'ISS affiche un message d\'erreur.'
    
    
    txt = 'La position de l\'ISS ' + strftime("le %d/%m/%Y à %Hh%Mm%Ss ") + 'sont :\n'
    
    txt += '- Latitude : ' + data['iss_position']['latitude'] + '\n'
    txt += '- Longitude : ' + data['iss_position']['longitude'] + '\n'

    print(txt)
    return





def view_position() :
    
    test_connexion()

    fond = turtle.Screen()
    fond.setup(1750, 847)
    fond.title('Position actuelle de l\'ISS')
    
    # configuration : liaison fenêtre/coordinnées, et images
    fond.setworldcoordinates(-180, -90, 180, 90)
    fond.bgpic(courant+"\map.gif")
    fond.register_shape(courant+"\iss.gif")
    
    # changement de l'apparence du pointeur
    iss = turtle.Turtle()
    iss.shape(courant+"\iss.gif")
    iss.setheading(40)
    iss.penup()
    
    while True :
        url = "http://api.open-notify.org/iss-now.json"
        rep = requests.get(url)
        data = rep.json()
        assert data['message'] == 'success', turtle.bye()
        iss.goto(float(data["iss_position"]['longitude']),
                 float(data["iss_position"]['latitude']))
        sleep(1)
        
    return





def test_connexion() :
    temp, tries = 0, 0
    while temp == 0 and tries < 3 :
        try :
            requests.get("http://api.open-notify.org/", timeout=5)
            temp = 1
        except ConnectionError :    
            print('\n\nProblème réseau.\nTentative de reconnexion en cours...')
            sleep(10)
            tries += 1
    assert tries != 3, ('\nNous n\'avons pas pu se connecter à internet.\nVérifiez votre connexion et réessayez.')