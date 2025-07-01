from pydantic import BaseModel
from fastapi import Form

class CafeFormData(BaseModel):
    cafe: str
    location: str
    open: str
    close: str
    coffee_rating: str
    wifi_rating: str
    power_rating: str

    @classmethod
    def as_form(cls,
                cafe: str = Form(...),
                location: str = Form(...),
                open: str = Form(...),
                close: str = Form(...),
                coffee_rating: str = Form(...),
                wifi_rating: str = Form(...),
                power_rating: str = Form(...)
    ):
        return cls(
            cafe=cafe,
            location=location,
            open=open,
            close=close,
            coffee_rating=coffee_rating,
            wifi_rating=wifi_rating,
            power_rating=power_rating
        )