class APIException(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)
        
        
class InvalidAuthToken(APIException):
    detail = "Неверный токен доступа"