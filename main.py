# main.py
from fastapi import FastAPI

from routers.blog import router as blog_router
from routers.education import router as education_router
from routers.favorits import router as favorits_router
from routers.lessons import router as lessons_router
from routers.profile import router as profile_router
from routers.projects import router as projects_router
from routers.publications import router as publications_router
from routers.skills import router as skills_router
from routers.volunteers import router as volunteers_router
from routers.workexp import router as workexp_router
from routers.users import router as user_router

app = FastAPI()

app.include_router(workexp_router)
app.include_router(blog_router)
app.include_router(education_router)
app.include_router(favorits_router)
app.include_router(lessons_router)
app.include_router(profile_router)
app.include_router(projects_router)
app.include_router(publications_router)
app.include_router(skills_router)
app.include_router(volunteers_router)
app.include_router(user_router)

