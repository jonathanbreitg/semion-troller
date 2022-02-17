import os
clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
print("LOADING LIBRARIES AND FILES, PLEASE WAIT")



#IMPORTS
import requests
import urllib
import pyperclip
from termcolor import colored
import sympy
from sympy import *
import matplotlib.pyplot as plt
import sys
from PIL import Image, ImageDraw, ImageFilter
from slowprint.slowprint import *
from time import sleep

#CONSTANTS AND TOKENS
appid= "9Y37LX-K3PLE79VTV"
lat = ""
BG_IMAGE = Image.open('background.jpeg')
highest = 0
true_expression=""
#remove previous temporary files
import os
from PIL import Image, ImageDraw, ImageFilter

#dumb obama
try:
    import ueberzug.lib.v0 as ueberzug
    with ueberzug.Canvas() as c:
        path = "obama.jpg"
        demo = c.create_placement('demo',x=0, y=0, scaler=ueberzug.ScalerOption.COVER.value)
        demo.path = path
        demo.visibility = ueberzug.Visibility.VISIBLE
        for i in range(60):
            with c.lazy_drawing:
                demo.y = i * 1.2
            sleep(1/30)

clearConsole()
slowprint(colored("Made by Bira ❤️ ","magenta",attrs=['reverse','bold']),0.4)

files = os.listdir()
for file in files:
    if file.startswith("outputexpr"):
        os.remove(file)
#UTILITY FUNCTIONS
def make_sympy_like(expression):
    print(expression)
    counter = 0
    index = 0
    #expression = expression.replace(":","")
    new_expression = 'Eq(' + expression.replace(" = ",",") + ')' if " = " in expression else expression
#    new_expression = expression.replace(" ","*")
    #for char in expression:
    #    if char.isalpha()
    #print(new_expression)
    return new_expression


def save_fig(expression,filename):
    global lat
    global true_expression
    print("gothere")
    x = sympy.symbols('x')
    y = make_sympy_like(expression)
    try:
        lat = sympy.latex(eval(y))
        print(colored(str(lat),"green"))
        if str(lat) == "\\text{True}":
            print(colored("SOLVED! EXPRESSION IS TRUE","red"))
            true_expression = expression
            return True
        plt.text(0.5, 0.5, r"$%s$" % lat,horizontalalignment='center',verticalalignment='center', fontsize = 15)
        print(colored("ACTUALLY VALID SYNTAX","red"))
        print(lat)
    except Exception as e:
        print(e)
        lat = y
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        plt.text(0.5, 0.5, s=lat,horizontalalignment='center',verticalalignment='center', fontsize = 15)
    finally:
        #hide axes
        fig = plt.gca()
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        plt.savefig(f"output{filename}.png")
        plt.show()

def remove_white_background(img):
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] >= 125 and item[1] >= 125 and item[2] >= 125:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    return img



eq = input()
eq = urllib.parse.quote(eq)
req = requests.get(f"http://api.wolframalpha.com/v2/query?input={eq}&appid={appid}&podstate=Step-by-step%20solution&format=plaintext&output=json").json()
pyperclip.copy(str(req))
intermediate = req.get("queryresult").get("pods")[1]
answer = intermediate.get('subpods')[0].get('plaintext')
slowprint(colored(answer,"blue"),1)
sleep(0.3)

i = 1
while True:
    try:
        intermediate2 = intermediate.get('subpods')[i]
    except Exception as e:
        print(colored("weird... do you have internet? if yes check the api requests","red"))
    if intermediate2.get('title') == 'Possible intermediate steps':
        steps = intermediate.get('subpods')[i].get('plaintext')
        break
    i += 1
#processing response
splitted_steps = steps.split('\n')

print(splitted_steps)
splitted_steps[-1] = splitted_steps[-1][3:]
i = 0
for sub_step in splitted_steps:
    i = splitted_steps.index(sub_step)
    print("first got here")
    print(f"index is {i}")
    contains_two_letters_in_a_row=False
    counter = 0
    for char in sub_step:
        if char.isalpha():
            counter = counter + 1
        if counter > 3:
            contains_two_letters_in_a_row=True
            print(sub_step," contains two letter in a row")
            break
    if contains_two_letters_in_a_row: #TODO: IMPLEMENT SOMETHING WAY BETTER
       splitted_steps.remove(sub_step)
       continue
    print("got here?")

i = 0
for expr_string in splitted_steps:
    expr_string = expr_string.replace(":",'') if ':' in expr_string else expr_string
#    expr_string = make_sympy_like(expr_string)
    print(f"expr_string is {expr_string}")
    temp = save_fig(expr_string,f"expr{i}")
    if temp:
        break
    pyperclip.copy(expr_string)
    i += 1
print(colored(splitted_steps,"red"))

# using images to fake handwriting and images
i = 0
for expr_string in splitted_steps:
    print(f"expr_string is {expr_string}; true_expression is {true_expression}")
    if true_expression != "" and expr_string == true_expression:
        print("finished")
        break

    im_expr = Image.open(f'outputexpr{i}.png')
    im_expr = im_expr.crop((100, 230, 440, 250))
    im_expr = remove_white_background(im_expr)
    im_expr.show()
    BG_IMAGE.paste(im_expr,(200,10+25*i),im_expr)
    i = i+ 1
BG_IMAGE.show()
if 'SOLVED-HOMEWORK0.jpeg' in files:
    print(colored(f"saving under new filename because SOLVED-HOMEWORK already exists in this folder","red",attrs=["reverse"]))
    for file in files:
        if file.startswith("SOLVED-HOMEWORK"):
            print(f"file[15] is {file[15]}")
            highest = int(file[15]) if int(file[15]) > highest else highest
    highest += 1
BG_IMAGE.save(f"SOLVED-HOMEWORK{highest}.jpeg")
print(colored(f"HOMEWORK SOLVED AND SAVED UNDER FILE: SOLVED-HOMEWORK{highest}.jpeg","green",attrs=["reverse"]))
