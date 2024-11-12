import openai
import re
import json
from services import whatsapp_integration as wssp

openai.api_key = 'sk-svcacct-olBaVIbpfoSeoKW0agDnqYBumeu25LRnVttXK5tObVIyYywSPC7DeU_yAxpkaBQBJT3BlbkFJGduWp3r4pHcgCzmxWGXRDz7AfIYjIMs6ATRIr0fPTpLoOuxoqIRMwhCxvA2AnMfVwA'

task_prompt = {
    "AirSeaLogistics": 
       f"""
Eres un asistente de operaciones en una empresa de logística especializada en comercio internacional. Tu tarea es revisar correos electrónicos y, basándote en el contenido del último correo que te proporcionaré, debes determinar qué proceso realizar. Sigue las siguientes reglas para identificar el tipo de tarea:

1. **CargoRateUpdate**: Si encuentras información relacionada con una actualización de tarifa en el costo de flete, ya sea en términos de peso (w) o volumen (m), como por ejemplo "costo de flete en w/m" o "tarifa por costo por volumen", asigna esta tarea.
2. **DeconsolidateInTon**: Si encuentras informacion sobre la desconsolidación o la descarga realizada en toneladas, asigna esta tarea.
3. **NoRecognition**: Si no encuentras una descripción clara sobre ninguna de las tareas anteriores, asigna esta categoría.


Devuelve **solo** los títulos de la tarea correspondiente en un arrelgo entre corchetes, separados por comas.
"""
}

specific_tasks_prompts = {
    "CargoRateUpdate": """
Eres un asistente de operaciones en una empresa de logística especializada en comercio internacional. Tu tarea es revisar correos electrónicos. Con base en la información que te proporcionaré, extrae los siguientes datos:
1. Número de referencia
2. Primer tarifario (con las tarifas por volumen)
3. Detalles de la carga: Peso (kg) y volumen (CBM)
4. Actualización de la tarifa: Identifica la tarifa de flete y determina cuál es la más conveniente. Si hay el costo de flete en W/M, donde:
	•	W = peso de la carga (Toneladas)
	•	M = volumen de la carga (CBM)
Debes usar el mayor valor entre el peso (W) y el volumen (M) para multiplicarlo por el costo W/M . Estima el valor con el primer tarifario y dime cuál tarifa resulta más conveniente.
5. Título del correo: Título completo del correo
6. Customer Service: Nombre de la persona de atención al cliente

Variables a extraer:
- Ref_number: Número de referencia
- final_rate: La tarifa de flete más conveniente 
- final_rate_currency: La moneda de final_rate
- last_rate: La tarifa de flete más cercana inicial
- last_rate_currency: La moneda de last_rate
- final_cost: Costo total de flete calculado
- final_cost_currency : La moneda de final_cost
- initial_usd_rate: Las tarifas de flete inicial
- update_usd_rate: Las tarifas actualizadas
- weight_kg: Peso de la carga en kg
- volume_cbm: Volumen de la carga en cbmx`
- Customer_Service: Nombre de atención al cliente
- generated_text : texto con el formato de salida deseado.
- final_usd_rate_is_major : Boolean. True si la tarifa de flete final es mayor a la La tarifa de flete más cercana inicial

Ejemplo de generated_text:
1. Número de referencia: S00045029
2. Primer tarifario:
   - USD 60 hasta 5 CBM
   - USD 65 hasta 10 CBM 
   - USD 70 hasta 15 CBM 
3. Detalles de la carga:
   - Peso (Kg): **weight_kg** 
   - Volumen (CBM): **volume_cbm**
4. Actualización de la tarifa:
   - La tarifa final es **final_rate** **final_rate_currency**, totalizando **final_cost** **final_cost_currency**
5. Customer Service: Mária Victoria Solis, AirSeaLogistics SAC
6. Título del correo : **Título del correo**

Entregame como salida un texto que contenga el json con todas las variables solicitadas. El texto solo debe mostrar el contenido dentro de las llaves. 
""", 
    "DeconsolidateInTon" : """

"""
 
}


VINCENT_NUMBER = "+51983569250"
# MSOLIS_NUMBER = "+51941395276"

def talk_ai(message):
    respuesta = openai.chat.completions.create(
        model="gpt-4o",
        messages=message,
        max_tokens= 400
    )
    return respuesta.choices[0].message.content



def deliver_tasks(company, mail):
    latest_mail = mail["latest_mail"]
    company_prompt = task_prompt[company] 
    # print (company_prompt)
    # print (f"Processing lastest mail ...{latest_mail}" )
    messages=[
            {"role": "system", "content": company_prompt},
            {"role": "user", "content": latest_mail}
              
              ]
    response = talk_ai(messages)
  
    specific_tasks = response.strip("[]").split(", ")
   
    for specific_task in specific_tasks:
        specific_task_prompt = specific_tasks_prompts[specific_task]
        print(f"Task: {specific_task}")

        messages=[
                {"role": "system", "content": specific_task_prompt},
                {"role": "user", "content": str(mail)}
                
                ]
        # print ("specific_task_prompt")

        response = talk_ai(messages)
        trimmed_content = re.search(r'\{(.*)\}', response, re.DOTALL).group(0)
        json_data = json.loads(trimmed_content)
        try:
            text_to_send = json_data['generated_text']
            print (text_to_send)

            if(json_data['final_usd_rate_is_major'] == True):

                text_to_send += "\nComo la tarifa es mayor, se le dará aviso al comercial asignado."
            else: 

                text_to_send += "\nComo la tarifa es menor o igual, no se le dará aviso al comercial asignado."
            
            print (text_to_send)
            
                
            wssp.send_whatsapp_message(text_to_send, VINCENT_NUMBER)
            # wssp.send_whatsapp_message(text_to_send, MSOLIS_NUMBER)


        except Exception as e:
            return f"Error accessing : {e}" 
        return json_data
              
        

