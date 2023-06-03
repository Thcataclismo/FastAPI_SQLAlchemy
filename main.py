from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uvicorn

app = FastAPI()

# URL de conexão do banco de dados MySQL
database_url = "mysql+mysqlconnector://user:password@localhost:port/database_name"

# conexão com o banco de dados
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# modelo de dados
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)

Base.metadata.create_all(bind=engine)

#  rotas do FastAPI
@app.post("/tasks")
def create_task(description: str):
    # Crie uma nova tarefa
    task = Task(description=description)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/")
def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
