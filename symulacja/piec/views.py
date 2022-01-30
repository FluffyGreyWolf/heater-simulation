from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def configuration_view(request):
    powierzchnia = request.POST.get('powierzchnia')
    wysokosc = request.POST.get('wysokosc')
    moc = request.POST.get('moc')
    

    context = {"powierzchnia": powierzchnia, "wysokosc": wysokosc, "moc": moc}
    return render(request, "configuration.html", context)

def temperature_view(request):
    temperatura_docelowa = request.POST.get('temperatura_docelowa')
    powierzchnia = request.session.get('powierzchnia')
    wysokosc = request.session.get('wysokosc')
    moc = request.session.get('moc')
    

    context = {"temperatura_docelowa": temperatura_docelowa}
    return render(request, "temperature.html", context)

def ustaw_czas_view(request):
    czas = request.POST.get('czas')
    powierzchnia = request.session.get('powierzchnia')
    wysokosc = request.session.get('wysokosc')
    moc = request.session.get('moc')
    temperatura_docelowa = request.POST.get('temperatura_docelowa')

    context = {"czas": czas}
    return render(request, "ustaw_czas.html", context)


def menu_view(request):
    try:
        powierzchnia = int(request.POST.get('powierzchnia'))
        wysokosc = int(request.POST.get('wysokosc'))
        moc = int(request.POST.get('moc'))
    except:
        powierzchnia = request.session.get('powierzchnia')
        wysokosc = request.session.get('wysokosc')
        moc = request.session.get('moc')       
    try:
        temperatura_docelowa = int(request.POST.get('temperatura_docelowa'))
    except:
        temperatura_docelowa = request.session['temperatura_docelowa'] 
    try:
        czas = int(request.POST.get('czas'))
    except:
        czas = request.session['czas']
    

    request.session['powierzchnia'] = powierzchnia
    request.session['wysokosc'] = wysokosc
    request.session['moc'] = moc
    request.session['temperatura_docelowa'] = temperatura_docelowa
    request.session['czas'] = czas

    table = {    #[0] GESTOSC [1] CIEPLO WLASCIWE 
    "-20" : (1.377,10.072),        #[0] GESTOSC [1] CIEPLO WLASCIWE
    "-15" : (1.350,10.079),
    "-10" : (1.324,10.09),
    "-5" : (1.298,10.107),
    "0" : (1.273,10.131),
    "5" : (1.249,10.162),
    "10" : (1.225,10.205),
    "15" : (1.202,10.268),
    "20" : (1.179,10.339),
    "25" : (1.155,10.435),
    "30" : (1.131,10.586),
    "35" : (1.107,10.75),
    "40" : (1.082,10.999),
    "45" : (1.056,11.299),
    "50" : (1.028,11.711),
    "55" : (0.999,13.245),      
    }

    temperatura_startowa = 21
    objetosc = powierzchnia * wysokosc
    gestosc = float(table[str(round(temperatura_startowa/5)*5)][0])
    cieplo = float(table[str(round(temperatura_startowa/5)*5)][1]) # cieplo wlasciwe  
    masa_powietrzna = objetosc * gestosc
    potrzebne_cieplo = masa_powietrzna * cieplo * (temperatura_docelowa - temperatura_startowa)
    planowany_czas_grzania = potrzebne_cieplo / moc   # wynik w sekundach
    planowany_czas_grzania = round(planowany_czas_grzania, 0)
    zuzycie_pradu = moc * planowany_czas_grzania/3600
    planowany_czas_grzania_minuty = planowany_czas_grzania/60
    cieplo_na_minute = (temperatura_docelowa -temperatura_startowa)/planowany_czas_grzania_minuty # trzeba policzyć o ile wzrośnie temperatura w minutę

    context = {"czas": czas, "planowany_czas_grzania_minuty": planowany_czas_grzania_minuty, "zuzycie_pradu": zuzycie_pradu, "temperatura_docelowa": temperatura_docelowa }
    return render(request, "menu.html", context)

