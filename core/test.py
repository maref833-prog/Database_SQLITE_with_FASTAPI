from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.sql import func
DATABASE_URL="sqlite:///./test.db"
engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
sessionlocal=sessionmaker(autoflush=False,bind=engine)
base=declarative_base()
class user(base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(50))
    last=Column(String(50))
    age=Column(Integer)
    def __repr__(self):
     return f"useer={self.id},name={self.name},lastname={self.last},age={self.age}"
    
base.metadata.create_all(bind=engine)
ses=sessionlocal()
userr=user(name="aref",age=26,last="moradi")
ses.add(userr)
ses.commit()
user_fond=list(ses.query(user).filter_by(name="aef"))
if user_fond:
   for item in user_fond:
    ses.delete(item)
    ses.commit()
use=ses.query(user).filter_by(name="s").first()
if use:
 use.name="mamad"
 ses.commit()
 
 #فیلتر برای بالای 25سال
ages=ses.query(user.age)
sss=ses.query(user).filter(user.age>25).all()
print(sss)
#جمع کردن سن ها
summ=ses.query(func.sum(user.age)).scalar()
print(summ)
#میانگین سن
avg=ses.query(func.avg(user.age)).scalar()
print(avg)

