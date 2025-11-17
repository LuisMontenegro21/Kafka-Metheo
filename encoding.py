import math

DIR_TO_CODE = {
    "N": 0,
    "NO": 1,
    "O": 2,
    "SO": 3,
    "S": 4,
    "SE": 5,
    "E": 6,
    "NE": 7,
}

CODE_TO_DIR = {v: k for k, v in DIR_TO_CODE.items()}

def encode(data: dict) -> bytes:
    '''
    converts JSON to bytes
    '''
    temp = float(data["temperatura"])
    hum = int(data["humedad"])
    wind = data["direccion_viento"]

    temp_q = int(round(temp * 2))
    dir_code = DIR_TO_CODE[wind]

    # check ranges
    if temp_q > 0xFF:
        raise ValueError("temp_q fuera de rango para 8 bits")
    if hum > 0x7F:
        raise ValueError("humedad fuera de rango para 7 bits")
    if dir_code > 0x7:
        raise ValueError("dir_code fuera de rango para 3 bits")
    
    # bitwise operation
    packed = (temp_q << 16) | (hum << 9) | (dir_code << 6)

    return packed.to_bytes(3, byteorder="big")


def decode(payload: bytes) -> dict:
    '''
    converts bytes back to JSON
    '''
    if len(payload) != 3:
        raise ValueError("Payload must be exactly 3 bytes")
    
    val = int.from_bytes(payload, byteorder="big")
    # bitwise operations to turn back to int 
    temp_q = (val >> 16) & 0xFF      
    hum    = (val >> 9)  & 0x7F      
    dir_code = (val >> 6) & 0x7      

    # turn back precision 
    temp = temp_q / 2.0 
    wind = CODE_TO_DIR[dir_code]

    return {
        "temperatura" : temp,
        "humedad" : hum,
        "direccion_viento" : wind
    }

