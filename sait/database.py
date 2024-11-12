from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import asyncio

DATABASE_URL = "mysql+aiomysql://root@localhost/reviews_db"  # Используем базу данных для отзывов

class workwithbd:
    def __init__(self) -> None:
        self.engine = create_async_engine(DATABASE_URL, echo=True, future=True)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.Base = declarative_base()

    # Проверка соединения с базой данных
    async def check_connection(self):
        try:
            async with self.async_session() as session:
                result = await session.execute(text("SELECT 1"))
                print("Подключение к базе данных успешно!")
        except SQLAlchemyError as e:
            print(f"Ошибка подключения к базе данных: {e}")

    # Получение всех отзывов
    async def get_reviews(self):
        async with self.async_session() as session:
            stmt = text("SELECT ReviewId, Name, Photo, ReviewText, Created_at FROM Reviews;")
            result = await session.execute(stmt)
            rows = result.all()
            await session.commit()
            return rows

    # Добавление нового отзыва
    async def post_review(self, name, photo, review_text):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "INSERT INTO Reviews (Name, Photo, ReviewText) VALUES (:name, :photo, :review_text);"
                )
                params = {
                    "name": name,
                    "photo": photo,
                    "review_text": review_text,
                }
                result = await session.execute(stmt, params)
                await session.commit()
                return result.lastrowid
        except SQLAlchemyError as e:
            print(f"Ошибка при добавлении отзыва: {e}")

    # Обновление отзыва
    async def update_review(self, review_id, name, photo, review_text):
        try:
            async with self.async_session() as session:
                stmt = text(
                    "UPDATE Reviews SET Name = :name, Photo = :photo, ReviewText = :review_text WHERE ReviewId = :review_id;"
                )
                params = {
                    "review_id": review_id,
                    "name": name,
                    "photo": photo,
                    "review_text": review_text,
                }
                result = await session.execute(stmt, params)
                await session.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при обновлении отзыва: {e}")

    # Удаление отзыва
    async def delete_review(self, review_id):
        try:
            async with self.async_session() as session:
                stmt = text("DELETE FROM Reviews WHERE ReviewId = :review_id;")
                params = {"review_id": review_id}
                result = await session.execute(stmt, params)
                await session.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при удалении отзыва: {e}")
