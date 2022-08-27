

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """ Gets body mass index from the height (cm) and weight (kg) """
    return round(weight_kg / ((height_cm / 100.0) ** 2), 1)


def alcohol_grams_per_day(alcohol_units_per_week: float) -> float:
    """ Converts units per week to grams per day """
    GRAMS_PER_UNIT = 8
    DAYS_PER_WEEK = 7
    return round(alcohol_units_per_week * GRAMS_PER_UNIT / DAYS_PER_WEEK)
