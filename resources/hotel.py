from flask_restful import Resource, reqparse

from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },{
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.34,
        'cidade': 'Santa Catarina'
    },{
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.3,
        'diaria': 420.34,
        'cidade': 'São Paulo'
    }
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}  # SELECT * FROM hoteis


class Hotel(Resource):
    """
    Atributos da classe
    """
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="O campo 'nome' não pode ser vazio!!")
    argumentos.add_argument('estrelas', type=float, required=True, help="O campo 'estrelas' não pode ser vazio!!")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'Menssagem': 'Hotel não encontrado!'}, 404  #NOT FOUND
    
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'Mensagem': f'Hotel id {hotel_id} já existe. '}, 400  # BAD REQUEST

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'Mensagem': 'Houve um erro ao tentar salvar hotel.'}, 500       # INTERNAL SERVER ERROR

        return hotel.json()


    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'Mensagem': 'Houve um erro ao tentar salvar hotel.'}, 500  # INTERNAL SERVER ERROR
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
           try:
               hotel.delete_hotel()
           except:
               return {'Mensagem': 'Um erro ocorreu ao tentar deletar hotel'}, 500      # INTERNAL SERVER ERROR
           return {'Mensagem': 'Hotel deletado.'}

        return {'Mensagem': 'Hotel não encontrado'}, 404





