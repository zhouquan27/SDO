# NFPA Scraper

Playwright-based scraper that opens `nfpa.org`, searches for a term, and prints product titles. Environment variables configure headless mode, query term, and trace path.

## Quick start (Docker)

```powershell
# Build image
docker build -t nfpa-scraper .

# Run (headless by default)
docker run --rm -e NFPA_QUERY="NFPA 70" nfpa-scraper

# Run with UI (not typical in containers)
docker run --rm -e HEADLESS=false -p 9222:9222 nfpa-scraper
```

Environment variables:
- `HEADLESS` (default `true`): set to `false`/`0` to see the browser.
- `NFPA_QUERY` (default `"NFPA 70"`): search term.
- `TRACE_PATH` (default `handler_trace.zip`): path for Playwright trace zip.

## Local run

Install Playwright and browsers, then run:
```powershell
pip install playwright
playwright install chromium
python nfpa.py
```

## CEN Standards API

Expose `cen.py` scraping logic as a FastAPI service.

```powershell
# Install deps
pip install -r requirements.txt

# Run API (listens on http://0.0.0.0:8000)
uvicorn cen_api:app --host 0.0.0.0 --port 8000

# Call the search endpoint
curl -X POST "http://localhost:8000/search" -H "Content-Type: application/json" -d "{\"query\":\"ISO 9001\"}"
```

Endpoints:
- `GET /health`: service status.
- `POST /search`: body `{ "query": "ISO 9001" }`; returns parsed rows plus raw excerpt for debugging.

运行并测试
cd "c:\Users\enzo.zhou\Enzo\Dev\TUV\SDO"
docker build -t SDO-scraper .

# 启动容器（映射 8000 端口）
docker run --rm -p 8000:8000 gaipublishcr.azurecr.cn/poc/sdo-scraper

# 健康检查
curl http://127.0.0.1:8000/health

# 触发搜索
curl -X POST "http://127.0.0.1:8000/nfpa" -H "Content-Type: application/json" -d "{\"query\":\"NFPA 70\"}"


本地运行（不经容器）
uvicorn main:app --host 127.0.0.1 --port 8000

测试接口
curl http://localhost:8000/health
curl -X POST "http://localhost:8000/nfpa" -H "Content-Type: application/json" -d "{\"query\":\"NFPA 70\"}"


--1.创建本地docker
docker build -t gaipublishcr.azurecr.cn/poc/sdo-scraper .
--2.登录
az cloud set --name AzureChinaCloud
docker login --username=gaipublishcr --password=<replace-with-your-password>
--3.推送包

docker tag gaipublishcr.azurecr.cn/poc/sdo-scraper:v1.0 gaipublishcr.azurecr.cn/poc/sdo-scraper:v1.0
docker push gaipublishcr.azurecr.cn/poc/sdo-scraper:v1.0

docker tag gaipublishcr.azurecr.cn/poc/sdo-scraper:latest gaipublishcr.azurecr.cn/poc/sdo-scraper:latest
docker push gaipublishcr.azurecr.cn/poc/sdo-scraper:latest