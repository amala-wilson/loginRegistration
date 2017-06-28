from __future__ import unicode_literals

from django.db import models

import re, bcrypt

# Create your models here.

# Defining regular expressions for each of the fields
N_REGEX = re.compile(r'^[a-zA-Z]{2,}$')  # name
AL_REGEX = re.compile(r'^([a-zA-Z]){2,}$')  # alias
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  # email
PWD_REGEX = re.compile(r'^.{8,}$') # password

# Create your models here.
class UserManager(models.Manager):
    def validateUser(self, postData):
        name = postData['name']
        alias = postData['alias']
        email = postData['email']
        password = postData['password']
        pwd_confirm = postData['pwd_confirm']
        dob = postData['birthday']

        print dob
        errors = []

        nChk, msg = self.validateN(name) # Validate first name
        if not nChk:
            errors.append(msg)
        aChk, msg = self.validateA(alias)  # Validate last name
        if not aChk:
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
        
        # Verify if user provided date of birth
        if not dob:
            errors.append("Provide Date of Birth!")

        if not errors:  # No errors
            try:
                user = User.objects.get(email=email)  # Check if email exists
                errors.append("User already registered!")
                return {'status':False, "errors":errors}
            except:
                hashedpwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user = User.objects.create(name=name, alias=alias, email=email, password=hashedpwd, dob=dob)
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
        
    def validateN(self, name):
        nChk = False
        msg = ""

        if (len(name) < 1):
            msg = "Name cannot be blank!"
        elif not N_REGEX.match(name):
            msg = "Invalid name! Must contain at least 2 characters!"
        else:
            nChk = True
        
        return (nChk, msg)
    
    def validateA(self, alias):
        aChk = False
        msg = ""

        if (len(alias) < 1):
            msg = "Alias cannot be blank!"
        elif not AL_REGEX.match(alias):
            msg = "Invalid alias! Must contain at least 2 characters!"
        else:     
            aChk = True
        
        return (aChk, msg)

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

class PokeManager(models.Manager):
    # def pokeCount(self, userID):
    #     try:
    #         user = User.objects.get(id=userID)
    #         count = count + 1
    #         mypoke = Poke.objects.create(user=user, poke=count)

    def checkPoke(self, count, userID):
        try:
            user = User.objects.get(id=userID)
            # print user.name
            mypoke = Poke.objects.create(user=user, poke=count)
            # print mypoke
            return (True, "Got your poke")
        except:
            return (False, "Didn't receive your poke")

    # def newpoke(self, pokeID, userID):
    #     # try:
    #     poke = Poke.objects.get(id=pokeID)
    #     # except:
    #         # return (False, "Secret not found")
    #     user = User.objects.get(id=userID)
    #     poke.poked_by.add(user)
    #     return #(True, "Secret liked")

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateField(null=True)

    objects = UserManager()

class Poke(models.Model):
    user = models.ForeignKey(User)  # A User can have many pokes
    poke = models.IntegerField()  # Store poke count of each user
    poked_by = models.ManyToManyField(User, related_name="pokes")

    objects = PokeManager()