from flask_restful import Resource,reqparse
from model.child import ChildModel
from model.event import eventModel
from flask import request
from builtfunction import time_t
import datetime
dates = list()
li = list()


class EventsResource(Resource):
    
    def get(self,child_id):
        di = {"date":None, "events":None}
        date=""
        result = eventModel.find_by_child_id(baby_id=child_id)
        latest_events = eventModel.latest_events(child_id=child_id)
        lis = list()
        li = list()
        for event in latest_events:
            c = datetime.datetime.now() - event.day
            minutes = c.seconds / 60
            lis.append({'type':event.type,
            'date':time_t(c.days,minutes=minutes)})
        for row in result:
            if row.day.date()!=date:
                if di["date"]!=None:
                    li.append(di)
                di = {"date":None, "events":None}
                events = list()
                date=row.day.date()
                di["date"] = str(date)
            events.append({"id":row.id, "day":str(row.day.time()), "details":row.details,'type':row.type})
            di["events"] = events
        li.append(di)
        return {"date":li,"latest_events":lis}
        
    def post(self,child_id):
    
        data = request.get_json(force=True)
        event = eventModel(child_id,data["type"],data['details'],data['day'])
        event.save_to_db()
        return {"message":True}


class EventResource(Resource):
    

    def get(self,event_id):
        event = eventModel.find_by_event_id(event_id=event_id) 
        return {"event":event.json()}
    
    
    def post(self,event_id):
        data = request.get_json(force=True)
        event = eventModel.find_by_event_id(event_id=event_id) 
        if event:
            if data["type"]:
                event.type = data["type"]
            if data["day"]:
                event.day = data["day"]
            if data["details"]:
                event.details = data["details"]
        event.update()
        return {"message":True}
    
    def delete(self,event_id):
        event = eventModel.find_by_event_id(event_id=event_id)
        if event:
            event.delete_from_db()
            return {"message":True}
        else:
            return {"message":False}

    
    




