from flask import render_template, request, redirect, url_for, get_flashed_messages, Blueprint, current_app as app
from flask_login import login_required, login_user, current_user
from . import lm
from .admini import Admini
from .loginForm import LoginForm
from .announcementsForm import AnnouncementsForm
from .dbService import fetch_all_announcements

auth = Blueprint('auth', __name__)

# main login page, default to announcement page
@auth.route('/login-main', methods=['GET'])
@login_required
def login_main():
  form = AnnouncementsForm()
  # Fetch existing announcement from db
  # transform Objectid to string
  announcements, total_pages = \
    fetch_all_announcements(app.config['MONGO_COLLECTION_ANNOUNCEMENT'], app.config['AC_PER_PAGE'])

  return render_template(
    'login/loginMain.jinja2',
    form=form,
    ac_per_page=app.config['AC_PER_PAGE'],
    announcements=announcements,
    total_pages=total_pages,
    request_ip=app.config['REQUEST_IP']
  )

# Login form
@auth.route('/login', methods=['GET', 'POST'])
def login():
  # Create the form
  form = LoginForm()
  # If someone tries to access protected route, get_flashed_messages() will get the warning
  error_msgs = get_flashed_messages()
  # current_user is a proxy for current login user
  # it will be an anonymous user if he is not logged in
  # anonymous user will return None when get_id() is called
  idd = current_user.get_id()
  if request.method == 'GET':
    if idd:
      return redirect(url_for('.login_main'))
    else:
      return render_template('login/loginForm.jinja2', form=form, error_msgs=error_msgs)
  else: # post request
    if not form.validate_on_submit():
      # All fields must be validated when submit btn is clicked
      # Or the method is get
      # simply return loginForm.jinja2
      return render_template('login/loginForm.jinja2', form=form, error_msgs=error_msgs)

    # Fetch the db to get the admini
    admini_doc = app.config['MONGO_COLLECTION_ADMINI'].find_one({'username': form.username.data})

    # Check if admini exists and the password
    if not admini_doc or not Admini.validate_password(admini_doc['password'], form.password.data):
      # Password is not correct or admini name not exists
      # Flash the message
      # Because flashed messages are for the next request
      error_msgs.append(u'帳號或密碼錯誤，請重新輸入')
      return render_template('login/loginForm.jinja2', form=form, error_msgs=error_msgs)
    
    admini_obj = Admini(admini_doc['username'])
    # Login the user
    login_user(admini_obj)
    return redirect(url_for('.login_main'))


# Reload the user object through different session
# return User obj if the ID is valid
# return None if the ID is not valid
@lm.user_loader
def load_user(username):
  admini_obj = app.config['MONGO_COLLECTION_ADMINI'].find_one({'username': username})
  if not admini_obj:
      return None
  return Admini(admini_obj['username'])
