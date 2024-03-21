from flask import Flask, render_template, request, redirect
from todo_app.data import trello_items
from todo_app.flask_config import Config
from todo_app.view_models.ViewModel import ViewModel

def create_app(): 

    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        items = trello_items.get_items()
        sort_order = {status:i for i,status in enumerate(['To Do', 'Doing', 'Done'])}
        to_dos = sorted(items, key=lambda x: sort_order.get(x.status, len(sort_order)))
        view_model = ViewModel(to_dos)
        
        return render_template("index.html", view_model=view_model)


    @app.route('/', methods=['POST'])
    def add_to_do():
        new_item_title = request.form.get('new_to_do')
        trello_items.add_item(new_item_title)
        return redirect('/')


    @app.route('/complete/<id>', methods=['POST'])
    def complete_to_do(id):
        trello_items.complete_item(id)
        return redirect('/')


    @app.route('/delete/<id>', methods=['POST'])
    def delete_to_do(id):
        trello_items.delete_item(id)
        return redirect('/')

    return app