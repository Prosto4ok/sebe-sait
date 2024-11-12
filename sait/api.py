from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from database import workwithbd
import uvicorn

app = FastAPI()

# Настройка CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic модели для работы с отзывами

class ReviewItem(BaseModel):
    ReviewId: Optional[int] = None
    Name: Optional[str] = None
    Photo: Optional[str] = None
    ReviewText: Optional[str] = None
    Created_at: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True

class Reviews(BaseModel):
    count: int
    results: List[ReviewItem]

    class Config:
        orm_mode = True
        from_attributes = True

# Эндпоинты API для работы с отзывами

@app.get("/reviews/", response_model=Reviews)
async def read_reviews():
    results = await conn.get_reviews()
    
    review_items = [ReviewItem(ReviewId=i[0], Name=i[1], Photo=i[2], ReviewText=i[3], Created_at=i[4]) for i in results]
    return {"count": len(results), "results": review_items}


@app.post("/reviews/")
async def create_review(name: str = Form(...), photo: str = Form(None), review_text: str = Form(...)):
    result = await conn.post_review(name, photo, review_text)
    return {"ReviewId": result}


@app.put("/reviews/{review_id}/")
async def update_review(review_id: int, name: str = Form(...), photo: str = Form(None), review_text: str = Form(...)):
    await conn.update_review(review_id, name, photo, review_text)
    return {"message": "Review updated successfully"}


@app.delete("/reviews/{review_id}/")
async def delete_review(review_id: int):
    await conn.delete_review(review_id)
    return {"message": "Review deleted successfully"}

# Запуск сервера
if __name__ == "__main__":
    conn = workwithbd()
    uvicorn.run(app, host="127.0.0.1", port=9010)
