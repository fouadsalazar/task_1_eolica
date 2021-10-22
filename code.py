"# task_1_eolica" 
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
import plotly.graph_objects as go

def leer(año):
    datos = pd.read_csv('{}.txt'.format(año), sep=",")
    
    # Se arregla el formato de las fechas para poder trabajarlo
    datos["DATE (MM/DD/YYYY)"]= pd.to_datetime(datos["DATE (MM/DD/YYYY)"])
    datos['Año'] = datos["DATE (MM/DD/YYYY)"].dt.year
    datos['Mes'] = datos["DATE (MM/DD/YYYY)"].dt.month
    datos['Dia'] = datos["DATE (MM/DD/YYYY)"].dt.day
    
    # Se arregla el formato de las horas 
    hora=[]
    for i in range(len(datos)):
        hora.append(datetime.strptime(datos["MST"][i],"%H:%M"))
    datos['Hora'] = hora
    datos['Hora'] = datos["Hora"].dt.hour
    
    return(datos)


def corregir_datos(datos):
    columna=["Station Pressure [mBar]","Avg Wind Speed @ 2m [m/s]","Avg Wind Speed @ 5m [m/s]",
             "Avg Wind Speed @ 10m [m/s]","Avg Wind Speed @ 20m [m/s]","Avg Wind Speed @ 50m [m/s]",
             "Avg Wind Speed @ 80m [m/s]"]

    datos.fillna(0,inplace=True)
    
    for i in range(len(datos)):
        for j in range(len(columna)):
            if i > 0  and i < (len(datos)-1):
                if datos[columna[j]][i] < 0:
                    datos[columna[j]][i] = (datos[columna[j]][i-1] + datos[columna[j]][i+1])/2
    return (datos)


def graficas_de_mes(datos,año):
    datos_por_mes=datos.groupby(["Mes"]).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="Presion",x=datos_por_mes.index, y=datos_por_mes['Station Pressure [mBar]']))
    fig.update_layout(title = 'Presión mensual del año '+str(año),title_x=0.5,
                      xaxis = dict(tick0 = 1,dtick = 1),xaxis_title='Meses',yaxis_title='Presión [mBar]')
    fig.show()
    

    fig = go.Figure()
    vel_viento=[2,5,10,20,50,80]
    for i in range(len(vel_viento)):
        fig.add_trace(go.Scatter(name="Avg Wind Speed @ {}m [m/s]".format(vel_viento[i]),x=datos_por_mes.index, y=datos_por_mes["Avg Wind Speed @ {}m [m/s]".format(vel_viento[i])]))
    fig.update_layout(title = 'Velocidades del viento para el año '+str(año),title_x=0.5, xaxis_title='Meses',
                      xaxis = dict(tick0 = 1,dtick = 1),yaxis_title='V [m/s]')
    fig.show()
    
def datos_verano_invierno(datos,año,mes):
    datos_febrero=datos[(datos["Mes"] == mes)]
    if mes == 2:
        mes_a="febrero"
    else:
        mes_a="julio"
    # grafica por minuto
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="Velocidad",x=datos_febrero.index, y=datos_febrero['Avg Wind Speed @ 80m [m/s]']))
    fig.update_layout(title = 'Velocidades del viento por minuto de {} para el año {}'.format(mes_a,año),title_x=0.5, 
                      xaxis_title='Min', xaxis = dict(tick0 = 1),yaxis_title='V [m/s]')
    fig.show()
    
    # Grafica para un dia por hora
    datos_febrero_hora=datos_febrero.groupby(["Hora"]).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(name="Velocidad",x=datos_febrero_hora.index, y=datos_febrero_hora['Avg Wind Speed @ 80m [m/s]']))
    fig.update_layout(title = 'Velocidades del viento media diaria de {} para el año {}'.format(mes_a,año),title_x=0.5,
                      xaxis_title='Hora',xaxis = dict(tick0 = 1,dtick = 1),yaxis_title='V [m/s]')
    fig.show()
    

for i in [2017,2018,2019]:
    datos=leer(i)
    corregir_datos(datos)
    graficas_de_mes(datos,i)
    datos_verano_invierno(datos,i,2)
    datos_verano_invierno(datos,i,7)
    
fig = go.Figure()
mes = [2,7]
for i in [2017,2018,2019]:
    año=i
    datos=leer(i)
    corregir_datos(datos)
    
    for j in range(len(mes)):
        datos_febrero=datos[(datos["Mes"] == mes[j])]
        if mes[j] == 2:
            mes_a="febrero"
        else:
            mes_a="julio"

        # Grafica para un dia por hora
        datos_febrero_hora=datos_febrero.groupby(["Hora"]).mean()
        fig.add_trace(go.Scatter(name='{} - {}'.format(mes_a,año),
                                 x=datos_febrero_hora.index, y=datos_febrero_hora['Avg Wind Speed @ 80m [m/s]']))
        fig.update_layout(xaxis_title='Hora',xaxis = dict(tick0 = 1,dtick = 1),yaxis_title='V [m/s]')

fig.show()



import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=datos_febrero_hora.index, y=datos_febrero_hora['Avg Wind Speed @ 80m [m/s]'], name="V viento [m/s]"),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=datos_hora.index, y=datos_hora['dem'], name="Demanda [W]"),
    secondary_y=True,
)

# Add figure title
fig.update_layout(
    title_text="Valores diarios de Velocidad del viento y Demanda energetica para Febrero del 2019",title_x=0.5)

# Set x-axis title
fig.update_xaxes(title_text="Hora",tick0 = 1,dtick = 1)

# Set y-axes titles
fig.update_yaxes(title_text="Velocidad viento [m/s]", secondary_y=False)
fig.update_yaxes(title_text="Demanda [MW]", secondary_y=True)

fig.show()
