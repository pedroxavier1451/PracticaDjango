import sys

sys.path.append(".")
from django.shortcuts import render
from appEnfermedadesCardiacas.Logica.modelo_enfermedad import ModeloEnfermedad #para utilizar el método inteligente
from appEnfermedadesCardiacas.Logica import modelo_enfermedad
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse

def determinarEnfermedad(request):
    return render(request, "formularioPaciente.html")

@api_view(['GET','POST'])
def predecir2(request):
    try:
        #Formato de datos de entrada
        print("Entro al request")
        age = int(request.POST.get('edad'))
        gender = int(request.POST.get('genero'))
        restingBP = float(request.POST.get('presion_arterial'))
        serumcholestrol = float(''+request.POST.get('colesterol'))
        fastingbloodsugar = int(''+request.POST.get('glucosa'))
        chestpain = int(request.POST.get('tipo_dolor'))
        restingrelectro = int(request.POST.get('electrocardiograma'))
        maxheartrate = float(request.POST.get('frecuencia_cardiaca'))
        exerciseangia = int(''+request.POST.get('angina_inducida'))
        oldpeak = float(''+request.POST.get('oldpeak_st'))
        slope = int(''+request.POST.get('pendiente_st'))
        noofmajorvessels = int(''+request.POST.get('num_vasos'))
        modelo = request.POST.get('modelo')
        #Consumo de la lógica para predecir si se aprueba o no el crédito
        print("MODELO SELECCIONADO: ", modelo)
        resul=ModeloEnfermedad.predecirNuevoPaciente(modelo=modelo, age=age,gender=gender,restingBP=restingBP,serumcholestrol=serumcholestrol,fastingbloodsugar=fastingbloodsugar,chestpain=chestpain,restingrelectro=restingrelectro,maxheartrate=maxheartrate,exerciseangia=exerciseangia,oldpeak=oldpeak,slope=slope,noofmajorvessels=noofmajorvessels)
    except Exception as e:
        print("Ocurrio un error: ", e)
        resul = ['ERROR', 'ERROR', 'ERROR']

    return render(request, "resultado.html",{"datos":resul})

@api_view(['GET','POST'])
def predecirNB(request):
    try:
        #Formato de datos de entrada
        print("Entro al request")
        age = int(request.POST.get('edad'))
        gender = int(request.POST.get('genero'))
        restingBP = float(request.POST.get('presion_arterial'))
        serumcholestrol = float(''+request.POST.get('colesterol'))
        fastingbloodsugar = int(''+request.POST.get('glucosa'))
        chestpain = int(request.POST.get('tipo_dolor'))
        restingrelectro = int(request.POST.get('electrocardiograma'))
        maxheartrate = float(request.POST.get('frecuencia_cardiaca'))
        exerciseangia = int(''+request.POST.get('angina_inducida'))
        oldpeak = float(''+request.POST.get('oldpeak_st'))
        slope = int(''+request.POST.get('pendiente_st'))
        noofmajorvessels = int(''+request.POST.get('num_vasos'))
        modelo = request.POST.get('modelo')
        print("MODELO SELECCIONADO: ", modelo)
        #Naive Bayes
        resul=modelo_enfermedad.ModeloEnfermedad.predecirNuevoPacienteNB(modelo_enfermedad.ModeloEnfermedad, age=age,gender=gender,restingBP=restingBP,serumcholestrol=serumcholestrol,fastingbloodsugar=fastingbloodsugar,chestpain=chestpain,restingrelectro=restingrelectro,maxheartrate=maxheartrate,exerciseangia=exerciseangia,oldpeak=oldpeak,slope=slope,noofmajorvessels=noofmajorvessels)
        #NBayes
    except Exception as e:
        print("Ocurrio un error: ", e)
        resul = ['ERROR', 'ERROR', 'ERROR']
        
    return render(request, "resultado.html",{"datos":resul})