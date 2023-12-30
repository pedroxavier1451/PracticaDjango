import sys

sys.path.append(".")
from django.shortcuts import render
from appEnfermedadesCardiacas.Logica import modelo #para utilizar el método inteligente
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse

class Clasificacion():
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
            restingelectro = int(request.POST.get('electrocardiograma'))
            maxheartrate = float(request.POST.get('frecuencia_cardiaca'))
            exerciseangina = int(''+request.POST.get('angina_inducida'))
            oldpeak = float(''+request.POST.get('oldpeak_st'))
            slope = int(''+request.POST.get('pendiente_st'))
            noofmajorvessels = int(''+request.POST.get('num_vasos'))
            #Consumo de la lógica para predecir si se aprueba o no el crédito
            modelo = modelo()
            print("Creo la clase modeloSNN")
            resul=modelo.predecirNuevoCliente(age=age,gender=gender,restingBP=restingBP,serumcholestrol=serumcholestrol,fastingbloodsugar=fastingbloodsugar,chestpain=chestpain,restingelectro=restingelectro,maxheartrate=maxheartrate,exerciseangina=exerciseangina,oldpeak=oldpeak,slope=slope,noofmajorvessels=noofmajorvessels)
        except:
            resul='Datos inválidos'
        return render(request, "informe.html",{"e":resul})
    
    @csrf_exempt
    @api_view(['GET','POST'])
    def predecirIOJson2(request):
        print(request)
        print('***********************************************')
        print(request.body)
        print('***********************************************')
        body = json.loads(request.body.decode('utf-8'))
        #Formato de datos de entrada
        age = int(body.get("age"))
        gender = int(body.get("gender"))
        restingBP = float(body.get("restingBP"))
        serumcholestrol = float(body.get("serumcholestrol"))
        fastingbloodsugar= int(body.get("fastingbloodsugar"))
        chestpain=int(body.get("chestpain"))
        restingelectro = int(body.get("restingelectro"))
        maxheartrate = float(body.get("maxheartrate"))
        exerciseangina = int(body.get("exerciseangina"))
        oldpeak = float(body.get("oldpeak"))
        slope= int(body.get("slope"))
        noofmajorvessels=int(body.get("noofmajorvessels"))
        print(age)
        print(gender)
        print(restingBP)
        print(serumcholestrol)
        print(fastingbloodsugar)
        print(chestpain)
        print(restingelectro)
        print(maxheartrate)
        print(exerciseangina)
        print(oldpeak)
        print(slope)
        print(noofmajorvessels)
        modelo = modelo()
        resul = modelo.predecirNuevoCliente(modelo,age=age,gender=gender,restingBP=restingBP,serumcholestrol=serumcholestrol,fastingbloodsugar=fastingbloodsugar,chestpain=chestpain,restingelectro=restingelectro,maxheartrate=maxheartrate,exerciseangina=exerciseangina,oldpeak=oldpeak,slope=slope,noofmajorvessels=noofmajorvessels)  
        
        data = {'result': resul}
        resp=JsonResponse(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp