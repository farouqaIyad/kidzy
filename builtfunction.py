def get_status(start, end, number):
    if number>=start:
        if number<=end:
            return {"message":"طبيعي "}
        elif number > end:
            return {"message":"اعلى من الطبيعي "}
    else:
        return {"message":"اقل من الطبيعي "}
    
def time_t(days,minutes):
    if days<1:
        if minutes <= 59:
            return "منذ "+ str(round(minutes)) +" دقيقة"
        elif minutes >= 60 and minutes<=1409:
            minutes = minutes /60
            return "منذ "+ str(round(minutes))+" ساعة"
    else:
            return "منذ "+str(days)+" يوم"

