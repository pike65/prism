from contextlib import contextmanager
from sqlalchemy.orm import Session


@contextmanager
def transaction_scope(db: Session):
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
