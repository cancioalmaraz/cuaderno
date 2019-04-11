from django.shortcuts import render
import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample
from .models import worker, design

# Create your views here.
def index(request, ot):
    return render(request, "core/index.html", {'ot':ot})

def minutes(obj, oj):
    minutes = []
    codes = [w.code for w in worker.objects.all()]
    for jober in codes:
        ok = False
        hoursWorkeds = 0
        #print("Code: " + jober)
        for registers in obj.objects.filter(ot = oj):
            #print(str(registers))
            for workered in registers.worker.all():
                #print("Code view: " + workered.code)
                if workered.code == jober:
                    #print("Adherido!!")
                    hoursWorkeds += ( registers.hourf.hour - registers.houri.hour )*60 + (registers.hourf.minute - registers.houri.minute)
                    ok = True
        if ok:
            minutes.append(hoursWorkeds)
        else:
            minutes.append(0)
    return minutes

def clean(mnts, workers):
    w = []
    m = [] 

    for i in range(len(mnts)):
        if mnts[i] != 0:
            m.append(mnts[i])
            w.append(workers[i])

    return m, w

def percents(mnts, workers, total):

    for i in range(len(mnts)):
        percent = (mnts[i]*100)/total
        workers[i] += "\n" + str(percent)
    return workers

def graph(request, oj):

    workers = [w.name for w in worker.objects.all()]
    mnts= minutes(design, oj)
    totalMin = sum(mnts)

    mnts, workers = clean(mnts, workers)

    for i in range(len(mnts)):
        percent = (mnts[i]*100)/totalMin
        workers[i] += "\n" + str(percent) + " %"

    f = plt.figure()

    # Creamos los ejes
    axes = f.add_axes([0.1, 0.1, 0.75, 0.75]) # [left, bottom, width, height]
    axes.pie(mnts, labels = workers)
    axes.set_title("Estadistica\nTotal Tiempo Trabajado: " + str(totalMin) + " minutos.\nOrden de Trabajo: " + str(oj))

    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    f.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response