from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from airbnb.models import User
from airbnb.admin import Admin

# registration
class RegistrationForm(FlaskForm):
  username = StringField('Username', 
                         validators=[DataRequired(), Length(min=4, max=20)])
  
  email = StringField('Email',
                  validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  
  confirm_password = PasswordField('Confirm Password',
                          validators=[DataRequired(), EqualTo('password')])
  
  submit = SubmitField('Sign Up')
  
  def validate_username(self, username):
    user= User.query.filter_by(username= username.data).first()
    if user:
      raise ValidationError(f'the username {username.data} is already taken. Please use a different name.')
    
  def validate_email(self, email):
    user= User.query.filter_by(email= email.data).first()
    if user:
      raise ValidationError(f'This Email is already in Use.')
  

# login
class LoginForm(FlaskForm):
  email = StringField('Email',
                  validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember me')
  
  
  submit = SubmitField('Login')


# user update
class UpdateAccountForm(FlaskForm):
  username = StringField('Username', 
                         validators=[DataRequired(), Length(min=4, max=20)])
  
  email = StringField('Email',
                  validators=[DataRequired(), Email()])
  picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
  
  submit = SubmitField('Update')
  
  def validate_username(self, username):
        if username.data != current_user.username: # type: ignore
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

  def validate_email(self, email):
        if email.data != current_user.email: # type: ignore
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class AdminPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()],render_kw={'placeholder': 'Enter category, eg: studio, one_bedroom'})
    picture_1 = FileField('Upload Image 1', validators=[FileAllowed(['jpg', 'png'])])
    picture_2 = FileField('Upload Image 2', validators=[FileAllowed(['jpg', 'png'])])
    picture_3 = FileField('Upload Image 3', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')
  
  
  
  
  
  



# Post Comments
class PostForm( FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  content = TextAreaField('Content', validators=[DataRequired()])
  submit = SubmitField("Post")
  
 

# reset password
class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    def validate_email(self, email):
      user= User.query.filter_by(email= email.data).first()
      if user is None:
        raise ValidationError(f'There is no acccount with this email, check email and try again. Or register first.')
      
class ResetPasswordForm(FlaskForm):
  password = PasswordField('Password', validators=[DataRequired()])
  
  confirm_password = PasswordField('Confirm Password',
                          validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField("Reset Password")
  
  
  

  