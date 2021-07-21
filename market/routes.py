
from threading import current_thread
from market import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, AddItemForm
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
      return render_template('home.html')

@app.route('/market', methods = ['GET', 'POST'])
@login_required
def market_page():
      purchase_form= PurchaseItemForm()
      selling_form = SellItemForm()
      
      if request.method == 'POST':
            #Purchase Item
            purchased_item = request.form.get('purchased_item')
            p_item_object = Item.query.filter_by(name=purchased_item).first()
            if p_item_object:
                  if current_user.budget >= p_item_object.price:
                        p_item_object.owner = current_user.id
                        current_user.budget -= p_item_object.price
                        db.session.commit()
                        flash(f"Congratulations, you purchased {p_item_object.name} for {p_item_object.price}$", 'success')
                  else:
                        flash(f'Insufficient Budget for {p_item_object.name}', 'danger')

            #Sell Item
            sold_item = request.form.get('sold_item')
            s_item_object = Item.query.filter_by(name=sold_item).first()
            print(s_item_object)
            if s_item_object:
                  if s_item_object in current_user.items:
                        s_item_object.owner = None
                        current_user.budget += s_item_object.price
                        db.session.commit()
                        flash(f"Congratulations, you sold {s_item_object.name} for {s_item_object.price}$", 'info')
                  else:
                        flash(f"Something went wrong in selling!", 'danger')


            return redirect(url_for('market_page'))
      if request.method == 'GET':
            items = Item.query.filter_by(owner=None)
            owned_items = Item.query.filter_by(owner = current_user.id)
            return render_template('market.html', title = 'Market', items = items, purchase_form=purchase_form, owned_items=owned_items,selling_form=selling_form)

@app.route('/register', methods = ['GET', 'POST'])
def register_page():
      form = RegisterForm()

      if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user_to_create = User(username= form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user_to_create)
            db.session.commit()
            flash(f'Account Created!', 'success')
            return redirect(url_for('market_page'))
      return render_template('register.html', title='Register', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login_page():
      form = LoginForm()

      
      if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash(f'Success! You are logged in as: {user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or password did not match! Please try again.', category='danger')
            return redirect(url_for('login_page'))
      if request.method == 'GET':
            return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout_page():
      logout_user()
      flash('You have been logged out', 'info')
      return redirect(url_for("home_page"))

@app.route('/add_item', methods = ['GET', 'POST'])
@login_required
def add_item():
      form = AddItemForm()
      if request.method == "POST":
            item = Item(name = form.name.data, price = form.price.data, barcode = form.barcode.data, description = form.description.data)
            db.session.add(item)
            db.session.commit()
            flash(f"Congratulations, you have added {item.name} for {item.price}$", 'info')
            return redirect(url_for('market_page'))
      if request.method == 'GET':
            return render_template ('add_item.html', title = 'Add Item',form=form)
