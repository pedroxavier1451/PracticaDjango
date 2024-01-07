import os
from django.urls import reverse
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
#from appCreditoBanco.Logica import modeloSNN
import pickle
import keras

class ModeloEnfermedad:
    _modelo_red_neuronal = None
    _modelo_naive_bayes = None

    #Función para cargar preprocesador
    @staticmethod
    def cargarPipeline(nombreArchivo):
        with open(nombreArchivo, 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline
    
    #Función para cargar red neuronal 
    @staticmethod
    def cargarNN(nombreArchivo):  
        model = keras.models.load_model(nombreArchivo)
        print("Red Neuronal Cargada desde Archivo") 
        return model
    
    @staticmethod
    def cargar_naive_bayes(nombreArchivo):
        with open(nombreArchivo, 'rb') as file:
            modelo_cargado = pickle.load(file)
        return modelo_cargado
    
    def cargar_naive_bayes2(self, nombreArchivo):
        with open(nombreArchivo, 'rb') as file:
            modelo_cargado = pickle.load(file)
        return modelo_cargado
    
    def cargarPipeline2(self, nombreArchivo):
        with open(nombreArchivo, 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline
    
    def cargarPipeNB(self):
        try:
            print("cargando pipe")
            directorio_actual = os.path.abspath(os.path.dirname(__file__))
            #Se carga el Pipeline de Preprocesamiento
            nombreArchivoPreprocesador= os.path.join(directorio_actual, 'Recursos','pipePreprocesadores.pickle')
            #nombreArchivoPreprocesador='Recursos/pipePreprocesadores.pickle'
            print(nombreArchivoPreprocesador)
            pipe=self.cargarPipeline2(self, nombreArchivoPreprocesador)
            print('Pipeline de Preprocesamiento Cargado')
            cantidadPasos=len(pipe.steps)
            print("Cantidad de pasos: ", cantidadPasos)
            print(pipe.steps)
            cantidadPasos=len(pipe.steps)
            print("Cantidad de pasos: ",cantidadPasos)
            print(pipe.steps)
            print('PIPE PARA NB CARGADO CORRECTAMENTE')
            return pipe
        except FileNotFoundError as e:
            print(f"Error archivo no encontrado: {e.filename}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        return None
    
    def cargarModeloNB(self):
        try:
            print("cargando modelo")
            directorio_actual = os.path.abspath(os.path.dirname(__file__))
            #Se carga el modelo
            modeloOptimizado=self.cargar_naive_bayes2(self , os.path.join(directorio_actual, 'Recursos', 'modeloNaiveBayesBase.pickle'))
            #Se integra la Red Neuronal al final del Pipeline
            return modeloOptimizado
        except FileNotFoundError as e:
            print(f"Error archivo no encontrado: {e.filename}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        return None
    
    #Función para integrar el preprocesador y la red neuronal en un Pipeline
    @staticmethod
    def cargarModelo(modelo):

        archivo_modelo = None

        if modelo == "red_neuronal":
            # verifica si el modelo ya esta cargado en la variable _modelo_red_neuronal
            if ModeloEnfermedad._modelo_red_neuronal is not None:
                print("Modelo ya esta cargado")
                return ModeloEnfermedad._modelo_red_neuronal

            archivo_modelo = 'modeloRedNeuronalBase.h5'

        if modelo == "naive_bayes":
            # verifica si el modelo ya esta cargado en la variable _modelo_naive_bayes
            if ModeloEnfermedad._modelo_naive_bayes is not None:
                print("Modelo ya esta cargado")
                return ModeloEnfermedad._modelo_naive_bayes

            archivo_modelo = 'modeloNaiveBayesBase.pkl'

        print(f"Cargando modelo: {modelo},  archivo : {archivo_modelo}")

        try:
            directorio_actual = os.path.abspath(os.path.dirname(__file__))
            #Se carga el Pipeline de Preprocesamiento
            nombreArchivoPreprocesador= os.path.join(directorio_actual, 'Recursos','pipePreprocesadores.pickle')
            #nombreArchivoPreprocesador='Recursos/pipePreprocesadores.pickle'
            pipe=ModeloEnfermedad.cargarPipeline(nombreArchivoPreprocesador)
            print('Pipeline de Preprocesamiento Cargado')
            cantidadPasos=len(pipe.steps)
            print("Cantidad de pasos: ", cantidadPasos)
            print(pipe.steps)

            if modelo == 'red_neuronal':

                #Se carga la Red Neuronal
                redNeuronal=ModeloEnfermedad.cargarNN(os.path.join(directorio_actual, 'Recursos', archivo_modelo))
                #modeloOptimizado=self.cargarNN(self,'Recursos/modeloRedNeuronalOptimizada.h5')
                #Se integra la Red Neuronal al final del Pipeline
                pipe.steps.append(['modelNN',redNeuronal])
                cantidadPasos=len(pipe.steps)
                print("Cantidad de pasos: ",cantidadPasos)
                print(pipe.steps)
                print('Red Neuronal integrada al Pipeline')

                # se guarda el modelo en una variable para cargar una sola vez los archivos pipeline y red neuronal
                ModeloEnfermedad._modelo_red_neuronal = pipe
                return ModeloEnfermedad._modelo_red_neuronal
            else:
                #Se carga la Naive Bayes
                naiveBayes=ModeloEnfermedad.cargarNN(os.path.join(directorio_actual, 'Recursos', archivo_modelo))
                #modeloOptimizado=self.cargarNN(self,'Recursos/modeloRedNeuronalOptimizada.h5')
                #Se integra la Red Neuronal al final del Pipeline
                pipe.steps.append(['modelNB',naiveBayes])
                cantidadPasos=len(pipe.steps)
                print("Cantidad de pasos: ",cantidadPasos)
                print(pipe.steps)
                print('Naive Bayes integrada al Pipeline')

                # se guarda el modelo en una variable para cargar una sola vez los archivos pipeline y red neuronal
                ModeloEnfermedad._modelo_naive_bayes  = pipe
                return ModeloEnfermedad._modelo_naive_bayes 

        except FileNotFoundError as e:
            print(f"Error archivo no encontrado: {e.filename}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        return None
    
    
    @staticmethod
    def obtener_resultados_certezas(prediccion):
        marca = None
        certeza = None
        nuevomax = 1
        nuevomin = 0

        if prediccion < 0.5:
            marca = '¡Felicidades! No tienes ninguna enfermedad cardíaca.'
            maxa = 0.5
            mina = 0
            certeza = 1 - ((prediccion - mina) / (maxa - mina) * (nuevomax - nuevomin) + nuevomin)
            certeza = str(int(certeza * 100)) + '%'

        elif prediccion >= 0.5:
            marca = 'Lo sentimos, se ha detectado una enfermedad cardíaca.'
            maxa = 1
            mina = 0.5
            certeza = (prediccion - mina) / (maxa - mina) * (nuevomax - nuevomin) + nuevomin
            certeza = str(int(certeza * 100)) + '%'

        return prediccion, marca, certeza
    
    @staticmethod
    def predecirNuevoPaciente(modelo='red_neuronal',age=40,gender=1,chestpain=0,restingBP=94,serumcholestrol=229,fastingbloodsugar=0,
                                                restingrelectro=1,maxheartrate=115,exerciseangia=0,oldpeak=3.7,slope=1,noofmajorvessels=1):
        cnames = ['age','gender','chestpain','restingBP','serumcholestrol','fastingbloodsugar','restingrelectro',
            'maxheartrate','exerciseangia','oldpeak','slope','noofmajorvessels']
        Xnew=[age,gender,chestpain,restingBP,serumcholestrol,fastingbloodsugar,restingrelectro,maxheartrate,exerciseangia,oldpeak,slope,noofmajorvessels]
        Xnew_Dataframe = pd.DataFrame(data=[Xnew],columns=cnames)
        print(Xnew_Dataframe)
        print("EMPIEZA A PREDECIR EL MODELO")
        pipe=ModeloEnfermedad.cargarModelo(modelo)
        pred = pipe.predict(Xnew_Dataframe)
        pred = pred.flatten()[0]# de 2D a 1D
        print(f"Prediccion realizada {modelo}")
        prediccion, marca, certeza = ModeloEnfermedad.obtener_resultados_certezas(pred)
        dataframe_final = pd.DataFrame({'Predicción': [prediccion], 'Resultado': [marca], 'Certeza': [certeza]})
        np.set_printoptions(formatter={'float': lambda x: "{0:0.0f}".format(x)})
        print(dataframe_final.head())
        lista_resultados = dataframe_final.iloc[0].tolist()
        return lista_resultados
    
    def predecirNuevoPacienteNB(self, age,gender,chestpain,restingBP,serumcholestrol,fastingbloodsugar,
                                                restingrelectro,maxheartrate,exerciseangia,oldpeak,slope,noofmajorvessels):

        cnames = ['age','gender','chestpain','restingBP','serumcholestrol','fastingbloodsugar','restingrelectro',
            'maxheartrate','exerciseangia','oldpeak','slope','noofmajorvessels']

        Xnew=[age,gender,chestpain,restingBP,serumcholestrol,fastingbloodsugar,restingrelectro,maxheartrate,exerciseangia,oldpeak,slope,noofmajorvessels]

        pipeNB = ModeloEnfermedad.cargarPipeNB(self)

        Xnew_Dataframe = pd.DataFrame(data=[Xnew],columns=cnames)
        #pipe=cargarPipeline("pipePreprocesadores")
        Xnew_Transformado=pipeNB.transform(Xnew_Dataframe)
        modelo=ModeloEnfermedad.cargarModeloNB(self)

        y_pred=modelo.predict(Xnew_Transformado)
        prediccion, marca, certeza= ModeloEnfermedad.obtener_resultados_certezas(y_pred)
        dataframe_final = pd.DataFrame({'Predicción': [prediccion], 'Resultado': [marca], 'Certeza': [certeza]})
        np.set_printoptions(formatter={'float': lambda x: "{0:0.0f}".format(x)})
        print(dataframe_final.head())
        lista_resultados = dataframe_final.iloc[0].tolist()
        return lista_resultados