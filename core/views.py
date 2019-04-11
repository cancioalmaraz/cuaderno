from django.shortcuts import render
import io
import matplotlib.pyplot as plt
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample
from .models import worker, design

# Create your views here.
def index(request):
    return render(request, "core/index.html")

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

def graph(request):
 
    ot = 9996
    workers = [w.name for w in worker.objects.all()]
    mnts= minutes(design, ot)
    totalMin = sum(mnts)

    cont = 0
    for i in mnts:
        if i == 0:
            mnts.pop(cont)
            workers.pop(cont)
        cont = cont + 1


    f = plt.figure()

    # Creamos los ejes
    axes = f.add_axes([0.1, 0.1, 0.75, 0.75]) # [left, bottom, width, height]
    axes.pie(mnts, labels = workers)
    axes.set_title("Estadistica\nTotal Tiempo Trabajado: " + str(totalMin) + " minutos.\nOrden de Trabajo: " + str(ot))

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