from datetime import datetime

def string_queryset(objs):
    if not objs:
        return 'Запросов не было'
    else:
        sr=''
        for num, i in enumerate(objs):
            st_time = i.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            sr += f"№{num+1} Запрос от {st_time}\n"
        return sr



def format_datetime(date_str):
        data = datetime.fromisoformat(date_str)
        return data.strftime("%Y-%m-%d %H:%M:%S")
