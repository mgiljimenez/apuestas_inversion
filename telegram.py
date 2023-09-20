import requests
token="sdf"


def envio_notificacion(casa1, mul1,casa2, mul2,fecha_hora,rentabilidad):
    mensaje_plantilla=f"""
    Nueva oportunidad de apuesta:
    -Casa 1:{casa1} : {mul1}
    -Casa 2:{casa2} : {mul2}
    -Fecha:{fecha_hora}
    -Rentabilidad mínima:{rentabilidad}
    """

