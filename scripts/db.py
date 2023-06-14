from base64 import b64encode, b64decode
from datetime import datetime

from pymongo.mongo_client import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler

import pytz

from . import extract

PY_T = extract.PY_TESSERACT()

class OPERATIONS:
    def __init__(self) -> None:
        self.uri: str = "mongodb+srv://[USERNAME]:[YOUR PASSWORD]@[CLUSTER NAME].jlgzq.mongodb.net/?retryWrites=true&w=majority"
        self.client: object = MongoClient(self.uri)
        self.db: dict = self.client['database_name']

        self.data_store: dict = self.db["collection_name"]

        self.start_cron_worker()
    
    def extract_text(self, doc) -> None:
        PY_T.load_image_from_bytes(b64decode(doc['img_b64']))
        text: str = PY_T.extract()
        self.data_store.find_one_and_update({"_id":doc['_id']}, {"$set": {"text": text}}, upsert=True)
    
    def check_status(self) -> None:
        docs: dict = self.get_all()
        if docs:
            for doc in docs:
                if doc['time'] <= self.sv_utc():
                    self.extract_text(doc)
    
    def start_cron_worker(self) -> None:
        scheduler: object = BackgroundScheduler()
        scheduler.add_job(self.check_status, 'interval', seconds=10)
        scheduler.start()

    def sv_utc(self) -> str:
        dt: object = datetime.now(pytz.utc)
        dt_utc: str= dt.strftime("%Y-%m-%d %H:%M")
        return dt_utc
    
    def utc_time(self, tz, dt) -> str:
        local: object = pytz.timezone(tz)
        naive: object = datetime.strptime(dt, "%Y-%m-%d %H:%M")
        local_dt: object = local.localize(naive, is_dst=None)
        utc_dt: object = local_dt.astimezone(pytz.utc)

        c_utc: str = utc_dt.strftime("%Y-%m-%d %H:%M")
        
        return c_utc

    def upload(self, img_b64, timzone, datetime) -> str:
        datetime: object = self.utc_time(timzone, datetime)
        doc: object = self.data_store.insert_one({
            "img_b64":img_b64,
            "text":"pending_extraction",
            "time":datetime
            })
        _id: str = doc.inserted_id.__str__()
        return _id
    
    def get_all(self) -> list:
        docs: list[dict] = []
        
        cursor: object = self.data_store.find({})

        for doc in cursor:
            docs.append(doc)
        for doc in docs:
            doc['img_b64'] = doc['img_b64'].decode()
        
        return docs
    
    def img_b64(self, imgb) -> bytes:
        return b64encode(imgb)
