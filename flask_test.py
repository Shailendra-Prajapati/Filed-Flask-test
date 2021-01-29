from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from marshmallow import Schema, fields, post_load, ValidationError, validates, validate
from datetime import date
import random
app = Flask(__name__)
api = Api(app)


class PaymentGateway:
    def __init__(self, credit_card_number, card_holder, expiration_date, security_code, amount):
        self.credit_card_number = credit_card_number
        self.card_holder = card_holder
        self.expiration_date = expiration_date
        self.security_code = security_code
        self.amount = amount


    def CheapPaymentGateway(self):
        num  = random.randint(10,99)
        if num % 5 == 0:
            return True
        return False

    def ExpensivePaymentGateway(self):
        num  = random.randint(10,99)
         if num % 5 == 0:
            return True
        return False

    def PremiumPaymentGateway(self):
        num  = random.randint(10,99)
         if num % 5 == 0:
            return True
        return False



class Payment(Schema):
    credit_card_number = fields.Str(reqired=True, validate=validate.Length(max=16, min=16))
    card_holder = fields.String(reqired=True)
    expiration_date = fields.DateTime(reqired=True)
    security_code =fields.Str()
    amount = fields.Integer(reqired=True, validate=validate.Range(min=0))


    @validates('expiration_date')
    def validate_expiration_date(self, expiration_date):
        if datetime.now() > expiration_date:
            raise ValidationError('Expirtaion date cant be past date!')

    @validates('expiration_date')
    def validate_expiration_date(self, expiration_date):
        if datetime.now() > expiration_date:
            raise ValidationError('Expirtaion date cant be past date!')
    @post_load
    def create_payemnt(self, data, **kwrgs):
       pay = PaymentGateway(**data)
       if data['amount']  <= 20:
            process_pay = pay.CheapPaymentGateway()
            if process_pay:
                return sonify(isError= False,
                    message= "payment processed",
                    statusCode= 200,
                    ), 200
            return sonify(isError= True,
                    message= "payment failed",
                    statusCode= 400,
                    ), 400
        elif data['amount'] <= 500:
            processed =  False
            process_pay = pay.ExpensivePaymentGateway()
            if process_pay:
                return sonify(isError= False,
                    message= "payment processed",
                    statusCode= 200,
                    ), 200
            else:

                if  not processed:
                    process_pay = pay.CheapPaymentGateway()
                    if process_pay:
                        return sonify(isError= False,
                            message= "payment processed",
                            statusCode= 200,
                            ), 200
                    return sonify(isError= True,
                            message= "payment failed",
                            statusCode= 400,
                            ), 400

                return sonify(isError= True,
                        message= "payment failed",
                        statusCode= 400,
                        ), 400
        else:

            processed =  False
            process_pay = pay.PremiumPaymentGateway()
            if process_pay:
                return sonify(isError= False,
                    message= "payment processed",
                    statusCode= 200,
                    ), 200
            else:
                i = 1
                while (not processed and i<4):
                    process_pay = pay.PremiumPaymentGateway()
                    if process_pay:
                        processed = True
                        return sonify(isError= False,
                            message= "payment processed",
                            statusCode= 200,
                            ), 200
                    else:
                        i+=1
                        if i == 3:
                            return sonify(isError= True,
                        message= "payment failed",
                        statusCode= 400,
                        ), 400

                return sonify(isError= True,
                        message= "payment failed",
                        statusCode= 400,
                        ), 400


        
        
@app.route('/', methods = ['POST'])
def ProceessPayment():
    data = request.form['data']
    schema = Payment()
    try:
        payment = schema.load(data)

    except ValidationError as err:
        return jsonify(err), 400


if __name__ == '__main__':
    app.run(debug=False)
