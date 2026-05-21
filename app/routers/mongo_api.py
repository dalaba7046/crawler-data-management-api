from fastapi import APIRouter, HTTPException, status

from app.config.mongodb import mongo_client, mongo_db

router = APIRouter()


def serialize_raw_item(document):
    return {
        "id": str(document["_id"]),
        "sku_id": document.get("sku_id"),
        "site_id": document.get("site_id"),
        "source_url": document.get("source_url"),
        "raw_title": document.get("raw_title"),
        "raw_price": document.get("raw_price"),
        "scraped_at": document.get("scraped_at"),
    }


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    try:
        mongo_client.admin.command("ping")
    except Exception as exc:
        raise HTTPException(status_code=503, detail="MongoDB unavailable") from exc
    return {"status": "ok", "database": mongo_db.name}


@router.get("/raw-items", status_code=status.HTTP_200_OK)
def get_raw_items():
    documents = mongo_db.raw_items.find().sort("sku_id", 1).limit(50)
    return [serialize_raw_item(document) for document in documents]
