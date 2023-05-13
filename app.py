from flask import *
import datetime
import uuid
from utils import *
app = Flask(__name__ )


app.secret_key = 'AIRBUS'
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=10)
@app.route('/')
def index():
    return render_template('main.html')



def generate_uuid_from_pass(password):
  # Convert the email address to a byte string.
#   email_bytes = password.encode('utf-8')

  # Generate a UUID from the byte string.
  uuid_bytes = uuid.uuid5(uuid.NAMESPACE_DNS, password)

  # Convert the UUID bytes to a string.
  uuid_string = uuid_bytes.hex

  # Return the UUID string.
  return uuid_string
@app.route('/signup',methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usertype = request.form.get('usertype')
        manuf = request.form.get('manuf')
        if email and password and usertype:
            password = generate_uuid_from_pass(password)
            SQL = f'''
            INSERT INTO Users (email, password, usertype,manufacturer, created_at)
            VALUES
            ('{email}', '{password}', '{usertype}','{manuf}' , '{datetime.datetime.now()}')
            '''
            client.command(SQL)
            return redirect(url_for('login_page'))
    return redirect(url_for('index'))

@app.route('/signup-page',methods=['POST'])
def signup_page():
    manu = get_manufacturer()
    return render_template('signup.html',manu=manu)

@app.route('/login-page',methods=['POST','GET'])
def login_page(mess=None):
    mess = request.args.get('mess')
    return render_template('login.html',mess=mess)

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        usertype = request.form.get('usertype')
        password_up = generate_uuid_from_pass(password)
        e =  get_email_password(email,password_up ,usertype)

        if email and password and e:
           if e[0] == email and e[1] == password_up:
               session['email'] = email
               return redirect(url_for('home'))
        return redirect(url_for('login_page',mess='Invalid Credentials'))

    return redirect(url_for('login_page'))

@app.route('/qyeried-data',methods=['GET'])

@app.route('/query', methods=['POST'])
def query():
    if not session.get('email'):
        return redirect(url_for('index'))
    email = session.get('email')
    # selected_value = request.form['selected_value']
    partname ,metrc = get_parts(session.get('email'))
    partn = request.form['partnames']
    mter = request.form['metr']
    poten = request.form['pote']
    vals = get_query_data(session.get('email'),partn,mter,poten )
    # Perform database query using selected_value
    if vals:
        return render_template('home.html',totalData = vals,
                               partnames=partname,mtrs =metrc, session=session,tables1=get_table_data(session.get('email')) ,plot1=get_plot1(session.get('email')),plot2=get_plot2(session.get('email')) ,plot3=get_plot3(session.get('email')) ,plot4=get_plot4(session.get('email')))
    return render_template('home.html',partnames=partname,mtrs =metrc, session=session,tables1=get_table_data(session.get('email')) ,plot1=get_plot1(session.get('email')),plot2=get_plot2(email) ,plot3=get_plot3(email) ,plot4=get_plot4(email))

    results = ''
    return jsonify(results)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        df = pd.read_excel(f)
        insert_data(df)
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/home')
def home():
    
    if not session.get('email'):
        return redirect(url_for('index'))
    partname ,metrc = get_parts(session.get('email'))
    totalData4 = recycle_data()
    # print(metrc)
    email = session.get('email')
    return render_template('home.html',partnames=partname,mtrs =metrc,totalData4=totalData4, session=session,tables1=get_table_data(session.get('email')) ,plot1=get_plot1(email),plot2=get_plot2(email) ,plot3=get_plot3(email) ,plot4=get_plot4(email)) 


@app.route('/<path:path>')
def catch_all(path):
    if session.get('email'):
    # returns a 200 (not a 404) with the following contents:
        return app.send_static_file(path)
        return render_template(path,session=session )
    return redirect(url_for('index'))

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template(request.path[1:],session=session)

#     return {'status': 404}


    return {}
if __name__ == '__main__':
    app.run(debug=True)