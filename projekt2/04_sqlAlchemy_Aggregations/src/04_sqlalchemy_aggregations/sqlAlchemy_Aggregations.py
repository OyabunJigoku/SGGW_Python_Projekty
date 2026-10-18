from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, Integer, String, create_engine, select, update, delete, ForeignKey, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, Session, relationship
import random

# Połączenie z bazą SQLite
engine = create_engine("sqlite:///experiments.db", echo=True)
print(engine.connect())

Base = declarative_base()

class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, default=False)
    dataPoints = relationship("DataPoint", back_populates="experiment")


class DataPoint(Base):
    __tablename__ = "data_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)
    experiment = relationship("Experiment", back_populates="dataPoints")
    experiment_id: Mapped[int] = mapped_column(Integer, ForeignKey("experiments.id"))


# Tworzenie pliku bazy danych i wszystkich zdefiniowanych powyżej tabel
Base.metadata.create_all(engine)

with Session(engine) as session:

    e1 = Experiment(title = 'Title 1', type=1)
    e2 = Experiment(title = 'Title 2', type=2)
    elements = [e1, e2]

    for i in range(10):
        elements.append(DataPoint(real_value = random.random(), target_value=random.random(), experiment = e1))

    for i in range(10):
        elements.append(DataPoint(real_value = random.random(), target_value=random.random(), experiment = e2))

    session.add_all(elements)
    session.commit()

with Session(engine) as session:
    experients = session.scalars(select(Experiment)).all()
    print('Experiments:')
    for x in experients:
        print(f'{x.id} - {x.title} - {x.created_at} - {x.type} - {x.finished}')
    print('Data Points:')
    data_points = session.scalars(select(DataPoint)).all()
    for x in data_points:
            print(f'{x.id} - {x.real_value} - {x.target_value} - {x.experiment_id}')

with Session(engine) as session:
     stmt = update(Experiment).values(finished=True)
     session.execute(stmt)
     session.commit()

with Session(engine) as session:
    experients = session.scalars(select(Experiment)).all()
    print('Experiments after update:')
    for x in experients:
        print(f'{x.id} - {x.title} - {x.created_at} - {x.type} - {x.finished}')

with Session(engine) as session:
    stmt = (
        select(
            Experiment.title, 
            func.sum(DataPoint.real_value).label("sum_real"), 
            func.sum(DataPoint.target_value).label("sum_target"),
            func.avg(DataPoint.real_value).label("avg_real"),
            func.avg(DataPoint.target_value).label("avg_target"), 
        )
        .join(Experiment.dataPoints)
        .group_by(Experiment.id)
    )

    print('DataPoints aggregation:')
    for row in session.execute(stmt).all():
         print(f'{row.title}: sum real={row.sum_real}, sum target={row.sum_target}, avg real={row.avg_real}, avg target={row.avg_target}')
    
# with Session(engine) as session:
#      stmt = delete(Experiment)
#      session.execute(stmt)
#      stmt = delete(DataPoint)
#      session.execute(stmt)
#      session.commit()