from pydantic import BaseModel, constr, Field
from datetime import datetime


class ExpData(BaseModel):
    exp_date: datetime = Field(le=datetime.today())
    exp_category: constr(min_length=1)
    exp_amount: int = Field(gt=0)
