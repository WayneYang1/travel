# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
import datetime
from dateutil.relativedelta import relativedelta
from django.db import models

# Create your models here.
class UserManager(models.Manager):
	def register(self, data):
		errors = []
		for field in data:
			if len(data[field]) == 0:
				errors.append(field.replace('_', ' ').title() + " may not be empty")
		if len(data['first_name']) < 3 or len(data['last_name']) < 3 or len(data['username']) < 3:
			errors.append("Name and Username must be at least 3 characters long")
		if not data['first_name'].isalpha() or not data['last_name'].isalpha() or not data['username'].isalpha():
			errors.append("Name and Username may only be letters")
		if len(data['password']) < 8:
			errors.append("Password must be at least 8 characters long")
		if data['password'] != data['confirm_password']:
			errors.append("Passwords do not match")
		try:
			User.objects.get(username=data['username'])
			errors.append("Username already registered")
		except:
			pass
		if len(errors) == 0:
			hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], username=data['username'], password=hashed_pw)
			return user.id
		else:
			return errors

	def login(self, data):
		errors=[]
		for field in data:
			if len(data[field]) == 0:
				errors.append(field.replace('_', ' ').title() + " may not be empty")
		try:
			user = User.objects.get(username=data['username'])
			encrypted_pw = bcrypt.hashpw(data['password'].encode(), user.password.encode())
			if encrypted_pw == user.password.encode():
				return user.id
			else:
				errors.append("Incorrect password")
		except:
			errors.append("User not registered")

		if len(errors) > 0:
			return errors

class TripManager(models.Manager):
	def validate(self, data, user_id):
		errors = []
		for field in data:
			if len(data[field]) == 0:
				errors.append(field.replace('_', ' ').title() + " may not be empty")
		if data['travel_date_from'] and data['travel_date_to']:
			travel_from = datetime.datetime.strptime(data['travel_date_from'], '%Y-%m-%d')
			travel_to = datetime.datetime.strptime(data['travel_date_to'], '%Y-%m-%d')
			today = today = datetime.datetime.today()
			if travel_from < today or travel_to < today:
				errors.append("Travel date(s) may not be before today")
			if travel_from > travel_to:
				errors.append("Your trip start date may not be after your end date")
		if len(errors) == 0:
			user = User.objects.get(id=user_id)
			trip = Trip.objects.create(planner=user, destination=data['destination'], description=data['description'], travel_date_from=data['travel_date_from'], travel_date_to=data['travel_date_to'])
			return trip
		return errors


class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password= models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Trip(models.Model):
	planner = models.ForeignKey(User, related_name="planned_trips")
	destination = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	travel_date_from = models.DateField()
	travel_date_to = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TripManager()

class Attendee(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	trip = models.ManyToManyField(Trip, related_name="attendees")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



