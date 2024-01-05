class Address:
    def __init__(self, address_line_1: str, address_line_2: str, city: str, state: str, zipcode: str, person_id: int):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.person_id = person_id