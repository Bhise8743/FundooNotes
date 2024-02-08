
from fastapi import APIRouter, status, Depends, HTTPException, Request,Path
from schema import UserNotes
from fastapi.responses import Response
from sqlalchemy.orm import Session
from model import get_db, Notes, User
from Core.utils import logger

notes_router = APIRouter()


@notes_router.post('/add/{id}', status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_notes(data: UserNotes, response: Response, db: Session = Depends(get_db),id:int = Path(...,description="Enter the user id")):
    """
    Description: This function used to create the new note
    Parameter:  data : UserNotes (schema)  in that username, password, first_name, last_name, phone, email, city, state, is_verified
                request : Request used to getting all authenticated data
                response : Response  it response to the user
                db: Session = this session  Depends on get_db (yield the database )
    Return: message, status code and data in the JSON or dict format
    """
    try:
        notes_data = data.model_dump()
        notes_data.update({'user_id': id})
        notes = Notes(**notes_data)
        db.add(notes)
        db.commit()
        db.refresh(notes)
        return {'message': 'Notes Added Successfully ', 'status': 201, 'data': notes}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.get('/get/{id}', status_code=status.HTTP_200_OK, tags=["Notes"])
def get_all_user_notes( response: Response, db: Session = Depends(get_db),id:int = Path(...,description="Enter the user id")):
    """
    Description: This function used to get the all notes of the users
    Parameter:  user : UserLogin in that username and password
                request : Request used to getting all authenticated data
                response : Response  it response to the user
                db: Session = this session  Depends on get_db (yield the database )
    Return: message, status code and data in the JSON or dict format
    """
    try:
        notes = db.query(Notes).filter_by(user_id=id).all()
        # notes = db.query(Notes).filter_by(user_id=user_id).all()
        if not notes:
            return {'message': "User Does not have any notes ", 'status': 400}
        return {'message': "Notes Founds ", 'status': 200, 'data': notes}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.patch('/update/{note_id}', status_code=status.HTTP_200_OK, tags=["Notes"])
def update_notes(note_id: int, notes: UserNotes, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used to update the note
        Parameter:  title : str
                    user : UserLogin in that username and password
                    notes : UserNotes (schema) in that title , description , color
                    response : Response  it response to the user
                    db: Session = this session  Depends on get_db (yield the database )
        Return: it return the message and status code in JSON or dict format
    """
    try:
        # note = db.query(Notes).filter_by(title=title).one_or_none()

        note = db.query(Notes).filter_by(id=note_id).one_or_none()
        if not notes:
            return {'message': "User Does not have any notes ", 'status': 400}

        updated_data = notes.model_dump()
        [setattr(note, key, value) for key, value in updated_data.items()]
        db.commit()
        db.refresh(note)
        return {'message': "Notes updated Successfully ", 'status': 200,"data":updated_data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.delete('/del/{id}', status_code=status.HTTP_200_OK, tags=["Notes"])
def del_one_notes_of_user(id: int, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used to del one notes of the user
        Parameter:  title : str
                    user : UserLogin in that username and password data members
                    request : Request used to getting all authenticated data
                    response : Response  it response to the user
                    db: Session = this session  Depends on get_db (yield the database )
        Return: it return the message and status code in JSON or dict format
    """
    try:
        note = db.query(Notes).filter_by(id=id).one_or_none()
        # note = db.query(Notes).filter_by().first()
        if note is None:
            raise HTTPException(detail="Note is not present",status_code=status.HTTP_400_BAD_REQUEST)
        db.delete(note)
        db.commit()
        return {'message': "Deletes Note of the User ", 'status': 200}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.delete('/del_all/{id}', status_code=status.HTTP_200_OK, tags=["Notes"])
def del_all_notes_of_user(response: Response, db: Session = Depends(get_db),id:int = Path(...,description="Enter the user id")):
    """
        Description: This function used remove a notes of the users.
        Parameter:  request as Request Object,response as Response object,
                    db: Session = this session  Depends on get_db (yield the database )
        Return: it return the message and status code in JSON or dict format
    """
    try:
        notes = db.query(Notes).filter_by(user_id=id).all()
        # notes = db.query(Notes).filter_by(user_id=user_id).first()
        if not notes:
            return {'message': "User not write any notes ", 'status': 200}
        # for i in notes:
        #     print(type(i))
        #     db.delete(i)
        [db.delete(i) for i in notes]
        db.commit()
        return {'message': "Deleted Notes of Users", 'status': 200}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
