from fastapi import APIRouter, Depends
from sqlmodel import Session , select
from app.model import Todo, TodoCreate, TodoRead , TodoUpdate
from app.api.deps import get_session , get_error_404 , get_todo 
from app.api.deps import SessionDep
from app.api.deps import CurrentUser
from typing import Annotated


# kafka configuration for todos
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
from app import settings
import json
from app import todo_pb2

router = APIRouter()
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()


@router.post("/todo/create")
async def create_todo( session: Annotated[Session, Depends(get_session)], current_user: CurrentUser,todo: TodoCreate, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    db_todo = Todo.model_validate(todo,update={"user_id": current_user.id})
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    
    # Create a new Person message
    todo_protobuf = todo_pb2.Todo()
    todo_protobuf.id = db_todo.id
    todo_protobuf.title = db_todo.title
    todo_protobuf.description = db_todo.description
    todo_protobuf.completed = db_todo.completed
    todo_protobuf.user_id = db_todo.user_id
    todo_protobuf.created_at.FromDatetime(db_todo.created_at)
    todo_protobuf.updated_at.FromDatetime(db_todo.updated_at)
    
    print("todo_protobuf \n", todo_protobuf)
    
     # Serialize the message to a byte string
    serialized_todo = todo_protobuf.SerializeToString()
    print(f"Serialized data: {serialized_todo}")
    
    await producer.start()
    
    # Produce message
    await producer.send_and_wait("todo", serialized_todo)
    
    
    # for development server we will use 
    # broker:9092
    # producer=AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER) # settings.KAFKA_BOOTSTRAP_SERVER
    # await producer.start()
    
    
    # todoJson = json.dumps(db_todo.__dict__).encode("utf-8")
    # Serialize the todo item to JSON
    
    # method 02
    # todo_dict = {field: getattr(todo, field) for field in todo.dict()}
    # todo_json = json.dumps(todo_dict).encode("utf-8")
    
    
    # todoJson = db_todo.json().encode("utf-8")

    # print("todoJson")
    # print(todoJson)

    # await producer.send_and_wait(topic=settings.KAFKA_ADD_TOPIC, value=todoJson)
    
    # db_todo = Todo.model_validate(todo,update={"user_id": current_user.id})
    # session.add(db_todo)
    # session.commit()
    # session.refresh(db_todo)
    # return db_todo
    return db_todo
        
    
    

@router.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
        todos = session.exec(select(Todo)).all()
        if not todos:
            raise get_error_404(current_user.id)
        return todos
    



# get single todo with id
@router.get("/todos/{todo_id}", response_model=TodoRead)
def read_todo(todo_id: int, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    todo = get_todo(todo_id, session)
    if not todo:
        raise get_error_404(todo_id)
    return todo

# update todo using its id with default values
@router.put("/todos/{todo_id}", response_model=Todo)
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
@router.delete("/todos/{todo_id}",response_model=dict)
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)], current_user: CurrentUser):
    todo = get_todo(todo_id, session)
    if not todo:
        raise get_error_404(todo_id)
    session.delete(todo)
    session.commit()
    return {"todo" : "Todo deleted successfully Against id={}".format(todo_id)}