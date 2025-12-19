# 📊 네이버 지도 리뷰 데이터 분석 대시보드

Streamlit 기반 네이버 지도 리뷰 데이터 분석 및 시각화 대시보드입니다.

## 🚀 실행 방법

1. **필요한 패키지 설치**
```bash
pip install -r requirements.txt
```

2. **앱 실행**
```bash
streamlit run app.py
```

3. **브라우저에서 자동으로 열립니다** (보통 http://localhost:8501)

## 📋 필수 컬럼

업로드하는 엑셀 파일에는 다음 컬럼들이 반드시 포함되어야 합니다:

- `Listing_Position`: 상단/하단 구분
- `Sentiment_Score`: 감정 점수
- `Visitor_Review_Count`: 방문자 리뷰 수
- `Blog_Review_Count`: 블로그 리뷰 수
- `Keywords_Excl_Food`: 음식 제외 키워드

## 📊 제공 기능

1. **감정 점수 평균**: 상단 vs 하단 비교
2. **리뷰 수 비교**: 방문자 리뷰 & 블로그 리뷰 박스플롯
3. **산점도**: 감정 점수 vs 리뷰 수 관계 분석
4. **워드클라우드**: 키워드 기반 시각화
5. **카테고리별 분석**: 업종별 감정 점수 비교 (선택)

## ⚠️ 한글 폰트 설정 (워드클라우드)

한글이 깨지는 경우, `app.py`의 `font_path`를 수정하세요:

```python
wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color='white',
    font_path='C:/Windows/Fonts/malgun.ttf'  # Windows 맑은 고딕
).generate(text)
```
