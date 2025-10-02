from typing import Generator
from shared.db import get_session

def db_session() -> Generator:
    s = get_session()
    try:
        yield s
    finally:
        s.close()
