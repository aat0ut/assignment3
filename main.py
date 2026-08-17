from fastapi import FastAPI, HTTPException
from typing_extensions import TypedDict
from typing import Optional
import db

app = FastAPI()

class Tasks(TypedDict):
    id: int
    title: str
    done: bool

class updateTasks(TypedDict):
    title: Optional[str]
    done: Optional[bool]

conn, cur = db.getdb()
db.initialize_table(conn, cur)

data = db.retrieve_all(conn, cur)
if len(data) == 0:
    tasks = [
        Tasks(id=1, title='solve homework', done=False),
        Tasks(id=2, title='get groceries', done=True),
        Tasks(id=3, title='work out', done=False)
    ]
    tasks_tuples = [(rec['id'], rec['title'], rec['done']) for rec in tasks]
    db.insert_data(conn, cur, tasks_tuples)

@app.get('/tasks')
def return_tasks():
    return db.retrieve_all(conn, cur)

@app.get("/tasks/{req_id}")
def return_task(req_id: int):
    result = db.retrieve(conn, cur, req_id)
    if "404" in result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result["200"]

@app.post("/tasks/", status_code=201)
def create_task(task: Tasks):
    if not task.get("title"):
        raise HTTPException(status_code=400, detail="Title is required")
    tuple_task = (task['id'], task['title'], task['done'])
    return db.insert_data(conn, cur, tuple_task)

@app.put("/tasks/{req_id}")
def update_task(req_id: int, task: updateTasks):
    existing = db.retrieve(conn, cur, req_id)
    if "404" in existing:
        raise HTTPException(status_code=404, detail="Task not found")
    task['id'] = req_id
    return db.update(conn, cur, task)

@app.delete("/tasks/{req_id}", status_code=204)
def del_task(req_id: int):
    result = db.delete(conn, cur, req_id)
    if "404" in result:
        raise HTTPException(status_code=404, detail="Task not found")
    return None