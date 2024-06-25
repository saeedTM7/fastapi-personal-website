from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

DATABASE_URL = "postgresql://postgres:1234@localhost/fastapisaeed"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



from models.blog import Blog
from models.education import Education
from models.favorits import Favorit
from models.lessons import Lesson
from models.profile import Profile
from models.projects import Project
from models.publications import Publication
from models.skills import Skill
from models.volunteers import Volunteer
from models.workexp import Workexp
from models.users import User

Base.metadata.create_all(bind=engine)
