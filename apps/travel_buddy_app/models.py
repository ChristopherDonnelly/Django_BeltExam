# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..users_app.models import User
import datetime, time

# Create your models here.
class TripManager(models.Manager):
    def trip_validator(self, postData, user_id):
        destination = postData['destination']
        description = postData['description']
        start_date = postData['start_date']
        end_date = postData['end_date']
        currentDate = datetime.datetime.now().strftime('%Y-%m-%d')

        user = User.objects.get(id = user_id)

        errors = {}
        response = {
            'status': True
        }

        if len(destination) < 1:
            errors["destination"] = "Destination cannot be blank!"
        
        if len(description) < 1:
            errors["description"] = "Description cannot be blank!"
        
        if len(start_date) < 1:
            errors["start_date"] = "Trip start date cannot be blank!"
        elif start_date < currentDate:
            errors["start_date"] = "Trip start date cannot be in the past!"

        if len(end_date) < 1:
            errors["end_date"] = "Trip end date cannot be blank!"
        elif end_date < start_date:
            errors["end_date"] = "Trip end date cannot be prior to the starting date!"

        if len(errors) == 0:
            newTrip = TripPlan.objects.create(destination = destination, description = description, start_date = start_date, end_date = end_date, trip_planner = user)

            newTrip.joined_users.add(user)
            newTrip.save()

        if len(errors) > 0:
            response['status'] = False
            response['errors'] = errors

        return response

    def join_validator(self, trip_id, user_id):
        user = User.objects.get(id = user_id)
        joinTrip = TripPlan.objects.get(id = trip_id)
        joinTrip.joined_users.add(user)
        joinTrip.save()

        response = {
            'status': True
        }

        return response

class TripPlan(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    trip_planner = models.ForeignKey(User, related_name = "planned_trips")
    joined_users = models.ManyToManyField(User, related_name = "joined_trips")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()

    def __str__(self):
        return "\n\tID: {}\n\tDestination: {}\n\tDescription: {}\n\tStart Date: {}n\tEnd Date: {}\n".format(str(self.id), str(self.destination), str(self.description), str(self.start_date), str(self.end_date))

    __repr__ = __str__