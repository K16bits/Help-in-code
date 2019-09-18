class Property:
    def __init__(self, square_feet='', beds='', baths='', **kwargs):
        super().__init__(**kwargs)
        self.square_feet = square_feet
        self.beds = beds
        self.baths = baths
        
    def display(self):
        print("DETALHES DA PROPRIEDADE")
        print("=======================")
        print("Tamanho em pés quadrados: {}".format(self.square_feet))
        print("Número de quartos: {}".format(self.beds))
        print("Número de banheiros: {}\n".format(self.baths))
        
    def prompt_init():#método de classe (método estático)
        return dict(square_feet=input("Entre com o tamanho em pés quadrados:"),
                   beds=input("Entre com o número de quartos:"),
                   baths=input("Entre com o número de banheiros:"))
    prompt_init = staticmethod(prompt_init)

class Apartment(Property):
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")
    
    def __init__(self, balcony='', laundry='', **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry
        
    def display(self):
        super().display()
        print("DETALHES DO APARTAMENTO")
        print("lavanderia: %s" % self.laundry)
        print("possui varanda: %s" % self.balcony)
        
    def prompt_init():
        parent_init = Property.prompt_init()
        laundry = ''
        while laundry.lower() not in Apartment.valid_laundries:
            laundry = input("Como é a lavanderia da "
                           "propriedade ? ({})".format(
                           ", ".join(Apartment.valid_laundries)))            
        balcony = ''
        while balcony.lower() not in Apartment.valid_balconies:
            balcony = input("A propriedade tem uma varanda? "
                           "({})".format(", ".join(Apartment.valid_balconies)))        
        parent_init.update({
            "laundry": laundry,
            "balcony": balcony
        })        
        return parent_init
    prompt_init = staticmethod(prompt_init)

def get_valid_input(input_string, valid_options):
    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response

class Apartment(Property):
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")
    
    def __init__(self, balcony='', laundry='', **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry
        
    def display(self):
        super().display()
        print("DETALHES DO APARTAMENTO")
        print("lavanderia: %s" % self.laundry)
        print("possui varanda: %s" % self.balcony)
        
    def prompt_init():
        parent_init = Property.prompt_init()
        laundry = get_valid_input("Como é a lavanderia da "
                           "propriedade ?", Apartment.valid_laundries)
        balcony = get_valid_input("A propriedade tem uma varanda? ",
                           Apartment.valid_balconies)
        parent_init.update({
            "laundry": laundry,
            "balcony": balcony
        })        
        return parent_init
    prompt_init = staticmethod(prompt_init)

class House(Property):
    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")
    
    def __init__(self, num_stories='', garage='', fenced='', **kwargs):
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories
        
    def display(self):
        super().display()
        print("DETALHES DA CASA")
        print("Número de andares: {}".format(self.num_stories))
        print("garagem: {}".format(self.garage))
        print("quintal cercado: {}".format(self.fenced))
    
    def prompt_init():
        parent_init = Property.prompt_init()
        fenced = get_valid_input("O quintal é cercado ",
        House.valid_fenced)
        garage = get_valid_input("Tem garagem ",
        House.valid_garage)
        num_stories = input("A casa tem quantos andares? ")
        
        parent_init.update({
            "fenced": fenced,
            "garage": garage,
            "num_stories": num_stories
        })
        return parent_init
    prompt_init = staticmethod(prompt_init)

class Purchase:
    def __init__(self, price='', taxes='', **kwargs):
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes
    
    def display(self):
        super().display()
        print("DETALHES DA COMPRA")
        print("preço de compra: {}".format(self.price))
        print("taxas anuais: {}".format(self.taxes))
        
    def prompt_init():
        return dict(
            price=input("Qual o preço de venda? "),
            taxes=input("Qual o valor das taxas anuais? "))
    prompt_init = staticmethod(prompt_init)

class Rental:
    def __init__(self, furnished='', utilities='', rent='', **kwargs):
        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent
        self.utilities = utilities
        
    def display(self):
        super().display()
        print("DETALHES DO ALUGUEL")
        print("aluguel: {}".format(self.rent))
        print("contas: {}".format(self.utilities))
        print("mobiliada: {}".format(self.furnished))
        
    def prompt_init():
        return dict(
        rent=input("Qual o valor mensal do aluguel? "),
        utilities=input("Qual o valor das contas (água, luz, etc.)? "),
        furnished = get_valid_input("A propriedade é mobiliada? ", 
                                    ("yes", "no")))
    prompt_init = staticmethod(prompt_init)


class HouseRental(Rental, House):
    def prompt_init():
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class ApartmentRental(Rental, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class ApartmentPurchase(Purchase, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)

class HousePurchase(Purchase, House):
    def prompt_init():
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class Agent:
    def __init__(self):
        self.property_list = []
    
    def display_properties(self):
        for property in self.property_list:
            property.display()
            
    type_map = {
        ("house", "rental"): HouseRental,
        ("house", "purchase"): HousePurchase,
        ("apartment", "rental"): ApartmentRental,
        ("apartment", "purchase"): ApartmentPurchase
    }

    def add_property(self):
        property_type = get_valid_input(
            "What type of property? ",
            ("house", "apartment")).lower()
        payment_type = get_valid_input(
            "What payment type? ",
            ("purchase", "rental")).lower()

        PropertyClass = self.type_map[(property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass(**init_args))

