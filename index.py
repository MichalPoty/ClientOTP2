#!"C:\ms4w\Python\python.exe"

print("Content-Type: text/html")    # HTML is following
print()

import cgi
import requests
import json
import polyline
import datetime
import time

form = cgi.FieldStorage()

odkudd = form.getvalue("odkud") #Odkud
kamm = form.getvalue("kam") #Kam
modd = form.getvalue("radioo") #Mód cesty
timee = form.getvalue("timek") #čas 
datee = form.getvalue("datek") #datum
arriveby = form.getvalue("arrive") #departure/arrive
numiti = 3 #parametr pro max pocet iti
s1 = "" #Proměnná souřadnic
iti_cas1 = "" #promenna pro cas v buttonu itinerary2
iti_cas2 = "" #promenna pro cas v buttonu itinerary3
neexistuje = 0 #Proměnná pro neexistujici cestu
vzdalenost = 0
vzdalenost2 = 0
vzdalenost3 = 0 #porměnná pro vzdálenost
dict_cesta = {} #dictionary pro vypis vrstev
dict_souradnice = {} #dictionary pro kroky souradnic cesty
dict_barva = {} #dictionary pro barvy cest
dict_cas = {} #dictionary pro barvy cas
dict_cas_iti = {} #dictionary pro casy v buttonech
step_dist = {} #dict pro délku steps v metrech
step_streetname = {} #dict pro název ulice v steps
step_direction = {} #dict pro směr v steps
pocet_souradnice = 0 #pomocná proměnná pro počet u souřadnic
pocet_souradnice1 = 0
pocet_souradnice2 = 0
pocet_color = 0 #pomocná proměnná pro počet u barev
pocet_color1 = 0
pocet_color2 = 0
pocet_cas = 0 #pomocná proměnná pro cas u kroku
pocet_div = 0 #pomocná proměnná pro genereaci divu kroku
pocet_div1 = 0
pocet_div2 = 0
pocet_style = 0 #pomocná pro style v html
pocet_style1 = 0
pocet_style2 = 0

if odkudd and kamm and modd != None: #Pokud uživatel odešle formulář vykoná se násleudjící kod. Do té doby se nic neprovede.
    try:
        para = {"fromPlace": odkudd, "toPlace": kamm, "mode": modd, "time": timee, "date": datee, "arriveBy": arriveby, "numItineraries": numiti} #Parametry

        r = requests.get("http://localhost:8080/otp/routers/{ignoreRouterId}/plan", params=para)
        
        data = json.loads(r.text)
        
        odkud = (data['requestParameters']['fromPlace'])
        kam = (data['requestParameters']['toPlace'])
        mod = (data['requestParameters']['mode'])
        
        cesta = "" #Proměnná pro cestu v TRANSIT,WALK
        
        if len(data['plan']['itineraries']) != 0: #Osetreni, kdyz cesta neexistuje nebo uzivatel zadá blbost
            
            if modd == "TRANSIT,WALK":  #Pokud je mod Přeprava, tak se vezme první itinerary a vsechny kroky se spojí do jedne cesty
                for iti in data['plan']['itineraries'][0]['legs']:
                    cesta = cesta + str(polyline.decode(iti['legGeometry']['points'])) + "," #Spojení vsech legs do jedné cesty
                
                s1 = cesta.replace("(","[") #Nahrazení kulatých závorek za hranaté
                s1 = s1.replace(")","]")
            
            else: #Vsechny ostatni mody
                cesta = (data['plan']['itineraries'][0]['legs'][0]['legGeometry']['points'])

                souradnice = str(polyline.decode(cesta))
                s1 = souradnice.replace("(","[") #Nahrazení kulatých závorek za hranaté
                s1 = s1.replace(")","]")
        else:
            neexistuje = 1 #promenna pro neexistujici cestu, se kterou se pracuje dale v kodu
    except:
        neexistuje = 1   
        
if s1: #pokud cesta existuje, tak se vypocita cas a datum cesty
    for iti in data['plan']['itineraries']:
        starttime_date = datetime.datetime.fromtimestamp(int(iti['startTime']/1000)).strftime('%d.%m.%Y')
        starttime = datetime.datetime.fromtimestamp(int(iti['startTime']/1000)).strftime('%H:%M') #startime se vydeli 1000 a prevede na D.M. H:M
        starttime_iti = datetime.datetime.fromtimestamp(int(iti['startTime']/1000)).strftime('%H:%M')
        endtime = datetime.datetime.fromtimestamp(int(iti['endTime']/1000)).strftime('%H:%M') #endtime
        sec = int(iti['duration']) #cas cesty v sekundach
        ty_res = time.gmtime(sec) #prevedeni sekund na hodiny,minuty
        res = time.strftime("%H:%M",ty_res) #format casu na H:M
        dict_cas["promenna%s" %pocet_cas] = "<span class=\"cas\">" + str(starttime) +" - "+ str(endtime) +" </span><span class=\"hod\">(" + str(starttime_date)+ ")<br><br><i class=\"fa-regular fa-clock\"></i>&nbsp;&nbsp;</span><span class=\"cas\">"+ str(res) + "</span><span class=\"hod\">&nbsp;hod</span>" #prideleni casů do dictionary pro lepsi print
        dict_cas_iti["promenna%s" %pocet_cas] = str(starttime_iti) +"-"+ str(endtime)
        pocet_cas = pocet_cas + 1 #pomocna promena pro dictionary
    
    for iti in data['plan']['itineraries'][0]['legs']: #cyklus ktery projde leg v prvni itinerary
        vzdalenost = int(iti['distance'])/1000 + vzdalenost #Vzdálenost cele itinerary v km

 
print('''
<!DOCTYPE html>
<html>
	<head>
	<title>OTP Plánovač</title>
	<meta charset = "Windows-1250">
	<meta language= "czech">
	<meta name = "description" content = "">
	<meta name="keywords" content="">
	<meta name="author" content="Michal Potociar">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="../bakacss/style.css">
	
	<!--  Zaklad leafletu  -->
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="crossorigin=""/>
	<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="crossorigin=""></script>
    
    <!--  Contextmenu  -->
    <link rel="stylesheet" href="http://aratcliffe.github.io/Leaflet.contextmenu/dist/leaflet.contextmenu.css"/>
    <script src="http://aratcliffe.github.io/Leaflet.contextmenu/dist/leaflet.contextmenu.js"></script>
    
    <!--  FontAwesome  -->
    <script src="https://kit.fontawesome.com/04248741da.js" crossorigin="anonymous"></script>
    
    <!--  Geolocator  -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css" />
    <script src="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"></script>
    
     <!--  jQuery  -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

    
</head>
<body>
<div id="info_div"><i id="info_close" class="fa-solid fa-xmark"></i>
<h2>Základní informace o plánovači</h2><br>
<p>Jedná se o multimodální plánovač cest, který generuje cesty za pomocí programu <b>OpenTripPlanner 2</b>.</p>
<p><b>Jak vygenerovat cestu:</b></p>
<p>1) Vybrat počáteční a koncový bod cesty kliknutím pravým tlačítkem do mapy nebo zadáním adresy do textového pole. Po napsání adresy do textového pole musí být adresa potvrzena přes vedlejší tlačítko a tím se vyvoří na daném místě bod v mapě.</p>
<p>2) Vybrat nasatvení cesty. Uživatel má možnost si vybrat mezi čtyřmi druhy přepravy a datum a čas odjezdu nebo příjezdu.</p>
<p>3) Po vybrání dvou bodů uvnitř oblasti a natsvení formuláře, stačí kliknout na vyhledat cestu a v mapě se zobrazí linie a pod formulářem textové informace o cestě.</p><br>

<p>Pod formulářem se nacházejí tlačítka pro přepínání až z tří možných cest. Typ přepravy chůze nefunguje na velké vzdálenosti, max cca kolem 10 km. Pro správný chod programu jsou použita GTFS data jízdních řádů Jihomoravského kraje od společnosti KORDIS JMK a PBF data z OpenStreetMap. Pro detailnější informace o jednotlivých úsecích, může uživatel jednotlivé kroky rozkliknout.</p>
</div>
<div class="row">
  <div class="column levy">
  <button class='button_info' type='button' id="infobutton" title="Základní informace o klientovi"><i class="fa-solid fa-info"></i></i></button>
  <h1>OTP PLÁNOVAČ</h1>
  </br></br>
  
        <!--  Formulář  -->
		
		<form action="" method="post" name="form1" accept="text/hmtl"> 
		
		<input type="text" name="odkud" placeholder="Odkud" id="odkud1" title="Zadej adresu počátečního místa">
        <button type='button' id="odkudbutton" title="Vytvoření bodu z adresy ve vedlejším textovém poli"><i class="fa-solid fa-location-dot"></i></button>
		</br>
		<input type="text" name="kam" placeholder="Kam" id="kam1" title="Zadej adresu konečného místa">
        <button type='button' id="kambutton" title="Vytvoření bodu z adresy ve vedlejším textovém poli"><i class="fa-solid fa-location-dot"></i></button>
		</br>
        
        
        
		<div class="radio-toolbar">
		<input type="radio" id="transit" name="radioo"  title="Mod přeparvy veřejnou dopravou" value="TRANSIT,WALK" checked>
		<label for="transit">Přeprava</label>

		<input type="radio" id="walk"  title="Pěší mod přepravy" name="radioo" value="WALK">
		<label for="walk">Chůze</label>

		<input type="radio" id="car"  title="Přeprava pouze autem" name="radioo" value="CAR">
		<label for="car">Auto</label> 
		
		<input type="radio" id="bike"  title="Přeprava pouze na kole" name="radioo" value="BICYCLE">
		<label for="bike">Kolo</label> 
		</div>
        
        <div class="radio-toolbar2">
        <button type='button' title="Resetovat čas a datum na aktuální" onclick="myFunc()"><i class="fas fa-redo"></i></button>
        <input id="currentTime" type="time" name="timek"  title="Výběr času">
        <input id="currentDate" type="date" name="datek" title="Výběr datumu">
        <input type="radio" title="čas a datum odjzedu" id="departure" name="arrive" value="false" checked><label for="departure">Odjezd</label>
        <input type="radio" title="čas a datum příjezdu" id="arrive" name="arrive" value="true"><label for="arrive">Příjezd</label><br>
        </div>
        
        <!--  script pro aktuální datum a čas   -->
        <script>
            var date = new Date();
            var currentDate = new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toISOString().substring(0,10);
            var currentTime = new Date(date.getTime() - (date.getTimezoneOffset() * 60000)).toISOString().substring(11,16);

            document.getElementById('currentDate').value = currentDate;
            document.getElementById('currentTime').value = currentTime;
            
            function myFunc() {
                var date1 = new Date();
                var currentDate1 = new Date(date1.getTime() - (date1.getTimezoneOffset() * 60000)).toISOString().substring(0,10);
                var currentTime1 = new Date(date1.getTime() - (date1.getTimezoneOffset() * 60000)).toISOString().substring(11,16);
                
                document.getElementById('currentDate').value = currentDate1;
                document.getElementById('currentTime').value = currentTime1;
             }
        </script>
        
        <script>
        $(document).ready(function(){
            $("#infobutton").click(function(){
                $("#info_div").animate({height:'show'},300);
            });
        });

        $(document).ready(function(){
            $("#info_close").click(function(){
                $("#info_div").animate({height:'hide'},300);
            });
        });
        </script>
		</br>
		
		<input type="submit" name="submit" title="Odeslat nastavení formuláře a vygenerovat cestu" value="Vyhledat cestu">
		
		
		</form>
		<br><br><br>''')
