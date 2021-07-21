from market.models import User
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField,PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterForm(FlaskForm):

      def validate_username(self, username):
            user = User.query.filter_by(username = username.data).first()
            if user:
                  raise ValidationError('Username already exists.')

      def validate_email(self, email):
            user = User.query.filter_by(email = email.data).first()
            if user:
                  raise ValidationError('Eamil already exists.')

      username = StringField(label='Username', validators=[DataRequired(), Length(min=2, max=30)])
      email = StringField(label='Email',validators=[DataRequired(), Email()])
      password = PasswordField(label='Password',validators=[DataRequired(), Length(min=6)])
      confirm_password= PasswordField(label='Confirm Password',validators=[DataRequired(), EqualTo('password')])
      submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
      username = StringField(label='Username',validators=[DataRequired()])
      password = PasswordField(label='Password',validators=[DataRequired(), Length(min=6)])
      submit = SubmitField(label='Login')


class PurchaseItemForm(FlaskForm):
      submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
      submit = SubmitField(label='Sell Item')

class AddItemForm(FlaskForm):
      name = StringField(label='Name', validators=[DataRequired()])
      price = IntegerField(label='Price', validators=[DataRequired()])
      barcode = StringField(label='Barcode', validators=[DataRequired(), Length(max=12)])
      description = StringField(label='Description', validators=[DataRequired()])
      submit = SubmitField(label='Add Item')