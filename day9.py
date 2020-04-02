class car:
    no_of_tyres = 4
    """
        The car class describes a car object

        Attributes
       ------------
       b: brand
       mdn:model_no
       c:color

    """
    def __init__(self,brand,model_no,color):
        self.b = brand
        self.mdn = model_no
        self.c = color

    @classmethod
    def tyres(cls):
        return car.no_of_tyres

# print tyres from class
print(car.tyres())