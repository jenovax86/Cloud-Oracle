def remove_temperature_sign(temperature):
    return temperature.str.slice(3)
