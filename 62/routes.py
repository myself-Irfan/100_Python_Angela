from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Cafe
from forms import CafeFormData
from logger import get_logger

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = get_logger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# routes
@router.get("/")
def home(request: Request):
    logger.info('Rendering home')
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/add")
def add_form(request: Request):
    logger.info('Rendering add form')
    return templates.TemplateResponse("add.html", {"request": request})

@router.post("/add")
def add_cafe(
    request: Request,
    form_data: CafeFormData = Depends(CafeFormData.as_form),
    db: Session = Depends(get_db)
):
    try:
        new_cafe = Cafe(
            name=form_data.cafe,
            location=form_data.location,
            open_time=form_data.open,
            close_time=form_data.close,
            coffee_rating=form_data.coffee_rating,
            wifi_rating=form_data.wifi_rating,
            power_rating=form_data.power_rating
        )
        db.add(new_cafe)
        db.commit()
        logger.info(f"Added new cafe: {new_cafe.name}")
        return RedirectResponse(url="/cafes", status_code=status.HTTP_303_SEE_OTHER)
    except SQLAlchemyError as sql_err:
        db.rollback()
        logger.exception(f"Error while adding a cafe: {sql_err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/cafes", name='cafes')
def cafes_list(request: Request, db: Session = Depends(get_db)):
    try:
        cafes = db.query(Cafe).all()
        logger.info('Fetched cafe list')
        return templates.TemplateResponse("cafes.html", {"request": request, "cafes": cafes})
    except SQLAlchemyError as sql_err:
        logger.exception(f'Failed to fetch cafes from db: {sql_err}')
        raise HTTPException(status_code=500, detail='Could not fetch cafes')
