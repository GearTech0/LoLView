from PIL import Image
from pytesseract import Output
import pytesseract

def output_to_array(output):
    ret = []
    word = ""
    for c in output:
        if c is '\n':
            if "joined the room" in word:
                ret.append(word)    
            word = ""
            continue
        else:
            word += c
    return ret

def get_players(list):
    players = []
    for word in list:
        ind = word.index("joined the room")
        player = word[:ind-1]
        if player not in players:
            players.append(player)
    return players

#im = Image.open("lolqueue_example.jpg")
output_dict = pytesseract.image_to_string("lolqueue_example_300.png", config=r'-l eng --psm 3 --dpi 300')
output_list = output_to_array(output_dict)
players = get_players(output_list)
print(players)