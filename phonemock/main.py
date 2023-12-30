from collections import deque
from fastapi import FastAPI

app = FastAPI()
storage = deque(maxlen=128)
