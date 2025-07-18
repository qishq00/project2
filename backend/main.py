from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# --- Конфигурация приложения ---
app = FastAPI()

# --- Настройка CORS ---
origins = [
    "http://localhost:3000",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic модели (структура данных) ---
class PostBase(BaseModel):
    slug: str
    title: str
    author: str
    date: str
    category: str

class PostFull(PostBase):
    content: str

# --- База данных в памяти (простой список Python) ---
fake_posts_db: List[PostFull] = [
    PostFull(
        slug="first-post",
        title="Мой первый пост",
        author="Иван Иванов",
        date="2024-06-01",
        category="Разработка",
        content="# Привет, мир!\n\nЭто **содержимое** моего первого поста. Здесь много интересного текста о веб-разработке!\n\n- Пункт 1\n- Пункт 2\n\n[FastAPI](https://fastapi.tiangolo.com/) — современный Python-фреймворк."
    ),
    PostFull(
        slug="fastapi-and-nextjs",
        title="FastAPI + Next.js = ❤️",
        author="Анна Петрова",
        date="2024-06-02",
        category="Фреймворки",
        content="## Почему это круто?\n\nСочетание **FastAPI** для бэкенда и _Next.js_ для фронтенда — это мощный и современный стек.\n\n- Асинхронность FastAPI\n- SSR и SSG в Next.js\n\n> Вместе они творят чудеса!"
    ),
    PostFull(
        slug="why-i-love-python",
        title="Почему я люблю Python",
        author="Павел Смирнов",
        date="2024-06-03",
        category="Языки программирования",
        content="Python — это язык с простым синтаксисом и огромной экосистемой.\n\n- Отлично подходит для бэкенда\n- Анализа данных\n- Многого другого!\n\n```python\nprint('Hello, Python!')\n```"
    )
]

# --- Эндпоинты API ---

# Отдает краткий список всех постов (slug и title)
@app.get("/api/posts", response_model=List[PostBase])
async def get_all_posts():
    return fake_posts_db

# Отдает полную информацию о конкретном посте по его slug
@app.get("/api/posts/{slug}", response_model=PostFull)
async def get_post_by_slug(slug: str):
    for post in fake_posts_db:
        if post.slug == slug:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/")
async def root():
    return {"message": "Blog API is running"}