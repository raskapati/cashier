from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}')"

class ProductForm(FlaskForm):
    name = StringField('Nama Produk', render_kw={"placeholder": "Nama Produk"}, validators=[DataRequired()])
    price = FloatField('Harga', render_kw={"placeholder": "Harga"}, validators=[DataRequired()])
    submit = SubmitField('Tambah Produk')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data)
        db.session.add(product)
        db.session.commit()
    return render_template('add_product.html', form=form)

@app.route('/financial_report')
def financial_report():
    products = Product.query.all()
    total_revenue = sum(product.price for product in products)
    return render_template('financial_report.html', products=products, total_revenue=total_revenue)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