#pokud je cesta tak print buttonu pro itineraries a jquery funkce pro show/hide divů
if s1:
    print('''
        <div class="cestaa">
		<div class="iti">''')
    #pokud je prave 3 itinerary, tak dictionary s časy, pokud 2, tak jen cas iti2, jinak iti 2 a 3 bez casu
    if len(data['plan']['itineraries']) > 2:
        iti_cas1 = dict_cas_iti["promenna1"]
        iti_cas2 = dict_cas_iti["promenna2"]
        
        for iti in data['plan']['itineraries'][1]['legs']: #cyklus ktery porjde leg ve druhe itinerary
            vzdalenost2 = int(iti['distance'])/1000 + vzdalenost2
        for iti in data['plan']['itineraries'][2]['legs']: #cyklus ktery porjde leg ve treti itinerary
            vzdalenost3 = int(iti['distance'])/1000 + vzdalenost3
            
    elif len(data['plan']['itineraries']) == 2:
        iti_cas1 = dict_cas_iti["promenna1"]
        iti_cas2 = "-----"
        
        for iti in data['plan']['itineraries'][1]['legs']: #cyklus ktery porjde leg ve druhe itinerary
            vzdalenost2 = int(iti['distance'])/1000 + vzdalenost2
    else:
        iti_cas1 = "-----"
        iti_cas2 = "-----"
    
    #print buttonu pro iti s casy odjezdu a prijezdu
    print("<label class=\"lbl\"><input type=\"radio\" name=\"radioname\" id =\"buttoniti1\" value=\"one\" checked=\"checked\" /><div class=\"iti_box1\"><p>"+dict_cas_iti["promenna0"]+"</p></div></label>")
    print("<label class=\"lbl\"><input type=\"radio\" name=\"radioname\" id =\"buttoniti2\" value=\"two\" /><div class=\"iti_box2\"><p>"+iti_cas1+"</p></div></label>")
    print("<label class=\"lbl\"><input type=\"radio\" name=\"radioname\" id =\"buttoniti3\" value=\"three\" /><div class=\"iti_box3\"><p>"+iti_cas2+"</p></div></label>")
    print('''</div>
        </div><br>
        <!--  script pro show a hide divů cesta. cesta2 a cesta3   -->
        <script type="text/javascript">
              $(function() {
                $(document).ready(function() {
                    $(".cesta").show();
                    $(".cesta2").hide();
                    $(".cesta3").hide();
                });
                $("input[name='radioname']").click(function() {
                  if ($("#buttoniti1").is(":checked")) {
                    $(".cesta").show();
                    $(".cesta2").hide();
                    $(".cesta3").hide();
                  } else if ($("#buttoniti2").is(":checked")) {
                    $(".cesta2").show();
                    $(".cesta").hide();
                    $(".cesta3").hide();
                  } else if ($("#buttoniti3").is(":checked")) {
                    $(".cesta3").show();
                    $(".cesta").hide();
                    $(".cesta2").hide();
                }
                });
              });
              
        </script>''')
    
    #Funkce kdy po kliknutí na iti buttony se v mapě objevují správné cesty
    if len(data['plan']['itineraries']) > 2:   #oveření pro počet itinerary, když jsou 3, 2 nebo 1 
        print('''<script type="text/javascript">
                  $(function() {
                    $(document).ready(function() {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.addLayer(polyline"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][1]['legs'])):              
            print("map.removeLayer(polyline1"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][2]['legs'])):              
            print("map.removeLayer(polyline2"+str(x)+");")
            
        print(''' });$("input[name='radioname']").click(function() {
                      if ($("#buttoniti1").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.addLayer(polyline"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][1]['legs'])):              
            print("map.removeLayer(polyline1"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][2]['legs'])):              
            print("map.removeLayer(polyline2"+str(x)+");")
            
        print('''} else if ($("#buttoniti2").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.removeLayer(polyline"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][1]['legs'])):              
            print("map.addLayer(polyline1"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][2]['legs'])):              
            print("map.removeLayer(polyline2"+str(x)+");")
            
        print('''} else if ($("#buttoniti3").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.removeLayer(polyline"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][1]['legs'])):              
            print("map.removeLayer(polyline1"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][2]['legs'])):              
            print("map.addLayer(polyline2"+str(x)+");")
        print('''   }
                    });
                  });
                  
            </script>''')
            
    elif len(data['plan']['itineraries']) == 2:    
        print('''<script type="text/javascript">
                  $(function() {
                    $(document).ready(function() {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.addLayer(polyline"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][1]['legs'])):              
            print("map.removeLayer(polyline1"+str(x)+");")
            
        print(''' });$("input[name='radioname']").click(function() {
                      if ($("#buttoniti1").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.addLayer(polyline"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][1]['legs'])):              
            print("map.removeLayer(polyline1"+str(x)+");")
            
        print('''} else if ($("#buttoniti2").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.removeLayer(polyline"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][1]['legs'])):              
            print("map.addLayer(polyline1"+str(x)+");")
            
        print('''} else if ($("#buttoniti3").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.removeLayer(polyline"+str(x)+");")
        for x in range(len(data['plan']['itineraries'][1]['legs'])):              
            print("map.removeLayer(polyline1"+str(x)+");")
        print('''   }
                    });
                  });
                  
            </script>''')
    else:
        print('''<script type="text/javascript">
                  $(function() {
                    $(document).ready(function() {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.addLayer(polyline"+str(x)+");")
            
        print(''' });$("input[name='radioname']").click(function() {
                      if ($("#buttoniti1").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.addLayer(polyline"+str(x)+");")
            
        print('''} else if ($("#buttoniti2").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.removeLayer(polyline"+str(x)+");")
            
        print('''} else if ($("#buttoniti3").is(":checked")) {''')
        for x in range(len(data['plan']['itineraries'][0]['legs'])):              
            print("map.removeLayer(polyline"+str(x)+");")
        print('''   }
                    });
                  });
             
         
            </script>''')
    
    
    
    
    
if neexistuje == 0: #Pokud cesta existuje tak se vypisi nasledujici divy
        
    print('''   <div class="cesta">   
                <div class="cestaobrazky">
                <span class="cestanadpis">''')
    if odkudd and kamm and modd != None: #ikony kroků cesty
        
        #====================================================================================ITI 1
        
        print("<span class=\"marker_start\"><i class=\"fas fa-map-marker-alt\"></i></span> ->")
        
        for iti2 in data['plan']['itineraries'][0]['legs']: 
            obr = iti2['mode']
            if obr == "WALK": #pokud se leg rovná walk tak vypise ikonu chuze atd
                print("<i class=\"fas fa-walking\"></i> ->")
            elif obr == "BUS":
                print("<i class=\"fas fa-bus\"></i> ->")
            elif obr == "TRAM":
                print("<i class=\"fas fa-subway\"></i> ->")
            elif obr == "RAIL":
                print("<i class=\"fas fa-train\"></i> ->")
            elif obr == "CAR":
                print("<i class=\"fas fa-car\"></i> ->")
            elif obr == "BICYCLE":
                print("<i class=\"fas fa-bicycle\"></i> ->")
        
        print("<span class=\"marker_end\"><i class=\"fas fa-map-marker-alt\"></i></span>")
        
        #print stylu tady, protoze musi se generovat unikatni nazev classy
        print("<style>")
        for iti3 in data['plan']['itineraries'][0]['legs']:   #cyklus ktery vygeneruje unikatni classy pro divy ve steps
            print(".lichy"+str(pocet_style)+"{background-color: #023406;padding: 10px;border-bottom: 2px solid #ffffff;cursor:pointer;}")
            print(".lichy"+str(pocet_style)+":hover{font-weight: bolder;}")
            print(".sudy"+str(pocet_style)+"{background-color: #2f6636;padding: 10px;border-bottom: 2px solid #ffffff;cursor:pointer;}")
            print(".sudy"+str(pocet_style)+":hover{font-weight: bolder;}")
            print(".lichy_steps"+str(pocet_style)+"{background-color: #023406;padding: 10px;border-bottom: 2px solid #ffffff; display:none;}")
            print(".sudy_steps"+str(pocet_style)+"{background-color: #2f6636;padding: 10px;border-bottom: 2px solid #ffffff; display:none;}")
            pocet_style = pocet_style + 1 
        print("</style>")    
            
            
        print('''</span><br>
            </div>
            <div class="lichy">
                <span class="cestanadpis">''')
        print(dict_cas["promenna0"]) #print casu itinerary 1
        print("<br><span class=\"hod\"><i class=\"fa-solid fa-road\"></i></span>&nbsp;&nbsp;<span class=\"cas\">"+ str(round(vzdalenost, 2)) + "</span><span class=\"hod\"> km</span>") #Vzdálenost cesty zaokrouhleno na 2 desetinná místa
        print('''</span><br>
            </div>''')
        #cyklus pro generaci divu korku cesty (lichy/sudy)    
        for iti in data['plan']['itineraries'][0]['legs']:
        
            
            div = iti['mode']     
            
            #pokud true, tak do promenych se ulozi informace ze steps (jedna se o BUS,Tramvaj a Vlak)
            if div == "BUS" or div == "TRAM" or div == "RAIL":
                bus_route = iti['routeLongName']
                bus_agency = iti['agencyName']
                bus_agencyurl = iti['agencyUrl']
                bus_from = iti['from']['name']
                bus_to = iti['to']['name']
                bus_departure = datetime.datetime.fromtimestamp(int(iti['from']['departure']/1000)).strftime('%H:%M')
                bus_arrival = datetime.datetime.fromtimestamp(int(iti['to']['arrival']/1000)).strftime('%H:%M')
            
            #do div_from se uklada nazev startu step, prvni step ma vzdy origin proto prepis na start
            if iti['from']['name'] == "Origin":
                div_from = "Start"
            else:
                div_from = iti['from']['name']
            
            #to stejny, akorat destination na cil            
            if iti['to']['name'] == "Destination":
                div_to = "Cíl"
            else:
                div_to = iti['to']['name']
            
            #cyklus ktery vytvori dictionaries pro chuzi, auto a kolo a ulozi do nich vzdalenost, nazev ulice a smer ve forme obrazku
            for x in range(len(data['plan']['itineraries'][0]['legs'][pocet_div]['steps'])):
                step_dist["promenna%s" %x] = round(int(iti['steps'][x]['distance']))
                
                if iti['steps'][x]['streetName'] == "sidewalk":
                    step_streetname["promenna%s" %x] = "chodníku"
                elif iti['steps'][x]['streetName'] == "path":
                    step_streetname["promenna%s" %x] = "chodníku"
                elif iti['steps'][x]['streetName'] == "road":
                    step_streetname["promenna%s" %x] = "silnici"
                elif iti['steps'][x]['streetName'] == "service road":
                    step_streetname["promenna%s" %x] = "silnici"
                elif iti['steps'][x]['streetName'] == "track":
                    step_streetname["promenna%s" %x] = "cestě"
                elif iti['steps'][x]['streetName'] == "bike path":
                    step_streetname["promenna%s" %x] = "cyklostezce"
                elif iti['steps'][x]['streetName'] == "ramp":
                    step_streetname["promenna%s" %x] = "nájezdu"
                elif iti['steps'][x]['streetName'] == "platform":
                    step_streetname["promenna%s" %x] = "nádraží"
                elif iti['steps'][x]['streetName'] == "link":
                    step_streetname["promenna%s" %x] = "napojení"
                else:
                    step_streetname["promenna%s" %x] = iti['steps'][x]['streetName']
                
                if iti['steps'][x]['absoluteDirection'] == "SOUTH":
                    step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-arrow.png\" alt=\"Down\" width=\"20\" height=\"20\">"
                elif iti['steps'][x]['absoluteDirection'] == "SOUTHEAST":
                    step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-right-arrow.png\" alt=\"Down-right\" width=\"16\" height=\"16\">"
                elif iti['steps'][x]['absoluteDirection'] == "EAST":
                    step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/right-arrow.png\" alt=\"Right\" width=\"20\" height=\"20\">"
                elif iti['steps'][x]['absoluteDirection'] == "NORTHEAST":
                    step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-right-arrow.png\" alt=\"Right-up\" width=\"16\" height=\"16\">"
                elif iti['steps'][x]['absoluteDirection'] == "NORTH":
                    step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-arrow.png\" alt=\"Up\" width=\"20\" height=\"20\">"
                elif iti['steps'][x]['absoluteDirection'] == "NORTHWEST":
                    step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-left-arrow.png\" alt=\"Left-up\" width=\"16\" height=\"16\">"
                elif iti['steps'][x]['absoluteDirection'] == "WEST":
                    step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/left-arrow.png\" alt=\"Left\" width=\"20\" height=\"20\">"
                elif iti['steps'][x]['absoluteDirection'] == "SOUTHWEST":
                    step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-left-arrow.png\" alt=\"Down-left\" width=\"16\" height=\"16\">"
                
            #promenne s pocatecnim a konecnym casem kroku cesty
            div_fromtime = datetime.datetime.fromtimestamp(int(iti['startTime']/1000)).strftime('%H:%M')
            div_endtime = datetime.datetime.fromtimestamp(int(iti['endTime']/1000)).strftime('%H:%M')
            
            #jQuery script pro interaktivitu kroku cesty, po kliknuti na krok cesty se vysune div s detaily
            print("<script>$(document).ready(function(){$(\".lichy"+str(pocet_div)+"\").click(function(){$(\".lichy_steps"+str(pocet_div)+"\").animate({height:'toggle'},150);});});</script>")
            print("<script>$(document).ready(function(){$(\".sudy"+str(pocet_div)+"\").click(function(){$(\".sudy_steps"+str(pocet_div)+"\").animate({height:'toggle'},150);});});</script>")

            if div == "WALK": #pokud se leg rovná walk tak vypise div se steps a jeste rozliseni lichy/sudy div
                if (pocet_div % 2) != 0:
                    #print krok cesty
                    print("<div class=\"lichy"+str(pocet_div)+"\"><i class=\"fas fa-walking\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy_steps"+str(pocet_div)+"\"><h3 style=\"color:#93949F;\">CHŮZE</h3>")
                    print("<script>$( \".lichy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'gray',opacity: 0.8,weight: 8});});</script>")
                   
                   #print detailu kroku cesty
                    for x in range(len(data['plan']['itineraries'][0]['legs'][pocet_div]['steps'])):
                        print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jdi po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                        
                    print("</div>")
                
                #to stejny pro sudy div                
                else:
                    print("<div class=\"sudy"+str(pocet_div)+"\"><i class=\"fas fa-walking\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy_steps"+str(pocet_div)+"\"><h3 style=\"color:#93949F;\">CHŮZE</h3>")
                    print("<script>$( \".sudy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'gray',opacity: 0.8,weight: 8});});</script>")
                    
                    for x in range(len(data['plan']['itineraries'][0]['legs'][pocet_div]['steps'])):
                        print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jdi po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                        
                    print("</div>")
                    
            elif div == "BUS": #print steps pro BUS
                
                if (pocet_div % 2) != 0:
                    print("<div class=\"lichy"+str(pocet_div)+"\"><i class=\"fas fa-bus\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy_steps"+str(pocet_div)+"\"><h3 style=\"color:#88C035;\">BUS</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                    print("<script>$( \".lichy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'green',opacity: 0.8,weight: 8});});</script>")
                else:
                    print("<div class=\"sudy"+str(pocet_div)+"\"><i class=\"fas fa-bus\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy_steps"+str(pocet_div)+"\"><h3 style=\"color:#88C035;\">BUS</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                    print("<script>$( \".sudy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'green',opacity: 0.8,weight: 8});});</script>")
            elif div == "TRAM": #print steps pro tramvaj
            
                if (pocet_div % 2) != 0:
                    print("<div class=\"lichy"+str(pocet_div)+"\"><i class=\"fas fa-subway\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy_steps"+str(pocet_div)+"\"><h3 style=\"color:#ffab03;\">TRAMVAJ</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                    print("<script>$( \".lichy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'orange',opacity: 0.8,weight: 8});});</script>")
                else:
                    print("<div class=\"sudy"+str(pocet_div)+"\"><i class=\"fas fa-subway\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy_steps"+str(pocet_div)+"\"><h3 style=\"color:#ffab03;\">TRAMVAJ</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                    print("<script>$( \".sudy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'orange',opacity: 0.8,weight: 8});});</script>")
            elif div == "RAIL": #print steps pro vlak
            
                if (pocet_div % 2) != 0:
                    print("<div class=\"lichy"+str(pocet_div)+"\"><i class=\"fas fa-train\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy_steps"+str(pocet_div)+"\"><h3 style=\"color:#C41508;\">VLAK</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                    print("<script>$( \".lichy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'red',opacity: 0.8,weight: 8});});</script>")
                    
                else:
                    print("<div class=\"sudy"+str(pocet_div)+"\"><i class=\"fas fa-train\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy_steps"+str(pocet_div)+"\"><h3 style=\"color:#C41508;\">VLAK</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                    print("<script>$( \".sudy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'red',opacity: 0.8,weight: 8});});</script>")
                    
            elif div == "CAR": #print steps pro auto, stejny jak walk
                if (pocet_div % 2) != 0:
                    print("<div class=\"lichy"+str(pocet_div)+"\"><i class=\"fas fa-car\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy_steps"+str(pocet_div)+"\"><h3 style=\"color:#f7f300;\">AUTO</h3>")
                    print("<script>$( \".lichy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'red',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 0.8,weight: 8});});</script>")
                    
                    for x in range(len(data['plan']['itineraries'][0]['legs'][pocet_div]['steps'])):
                        print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                        
                    print("</div>")
                    
                else: 
                    print("<div class=\"sudy"+str(pocet_div)+"\"><i class=\"fas fa-car\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy_steps"+str(pocet_div)+"\"><h3 style=\"color:#f7f300;\">AUTO</h3>")
                    print("<script>$( \".sudy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'red',opacity: 1,weight: 10});}).mouseleave(function() {polyline0.setStyle({color: 'yellow',opacity: 0.8,weight: 8});});</script>")
                    
                    for x in range(len(data['plan']['itineraries'][0]['legs'][pocet_div]['steps'])):
                        print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                        
                    print("</div>")
                    
            elif div == "BICYCLE": #print steps pro kolo, stejny jak walk
                if (pocet_div % 2) != 0:
                    print("<div class=\"lichy"+str(pocet_div)+"\"><i class=\"fas fa-bicycle\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy_steps"+str(pocet_div)+"\"><h3 style=\"color:#33ADFF;\">KOLO</h3>")
                    print("<script>$( \".lichy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'blue',opacity: 0.8,weight: 8});});</script>")
                    
                    for x in range(len(data['plan']['itineraries'][0]['legs'][pocet_div]['steps'])):
                        print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                        
                    print("</div>")
                    
                else:
                    print("<div class=\"sudy"+str(pocet_div)+"\"><i class=\"fas fa-bicycle\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy_steps"+str(pocet_div)+"\"><h3 style=\"color:#33ADFF;\">KOLO</h3>")
                    print("<script>$( \".sudy"+str(pocet_div)+"\" ).mouseenter(function() {polyline"+str(pocet_div)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline"+str(pocet_div)+".setStyle({color: 'blue',opacity: 0.8,weight: 8});});</script>")
                    
                    for x in range(len(data['plan']['itineraries'][0]['legs'][pocet_div]['steps'])):
                        print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                        
                    print("</div>") 
                
              
            pocet_div = pocet_div + 1 #pomocna promenna pro vsechny dict   
        
        print("</div>") #ukonceni divu cesta        

#=======================================================================================ITINERARY 2 + 3        
        #Pokud jsou prave3 itinerary tak print divu cesta 2 i cesta 3
        if len(data['plan']['itineraries']) > 2:
            print('''<div class="cesta2">
                        <div class="cestaobrazky">
                            <span class="cestanadpis">''')
            print("<span class=\"marker_start\"><i class=\"fas fa-map-marker-alt\"></i></span> ->")
        
            for iti2 in data['plan']['itineraries'][1]['legs']: 
                obr1 = iti2['mode']
                if obr1 == "WALK": #pokud se leg rovná walk tak vypise ikonu chuze atd
                    print("<i class=\"fas fa-walking\"></i> ->")
                elif obr1 == "BUS":
                    print("<i class=\"fas fa-bus\"></i> ->")
                elif obr1 == "TRAM":
                    print("<i class=\"fas fa-subway\"></i> ->")
                elif obr1 == "RAIL":
                    print("<i class=\"fas fa-train\"></i> ->")
                elif obr1 == "CAR":
                    print("<i class=\"fas fa-car\"></i> ->")
                elif obr1 == "BICYCLE":
                    print("<i class=\"fas fa-bicycle\"></i> ->")
            
            print("<span class=\"marker_end\"><i class=\"fas fa-map-marker-alt\"></i></span>")
            
            #print stylu tady, protoze musi se generovat unikatni nazev classy
            print("<style>")
            for iti3 in data['plan']['itineraries'][1]['legs']:   #cyklus ktery vygeneruje unikatni classy pro divy ve steps
                print(".lichy1"+str(pocet_style1)+"{background-color: #023406;padding: 10px;border-bottom: 2px solid #ffffff;cursor:pointer;}")
                print(".lichy1"+str(pocet_style1)+":hover{font-weight: bolder;}")
                print(".sudy1"+str(pocet_style1)+"{background-color: #2f6636;padding: 10px;border-bottom: 2px solid #ffffff;cursor:pointer;}")
                print(".sudy1"+str(pocet_style1)+":hover{font-weight: bolder;}")
                print(".lichy1_steps"+str(pocet_style1)+"{background-color: #023406;padding: 10px;border-bottom: 2px solid #ffffff; display:none;}")
                print(".sudy1_steps"+str(pocet_style1)+"{background-color: #2f6636;padding: 10px;border-bottom: 2px solid #ffffff; display:none;}")
                pocet_style1 = pocet_style1 + 1
            print("</style>")  
            
            print('''        </span><br>
                        </div>
                        <div class="lichy">
                            <span class="cestanadpis">''')
            print(dict_cas["promenna1"]) #print casu itinerary 2
            print("<br><span class=\"hod\"><i class=\"fa-solid fa-road\"></i></span>&nbsp;&nbsp;<span class=\"cas\">"+ str(round(vzdalenost2, 2)) + "</span><span class=\"hod\"> km</span>") #Vzdálenost cesty zaokrouhleno na 2 desetinná místa
            print('''</span><br>
            </div>''')
            #cyklus pro generaci divu korku cesty (lichy/sudy)    
            for iti in data['plan']['itineraries'][1]['legs']:
            
                
                div = iti['mode']     
                
                #pokud true, tak do promenych se ulozi informace ze steps (jedna se o BUS,Tramvaj a Vlak)
                if div == "BUS" or div == "TRAM" or div == "RAIL":
                    bus_route = iti['routeLongName']
                    bus_agency = iti['agencyName']
                    bus_agencyurl = iti['agencyUrl']
                    bus_from = iti['from']['name']
                    bus_to = iti['to']['name']
                    bus_departure = datetime.datetime.fromtimestamp(int(iti['from']['departure']/1000)).strftime('%H:%M')
                    bus_arrival = datetime.datetime.fromtimestamp(int(iti['to']['arrival']/1000)).strftime('%H:%M')
                
                #do div_from se uklada nazev startu step, prvni step ma vzdy origin proto prepis na start
                if iti['from']['name'] == "Origin":
                    div_from = "Start"
                else:
                    div_from = iti['from']['name']
                
                #to stejny, akorat destination na cil            
                if iti['to']['name'] == "Destination":
                    div_to = "Cíl"
                else:
                    div_to = iti['to']['name']
                
                #cyklus ktery vytvori dictionaries pro chuzi, auto a kolo a ulozi do nich vzdalenost, nazev ulice a smer ve forme obrazku
                for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                    step_dist["promenna%s" %x] = round(int(iti['steps'][x]['distance']))
                    
                    if iti['steps'][x]['streetName'] == "sidewalk":
                        step_streetname["promenna%s" %x] = "chodníku"
                    elif iti['steps'][x]['streetName'] == "path":
                        step_streetname["promenna%s" %x] = "chodníku"
                    elif iti['steps'][x]['streetName'] == "road":
                        step_streetname["promenna%s" %x] = "silnici"
                    elif iti['steps'][x]['streetName'] == "service road":
                        step_streetname["promenna%s" %x] = "silnici"
                    elif iti['steps'][x]['streetName'] == "track":
                        step_streetname["promenna%s" %x] = "cestě"
                    elif iti['steps'][x]['streetName'] == "bike path":
                        step_streetname["promenna%s" %x] = "cyklostezce"
                    elif iti['steps'][x]['streetName'] == "ramp":
                        step_streetname["promenna%s" %x] = "nájezdu"
                    elif iti['steps'][x]['streetName'] == "platform":
                        step_streetname["promenna%s" %x] = "nádraží"
                    elif iti['steps'][x]['streetName'] == "link":
                        step_streetname["promenna%s" %x] = "napojení"
                    else:
                        step_streetname["promenna%s" %x] = iti['steps'][x]['streetName']
                    
                    if iti['steps'][x]['absoluteDirection'] == "SOUTH":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-arrow.png\" alt=\"Down\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "SOUTHEAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-right-arrow.png\" alt=\"Down-right\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "EAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/right-arrow.png\" alt=\"Right\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTHEAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-right-arrow.png\" alt=\"Right-up\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTH":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-arrow.png\" alt=\"Up\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTHWEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-left-arrow.png\" alt=\"Left-up\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "WEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/left-arrow.png\" alt=\"Left\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "SOUTHWEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-left-arrow.png\" alt=\"Down-left\" width=\"16\" height=\"16\">"
                    
                #promenne s pocatecnim a konecnym casem kroku cesty
                div_fromtime = datetime.datetime.fromtimestamp(int(iti['startTime']/1000)).strftime('%H:%M')
                div_endtime = datetime.datetime.fromtimestamp(int(iti['endTime']/1000)).strftime('%H:%M')
                
                #jQuery script pro interaktivitu kroku cesty, po kliknuti na krok cesty se vysune div s detaily
                print("<script>$(document).ready(function(){$(\".lichy1"+str(pocet_div1)+"\").click(function(){$(\".lichy1_steps"+str(pocet_div1)+"\").animate({height:'toggle'},150);});});</script>")
                print("<script>$(document).ready(function(){$(\".sudy1"+str(pocet_div1)+"\").click(function(){$(\".sudy1_steps"+str(pocet_div1)+"\").animate({height:'toggle'},150);});});</script>")

                if div == "WALK": #pokud se leg rovná walk tak vypise div se steps a jeste rozliseni lichy/sudy div
                    if (pocet_div1 % 2) != 0:
                        #print krok cesty
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-walking\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#93949F;\">CHŮZE</h3>")
                        
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'gray',opacity: 0.8,weight: 8});});</script>")
                        #print detailu kroku cesty
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jdi po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                    
                    #to stejny pro sudy div                
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-walking\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#93949F;\">CHŮZE</h3>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'gray',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jdi po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                elif div == "BUS": #print steps pro BUS
                    
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-bus\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#88C035;\">BUS</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'green',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-bus\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#88C035;\">BUS</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'green',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "TRAM": #print steps pro tramvaj
                
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-subway\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#ffab03;\">TRAMVAJ</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'orange',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-subway\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#ffab03;\">TRAMVAJ</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'orange',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "RAIL": #print steps pro vlak
                
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-train\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#C41508;\">VLAK</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'red',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-train\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#C41508;\">VLAK</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'red',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "CAR": #print steps pro auto, stejny jak walk
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-car\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#f7f300;\">AUTO</h3>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'red',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                    else: 
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-car\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#f7f300;\">AUTO</h3>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'red',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                elif div == "BICYCLE": #print steps pro kolo, stejny jak walk
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-bicycle\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#33ADFF;\">KOLO</h3>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'blue',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-bicycle\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#33ADFF;\">KOLO</h3>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'blue',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                pocet_div1 = pocet_div1 + 1 #pomocna promenna pro vsechny dict   
            
            print("</div>") #ukonceni divu cesta
#-------------------------------------------------------------------------------------------- Konec cesty 2                        
            print('''<div class="cesta3">
                    <div class="cestaobrazky">
                             <span class="cestanadpis">''')
            print("<span class=\"marker_start\"><i class=\"fas fa-map-marker-alt\"></i></span> ->")
        
            for iti2 in data['plan']['itineraries'][2]['legs']: 
                obr2 = iti2['mode']
                if obr2 == "WALK": #pokud se leg rovná walk tak vypise ikonu chuze atd
                    print("<i class=\"fas fa-walking\"></i> ->")
                elif obr2 == "BUS":
                    print("<i class=\"fas fa-bus\"></i> ->")
                elif obr2 == "TRAM":
                    print("<i class=\"fas fa-subway\"></i> ->")
                elif obr2 == "RAIL":
                    print("<i class=\"fas fa-train\"></i> ->")
                elif obr2 == "CAR":
                    print("<i class=\"fas fa-car\"></i> ->")
                elif obr2 == "BICYCLE":
                    print("<i class=\"fas fa-bicycle\"></i> ->")
            
            print("<span class=\"marker_end\"><i class=\"fas fa-map-marker-alt\"></i></span>")
            
            #print stylu tady, protoze musi se generovat unikatni nazev classy
            print("<style>")
            for iti3 in data['plan']['itineraries'][2]['legs']:   #cyklus ktery vygeneruje unikatni classy pro divy ve steps
                print(".lichy2"+str(pocet_style2)+"{background-color: #023406;padding: 10px;border-bottom: 2px solid #ffffff;cursor:pointer;}")
                print(".lichy2"+str(pocet_style2)+":hover{font-weight: bolder;}")
                print(".sudy2"+str(pocet_style2)+"{background-color: #2f6636;padding: 10px;border-bottom: 2px solid #ffffff;cursor:pointer;}")
                print(".sudy2"+str(pocet_style2)+":hover{font-weight: bolder;}")
                print(".lichy2_steps"+str(pocet_style2)+"{background-color: #023406;padding: 10px;border-bottom: 2px solid #ffffff; display:none;}")
                print(".sudy2_steps"+str(pocet_style2)+"{background-color: #2f6636;padding: 10px;border-bottom: 2px solid #ffffff; display:none;}")
                pocet_style2 = pocet_style2 + 1 
            print("</style>")  
            
            print('''        </span><br>
                        </div>
                        <div class="lichy">
                            <span class="cestanadpis">''')
            print(dict_cas["promenna2"]) #print casu itinerary 2
            print("<br><span class=\"hod\"><i class=\"fa-solid fa-road\"></i></span>&nbsp;&nbsp;<span class=\"cas\">"+ str(round(vzdalenost3, 2)) + "</span><span class=\"hod\"> km</span>") #Vzdálenost cesty zaokrouhleno na 2 desetinná místa
            print('''</span><br>
            </div>''')
            #cyklus pro generaci divu korku cesty (lichy/sudy)    
            for iti in data['plan']['itineraries'][2]['legs']:
            
                
                div = iti['mode']     
                
                #pokud true, tak do promenych se ulozi informace ze steps (jedna se o BUS,Tramvaj a Vlak)
                if div == "BUS" or div == "TRAM" or div == "RAIL":
                    bus_route = iti['routeLongName']
                    bus_agency = iti['agencyName']
                    bus_agencyurl = iti['agencyUrl']
                    bus_from = iti['from']['name']
                    bus_to = iti['to']['name']
                    bus_departure = datetime.datetime.fromtimestamp(int(iti['from']['departure']/1000)).strftime('%H:%M')
                    bus_arrival = datetime.datetime.fromtimestamp(int(iti['to']['arrival']/1000)).strftime('%H:%M')
                
                #do div_from se uklada nazev startu step, prvni step ma vzdy origin proto prepis na start
                if iti['from']['name'] == "Origin":
                    div_from = "Start"
                else:
                    div_from = iti['from']['name']
                
                #to stejny, akorat destination na cil            
                if iti['to']['name'] == "Destination":
                    div_to = "Cíl"
                else:
                    div_to = iti['to']['name']
                
                #cyklus ktery vytvori dictionaries pro chuzi, auto a kolo a ulozi do nich vzdalenost, nazev ulice a smer ve forme obrazku
                for x in range(len(data['plan']['itineraries'][2]['legs'][pocet_div2]['steps'])):
                    step_dist["promenna%s" %x] = round(int(iti['steps'][x]['distance']))
                    
                    if iti['steps'][x]['streetName'] == "sidewalk":
                        step_streetname["promenna%s" %x] = "chodníku"
                    elif iti['steps'][x]['streetName'] == "path":
                        step_streetname["promenna%s" %x] = "chodníku"
                    elif iti['steps'][x]['streetName'] == "road":
                        step_streetname["promenna%s" %x] = "silnici"
                    elif iti['steps'][x]['streetName'] == "service road":
                        step_streetname["promenna%s" %x] = "silnici"
                    elif iti['steps'][x]['streetName'] == "track":
                        step_streetname["promenna%s" %x] = "cestě"
                    elif iti['steps'][x]['streetName'] == "bike path":
                        step_streetname["promenna%s" %x] = "cyklostezce"
                    elif iti['steps'][x]['streetName'] == "ramp":
                        step_streetname["promenna%s" %x] = "nájezdu"
                    elif iti['steps'][x]['streetName'] == "platform":
                        step_streetname["promenna%s" %x] = "nádraží"
                    elif iti['steps'][x]['streetName'] == "link":
                        step_streetname["promenna%s" %x] = "napojení"
                    else:
                        step_streetname["promenna%s" %x] = iti['steps'][x]['streetName']
                    
                    if iti['steps'][x]['absoluteDirection'] == "SOUTH":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-arrow.png\" alt=\"Down\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "SOUTHEAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-right-arrow.png\" alt=\"Down-right\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "EAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/right-arrow.png\" alt=\"Right\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTHEAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-right-arrow.png\" alt=\"Right-up\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTH":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-arrow.png\" alt=\"Up\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTHWEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-left-arrow.png\" alt=\"Left-up\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "WEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/left-arrow.png\" alt=\"Left\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "SOUTHWEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-left-arrow.png\" alt=\"Down-left\" width=\"16\" height=\"16\">"
                    
                #promenne s pocatecnim a konecnym casem kroku cesty
                div_fromtime = datetime.datetime.fromtimestamp(int(iti['startTime']/1000)).strftime('%H:%M')
                div_endtime = datetime.datetime.fromtimestamp(int(iti['endTime']/1000)).strftime('%H:%M')
                
                #jQuery script pro interaktivitu kroku cesty, po kliknuti na krok cesty se vysune div s detaily
                print("<script>$(document).ready(function(){$(\".lichy2"+str(pocet_div2)+"\").click(function(){$(\".lichy2_steps"+str(pocet_div2)+"\").animate({height:'toggle'},150);});});</script>")
                print("<script>$(document).ready(function(){$(\".sudy2"+str(pocet_div2)+"\").click(function(){$(\".sudy2_steps"+str(pocet_div2)+"\").animate({height:'toggle'},150);});});</script>")

                if div == "WALK": #pokud se leg rovná walk tak vypise div se steps a jeste rozliseni lichy/sudy div
                    if (pocet_div2 % 2) != 0:
                        #print krok cesty
                        print("<div class=\"lichy2"+str(pocet_div2)+"\"><i class=\"fas fa-walking\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#93949F;\">CHŮZE</h3>")
                        print("<script>$( \".lichy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'gray',opacity: 0.8,weight: 8});});</script>")
                        
                        #print detailu kroku cesty
                        for x in range(len(data['plan']['itineraries'][2]['legs'][pocet_div2]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jdi po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                    
                    #to stejny pro sudy div                
                    else:
                        print("<div class=\"sudy2"+str(pocet_div2)+"\"><i class=\"fas fa-walking\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#93949F;\">CHŮZE</h3>")
                        print("<script>$( \".sudy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'gray',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][2]['legs'][pocet_div2]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jdi po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                elif div == "BUS": #print steps pro BUS
                    
                    if (pocet_div2 % 2) != 0:
                        print("<div class=\"lichy2"+str(pocet_div2)+"\"><i class=\"fas fa-bus\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#88C035;\">BUS</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'green',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy2"+str(pocet_div2)+"\"><i class=\"fas fa-bus\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#88C035;\">BUS</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'green',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "TRAM": #print steps pro tramvaj
                
                    if (pocet_div2 % 2) != 0:
                        print("<div class=\"lichy2"+str(pocet_div2)+"\"><i class=\"fas fa-subway\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#ffab03;\">TRAMVAJ</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'orange',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy2"+str(pocet_div2)+"\"><i class=\"fas fa-subway\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#ffab03;\">TRAMVAJ</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'orange',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "RAIL": #print steps pro vlak
                
                    if (pocet_div2 % 2) != 0:
                        print("<div class=\"lichy2"+str(pocet_div2)+"\"><i class=\"fas fa-train\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#C41508;\">VLAK</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'red',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy2"+str(pocet_div2)+"\"><i class=\"fas fa-train\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#C41508;\">VLAK</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'red',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "CAR": #print steps pro auto, stejny jak walk
                    if (pocet_div2 % 2) != 0:
                        print("<div class=\"lichy2"+str(pocet_div2)+"\"><i class=\"fas fa-car\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#f7f300;\">AUTO</h3>")
                        print("<script>$( \".lichy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'red',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][2]['legs'][pocet_div2]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                    else: 
                        print("<div class=\"sudy2"+str(pocet_div2)+"\"><i class=\"fas fa-car\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#f7f300;\">AUTO</h3>")
                        print("<script>$( \".sudy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'red',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][2]['legs'][pocet_div2]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                elif div == "BICYCLE": #print steps pro kolo, stejny jak walk
                    if (pocet_div2 % 2) != 0:
                        print("<div class=\"lichy2"+str(pocet_div2)+"\"><i class=\"fas fa-bicycle\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#33ADFF;\">KOLO</h3>")
                        print("<script>$( \".lichy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'blue',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][2]['legs'][pocet_div2]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                    else:
                        print("<div class=\"sudy2"+str(pocet_div2)+"\"><i class=\"fas fa-bicycle\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy2_steps"+str(pocet_div2)+"\"><h3 style=\"color:#33ADFF;\">KOLO</h3>")
                        print("<script>$( \".sudy2"+str(pocet_div2)+"\" ).mouseenter(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline2"+str(pocet_div2)+".setStyle({color: 'blue',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][2]['legs'][pocet_div2]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                pocet_div2 = pocet_div2 + 1 #pomocna promenna pro vsechny dict   
            
#=======================================================================================ITI 2 + 3. prázdná            
        #Pokud jsou prave2 itinerary tak print pouze cesty2, cesta 3 bude prazdna    
        elif len(data['plan']['itineraries']) == 2:
            print('''<div class="cesta2">
                        <div class="cestaobrazky">
                            <span class="cestanadpis">''')
            print("<span class=\"marker_start\"><i class=\"fas fa-map-marker-alt\"></i></span> ->")
        
            for iti2 in data['plan']['itineraries'][1]['legs']: 
                obr1 = iti2['mode']
                if obr1 == "WALK": #pokud se leg rovná walk tak vypise ikonu chuze atd
                    print("<i class=\"fas fa-walking\"></i> ->")
                elif obr1 == "BUS":
                    print("<i class=\"fas fa-bus\"></i> ->")
                elif obr1 == "TRAM":
                    print("<i class=\"fas fa-subway\"></i> ->")
                elif obr1 == "RAIL":
                    print("<i class=\"fas fa-train\"></i> ->")
                elif obr1 == "CAR":
                    print("<i class=\"fas fa-car\"></i> ->")
                elif obr1 == "BICYCLE":
                    print("<i class=\"fas fa-bicycle\"></i> ->")
            
            print("<span class=\"marker_end\"><i class=\"fas fa-map-marker-alt\"></i></span>")
            
            #print stylu tady, protoze musi se generovat unikatni nazev classy
            print("<style>")
            for iti3 in data['plan']['itineraries'][1]['legs']:   #cyklus ktery vygeneruje unikatni classy pro divy ve steps
                print(".lichy1"+str(pocet_style1)+"{background-color: #023406;padding: 10px;border-bottom: 2px solid #ffffff;cursor:pointer;}")
                print(".lichy1"+str(pocet_style1)+":hover{font-weight: bolder;}")
                print(".sudy1"+str(pocet_style1)+"{background-color: #2f6636;padding: 10px;border-bottom: 2px solid #ffffff;cursor:pointer;}")
                print(".sudy1"+str(pocet_style1)+":hover{font-weight: bolder;}")
                print(".lichy1_steps"+str(pocet_style1)+"{background-color: #023406;padding: 10px;border-bottom: 2px solid #ffffff; display:none;}")
                print(".sudy1_steps"+str(pocet_style1)+"{background-color: #2f6636;padding: 10px;border-bottom: 2px solid #ffffff; display:none;}")
                pocet_style1 = pocet_style1 + 1
            print("</style>")  
            
            print('''        </span><br>
                        </div>
                        <div class="lichy">
                            <span class="cestanadpis">''')
            print(dict_cas["promenna1"]) #print casu itinerary 2
            print("<br><span class=\"hod\"><i class=\"fa-solid fa-road\"></i></span>&nbsp;&nbsp;<span class=\"cas\">"+ str(round(vzdalenost2, 2)) + "</span><span class=\"hod\"> km</span>") #Vzdálenost cesty zaokrouhleno na 2 desetinná místa
            print('''</span><br>
            </div>''')
            #cyklus pro generaci divu korku cesty (lichy/sudy)    
            for iti in data['plan']['itineraries'][1]['legs']:
            
                
                div = iti['mode']     
                
                #pokud true, tak do promenych se ulozi informace ze steps (jedna se o BUS,Tramvaj a Vlak)
                if div == "BUS" or div == "TRAM" or div == "RAIL":
                    bus_route = iti['routeLongName']
                    bus_agency = iti['agencyName']
                    bus_agencyurl = iti['agencyUrl']
                    bus_from = iti['from']['name']
                    bus_to = iti['to']['name']
                    bus_departure = datetime.datetime.fromtimestamp(int(iti['from']['departure']/1000)).strftime('%H:%M')
                    bus_arrival = datetime.datetime.fromtimestamp(int(iti['to']['arrival']/1000)).strftime('%H:%M')
                
                #do div_from se uklada nazev startu step, prvni step ma vzdy origin proto prepis na start
                if iti['from']['name'] == "Origin":
                    div_from = "Start"
                else:
                    div_from = iti['from']['name']
                
                #to stejny, akorat destination na cil            
                if iti['to']['name'] == "Destination":
                    div_to = "Cíl"
                else:
                    div_to = iti['to']['name']
                
                #cyklus ktery vytvori dictionaries pro chuzi, auto a kolo a ulozi do nich vzdalenost, nazev ulice a smer ve forme obrazku
                for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                    step_dist["promenna%s" %x] = round(int(iti['steps'][x]['distance']))
                    
                    if iti['steps'][x]['streetName'] == "sidewalk":
                        step_streetname["promenna%s" %x] = "chodníku"
                    elif iti['steps'][x]['streetName'] == "path":
                        step_streetname["promenna%s" %x] = "chodníku"
                    elif iti['steps'][x]['streetName'] == "road":
                        step_streetname["promenna%s" %x] = "silnici"
                    elif iti['steps'][x]['streetName'] == "service road":
                        step_streetname["promenna%s" %x] = "silnici"
                    elif iti['steps'][x]['streetName'] == "track":
                        step_streetname["promenna%s" %x] = "cestě"
                    elif iti['steps'][x]['streetName'] == "bike path":
                        step_streetname["promenna%s" %x] = "cyklostezce"
                    elif iti['steps'][x]['streetName'] == "ramp":
                        step_streetname["promenna%s" %x] = "nájezdu"
                    elif iti['steps'][x]['streetName'] == "platform":
                        step_streetname["promenna%s" %x] = "nádraží"
                    elif iti['steps'][x]['streetName'] == "link":
                        step_streetname["promenna%s" %x] = "napojení"
                    else:
                        step_streetname["promenna%s" %x] = iti['steps'][x]['streetName']
                    
                    if iti['steps'][x]['absoluteDirection'] == "SOUTH":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-arrow.png\" alt=\"Down\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "SOUTHEAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-right-arrow.png\" alt=\"Down-right\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "EAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/right-arrow.png\" alt=\"Right\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTHEAST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-right-arrow.png\" alt=\"Right-up\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTH":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-arrow.png\" alt=\"Up\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "NORTHWEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/up-left-arrow.png\" alt=\"Left-up\" width=\"16\" height=\"16\">"
                    elif iti['steps'][x]['absoluteDirection'] == "WEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/left-arrow.png\" alt=\"Left\" width=\"20\" height=\"20\">"
                    elif iti['steps'][x]['absoluteDirection'] == "SOUTHWEST":
                        step_direction["promenna%s" %x] = "<img src=\"../bakacss/img/down-left-arrow.png\" alt=\"Down-left\" width=\"16\" height=\"16\">"
                    
                #promenne s pocatecnim a konecnym casem kroku cesty
                div_fromtime = datetime.datetime.fromtimestamp(int(iti['startTime']/1000)).strftime('%H:%M')
                div_endtime = datetime.datetime.fromtimestamp(int(iti['endTime']/1000)).strftime('%H:%M')
                
                #jQuery script pro interaktivitu kroku cesty, po kliknuti na krok cesty se vysune div s detaily
                print("<script>$(document).ready(function(){$(\".lichy1"+str(pocet_div1)+"\").click(function(){$(\".lichy1_steps"+str(pocet_div1)+"\").animate({height:'toggle'},150);});});</script>")
                print("<script>$(document).ready(function(){$(\".sudy1"+str(pocet_div1)+"\").click(function(){$(\".sudy1_steps"+str(pocet_div1)+"\").animate({height:'toggle'},150);});});</script>")

                if div == "WALK": #pokud se leg rovná walk tak vypise div se steps a jeste rozliseni lichy/sudy div
                    if (pocet_div1 % 2) != 0:
                        #print krok cesty
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-walking\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#93949F;\">CHŮZE</h3>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'gray',opacity: 0.8,weight: 8});});</script>")
                        
                        #print detailu kroku cesty
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jdi po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                    
                    #to stejny pro sudy div                
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-walking\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#93949F;\">CHŮZE</h3>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'gray',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jdi po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                elif div == "BUS": #print steps pro BUS
                    
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-bus\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#88C035;\">BUS</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'green',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-bus\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#88C035;\">BUS</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'green',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "TRAM": #print steps pro tramvaj
                
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-subway\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#ffab03;\">TRAMVAJ</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'orange',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-subway\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#ffab03;\">TRAMVAJ</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'orange',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "RAIL": #print steps pro vlak
                
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-train\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#C41508;\">VLAK</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'red',opacity: 0.8,weight: 8});});</script>")
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-train\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"] <br></div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#C41508;\">VLAK</h3><p><i class=\"fa-solid fa-angles-right\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_from+"</span>&nbsp;<span class=\"hod2\">("+str(bus_departure)+")</span></p><p><i class=\"fa-solid fa-flag-checkered\"></i>&nbsp;&nbsp;<span class=\"cas2\">"+bus_to+"</span>&nbsp;<span class=\"hod2\">("+str(bus_arrival)+")</span></p><hr><p><span class=\"hod2\">Spoj: </span><span class=\"cas2\">"+bus_route+"</span></p><p>"+bus_agency+"</p><p><a href=\""+bus_agencyurl+"\">"+bus_agencyurl+"</a></p></div>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'red',opacity: 0.8,weight: 8});});</script>")
                
                elif div == "CAR": #print steps pro auto, stejny jak walk
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-car\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#f7f300;\">AUTO</h3>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'red',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                    else: 
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-car\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#f7f300;\">AUTO</h3>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'red',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                elif div == "BICYCLE": #print steps pro kolo, stejny jak walk
                    if (pocet_div1 % 2) != 0:
                        print("<div class=\"lichy1"+str(pocet_div1)+"\"><i class=\"fas fa-bicycle\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"lichy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#33ADFF;\">KOLO</h3>")
                        print("<script>$( \".lichy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'blue',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                    else:
                        print("<div class=\"sudy1"+str(pocet_div1)+"\"><i class=\"fas fa-bicycle\"></i> "+div_from+" -> "+div_to+" ["+div_fromtime+"-"+div_endtime+"]</div><div class=\"sudy1_steps"+str(pocet_div1)+"\"><h3 style=\"color:#33ADFF;\">KOLO</h3>")
                        print("<script>$( \".sudy1"+str(pocet_div1)+"\" ).mouseenter(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'yellow',opacity: 1,weight: 10});}).mouseleave(function() {polyline1"+str(pocet_div1)+".setStyle({color: 'blue',opacity: 0.8,weight: 8});});</script>")
                        
                        for x in range(len(data['plan']['itineraries'][1]['legs'][pocet_div1]['steps'])):
                            print("<p>"+step_direction["promenna%s" %x]+"&nbsp;&nbsp;Jeď po <b>"+str(step_streetname["promenna%s" %x])+"</b> "+str(step_dist["promenna%s" %x])+" metrů</p><hr>")
                            
                        print("</div>")
                        
                pocet_div1 = pocet_div1 + 1 #pomocna promenna pro vsechny dict   
            
            print("</div>") #ukonceni divu cesta
                        
            print('''<div class="cesta3">
                        <div class="cestaobrazky">
                            <span class="cestanadpis">
                            </span><br>
                        </div>
                        <div class="lichy">
                            <span class="cestanadpis">-------</span><br>
                        </div>
                        ''')

#=======================================================================================ITI 2 prázdná + ITI 3 prázdná                       
        else: #Pokud je 1 itinerary tak cesta 2 a cesta 3 je prazdna
            print('''<div class="cesta2">
                        <div class="cestaobrazky">
                            <span class="cestanadpis">
                            </span><br>
                        </div>
                        <div class="lichy">
                            <span class="cestanadpis">-------</span><br>
                        </div>
                        </div>''')
                        
            #div cesta3 pro iti 3
            print('''<div class="cesta3">
                        <div class="cestaobrazky">
                            <span class="cestanadpis">
                            </span><br>
                        </div>
                        <div class="lichy">
                            <span class="cestanadpis">-------</span><br>
                        </div>
                        ''')
                    
    else: #vychozi div kdyz neni cesta  
        print('''</span><br>
                </div>
                <div class="lichy">
                    <span class="cestanadpis">-------</span><br>
                </div>''')         
        
else: #pokud neexistuje cesta, tak se vypise varovný div
    print(''' <div class="cesta">
            <div class="neexistuje">
                <span class="cestanadpis">CESTU SE NEPODAŘILO NAJÍT<br>Cestu lze zobrazit jen uvnitř polygonu</span><br>
            </div>''')
    
print('''		</div>
		
		<div class="paticka">
        <br>
		<p>Created by Michal Potočiar &copy, 2022</p>
        <p style="font-size: 10px;"><a href="https://www.flaticon.com/free-icons/download" title="download icons">Download icons created by Roundicons Premium - Flaticon</a></p>
		</div>
        
  </div>

  <div class="column pravy""><div id="map"  style="width: 100%; height: 100vh;"></div></div>
</div>

<script src="../bakacss/kraj.json" type="text/javascript"></script>


<script>
    //PROMENNE PRO POCATECNI A KONCOVE BODY
    var pocatecnibod, konecnybod, pocatecnibod1, konecnybod1 = {}; 
    
    //PODKALDOVE MAPY
	var mapycz = new L.tileLayer('http://m{s}.mapserver.mapy.cz/base-m/{z}-{x}-{y}',{ident:'mapycz', attribution:'&copy;Seznam.cz a.s., | &copy;OpenStreetMap <a href="http://mapy.cz"><img class="print" target="_blank" src="//api.mapy.cz/img/api/logo.png" style="cursor: pointer; position:relative;top: 5px;"></a>',maxZoom:21,subdomains:"1234"});


	var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
		
	var grayscale   = L.tileLayer(mbUrl, {id: 'mapbox/light-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr}),
		streets  = L.tileLayer(mbUrl, {id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
    
    
    //BARVY A NASTAVENÍ BODŮ
    var greenIcon = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    
    var redIcon = new L.Icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    });
    
    //FUNKCE 
  
    //POCATECNI BOD
      function startPoint (e) {
      
        //Vymazaní bodu po pridani noveho
        if (pocatecnibod != undefined) {
              map.removeLayer(pocatecnibod);
        };
        
        //Vymazani vyvtoreneho bodu po kliknuti pravym a vybrani noveho bodu
        if (map.hasLayer(pocatecnibod1)) {
              map.removeLayer(pocatecnibod1);
        };
        
        pocatecnibod = L.marker(e.latlng,{
        draggable: true,
        icon: greenIcon
        }).addTo(map);
        
        //PRENESENI SOURADNIC DO FORMULARE
        document.getElementById('odkud1').value = pocatecnibod.getLatLng().lat.toFixed(5) + ", " + pocatecnibod.getLatLng().lng.toFixed(5);
        
        pocatecnibod.on('dragend', function (e) {
        document.getElementById('odkud1').value = pocatecnibod.getLatLng().lat.toFixed(5) + ", " + pocatecnibod.getLatLng().lng.toFixed(5);
        });
      }
      
      //KONECNY BOD
      function endPoint (e) {
      
        if (konecnybod != undefined) {
              map.removeLayer(konecnybod);
        };
        
        if (map.hasLayer(konecnybod1)) {
              map.removeLayer(konecnybod1);
        };
        
        konecnybod = L.marker(e.latlng,{
        draggable: true,
        icon: redIcon
        }).addTo(map);
        
        document.getElementById('kam1').value = konecnybod.getLatLng().lat.toFixed(5) + ", " + konecnybod.getLatLng().lng.toFixed(5);
        
        konecnybod.on('dragend', function (e) {
        document.getElementById('kam1').value = konecnybod.getLatLng().lat.toFixed(5) + ", " + konecnybod.getLatLng().lng.toFixed(5);
        });
    
      }

      function zoomIn (e) {
	      map.zoomIn();
      }

      function zoomOut (e) {
	      map.zoomOut();
      }
    
      //NASTAVENÍ MAPY
      var map = L.map('map', {
           center: [49.181884, 16.58952],
           zoom: 9,
           maxZoom: 18,
           layers: [mapycz], 
           contextmenu: true,
           contextmenuWidth: 140,
           contextmenuItems: [{
            text: 'Počáteční bod',
            callback: startPoint
        }, {
            text: 'Konečný bod',
            callback: endPoint
        }, '-', {
            text: 'Zoom in',
            callback: zoomIn
        }, {
            text: 'Zoom out',
            callback: zoomOut
        }]
        });
        
        
        $(function() {
            $('#odkudbutton').click(function () {
                
                $.get("https://nominatim.openstreetmap.org/search?format=json&accept-language=cs&q="+$('#odkud1').val(),
                function( data ) {
                    if (data != "") {
                        lat = data[0]["lat"];
                        lon = data[0]["lon"];
                        
                        if (pocatecnibod != undefined) {
                            map.removeLayer(pocatecnibod);
                        }
                        
                        if (map.hasLayer(pocatecnibod1)) {
                              map.removeLayer(pocatecnibod1);
                        };
                        
                        pocatecnibod = L.marker([lat,lon],{
                            draggable: true,
                            icon: greenIcon
                            }).addTo(map);
                            
                        document.getElementById('odkud1').value = pocatecnibod.getLatLng().lat.toFixed(5) + ", " + pocatecnibod.getLatLng().lng.toFixed(5);
        
                        pocatecnibod.on('dragend', function (e) {
                        document.getElementById('odkud1').value = pocatecnibod.getLatLng().lat.toFixed(5) + ", " + pocatecnibod.getLatLng().lng.toFixed(5);});
                        
                        map.setView([lat,lon],13)
                        
                } else {
                alert("Adresa nenalezena!");
                }
                });
            });
        });
        
         $(function() {
            $('#kambutton').click(function () {
                $.get("https://nominatim.openstreetmap.org/search?format=json&accept-language=cs&q="+$('#kam1').val(),
                function( data ) {
                    if (data != "") {
                        lat = data[0]["lat"];
                        lon = data[0]["lon"];
                        
                        if (konecnybod != undefined) {
                            map.removeLayer(konecnybod);
                        }
                        
                        if (map.hasLayer(konecnybod1)) {
                              map.removeLayer(konecnybod1);
                        };
                        
                        konecnybod = L.marker([lat,lon],{
                            draggable: true,
                            icon: redIcon
                            }).addTo(map);
                            
                        document.getElementById('kam1').value = konecnybod.getLatLng().lat.toFixed(5) + ", " + konecnybod.getLatLng().lng.toFixed(5);
        
                        konecnybod.on('dragend', function (e) {
                        document.getElementById('kam1').value = konecnybod.getLatLng().lat.toFixed(5) + ", " + konecnybod.getLatLng().lng.toFixed(5);});
                        
                        map.setView([lat,lon],13)
                        
                } else {
                alert("Adresa nenalezena!");
                }
                });
            });
        });
''')

if s1:   #Zobrazení cesty v mapě  
    
    #====================================================Polyline pro iti 1 + 2 + 3
    if len(data['plan']['itineraries']) > 2:    
        #cyklus, který do dictionary uloží souradnice jednotlivých korku
        for iti in data['plan']['itineraries'][0]['legs']:
            dict_souradnice["promenna%s" %pocet_souradnice] = str(polyline.decode(iti['legGeometry']['points']))
            dict_souradnice["promenna%s" %pocet_souradnice] = dict_souradnice["promenna%s" %pocet_souradnice].replace("(","[")
            dict_souradnice["promenna%s" %pocet_souradnice] = dict_souradnice["promenna%s" %pocet_souradnice].replace(")","]")
            pocet_souradnice = pocet_souradnice + 1 #pomocna prommena pro pocet
        
        #cyklus, který do dictionary uloží barvy podle modu cesty
        for iti in data['plan']['itineraries'][0]['legs']:
            color = iti['mode']
            if color == "WALK":
                dict_barva["promenna%s" %pocet_color] = "gray"
            elif color == "BUS":
                dict_barva["promenna%s" %pocet_color] = "green"
            elif color == "TRAM":
                dict_barva["promenna%s" %pocet_color] = "orange"
            elif color == "RAIL":
                dict_barva["promenna%s" %pocet_color] = "red"
            elif color == "CAR":
                dict_barva["promenna%s" %pocet_color] = "yellow"
            elif color == "BICYCLE":
                dict_barva["promenna%s" %pocet_color] = "blue"
            else:
                dict_barva["promenna%s" %pocet_color] = "black"
            pocet_color = pocet_color + 1 #pomocna prommena pro pocet
        
        #cyklus, který vytvori dictionary s JS promenyma (var polyline) a nasledne je vypise
        for x in range(len(data['plan']['itineraries'][0]['legs'])):
            dict_cesta["promenna%s" %x] = "var polyline"+str(x)+" = L.polyline("+dict_souradnice["promenna"+str(x)]+", {color: '"+dict_barva["promenna%s" %str(x)]+"', weight: 8, opacity: 0.8}).addTo(map);"
            print(dict_cesta["promenna"+str(x)])
    #-------------------------------------------------------------------------
    
        #cyklus, který do dictionary uloží souradnice jednotlivých korku
        for iti in data['plan']['itineraries'][1]['legs']:
            dict_souradnice["promenna%s" %pocet_souradnice1] = str(polyline.decode(iti['legGeometry']['points']))
            dict_souradnice["promenna%s" %pocet_souradnice1] = dict_souradnice["promenna%s" %pocet_souradnice1].replace("(","[")
            dict_souradnice["promenna%s" %pocet_souradnice1] = dict_souradnice["promenna%s" %pocet_souradnice1].replace(")","]")
            pocet_souradnice1 = pocet_souradnice1 + 1 #pomocna prommena pro pocet
        
        #cyklus, který do dictionary uloží barvy podle modu cesty
        for iti in data['plan']['itineraries'][1]['legs']:
            color = iti['mode']
            if color == "WALK":
                dict_barva["promenna%s" %pocet_color1] = "gray"
            elif color == "BUS":
                dict_barva["promenna%s" %pocet_color1] = "green"
            elif color == "TRAM":
                dict_barva["promenna%s" %pocet_color1] = "orange"
            elif color == "RAIL":
                dict_barva["promenna%s" %pocet_color1] = "red"
            elif color == "CAR":
                dict_barva["promenna%s" %pocet_color1] = "yellow"
            elif color == "BICYCLE":
                dict_barva["promenna%s" %pocet_color1] = "blue"
            else:
                dict_barva["promenna%s" %pocet_color1] = "black"
            pocet_color1 = pocet_color1 + 1 #pomocna prommena pro pocet
        
        #cyklus, který vytvori dictionary s JS promenyma (var polyline) a nasledne je vypise
        for x in range(len(data['plan']['itineraries'][1]['legs'])):
            dict_cesta["promenna%s" %x] = "var polyline1"+str(x)+" = L.polyline("+dict_souradnice["promenna"+str(x)]+", {color: '"+dict_barva["promenna%s" %str(x)]+"', weight: 8, opacity: 0.8}).addTo(map);"
            print(dict_cesta["promenna"+str(x)])
    #------------------------------------------------------------------------- 
    
        #cyklus, který do dictionary uloží souradnice jednotlivých korku
        for iti in data['plan']['itineraries'][2]['legs']:
            dict_souradnice["promenna%s" %pocet_souradnice2] = str(polyline.decode(iti['legGeometry']['points']))
            dict_souradnice["promenna%s" %pocet_souradnice2] = dict_souradnice["promenna%s" %pocet_souradnice2].replace("(","[")
            dict_souradnice["promenna%s" %pocet_souradnice2] = dict_souradnice["promenna%s" %pocet_souradnice2].replace(")","]")
            pocet_souradnice2 = pocet_souradnice2 + 1 #pomocna prommena pro pocet
        
        #cyklus, který do dictionary uloží barvy podle modu cesty
        for iti in data['plan']['itineraries'][2]['legs']:
            color = iti['mode']
            if color == "WALK":
                dict_barva["promenna%s" %pocet_color2] = "gray"
            elif color == "BUS":
                dict_barva["promenna%s" %pocet_color2] = "green"
            elif color == "TRAM":
                dict_barva["promenna%s" %pocet_color2] = "orange"
            elif color == "RAIL":
                dict_barva["promenna%s" %pocet_color2] = "red"
            elif color == "CAR":
                dict_barva["promenna%s" %pocet_color2] = "yellow"
            elif color == "BICYCLE":
                dict_barva["promenna%s" %pocet_color2] = "blue"
            else:
                dict_barva["promenna%s" %pocet_color2] = "black"
            pocet_color2 = pocet_color2 + 1 #pomocna prommena pro pocet
        
        #cyklus, který vytvori dictionary s JS promenyma (var polyline) a nasledne je vypise
        for x in range(len(data['plan']['itineraries'][2]['legs'])):
            dict_cesta["promenna%s" %x] = "var polyline2"+str(x)+" = L.polyline("+dict_souradnice["promenna"+str(x)]+", {color: '"+dict_barva["promenna%s" %str(x)]+"', weight: 8, opacity: 0.8}).addTo(map);"
            print(dict_cesta["promenna"+str(x)])
            
    #====================================================Polyline pro iti 1 + 2 
    elif len(data['plan']['itineraries']) == 2:
        #cyklus, který do dictionary uloží souradnice jednotlivých korku
        for iti in data['plan']['itineraries'][0]['legs']:
            dict_souradnice["promenna%s" %pocet_souradnice] = str(polyline.decode(iti['legGeometry']['points']))
            dict_souradnice["promenna%s" %pocet_souradnice] = dict_souradnice["promenna%s" %pocet_souradnice].replace("(","[")
            dict_souradnice["promenna%s" %pocet_souradnice] = dict_souradnice["promenna%s" %pocet_souradnice].replace(")","]")
            pocet_souradnice = pocet_souradnice + 1 #pomocna prommena pro pocet
        
        #cyklus, který do dictionary uloží barvy podle modu cesty
        for iti in data['plan']['itineraries'][0]['legs']:
            color = iti['mode']
            if color == "WALK":
                dict_barva["promenna%s" %pocet_color] = "gray"
            elif color == "BUS":
                dict_barva["promenna%s" %pocet_color] = "green"
            elif color == "TRAM":
                dict_barva["promenna%s" %pocet_color] = "orange"
            elif color == "RAIL":
                dict_barva["promenna%s" %pocet_color] = "red"
            elif color == "CAR":
                dict_barva["promenna%s" %pocet_color] = "yellow"
            elif color == "BICYCLE":
                dict_barva["promenna%s" %pocet_color] = "blue"
            else:
                dict_barva["promenna%s" %pocet_color] = "black"
            pocet_color = pocet_color + 1 #pomocna prommena pro pocet
        
        #cyklus, který vytvori dictionary s JS promenyma (var polyline) a nasledne je vypise
        for x in range(len(data['plan']['itineraries'][0]['legs'])):
            dict_cesta["promenna%s" %x] = "var polyline"+str(x)+" = L.polyline("+dict_souradnice["promenna"+str(x)]+", {color: '"+dict_barva["promenna%s" %str(x)]+"', weight: 8, opacity: 0.8}).addTo(map);"
            print(dict_cesta["promenna"+str(x)])         
    #-------------------------------------------------------------------------
    
        #cyklus, který do dictionary uloží souradnice jednotlivých korku
        for iti in data['plan']['itineraries'][1]['legs']:
            dict_souradnice["promenna%s" %pocet_souradnice1] = str(polyline.decode(iti['legGeometry']['points']))
            dict_souradnice["promenna%s" %pocet_souradnice1] = dict_souradnice["promenna%s" %pocet_souradnice1].replace("(","[")
            dict_souradnice["promenna%s" %pocet_souradnice1] = dict_souradnice["promenna%s" %pocet_souradnice1].replace(")","]")
            pocet_souradnice1 = pocet_souradnice1 + 1 #pomocna prommena pro pocet
        
        #cyklus, který do dictionary uloží barvy podle modu cesty
        for iti in data['plan']['itineraries'][1]['legs']:
            color = iti['mode']
            if color == "WALK":
                dict_barva["promenna%s" %pocet_color1] = "gray"
            elif color == "BUS":
                dict_barva["promenna%s" %pocet_color1] = "green"
            elif color == "TRAM":
                dict_barva["promenna%s" %pocet_color1] = "orange"
            elif color == "RAIL":
                dict_barva["promenna%s" %pocet_color1] = "red"
            elif color == "CAR":
                dict_barva["promenna%s" %pocet_color1] = "yellow"
            elif color == "BICYCLE":
                dict_barva["promenna%s" %pocet_color1] = "blue"
            else:
                dict_barva["promenna%s" %pocet_color1] = "black"
            pocet_color1 = pocet_color1 + 1 #pomocna prommena pro pocet
        
        #cyklus, který vytvori dictionary s JS promenyma (var polyline) a nasledne je vypise
        for x in range(len(data['plan']['itineraries'][1]['legs'])):
            dict_cesta["promenna%s" %x] = "var polyline1"+str(x)+" = L.polyline("+dict_souradnice["promenna"+str(x)]+", {color: '"+dict_barva["promenna%s" %str(x)]+"', weight: 8, opacity: 0.8}).addTo(map);"
            print(dict_cesta["promenna"+str(x)])
            
    #====================================================Polyline pro iti 1   
    else:
        #cyklus, který do dictionary uloží souradnice jednotlivých korku
        for iti in data['plan']['itineraries'][0]['legs']:
            dict_souradnice["promenna%s" %pocet_souradnice] = str(polyline.decode(iti['legGeometry']['points']))
            dict_souradnice["promenna%s" %pocet_souradnice] = dict_souradnice["promenna%s" %pocet_souradnice].replace("(","[")
            dict_souradnice["promenna%s" %pocet_souradnice] = dict_souradnice["promenna%s" %pocet_souradnice].replace(")","]")
            pocet_souradnice = pocet_souradnice + 1 #pomocna prommena pro pocet
        
        #cyklus, který do dictionary uloží barvy podle modu cesty
        for iti in data['plan']['itineraries'][0]['legs']:
            color = iti['mode']
            if color == "WALK":
                dict_barva["promenna%s" %pocet_color] = "gray"
            elif color == "BUS":
                dict_barva["promenna%s" %pocet_color] = "green"
            elif color == "TRAM":
                dict_barva["promenna%s" %pocet_color] = "orange"
            elif color == "RAIL":
                dict_barva["promenna%s" %pocet_color] = "red"
            elif color == "CAR":
                dict_barva["promenna%s" %pocet_color] = "yellow"
            elif color == "BICYCLE":
                dict_barva["promenna%s" %pocet_color] = "blue"
            else:
                dict_barva["promenna%s" %pocet_color] = "black"
            pocet_color = pocet_color + 1 #pomocna prommena pro pocet
        
        #cyklus, který vytvori dictionary s JS promenyma (var polyline) a nasledne je vypise
        for x in range(len(data['plan']['itineraries'][0]['legs'])):
            dict_cesta["promenna%s" %x] = "var polyline"+str(x)+" = L.polyline("+dict_souradnice["promenna"+str(x)]+", {color: '"+dict_barva["promenna%s" %str(x)]+"', weight: 8, opacity: 0.8}).addTo(map);"
            print(dict_cesta["promenna"+str(x)])
    #-------------------------------------------------------------------------        
            
    print("map.fitBounds([["+odkudd+"],["+kamm+"]]);") #Zoom na cestu, respektive na pocatecni a konecny bod.
    
    #Vytvoření bodů na koncích linie a prepis jejich souradnic do formulare
    print("pocatecnibod1 = L.marker(["+odkudd+"],{draggable: true, icon: greenIcon}).addTo(map);")
    print("konecnybod1 = L.marker(["+kamm+"],{draggable: true, icon: redIcon}).addTo(map);")
    print(''' 
        document.getElementById('odkud1').value = pocatecnibod1.getLatLng().lat.toFixed(5) + ", " + pocatecnibod1.getLatLng().lng.toFixed(5);
        
        pocatecnibod1.on('dragend', function (e) {
        document.getElementById('odkud1').value = pocatecnibod1.getLatLng().lat.toFixed(5) + ", " + pocatecnibod1.getLatLng().lng.toFixed(5);
        });
        
        document.getElementById('kam1').value = konecnybod1.getLatLng().lat.toFixed(5) + ", " + konecnybod1.getLatLng().lng.toFixed(5);
        
        konecnybod1.on('dragend', function (e) {
        document.getElementById('kam1').value = konecnybod1.getLatLng().lat.toFixed(5) + ", " + konecnybod1.getLatLng().lng.toFixed(5);
        
        });
        
    ''')
    
print('''    
    L.geoJSON(jmkraj, {
    style: myStyle
    }).addTo(map);
    
    L.Control.geocoder({position: 'topleft', errorMessage: 'Adresu se nepodařilo najít', placeholder: ' Zadej adresu (obec, ulice, č.p.)', expand: 'touch', collapsed: true}).addTo(map);

    
    
    //PODKLADOVE MAPY
	var baseLayers = {
        "Mapy.cz": mapycz,
        "Grayscale": grayscale,
        "OSM": streets
	};


	L.control.layers(baseLayers).addTo(map);
</script>

	</body>
</html>



''')


