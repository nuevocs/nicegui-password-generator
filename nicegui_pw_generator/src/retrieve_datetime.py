import datetime

def current_date_jst() -> str:
    jst_no_tz = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=9)
    return jst_no_tz.strftime("%Y%m%d%H%M%S")