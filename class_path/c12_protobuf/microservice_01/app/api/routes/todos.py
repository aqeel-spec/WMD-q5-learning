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


# Temp
from google.protobuf.timestamp_pb2 import Timestamp
from typing import Tuple
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer
from confluent_kafka import Producer

router = APIRouter()

SCHEMA_REGISTRY_URL = "http://schema-registry:8081"
KAFKA_BROKER_URL = "broker:19092"

def to_proto_timestamp(dt):
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp

async def get_kafka_producer():
    producer_conf = {'bootstrap.servers': KAFKA_BROKER_URL}
    schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)
    serializer_config = {'use.deprecated.format': False}
    serializer = ProtobufSerializer(todo_pb2.Todo, schema_registry_client, serializer_config)
    producer = Producer(producer_conf)
    try:
        yield producer, serializer
    finally:
        producer.flush()

class CustomProtobufSerializer(ProtobufSerializer):
    def get_schema_registry_client(self):
        return self._schema_registry_client

@router.post("/todo/create")
async def create_todo(
    session: Annotated[Session, Depends(get_session)], 
    current_user: CurrentUser, 
    todo: TodoCreate, 
    producer_dep: Annotated[Tuple[Producer, CustomProtobufSerializer], Depends(get_kafka_producer)]
):
    producer, serializer = producer_dep

    db_todo = Todo(
        **todo.dict(),
        user_id=current_user.id
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    todo_protobuf = todo_pb2.Todo(
        id=db_todo.id,
        title=db_todo.title,
        description=db_todo.description,
        completed=db_todo.completed,
        created_at=to_proto_timestamp(db_todo.created_at),
        updated_at=to_proto_timestamp(db_todo.updated_at),
        user_id=db_todo.user_id
    )

    todo_serialized = serializer(todo_protobuf, SerializationContext("todo", MessageField.VALUE))
    producer.produce(topic='todo', value=todo_serialized, key=str(db_todo.id))
    producer.flush()

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