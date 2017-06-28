from __future__ import unicode_literals

from django.db import models

import re, bcrypt

# Create your models here.

# Defining regular expressions for each of the fields
FN_REGEX = re.compile(r'^[a-zA-Z]{2,}$')  # first name
LN_REGEX = re.compile(r'^([a-zA-Z]){2,}$')  # last name
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  # email
PWD_REGEX = re.compile(r'^.{8,}$') # password

# Create your models here.
class UserManager(models.Manager):
    def validateUser(self, postData):
        first_name = postData['first_name']
        last_name = postData['last_name']
        email = postData['email']
        password = postData['password']
        pwd_confirm = postData['pwd_confirm']

        errors = []

        fnChk, msg = self.validateFN(first_name) # Validate first name
        if not fnChk:
            errors.append(msg)
        lnChk, msg = self.validateLN(last_name)  # Validate last name
        if not lnChk:
            errors.append(msg)
        emailChk, msg = self.validateEmail(email)  # Validate email
        if not emailChk:
            errors.append(msg)
        pwdChk, msg = self.validatePwd(password)  # Validate password
        if not pwdChk:
            errors.append(msg)

        # Verify password confirmation matches password
        if (password != pwd_confirm):
            errors.append("Passwords don't match!")

        if not errors:  # No errors
            try:
                user = User.objects.get(email=email)  # Check if email exists
                errors.append("User already registered!")
                return {'status':False, "errors":errors}
            except:
                hashedpwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashedpwd)
                return {'status':True, 'user':user}
        else:
            return {'status':False, "errors":errors}
        
    
    def login(self, postData):
        # Extracted information from the user through the login form
        email  = postData['login_email']
        password = postData['login_password']
        registerChk = False
        user = None
        errors = []

        # Check whether email the user typed in already exists
        email_list = User.objects.filter(email=email)  # Returns a list of objects which match the email in the db with the email the user typed in
        if (len(email_list) != 0):  # Making sure email list is not empty
            if bcrypt.hashpw(password.encode('utf-8'), email_list[0].password.encode('utf-8')) == email_list[0].password:
                print "It Matches!"
                registerChk = True
                user = email_list[0]
            else:
                print "It doesn't match!"
                errors.append("Incorrect Password!")
        else:
            registerChk = False
            user = None
            errors.append('User not found! Please register!')
    
        return (registerChk, user, errors)
        
    def validateFN(self, first_name):
        fnChk = False
        msg = ""

        if (len(first_name) < 1):
            msg = "First name cannot be blank!"
        elif not FN_REGEX.match(first_name):
            msg = "Invalid first name! Must contain at least 2 characters!"
        else:
            fnChk = True
        
        return (fnChk, msg)
    
    def validateLN(self, last_name):
        lnChk = False
        msg = ""

        if (len(last_name) < 1):
            msg = "Last name cannot be blank!"
        elif not LN_REGEX.match(last_name):
            msg = "Invalid last name! Must contain at least 2 characters!"
        else:     
            lnChk = True
        
        return (lnChk, msg)

    def validateEmail(self, email):
        emailChk = False
        msg = ""

        if len(email) < 1:
            msg = "Email cannot be blank!"
        elif not EMAIL_REGEX.match(email):
            msg = "Invalid Email Address!"
        else: 
            emailChk = True

        return (emailChk, msg)

    def validatePwd(self, pwd):
        pwdChk = False
        msg = ""
        
        if len(pwd) < 1:
            msg = "Password cannot be blank!"
        elif not PWD_REGEX.match(pwd):
            msg = "Invalid password! Must contain at least 8 characters!"
        else: 
            pwdChk = True
        
        return pwdChk, msg

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    objects = UserManager()