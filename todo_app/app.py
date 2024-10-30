import os
from urllib.parse import urlencode
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, login_user
import requests
from todo_app.data import mongo_items
from todo_app.flask_config import Config
from todo_app.view_models.ViewModel import ViewModel
from todo_app.authentication.user import User

def create_app(): 

    app = Flask(__name__)
    app.config.from_object(Config())

    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        params = {
            'client_id': os.getenv('FLASK_LOGIN_CLIENT_ID')
        }

        encoded_params = urlencode(params)
    
        return redirect(f'https://github.com/login/oauth/authorize?{encoded_params}')
       

    @login_manager.user_loader
    def load_user(user_id):
        app_user = User(id=user_id)
        return app_user
        

    login_manager.init_app(app)

    @app.route('/login/callback')
    def callback():
        access_token = __get_access_token()
        user_id = __validate_user_id(access_token)

        current_user = User(id=user_id)

        login_user(current_user)

        return redirect('/')
        

    @app.route('/')
    @login_required
    def index():
        items = mongo_items.get_items()
        view_model = ViewModel(items)
        
        return render_template("index.html", view_model=view_model)


    @app.route('/', methods=['POST'])
    @login_required
    def add_to_do():
        new_item_title = request.form.get('new_to_do')
        mongo_items.add_item(new_item_title)
        return redirect('/')


    @app.route('/complete/<id>', methods=['POST'])
    @login_required
    def complete_to_do(id):
        mongo_items.complete_item(id)
        return redirect('/')
    

    @app.route('/start/<id>', methods=['POST'])
    @login_required
    def start_to_do(id):
        mongo_items.start_item(id)
        return redirect('/')


    @app.route('/delete/<id>', methods=['POST'])
    @login_required
    def delete_to_do(id):
        mongo_items.delete_item(id)
        return redirect('/')
    

    def __get_access_token():
        code = request.args.get('code')
        request_base_url = 'https://github.com/login/oauth/access_token'

        headers = {
            "Accept":  "application/json"
        }

        params = {
            'client_id': os.getenv('FLASK_LOGIN_CLIENT_ID'),
            'client_secret': os.getenv('FLASK_LOGIN_CLIENT_SECRET'),
            'code': code
        }

        response = requests.post(request_base_url, json=params, headers=headers)
        data = response.json()
        return data.get("access_token")
    

    def __validate_user_id(access_token):
        base_url = 'https://api.github.com/user'

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(base_url, headers=headers)
        data = response.json()
        
        return data.get('id')

    return app