import os, secrets
from flask import flash, render_template, request, url_for, redirect
from airbnb import app, db, bcrypt, mail
from airbnb.models import User, Post, Wishlist
from airbnb.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm, AdminPostForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from PIL import Image
from airbnb.admin import AdminPost





@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    apartments = AdminPost.query.all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    form = PostForm()
    print('comments, posts', posts)
    print('apartments', apartments)
    
    if current_user.is_authenticated:
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your comment has been added.', category='success')
            return redirect(url_for('home'))

        apartments = AdminPost.query.all()
        return render_template('home.html', apartments=apartments, form=form, posts=posts)  
    
    return render_template('home.html', apartments=apartments, form=form, posts=posts)





def apartment_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/apartments_pics', picture_fn)
    form_picture.save(pic_path)
  
    return picture_fn

def save_apartment_pictures(pictures):
    saved_pictures = []
    for picture in pictures:
        if picture:
            picture_filename = apartment_picture(picture) 
            saved_pictures.append(picture_filename)
    return saved_pictures


@app.route('/admin', methods=['GET', 'POST'])
def admin():
  
    users= User.query.all()
    apartments= AdminPost.query.all()
    form = AdminPostForm()
    if form.validate_on_submit():
        pictures = [form.picture_1.data, form.picture_2.data, form.picture_3.data]
        saved_pictures = save_apartment_pictures(pictures)

        apartment = AdminPost(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            price=form.price.data,
            category= form.category.data,
            picture_1=saved_pictures[0],
            picture_2=saved_pictures[1],
            picture_3=saved_pictures[2],
            admin_id=current_user.id  
        )

        db.session.add(apartment)
        db.session.commit()
        flash('Apartment has been added successfully', 'success')
        return redirect(url_for('admin'))

    return render_template('admin.html', title='Admin Panel', form=form, users=users, apartments=apartments)
  
@app.route('/admin/edit_apartment/<int:apartment_id>', methods=['GET', 'POST'])
@login_required
def edit_apartment(apartment_id):
    apartment = AdminPost.query.get_or_404(apartment_id)
    form = AdminPostForm()
    if form.validate_on_submit():
        apartment.title = form.title.data
        apartment.description = form.description.data
        apartment.location = form.location.data
        apartment.price = form.price.data
        db.session.commit()
        flash('Apartment has been updated successfully', 'success')
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.title.data = apartment.title
        form.description.data = apartment.description
        form.location.data = apartment.location
        form.price.data = apartment.price
    return render_template('edit_apartment.html', title='Edit Apartment', form=form, apartment=apartment)



@app.route('/admin/delete_apartment/<int:apartment_id>', methods=['POST'])
def delete_apartment(apartment_id):
    apartment = AdminPost.query.get_or_404(apartment_id)
    
    db.session.delete(apartment)
    db.session.commit()
    
    flash('Apartment has been deleted successfully', 'success')
    return redirect(url_for('admin'))


# AUTH

@app.route('/signup', methods=['GET','POST'])
def signup():
  if current_user.is_authenticated: # type: ignore
    return redirect(url_for('home'))
  form =RegistrationForm()
  if form.validate_on_submit():
    hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    flash(f'Account created for {form.username.data}! You can now login', 'success')
    return redirect (url_for('home'))
  else:
    return render_template("signup.html", title='Sign Up', form =form)
  
  
  
@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated: # type: ignore
    return redirect(url_for('home'))
  form =LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email= form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page= request.args.get('next')
      flash(f'welcome back', 'success')
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login unsuccessful please check credentials', 'danger')
      
  return render_template("login.html", title='Login', form =form)

  
@app.route("/logout")
def logout():
  logout_user()
  flash('You have been loged out.')
  return redirect(url_for('home'))


# password reset
def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request', sender='anthonynchege52@gmail.com', recipients=[user.email])
  msg.body= f"""  To reset your password click: 
  {url_for('reset_token', token=token, _external=True)}.
  If you did not make this request please ignore this email.
  """
  mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated: # type: ignore
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated: # type: ignore
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
  
  
# wish list and account update

def save_picture(form_picture):
  random_hex= secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)  
  picture_fn = random_hex + f_ext
  pic_path = os.path.join(app.root_path, 'static/profile_pics',picture_fn)
  
  output_size=(125,125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(pic_path)
  
  return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    
    elif request.method == 'POST':
        item_name = request.form['item_name']
        description = request.form['description']
        wishlist_item = Wishlist(item_name=item_name, description=description, user_id=current_user.id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash('Item added to wishlist!', 'success')
        return redirect(url_for('wishlist'))
    
    form.username.data = current_user.username
    form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)