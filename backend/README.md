# TIPSMAX 1.0 Backend

FastAPI 기반 문서 분석 API 서버

## 설치 및 실행

```bash
# 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집하여 API 키 설정

# 서버 실행
uvicorn app.main:app --reload
```

## API 문서

서버 실행 후 `http://localhost:8000/docs`에서 Swagger UI 확인 가능
