# Crawler Data Management API

爬蟲資料管理 API 是一個後端 side project / practice project，目標是使用 FastAPI 建立一個可串接 MySQL 的 API server，用來管理爬蟲落地後的 SKU、產品評論與評價資料。

這個專案重點不是展示爬蟲本身，而是練習爬蟲資料進入資料庫後，如何透過後端 API、ORM model 與 schema 分層提供查詢與管理能力。

## 專案定位

- 建立 FastAPI API server
- 使用 SQLAlchemy ORM 對應 MySQL 資料表
- 使用 Pydantic schema 定義 API response / request 結構
- 以 Dockerfile 提供容器化執行基礎
- 練習產品 SKU、review、rating 等爬蟲資料的查詢與管理流程

## 技術棧

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- MySQL / PyMySQL
- pandas / openpyxl
- Docker
- Uvicorn

## 目前已實作 API

目前 `app/main.py` 將 `item_api` router 掛載在 `/v1/item` prefix 下，因此實際路由如下：

| Method | Path | 說明 |
|---|---|---|
| GET | `/v1/item/items` | 查詢資料庫中的所有 SKU |
| GET | `/v1/item/item/{item_id}` | 查詢指定 SKU 資料 |
| POST | `/v1/item/item` | 新增 SKU 資料 |
| PUT | `/v1/item/item/{item_id}` | 軟刪除指定 SKU 資料 |

## 資料模型

專案目前包含以下資料模型草稿：

- `Items`: SKU 主檔資料
- `Review`: 產品評論資料
- `Rating`: 產品評價資料
- `ReviewId`: 評論 ID 對應資料

這些 model 用來模擬爬蟲資料進入資料庫後的查詢與管理場景。

## 專案結構

```text
app/
├── main.py
├── config/
├── models/
│   ├── jd_model.py
│   └── dpms_model.py
├── routers/
│   ├── item_api.py
│   └── dpms_api.py
├── schemas/
│   └── jd_schema.py
└── services/
    └── jd/
```

## 執行方式

安裝套件：

```bash
pip install -r requirements.txt
```

啟動 API server：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 80
```

或使用 Dockerfile 建立容器化執行環境。

## 履歷摘要用語

可作為後端 side project 佐證：

> 建立 FastAPI + MySQL 的爬蟲資料管理 API，使用 SQLAlchemy ORM 與 Pydantic schema 管理 SKU、產品評論與評價資料，並以 Docker / Uvicorn 建立 API server 執行基礎。

## 備註

這是學習與 side project 用途的後端 API 專案，不宣稱為 production-ready 系統。