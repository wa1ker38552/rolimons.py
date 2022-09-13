import rolimons
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

# initialize app
app = Flask(__name__)

@app.route('/')
def home():
  # redirect home page to docs
  return redirect('/api/docs', code=302)

@app.route('/api')
def api_home():
  # return to show if api is down
  return {'success': True}

@app.route('/api/docs')
def api_docs():
  # render docs page
  return render_template('api_docs.html')

@app.route('/api/users')
def api_users():
  # get user object
  id = request.args.get('id')
  user = rolimons.User(id=id)

  # prepare json
  data = {
    'success': True,
    'data': {
      'rap': user.rap,
      'value': user.value,
      'ads': user.trade_ads
    }
  }
  return data

@app.route('/api/items')
def api_items():
  # get item object
  id = request.args.get('id')
  item = rolimons.Item(id)

  # prepare json
  data = {
    'success': True,
    'data': {
      'rap': item.rap,
      'value': item.value,
      'name': item.name
    }
  }
  return data

@app.route('/api/sales')
def api_sales():
  # get item object
  id = request.args.get('id')
  item = rolimons.Item(id)

  # get sales data
  data = item.sales_data()
  data = {
    'success': True,
    'data': {
      'timestamp': data['tiemstamp'],
      'price': data['price'],
      'old_rap': data['old_rap'],
      'new_rap': data['new_rap']
    }
  }
  return data

# run app
app.run(host='0.0.0.0', port=8080)
