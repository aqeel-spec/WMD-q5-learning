# todos.py

from typing import  Annotated

from app.model import Todo , TodoUpdate , TodoRead , TodoCreate, UserCreate , TodoUpdateStatus
from sqlmodel import  Session , select , desc
from fastapi import  Depends , APIRouter
from typing import List

from app.utils.db import  get_session, get_error_404 , get_todo
from app.api.dep import SessionDep , CurrentUser


router = APIRouter()



# @router.get("/")
# def read_root():
#     return {"Hello": "World"}

@router.post("/api/todo/create", response_model=Todo)
def create_todo(session: SessionDep, current_user: CurrentUser, todo: TodoCreate):
    db_todo = Todo.model_validate(todo,update={"user_id": current_user.id})
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
        
    

@router.get("/api/todos/", response_model=int)
def read_todos(session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
        todos = session.exec(select(Todo)).all()
        if not todos:
            raise get_error_404
        return len(todos)
    


    

@router.get("/api/my/todos",response_model=list[Todo])
def getCurrentUserTodos(session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    statement = select(Todo).where(Todo.user_id == current_user.id).order_by(desc(Todo.created_at))
    todos = session.exec(statement).all()

    if not todos:
        raise get_error_404(current_user.id)
    
    return todos
@router.patch("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id : int , todo: TodoUpdateStatus , session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    todo_to_update = get_todo(todo_id, session)
    if not todo:
        raise get_error_404(todo_id)
    todo_to_update.completed = todo.completed
    session.commit()
    session.refresh(todo_to_update)
    return todo_to_update
    

# get single todo with id
@router.get("/api/todos/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: int, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    todo = get_todo(todo_id, session)
    if not todo:
        raise get_error_404(todo_id)
    return todo

# update todo using its id with default values
@router.put("/api/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id : int , todo: TodoUpdate , session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    todo_to_update = get_todo(todo_id, session)
    if not todo:
        raise get_error_404(todo_id)
    changed_data = todo.model_dump(exclude_unset=True)
    for key, value in changed_data.items():
        if value is not None and value != "string":
            setattr(todo_to_update, key, value)
    session.commit()
    session.refresh(todo_to_update)
    return todo_to_update
    
# delete todo using todo id
@router.delete("/api/todos/{todo_id}",response_model=dict)
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    todo = get_todo(todo_id, session)
    if not todo:
        raise get_error_404(todo_id)
    session.delete(todo)
    session.commit()
    return {"todo" : "Todo deleted successfully Against id={}".format(todo_id)}