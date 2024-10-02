from flask import Flask, request # type: ignore
from flask_restful import Api, Resource # type: ignore
from helpers.user import *


class UsersApi (Resource) :
    def post (self,route):
        if route == "createuser":
            return CreateUser()
        
        if route == "getsingleuser":
            return GetSingleUser()
        
        if route == "loginusers":
            return LoginUsers()
        
        if route =="updateuser":
            return UpdateUser()
    

    def get (self,route):
        if route == "getAllusers":
            return GetAllUsers()
        

    # def patch (self,route):
    #     if route =="updateuser":
    #         return UpdateUser()
    

    def delete (self,route):
        if route == "deleteuser":
            return DeleteUser()