from datetime import datetime
from ..login import login
from flask_login import login_user,logout_user,login_required,current_user
from flask import flash,redirect,url_for,render_template,session,request
from .forms import LoginForm,UseraddForm,ChangepwForm
from .. import db
from ..models import Users,Role

@login.route('/',methods = ['GET','POST'])
def denglu():
    myform = LoginForm()
    if myform.validate_on_submit():
        username = Users.query.filter_by(name=myform.username.data).first()
        if username is not None and username.verify_password(myform.passwd.data):
            login_user(username,myform.remember_me.data)
            role_session = Role.query.filter_by(id=username.role_id).first()
            session['role'] = (role_session).name
            session['id'] = (role_session).id
            username.uptime = datetime.now()
            db.session.add(username)
            db.session.commit()
#                        print session.get('role')
#			print session.get('id')
            return redirect(url_for('main.index'))
        else:
            flash('Username or Password is error!')
            return render_template('login.html', form=myform)
    return render_template('login.html',form=myform)

@login.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('role',None)
    session.pop('id',None)
    flash('Logout Successful!')
    return redirect(url_for('login.denglu'))

@login.route('/useradd',methods = ['GET','POST'])
#######@login_required
def useradd():
    myform = UseraddForm()
    if request.method == 'POST':
        if Users.query.filter_by(name=myform.username.data).first():
            flash("User already exists!")
            return render_template('useradd.html',form=myform)
        else:
            u = Users()
            u.name = myform.username.data
            u.password_hash = myform.passwd.data
            u.role_id = 2
            u.groups_id = myform.groups.data
            db.session.add(u)
            db.session.commit()
            flash('User add Successful!')
            myform.username.data = None
        return redirect(url_for('login.denglu'))
    return render_template('useradd.html',form=myform)

@login.route('/userchange',methods=['GET','POST'])
@login_required
def userchange():
        myform = ChangepwForm()
        if myform.validate_on_submit():
                user = Users.query.filter_by(name=current_user.name).first()
                if user is not None and user.verify_password(myform.passwdold.data):
                        user.password_hash = myform.passwd.data
                        db.session.add(user)
                        db.session.commit()
                        flash('Password change Successfull!')
                        return redirect(url_for('main.index'))
                else:
                        flash('Change Fialed!')
                        return render_template('form.html',form=myform)
        return render_template('form.html',form=myform)
