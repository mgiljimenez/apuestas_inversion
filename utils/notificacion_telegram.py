import requests

token_telegram="" #token de telegram
chat_id_telegram="" #chat id de telegram

class send_message:
    """Esta clase se conecta a la API de Telegram y hace un POST de un mensaje"""
    def __init__(self):
        pass
    def enviar_notificacion(mensaje):
        """Envío de un mensaje concreto.
        -Input: mensaje
        -Output: Envío a telegram del mensaje"""
        requests.post("https://api.telegram.org/bot"+token_telegram+"/sendMessage",
                    data={"chat_id": chat_id_telegram, "text":mensaje, "parse_mode":"html"})
        print("Message sent OK")

class plantillas:
    """Esta clase contiene las plantillas usadas para el envío de notificaciones a telegram"""
    def __init__(self):
        pass
    def mensaje_inicio():
        """Mensaje de inicio. Se envío antes de enviar cada actualización al grupo como recordatorio"""
        mensaje = (f"""‼️ <strong><u>Nuevas oportunidades de apuesta</u></strong> ‼️
💡Se recuerda que el inversor debe comprobar siempre la veracidad de los datos y que la inversión la realiza asumiendo sus propios <b>riesgos y responsabilidad</b>💡""")
        return mensaje
    def enviar_mensaje_apuesta(casa1, mul1, casa2, mul2, evento, fecha, url, rentabilidad):
        """funcion que envia la plantilla para notificar al usuario una posibilidad de inversión rentable"""
        mensaje = (f"""‼️ <strong><u>Rentabilidad:</u></strong> {rentabilidad}
🏛️<b>Casa 1:</b> {casa1} : {mul1} 
🏛️<b>Casa 2:</b> {casa2} : {mul2} 
📅<b>Evento:</b> {evento}
📅<b>Fecha:</b> {fecha}
📅<b>Url:</b> {url}""")
        send_message.enviar_notificacion(mensaje)
 

## EJEMPLO DEL ENVÍO DE UNA NOTIFICACIÓN
# send_message.enviar_notificacion(plantillas.enviar_mensaje_apuesta("1xbet",3.1,"Bwin",1.95,"Futbol: Barcelona - Madrid","20/09/2023","www.ejemplo.com","19.7%"))