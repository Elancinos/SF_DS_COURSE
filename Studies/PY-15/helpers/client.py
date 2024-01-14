class Client():
    #Базовые данные
    def __init__(self, email, order_num, registration_year):
        self.email = email
        self.order_num = order_num
        self.registration_year = registration_year
        self.discount = 0
        
    def make_order(self, price):
        self.update_discount()
        self.order_num += 1
        # здесь должно быть оформление заказа, но мы просто выведем цену
        discounted_price = price * (1-self.discount)
        print(f'Order price for {self.email} is {discounted_price}')
        
    def update_discount(self):
        if self.registration_year < 2018 and self.order_num >= 5:
            self.discount = 0.1