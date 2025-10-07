from datetime import datetime


def remove_temperature_signs(temperature):
    return temperature.str.slice(3)


def generate_datetime(year, month, days_of_month, time):
    date_string = f"{year}-{month}-{days_of_month} {time}"
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M")


def find_element(element, class_name):
    return (
        element.find("div", class_=class_name).get_text(strip=True)
        if element.find("div", class_=class_name)
        else None
    )


def get_year_from_date(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").year
