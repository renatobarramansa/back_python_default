from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from back_python_default.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

database = []


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    summary='Retorna um JSON',
    description='Essa aplicação deve gerar um json' ' documentação do código.',
    response_model=Message,
)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get(
    '/ex01',
    status_code=HTTPStatus.OK,
    summary='Exercicio 01',
    description='Realizando exercicio 01',
    response_model=Message,
)
def read_ex01():
    return {'message': 'Deu bom!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id > 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    del database[user_id - 1]

    return {'message': 'User deleted'}
