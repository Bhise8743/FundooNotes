from fastapi import APIRouter, status, Depends, HTTPException, Request
from schema import LabelSchema
from fastapi.responses import Response
from sqlalchemy.orm import Session
from model import get_db,Labels
from Core.utils import logger
label_router = APIRouter()


@label_router.post('/add', status_code=status.HTTP_201_CREATED, tags=["Labels"])
def create_label(request: Request, response: Response, payload: LabelSchema, db: Session = Depends(get_db)):
    """
        Description: This function used to create the new label
        Parameter:  payload : LabelSchema in that name of the label
                    request : Request used to getting all authenticated data
                    response : Response  it response to the user
                    db: Session = this session  Depends on get_db (yield the database )
        Return: message, status code and data in the JSON or dict format
    """
    try:
        label = payload.model_dump()
        label.update({'user_id': request.state.user.id})
        label_data = Labels(**label)
        db.add(label_data)
        db.commit()
        db.refresh(label_data)
        return {'message': 'Label Added Successfully ', 'status': 201, 'data': label_data}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception(ex)
        return {'message': str(ex), 'status': 400}


@label_router.get('/get_all', status_code=status.HTTP_200_OK, tags=["Labels"])
def get_all_labels_of_user(request: Request, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used to get the all Labels of the user
        Parameter:  request : Request used to getting all authenticated data
                    response : Response  it response to the user
                    db: Session = this session  Depends on get_db (yield the database )
        Return: message, status code and data in the JSON or dict format
    """
    try:
        # cache_labels = Redis.getall_redis(f"user_{request.state.user.id}")
        label = db.query(Labels).filter_by(user_id=request.state.user.id).all()
        if label is None:
            raise HTTPException(detail='Label Not founds ', status_code=status.HTTP_404_NOT_FOUND)
        return {'message': "Data Retrieved ", 'status': 200, 'data': label}
    except Exception as ex:
        response.status_code = status.HTTP_400_BAD_REQUEST
        logger.exception(ex)
        return {'message': str(ex), 'status': 400}


@label_router.put('/update/{id}', status_code=status.HTTP_200_OK, tags=["Labels"])
def update_label(id:int, request: Request, response: Response, payload: LabelSchema, db: Session = Depends(get_db)):
    """
        Description: This function used to update the label
        Parameter:  payload : LabelSchema in that name of label
                    request : Request used to getting all authenticated data
                    response : Response  it response to the user
                    db: Session = this session  Depends on get_db (yield the database )
        Return: message, status code in the JSON or dict format
    """
    try:
        label = db.query(Labels).filter_by(user_id=request.state.user.id,id=id).one_or_none()
        if label is None:
            raise HTTPException(detail='Label Not founds ', status_code=status.HTTP_404_NOT_FOUND)
        updated_data = payload.model_dump()
        # for key, value in updated_data.items():
        #     pass
        [setattr(label, key, value) for key, value in updated_data.items()]

        db.commit()
        db.refresh(label)
        return {'message': 'Label updated Successfully', 'status': 200}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@label_router.delete('/del/{id}', status_code=status.HTTP_200_OK, tags=["Labels"])
def del_label(id:int, request: Request, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used to delete one label
        Parameter:
                    request : Request used to getting all authenticated data
                    response : Response  it response to the user
                    db: Session = this session  Depends on get_db (yield the database )
        Return: message, status code in the JSON or dict format
    """
    try:
        label = db.query(Labels).filter_by(user_id=request.state.user.id, id=id).first()
        if label is None:
            raise HTTPException(detail='Label Not founds ', status_code=status.HTTP_404_NOT_FOUND)
        db.delete(label)
        db.commit()
        return {'message': 'Label Deleted Successfully', 'status': 200}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
