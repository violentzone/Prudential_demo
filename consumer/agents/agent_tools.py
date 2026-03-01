"""
Tool library for consumer agents
"""


def calculate_insurance_fee(age: int, annual_income: int, family_member: int, chronic_diseases: bool, frequent_flyer: bool, ever_travel_aboard: bool) -> float:
    """
    Calculate insurance fee by given information of a client
    :param age: Age of the client
    :param annual_income: Income of client annually
    :param family_member: Family member count of the client
    :param chronic_diseases: Does client had chronic disease
    :param frequent_flyer: Information of client that is experienced flyer
    :param ever_travel_aboard: Information that client had experience travelling aboard
    :return: Travel insurance fee best suits the client
    """
    base_premium = 3000
    age_factor = 1 + (age - 30) * 0.01
    family_factor = 1 + family_member * 0.02
    chronic_factor = 1.5 if chronic_diseases else 1
    fly_factor = 1.1 if frequent_flyer else 1
    travel_factor = 0.9 if ever_travel_aboard else 1
    income_factor = 1 + (annual_income/100000) * 0.05

    best_fee = base_premium * age_factor * family_factor * chronic_factor * fly_factor * travel_factor * income_factor
    return best_fee


def description_adder(person_info: dict, description_content) -> dict:
    """
    Adds a 'description' to existed dict
    :param person_info: Original information of a person
    :param description_content: Value to add to description key
    :return: Dict with description key-value pair
    """
    return person_info.update({'description': description_content})
