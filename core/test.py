from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
sessionlocal = sessionmaker(autoflush=False, bind=engine)
base = declarative_base()

class user(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    last = Column(String(50))
    age = Column(Integer)
    
    
    addresses = relationship("Address", back_populates="user")  # به کلاس Address اشاره می‌کند

    def __repr__(self):
        return f"user={self.id}, name={self.name}, lastname={self.last}, age={self.age}"

class Address(base): 
    __tablename__ = "addresses"  # 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_id = Column(Integer, ForeignKey("users.id"))  
    city = Column(String(50))
    code_city = Column(Integer)
    
    # ✅ اصلاح: back_populates باید به "addresses" در کلاس user اشاره کند
    user = relationship("user", back_populates="addresses")  # back_populates="addresses" (جمع)
    
    def __repr__(self):
        return f"Address(id={self.id}, user_id={self.name_id}, city={self.city}, code={self.code_city})"

# ساخت جداول
base.metadata.create_all(bind=engine)
ses = sessionlocal()

# اضافه کردن کاربر
userr = user(name="aref", age=26, last="moradi")
ses.add(userr)
ses.commit()
print("1. User added:", userr)

# حذف کاربر با نام "aef"
user_found = list(ses.query(user).filter_by(name="aef"))
if user_found:
    for item in user_found:
        ses.delete(item)
        ses.commit()
        print("Deleted:", item)
else:
    print("2. No user found with name 'aef'")

# پیدا کردن و ویرایش کاربر با نام "s"
use = ses.query(user).filter_by(name="s").first()
if use:
    use.name = "mamad"
    ses.commit()
    print("3. Updated:", use)
else:
    print("3. No user found with name 's'")

# فیلتر برای بالای 25 سال
print("\n4. Users older than 25:")
sss = ses.query(user).filter(user.age > 25).all()
for u in sss:
    print(f"   {u}")

# جمع کردن سن ها
summ = ses.query(func.sum(user.age)).scalar()
print(f"\n5. Sum of ages: {summ}")

# میانگین سن
avg = ses.query(func.avg(user.age)).scalar()
print(f"6. Average age: {avg}")

# اضافه کردن چند کاربر دیگر
print("\n7. Adding more users...")
users_to_add = [
    user(name="ali", age=30, last="rezaei"),
    user(name="sara", age=22, last="ahmadi"),
    user(name="reza", age=35, last="karimi")
]
for u in users_to_add:
    ses.add(u)
ses.commit()
print(f"   Added {len(users_to_add)} users")

# نمایش همه کاربران
print("\n8. All users:")
all_users = ses.query(user).all()
for u in all_users:
    print(f"   {u}")

# اضافه کردن آدرس برای کاربر aref
print("\n9. Adding address for aref...")
user_aref = ses.query(user).filter_by(name="aref").first()
if user_aref:
    address = Address(name_id=user_aref.id, city="Tehran", code_city=12345)
    ses.add(address)
    ses.commit()
    print(f"   Added: {address}")

# نمایش کاربر با آدرس‌هایش
print("\n10. User with addresses:")
user_with_address = ses.query(user).filter_by(name="aref").first()
if user_with_address:
    print(f"   User: {user_with_address.name} {user_with_address.last}")
    for addr in user_with_address.addresses:
        print(f"     Address: {addr.city}, Code: {addr.code_city}")