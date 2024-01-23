from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import get_items, add_item, get_item, save_item, remove_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    items = get_items()
    to_dos = sorted(items, key=lambda x: x['status'], reverse=True)
    return render_template("index.html", to_dos=to_dos)

@app.route('/', methods=['POST'])
def add_to_do():
    new_item_title = request.form.get('new_to_do')
    add_item(new_item_title)
    return redirect('/')

@app.route('/complete/<id>', methods=['POST'])
def complete_to_do(id):
    item = get_item(id)
    item["status"] = "Completed"
    save_item(item)
    return redirect('/')

@app.route('/delete/<id>', methods=['POST'])
def delete_to_do(id):
    item = get_item(id)
    remove_item(item)
    return redirect('/')
