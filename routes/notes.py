"""

@Author: Omkar Bhise

@Date: 2024-01-03 11:30:00

@Last Modified by: Omkar Bhise

@Last Modified time: 2024-01-02 02:30:00

@Title : User Notes

"""

from fastapi import APIRouter, status, Depends, HTTPException, Request
from schema import UserNotes, CollaboratorDetails
from fastapi.responses import Response
from sqlalchemy.orm import Session
from model import get_db, Notes, User, collaborator
import json
from Core.utils import logger, Redis

notes_router = APIRouter()


@notes_router.post('/add', status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_notes(data: UserNotes, request: Request, response: Response, db: Session = Depends(get_db)):
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
        notes_data.update({'user_id': request.state.user.id})
        notes = Notes(**notes_data)
        db.add(notes)
        db.commit()
        db.refresh(notes)
        Redis.add_redis(f"user_{notes.user_id}", f"notes_{notes.id}", json.dumps(notes_data))
        # response.status_code=status.HTTP_201_CREATED
        return {'message': 'Notes Added Successfully ', 'status': 201, 'data': notes}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.get('/get', status_code=status.HTTP_200_OK, tags=["Notes"])
def get_all_user_notes(request: Request, response: Response, db: Session = Depends(get_db)):
    """
    Description: This function used to get the all notes of the users
    Parameter:  user : UserLogin in that username and password
                request : Request used to getting all authenticated data
                response : Response  it response to the user
                db: Session = this session  Depends on get_db (yield the database )
    Return: message, status code and data in the JSON or dict format
    """
    try:
        cache_notes = Redis.getall_redis(f"user_{request.state.user.id}")
        if cache_notes:
            data = list(map(lambda note: json.loads(note), cache_notes.values()))
            return {'message': "Notes Founds using Redis ", 'status': 200, 'data': data}

        notes = db.query(Notes).filter_by(user_id=request.state.user.id).all()
        # notes = db.query(Notes).filter_by(user_id=user_id).all()
        if not notes:
            return {'message': "User Does not have any notes ", 'status': 400}
        # print(type(notes))
        collaborator_notes = db.query(collaborator).filter_by(user_id=request.state.user.id).all()
        note = db.query(Notes).filter(Notes.id.in_(list(map(lambda x: x.note_id, collaborator_notes)))).all()
        notes.extend(note)
        return {'message': "Notes Founds ", 'status': 200, 'data': notes}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.patch('/update/{note_id}', status_code=status.HTTP_200_OK, tags=["Notes"])
def update_notes(note_id: int, request: Request, notes: UserNotes, response: Response, db: Session = Depends(get_db)):
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

        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=note_id).one_or_none()
        if not note:
            collab = db.query(collaborator).filter_by(user_id=request.state.user.id,note_id=note_id).first()
            if collab:
                note = db.query(Notes).filter_by(id=note_id).first()
            else:
                return {'message': "User Not authenticated ", 'status': 404}

        updated_data = notes.model_dump()
        [setattr(note, key, value) for key, value in updated_data.items()]
        db.commit()
        db.refresh(note)
        Redis.add_redis(f"user_{request.state.user.id}", f"notes_{note.id}", json.dumps(updated_data))

        return {'message': "Notes updated Successfully ", 'status': 200,"data":updated_data}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.delete('/del/{id}', status_code=status.HTTP_200_OK, tags=["Notes"])
def del_one_notes_of_user(id: int, request: Request, response: Response, db: Session = Depends(get_db)):
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
        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=id).one_or_none()
        # note = db.query(Notes).filter_by().first()
        if note is None:
            raise HTTPException(detail="Note is not present",status_code=status.HTTP_400_BAD_REQUEST)
        db.delete(note)
        db.commit()
        Redis.del_redis(f"user_{request.state.user.id}", f"notes_{id}")
        return {'message': "Deletes Note of the User ", 'status': 200}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.delete('/del_all', status_code=status.HTTP_200_OK, tags=["Notes"])
def del_all_notes_of_user(request: Request, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used remove a notes of the users.
        Parameter:  request as Request Object,response as Response object,
                    db: Session = this session  Depends on get_db (yield the database )
        Return: it return the message and status code in JSON or dict format
    """
    try:
        notes = db.query(Notes).filter_by(user_id=request.state.user.id).all()
        # notes = db.query(Notes).filter_by(user_id=user_id).first()
        if not notes:
            return {'message': "User not write any notes ", 'status': 200}
        # for i in notes:
        #     print(type(i))
        #     db.delete(i)
        [db.delete(i) for i in notes]
        db.commit()
        for i in notes:
            Redis.del_redis(f"user_{request.state.user.id}", f"notes_{i.id}")

        return {'message': "Deleted Notes of Users", 'status': 200}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.post('/collaborator', status_code=status.HTTP_201_CREATED, tags=["Collaborator"])
def add_collaborator(body: CollaboratorDetails, request: Request, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used add collaborator to a specific note.
        Parameter:  body as CollaboratorDetails object containing note_id and user_id in List Format,
                    request as Request Object,response as Response object,
                    db: Session = this session  Depends on get_db (yield the database )
        Return: it returen the message and status code in JSON or dict format
    """
    try:
        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=body.note_id).one_or_none()
        if note is None:
            raise HTTPException(detail='Notes Not Found', status_code=status.HTTP_404_NOT_FOUND)
        for user_id in body.user_ids:
            collaborator = db.query(User).filter_by(id=user_id).first()
            if collaborator is None:
                raise HTTPException(detail=f"User id : {user_id} is not present ",status_code=status.HTTP_404_NOT_FOUND)
            if not collaborator.is_verified:
                raise HTTPException(detail=f"User id: {collaborator.id} is not verified user ",status_code=status.HTTP_400_BAD_REQUEST)
            if user_id != request.state.user.id :
                note.user_m2m.append(collaborator)
                print("Hi")
        db.commit()
        return {'message': 'Collaborator is Added', 'status': 201}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}


@notes_router.delete('/del_Collaborator', status_code=status.HTTP_200_OK, tags=["Collaborator"])
def del_collaborator(body: CollaboratorDetails, request: Request, response: Response, db: Session = Depends(get_db)):
    """
        Description: This function used remove a collaborator form a specific note.
        Parameter:  body as CollaboratorDetails object containing note_id and user_id,
                    request as Request Object,response as Response object,
                    db: Session = this session  Depends on get_db (yield the database )
        Return: it return the message and status code in JSON or dict format
    """

    try:
        note = db.query(Notes).filter_by(user_id=request.state.user.id, id=body.note_id).one_or_none()
        if note is None:
            raise HTTPException(detail='Notes Not Founds ', status_code=status.HTTP_404_NOT_FOUND)
        for user_id in body.user_ids:
            collaborator = db.query(User).filter_by(id=user_id).first()
            if user_id != request.state.user.id and collaborator:
                note.user_m2m.remove(collaborator)
        db.commit()
        return {'message': 'Collaborators Remove Successfully', 'status': 200}
    except Exception as ex:
        logger.exception(ex)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'message': str(ex), 'status': 400}
