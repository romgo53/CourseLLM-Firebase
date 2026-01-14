import pytest
from httpx import AsyncClient
from app.main import app

# @pytest.mark.asyncio
# async def test_health():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         r = await ac.get('/health')
#         assert r.status_code == 200
#         assert r.json() == {"status": "ok"}

# @pytest.mark.asyncio
# async def test_extract():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         r = await ac.post('/extract', json={"text": "This is a test about machine learning and data science."})
#         assert r.status_code == 200
#         data = r.json()
#         assert 'topics' in data
#         assert isinstance(data['topics'], list)