def on_view(request):
    powierzchnia = request.session.get('powierzchnia')
    wysokosc = request.session.get('wysokosc')
    moc = request.session.get('moc')
    temperatura_docelowa = request.session.get('temperatura_docelowa')
    planowany_czas_grzania_minutes = request.session.get('planowany_czas_grzania_minutes')

    table = {    #[0] GESTOSC [1] CIEPLO WLASCIWE 
        "-20" : (1.377,10.072),        #[0] GESTOSC [1] CIEPLO WLASCIWE
        "-15" : (1.350,10.079),
        "-10" : (1.324,10.09),
        "-5" : (1.298,10.107),
        "0" : (1.273,10.131),
        "5" : (1.249,10.162),
        "10" : (1.225,10.205),
        "15" : (1.202,10.268),
        "20" : (1.179,10.339),
        "25" : (1.155,10.435),
        "30" : (1.131,10.586),
        "35" : (1.107,10.75),
        "40" : (1.082,10.999),
        "45" : (1.056,11.299),
        "50" : (1.028,11.711),
        "55" : (0.999,13.245),      
        }
 
    temperatura_startowa = 21
    objetosc = powierzchnia * wysokosc
    gestosc = float(table[str(round(temperatura_startowa/5)*5)][0])
    cieplo = float(table[str(round(temperatura_startowa/5)*5)][1]) # cieplo wlasciwe  
    masa_powietrzna = objetosc * gestosc
    potrzebne_cieplo = masa_powietrzna * cieplo * (temperatura_docelowa - temperatura_startowa)
    planowany_czas_grzania = potrzebne_cieplo / moc   # wynik w sekundach
    planowany_czas_grzania = round(planowany_czas_grzania, 0)
    zuzycie_pradu = moc * planowany_czas_grzania/3600
    planowany_czas_grzania_minuty = planowany_czas_grzania/60
    cieplo_na_minute = (temperatura_docelowa - temperatura_startowa)/planowany_czas_grzania_minuty # trzeba policzyć o ile wzrośnie temperatura w minutę

    time_elapsed = 0
    temeprature = 21
    symulacja = []
    while planowany_czas_grzania_minuty > time_elapsed:
        time_elapsed += 1
        temeprature += cieplo_na_minute
        symulacja.append(f"Upłynęło {time_elapsed} minut - aktualna temperatura wynosi {round(temeprature, 2)} stopni C")
        if planowany_czas_grzania_minuty < time_elapsed:
            symulacja.append(f"\n Nagrzanie pomieszczenia zajęło {time_elapsed} minut")

    context = {"temperatura_docelowa": temperatura_docelowa, "planowany_czas_grzania_minuty": planowany_czas_grzania_minuty,"zuzycie_pradu": zuzycie_pradu, "symulacja": symulacja}
    return render(request, "on.html", context)

def czas_view(request):
    powierzchnia = request.session.get('powierzchnia')
    wysokosc = request.session.get('wysokosc')
    moc = request.session.get('moc')
    temperatura_docelowa = request.session.get('temperatura_docelowa')
    planowany_czas_grzania_minutes = request.session.get('planowany_czas_grzania_minutes')
    czas = request.session.get('czas')

    table = {    #[0] GESTOSC [1] CIEPLO WLASCIWE 
        "-20" : (1.377,10.072),        #[0] GESTOSC [1] CIEPLO WLASCIWE
        "-15" : (1.350,10.079),
        "-10" : (1.324,10.09),
        "-5" : (1.298,10.107),
        "0" : (1.273,10.131),
        "5" : (1.249,10.162),
        "10" : (1.225,10.205),
        "15" : (1.202,10.268),
        "20" : (1.179,10.339),
        "25" : (1.155,10.435),
        "30" : (1.131,10.586),
        "35" : (1.107,10.75),
        "40" : (1.082,10.999),
        "45" : (1.056,11.299),
        "50" : (1.028,11.711),
        "55" : (0.999,13.245),      
        }
 
    temperatura_startowa = 21
    objetosc = powierzchnia * wysokosc
    gestosc = float(table[str(round(temperatura_startowa/5)*5)][0])
    cieplo = float(table[str(round(temperatura_startowa/5)*5)][1]) # cieplo wlasciwe  
    masa_powietrzna = objetosc * gestosc
    potrzebne_cieplo = masa_powietrzna * cieplo * (temperatura_docelowa - temperatura_startowa)
    planowany_czas_grzania = potrzebne_cieplo / moc   # wynik w sekundach
    planowany_czas_grzania = round(planowany_czas_grzania, 0)
    zuzycie_pradu = moc * planowany_czas_grzania/3600
    planowany_czas_grzania_minuty = planowany_czas_grzania
    cieplo_na_minute = (temperatura_docelowa -temperatura_startowa)/planowany_czas_grzania_minuty # trzeba policzyć o ile wzrośnie temperatura w minutę

    time_elapsed = 0
    temeprature = 21
    symulacja = []
    print(planowany_czas_grzania)
    while planowany_czas_grzania_minuty > time_elapsed:
        time_elapsed += 1
        temeprature += cieplo_na_minute
        symulacja.append(f"Upłynęło {time_elapsed} minut - aktualna temperatura wynosi {round(temeprature, 2)} stopni C")
        if planowany_czas_grzania_minuty < time_elapsed:
            symulacja.append(f"\n Nagrzanie pomieszczenia zajęło {time_elapsed} minut")


    context = {"temperatura_docelowa": temperatura_docelowa, "planowany_czas_grzania_minutes": planowany_czas_grzania_minutes,"zuzycie_pradu": zuzycie_pradu, "symulacja": symulacja, "czas": czas, "moc": moc}
    return render(request, "czas.html", context)