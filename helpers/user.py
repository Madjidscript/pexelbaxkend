import bcrypt # type: ignore
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity # type: ignore
from datetime import timedelta
from flask import request, jsonify # type: ignore
from config.db import db
from model.pexel import *
from werkzeug.security import check_password_hash # type: ignore



def CreateUser():
    response = {}
    contacts = request.json.get('contact')
    password_hash = request.json.get('password')
    user_existe= User.query.filter_by(contact=contacts).first()
    print ("papa",password_hash)
    if user_existe:
        response['status']="eror"
        response['user_info']="utilisateur existe deja"
        return response

    new_user = User()
    new_user.firstname = request.json.get('firstname')
    new_user.password = bcrypt.hashpw(password_hash.encode('utf-8'), bcrypt.gensalt())  # Assurez-vous de hacher le mot de passe
    new_user.lastname = request.json.get('lastname')
    new_user.contact = request.json.get('contact')
    new_user.years = request.json.get('years')
    new_user.month = request.json.get('month')
    new_user.day = request.json.get('day')
    new_user.genre = request.json.get('genre')
    
    db.session.add(new_user)
    db.session.commit()

    rs = {}
    rs['user_id'] = new_user.user_id
    rs['firstname'] = new_user.firstname
    rs['lastname'] = new_user.lastname
    rs['contact'] = new_user.contact
    rs['years'] = new_user.years
    rs['month'] = new_user.month
    rs['day'] = new_user.day
    rs['genre'] = new_user.genre
    

    response['status'] = 'Success'
    response['user_info'] = rs
   
    return response


def GetAllUsers():
    response = {}
    try:
        all_users = User.query.all()
        users_info = []
        for user in all_users:
            info_user = {
                'user_id': user.user_id,
                'firstname' :  user.firstname,
                'lastname' : user.lastname,
                'contact' : user.contact,
                'years' : user.years,
                'month' : user.month,
                'day' : user.day,
               'genre' : user.genre
            }
            users_info.append(info_user)
        response['status'] = 'success'
        response['users'] = users_info

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def GetSingleUser():
    response = {}

    try:
        user_id = request.json.get('user_id')
        single_user = User.query.filter_by(user_id=user_id).first()
        if single_user:
            info_user = {
                'user_id': single_user.user_id,
                'firstname' :  single_user.firstname,
                'lastname' : single_user.lastname,
                'contact' : single_user.contact,
                'years' : single_user.years,
                'month' : single_user.month,
                'day' : single_user.day,
               'genre' : single_user.genre
            }
            response['status'] = 'success'
            response['user'] = info_user
        else:
            response['status'] = 'error'
            response['error_description'] = 'User not found'

    except Exception as e:
        response['status'] = 'error'
        response['error_description'] = str(e)

    return response


def UpdateUser():

    response = {}
    try:
        id = '1'
        # id = request.json.get('user_id')
        user_to_update = User.query.filter_by(user_id=id).first()

        user_to_update.firstname = request.json.get('firstname')
        user_to_update.lastname = request.json.get('lastname')
        user_to_update.contact = request.json.get('contact')
        # user_to_update.password = request.json.get('password') 
        user_to_update.years = request.json.get('years')
        user_to_update.month = request.json.get('month')
        user_to_update.day = request.json.get('day')
        user_to_update.genre = request.json.get('genre')
        
        db.session.commit()

        rs = {}
        rs['user_id'] = user_to_update.user_id
        rs['firstname'] = user_to_update.firstname
        rs['lastname'] = user_to_update.lastname
        rs['contact'] = user_to_update.contact
        rs['years'] = user_to_update.years
        rs['month'] = user_to_update.month
        rs['day'] = user_to_update.day
        rs['genre'] = user_to_update.genre

        response['status'] = 'Success'
        response['users'] = rs

    except Exception as e:
        response['status']='erreur'
        response['message']=str(e)
    
    print("jhdfjh", gt)
    return response


def DeleteUser():
    response = {}
    try:
        user_id = request.json.get('user_id')
        user_to_delete = User.query.filter_by(user_id=user_id).first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            response['status'] = 'success'
        else:
            response['status'] = 'error'
            response['error_description'] = 'User not found'

    except Exception as e:
        response['error_description'] = str(e)
        response['status'] = 'error'

    return response


def LoginUsers():
    reponse = {}
    try:
        contact = request.json.get('contact')
        password = request.json.get('password')
        login_admin = User.query.filter_by(contact=contact).first()
        if not login_admin:
            reponse["status"]="error"
            reponse["infos"]="email ou numero incorect"
            return reponse
        users_infos = {
            'user_id': login_admin.user_id,
             'firstname' :  login_admin.firstname,
            'lastname' : login_admin.lastname,
            'contact' : login_admin.contact,
            'years' : login_admin.years,
            'month' : login_admin.month,
            'day' : login_admin.day,
            'genre' : login_admin.genre
                         
        }
        if login_admin and bcrypt.checkpw(password.encode('utf-8'), login_admin.password.encode('utf-8')):
            expires = timedelta(hours=1)
            access_token = create_access_token(identity=contact)

            reponse['status'] = 'success'
            reponse['admin_infos'] = users_infos
            reponse['access_token'] = access_token
            reponse["message"]="connexion effectuer"

        else:
            reponse['status'] = 'error'
            reponse['message'] = 'Invalid email or password'

    except Exception as e:
        reponse['error_description'] = str(e)
        reponse['status'] = 'error'

    return reponse
