import flask_login

class User(flask_login.UserMixin):

  def __init__(self, id) -> None:
    self.id = id
    super().__init__()