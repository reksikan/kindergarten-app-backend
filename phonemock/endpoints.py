from typing import List

from main import app, storage
from schemas import SMSSchema


@app.post('/sms')
async def sms(data: SMSSchema):
    storage.appendleft(data)


@app.get('/', response_model=List[SMSSchema])
async def sms_list():
    return storage
