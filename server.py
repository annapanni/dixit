from flask import Flask, escape, request, jsonify, render_template
import random
import config

app = Flask(__name__)
state={"eredeti pakli": [str(i)+".jpg" for i in range(100)],
       "jatekosok":{},
       "meselo": "",
       "meselosor":[],
       "beadott lapok":{},
       "szavazas":{},
       "szavazasi ido":{},
       "beadasi ido":{},
       "elso beadott lap ideje": None,
       "valaszthato lapok kiiirasanak idopontja":None}
state.update({"pakli":random.shuffle(state["eredeti pakli"])})

@app.route("/login")
def login():
    # global state <-- ez nem kell mert nem akarod felülírni! (többinél sem)
    name=request.args.get("name")
    if name is None:
        return "You must tell me your name.", 400
    try:
        kezben=[state["pakli"].pop(0) for i in range(6)]
    except: # <-- nem bölcs mindent except-elni!
        state["pakli"]=state["eredeti pakli"]
        random.shuffle(state["pakli"]) # <-- sajna ez is ilyen destruktív
        kezben=[state["pakli"].pop(0) for i in range(6)]   # itt ujra kell ezt irni?
    state["jatekosok"].update({name: (0, kezben)})
    return jsonify(state["jatekosok"][name])

@app.route("/start")
def start():
    global state
    state["meselosor"]=list(state["jatekosok"].keys())
    if state["meselosor"] == []:
        return "No players!", 400
    random.shuffle(state["meselosor"])
    state["meselo"]=state["meselosor"][0]
    return jsonify({
        'name': state["meselo"]
        }) #escape(name)   ??

@app.route("/startpoll")
def startpoll():
    global state
    if state["meselo"]!="":
        return jsonify(name) #escape(name) ,meselot kene visszaadni  ??
    else:
        return False #nincs ???

@app.route("/lapadas")
def lapadas():
    global state
    mytime=request.args.get("time")   #lehet egyzerre többet getelni?
    name=request.args.get("name")
    if state["elso beadott lap ideje"] is None:
        state["elso beadott lap ideje"]=mytime
    else:
        state["beadasi ido"].update({name: mytime - state["elso beadott lap ideje"]})  #lehet az időket kivonni?
    lap=request.args.get("lap")
    state["jatekosok"][name](1).remove(lap)
    state["beadott lapok"].update({lap:name})
    return

@app.route("/lappoll")
def lappoll():
    global state
    mytime=request.args.get("time")  
    if len(state["beadott lapok"])==len(state["jatekosok"]):
        state["valaszthato lapok kiiirasanak idopontja"]=mytime
        return jsonify(random.shuffle(list(state["beadott lapok"].keys())))
    else:
        return len(state["beadott lapok"])

@app.route("/valasztas")
def valasztas():
    global state
    name=request.args.get("name")  #lehet egyzerre többet getelni?
    if name==state["meselo"]:
        return "meselo nem szavaz!!!"   #false? nope? errror?
    lap=request.args.get("lap")
    state["szavazas"].update({name:lap})
    mytime=request.args.get("time")   
    state["szavazasi ido"].update({name: mytime - state["valaszthato lapok kiiirasanak idopontja"]})  #lehet az időket kivonni?
    return

@app.route("/eredmenypoll")
def eredmenypoll():
    global state
    if len(state["szavazas"])==len(state["jatekosok"])-1:
        #ujmeselo
        state["meselo"]=state["meselosor"][index(state["meselo"])+1]
        #pontozas
        for k,v in state["beadott lapok"]:
            if v==state["meselo"]:
                jolap=k
        if list(state["szavazas"].values())==[jolap*len(state["jatekosok"])] or jolap not in list(state["szavazas"].values()):
            for j in state["jatekosok"]:
                if j!=state["meselo"]:
                    state["jatekosok"][j][0]+=2
        else:
            state["jatekosok"][state["meselo"]][0]+=3
            for j, l in state["szavazas"].items():
                if l==jolap:
                    state["jatekosok"][j][0]+=2    #2 vagy 3 pontot kap?
                else:
                    ratippeltem=state["beadott lapok"][l]
                    state["jatekosok"][ratippeltem][0]+=1
        #uj lap osztas
        for j in state["jatekosok"]:
            try:
               state["jatekosok"][j](1).append(state["pakli"].pop(0))
            except:
                state["pakli"]=random.shuffle(state["eredeti pakli"])
                state["jatekosok"][j][1].append(state["pakli"].pop(0))   # itt ujra kell ezt irni?
        #nullazasok
        state["beadott lapok"]={}               #elotte state mentes?? 
        state["szavazas"]={}
        state["szavazasi ido"]={}
        state["beadasi ido"]={}
        state["elso beadott lap ideje"]= None,
        state["valaszthato lapok kiiirasanak idopontja"]=None
        
        name=request.args.get("name")
        return jsonify(state["szavazas"], state["beadott lapok"], state["meselo"], state["jatekosok"][name])   ## javitas?
    else:
        return len(state["szavazas"])
    
@app.route("/vege")
def vege():
    global state
    ##calculate awards
    name=request.args.get("name")
    return state["jatekosok"][name](0), #itt lehetne az egesz? + awardok is return


#app.run(host=config.host, port=config.port)
