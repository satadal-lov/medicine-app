from flask import Flask, render_template, request
from database import search_medicine, init_db

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    medicine_name = request.form.get('medicine_name', '').strip()
    results = search_medicine(medicine_name)
    return render_template('result.html', 
                         medicine_name=medicine_name, 
                         results=results)

if __name__ == '__main__':
    app.run(debug=True)