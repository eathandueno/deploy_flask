from flask import flash
from flask_app.models.users import User
from flask_app.config.mysqlconnection import connectToMySQL
db = 'carsdb'
class Cars(User):
    def __init__( self , data ):
            self.id = data['id']
            self.model = data['model']
            self.year = data['year']
            self.make = data['make']
            self.description = data['description']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
            self.users_id = data['users_id']
            # self.buyers_id = data['buyers_id']
            self.price = data['price']
            self.buyer = None
            self.seller = None

    @staticmethod
    def validate_car(form):
        is_valid = True
        if len(form['model']) < 3:
            flash("Model name must be longer than 3 characters")
            is_valid = False
        if  int(form['year']) < 1900:
            flash("Year must be sooner than 1900")
            is_valid = False
        if len(form['description']) < 3:
            flash("description name must be longer than 3 characters")
            is_valid = False
        if int(form['price']) <= 0:
            flash("Price must be greater than 0")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from cars left join users as seller on cars.users_id = seller.id;"

        results = connectToMySQL(db).query_db(query)
        cars = []

        for car in results:
            carShow = cls(car)
            seller_data = {
                'id' : car['seller.id'],
                'first_name' : car['first_name'],
                'last_name' : car['last_name'],
                'email' : car['email'],
                'password' : car['password'],
                'created_at' : car['created_at'],
                'updated_at' : car['updated_at']
            }
            carShow.seller = User(seller_data) 
            cars.append(carShow)
            
        return cars

    @classmethod
    def add_one(cls, data):
        query = "INSERT INTO cars ( model , year , make , description, users_id, price) VALUES ( %(model)s , %(year)s , %(make)s , %(description)s, %(creator_id)s, %(price)s);" 
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE cars Set model = %(model)s, year = %(year)s, make = %(make)s, description = %(description)s, price = %(price)s WHERE id = %(creator_id)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE from cars WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        print(results)
        cars = []
        for result in results:
            cars.append(cls(result))
        return cars[0]