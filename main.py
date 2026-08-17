from fastapi import FastAPI
from typing_extensions import TypedDict
from typing import Optional
import db

# Demonstrated SQL knowledge, so stage 4 is complete
app = FastAPI()

class Tasks(TypedDict):
    id: int
    title: str
    done: bool

class updateTasks(TypedDict):
    id: int
    title: Optional[str]
    done: Optional [bool]

tasks=[
    Tasks(id=1,title='solve homework',done=False),
    Tasks(id=2,title='get groceries', done=True),
    Tasks(id=3, title='work out', done=False)
]
tasks_tuples=[(rec['id'], rec['title'], rec['done']) for rec in tasks]
conn,cur=db.getdb()
db.initialize_table(conn,cur)

data=db.retrieve_all(conn,cur)

if len(data)==0:
    db.insert_data(conn,cur,tasks_tuples)
@app.get('/tasks')
def return_tasks():
    retrieved=db.retrieve_all(conn,cur)
    return {"200":retrieved}
@app.get("/tasks/{req_id}")
def return_task(req_id: int):
    return db.retrieve(conn,cur,req_id)
@app.post("/tasks/")
def create_task(task: Tasks):
    tuple_task=(task['id'],task['title'],task['done'])
    insertion=db.insert_data(conn,cur,tuple_task)
    return insertion
@app.put("/tasks/{req_id}")
def update_task(task: updateTasks):
    return db.update(conn,cur,task)
@app.delete("/tasks/{req_id}")
def del_task(req_id: int):
    return db.delete(conn,cur,req_id)
