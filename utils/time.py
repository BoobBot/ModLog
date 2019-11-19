from datetime import datetime

TIME_FORMAT = '%H:%M:%S'

@property
def now():
    return datetime.now().strftime(TIME_FORMAT)
