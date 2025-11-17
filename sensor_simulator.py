import random as rand
DIRS = ["N", "NO", "O", "SO", "S", "SE", "E", "NE"]


def generate_weather_data() -> dict:
    '''
    Generate random weather values
    '''
    temp = rand.gauss(mu=55, sigma=15)
    temp = max(0, min(110, temp))
    temp = round(temp, 2) 

    hum = rand.gauss(mu=60, sigma=20)
    hum = max(0, min(100, hum))
    hum = int(round(hum))

    direction = rand.choice(DIRS)

    return {
        "temperatura" : temp,
        "humedad" : hum, 
        "direccion_viento" : direction
    }


if __name__ == '__main__':
    for _ in range(0, 5):
        print(generate_weather_data())