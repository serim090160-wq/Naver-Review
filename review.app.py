import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import platform

# matplotlib 한글 폰트 설정
plt.rcParams['axes.unicode_minus'] = False

# 운영체제별 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux (Streamlit Cloud)
    plt.rcParams['font.family'] = 'DejaVu Sans'

st.set_page_config(page_title="네이버 리뷰 분석", layout="wide")

# 제목
st.title("📊 네이버 지도 리뷰 데이터 분석 대시보드")

# 파일 업로드 위젯
uploaded_file = st.file_uploader(
    "📁 엑셀 파일을 업로드하세요 (네이버 지도 방문자 리뷰 데이터)",
    type=['xlsx', 'xls'],
    help="전처리된 네이버 지도 리뷰 데이터 파일을 업로드해주세요"
)

# 엑셀 파일 읽기
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ 데이터 로드 성공!")
        
        # 데이터 미리보기
        with st.expander("� 데이터 미리보기 (처음 5행)", expanded=True):
            st.dataframe(df.head(), use_container_width=True)
        
        # 데이터 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 행 수", len(df))
        with col2:
            st.metric("총 열 수", len(df.columns))
        with col3:
            st.metric("컬럼 목록", ", ".join(df.columns[:3]) + "...")
        
        # 필수 컬럼 존재 확인
        required_cols = ['Listing_Position', 'Sentiment_Score', 'Visitor_Review_Count', 'Blog_Review_Count', 'Keywords_Excl_Food']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ 필수 컬럼이 누락되었습니다: {', '.join(missing_cols)}")
            st.info(f"📌 필요한 컬럼: {', '.join(required_cols)}")
            st.info(f"📌 현재 파일의 컬럼: {', '.join(df.columns.tolist())}")
            st.stop()
        
        # 열 정리
        df['Listing_Position'] = df['Listing_Position'].astype(str)
        
        st.divider()
        
        # ------------------------
        st.header("1️⃣ 감정 점수 평균 (상단 vs 하단)")
        avg_sentiment = df.groupby('Listing_Position')['Sentiment_Score'].mean()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(avg_sentiment)
        with col2:
            st.dataframe(avg_sentiment.reset_index().rename(columns={
                'Listing_Position': '위치',
                'Sentiment_Score': '평균 감정 점수'
            }), use_container_width=True)
        
        st.divider()
        
        # ------------------------
        st.header("2️⃣ 방문자 리뷰 수 & 블로그 리뷰 수 비교")
        st.subheader("박스플롯으로 비교")
        
        fig1, ax1 = plt.subplots(1, 2, figsize=(14, 5))
        sns.boxplot(data=df, x='Listing_Position', y='Visitor_Review_Count', ax=ax1[0], palette='Set2')
        ax1[0].set_title("📦 방문자 리뷰 수", fontsize=14, fontweight='bold')
        ax1[0].set_xlabel("위치", fontsize=12)
        ax1[0].set_ylabel("리뷰 수", fontsize=12)
        
        sns.boxplot(data=df, x='Listing_Position', y='Blog_Review_Count', ax=ax1[1], palette='Set3')
        ax1[1].set_title("📦 블로그 리뷰 수", fontsize=14, fontweight='bold')
        ax1[1].set_xlabel("위치", fontsize=12)
        ax1[1].set_ylabel("리뷰 수", fontsize=12)
        
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()
        
        st.divider()
        
        # ------------------------
        st.header("3️⃣ 감정 점수 vs 리뷰 수 (산점도)")
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(
            data=df,
            x='Visitor_Review_Count',
            y='Sentiment_Score',
            hue='Listing_Position',
            alpha=0.7,
            s=100,
            palette='viridis'
        )
        ax2.set_title("🟣 감정 점수 vs 방문자 리뷰 수", fontsize=14, fontweight='bold')
        ax2.set_xlabel("방문자 리뷰 수", fontsize=12)
        ax2.set_ylabel("감정 점수", fontsize=12)
        ax2.legend(title='위치')
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()
        
        st.divider()
        
        # ------------------------
        st.header("4️⃣ 키워드 기반 워드클라우드 (음식 키워드 제외)")
        
        text = " ".join(df["Keywords_Excl_Food"].dropna().astype(str))
        if len(text.strip()) > 0:
            # 한글 폰트 경로 설정 (시스템별)
            font_path = None
            if platform.system() == 'Windows':
                font_path = 'c:/Windows/Fonts/malgun.ttf'
            elif platform.system() == 'Darwin':
                font_path = '/System/Library/Fonts/AppleGothic.ttf'
            # Linux는 기본값 사용
            
            wordcloud = WordCloud(
                width=1200,
                height=600,
                background_color='white',
                font_path=font_path,
                colormap='viridis',
                relative_scaling=0.5,
                min_font_size=10
            ).generate(text)
            
            fig3, ax3 = plt.subplots(figsize=(14, 7))
            ax3.imshow(wordcloud, interpolation='bilinear')
            ax3.axis("off")
            ax3.set_title("☁️ 키워드 워드클라우드", fontsize=16, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close()
        else:
            st.info("ℹ️ 키워드 데이터가 부족하거나 비어 있습니다.")
        
        st.divider()
        
        # ------------------------
        if 'Category' in df.columns:
            st.header("5️⃣ 업종별 감정 점수 비교")
            
            fig4, ax4 = plt.subplots(figsize=(12, 6))
            sns.boxplot(data=df, x='Category', y='Sentiment_Score', palette='pastel')
            ax4.set_title("카테고리별 감정 점수", fontsize=14, fontweight='bold')
            ax4.set_xlabel("카테고리", fontsize=12)
            ax4.set_ylabel("감정 점수", fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig4)
            plt.close()
            
        # 데이터 다운로드
        st.divider()
        st.header("📥 데이터 다운로드")
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="💾 CSV 파일로 다운로드",
            data=csv,
            file_name='naver_review_analysis.csv',
            mime='text/csv',
        )
        
    except Exception as e:
        st.error(f"❌ 파일을 읽는 중 오류가 발생했습니다: {str(e)}")
        st.info("💡 엑셀 파일 형식이 올바른지 확인해주세요.")
        
else:
    st.info("👆 상단에서 엑셀 파일을 업로드하면 분석이 시작됩니다.")
    
    # 사용 안내
    with st.expander("📖 사용 방법", expanded=True):
        st.markdown("""
        ### 필수 컬럼
        업로드하는 엑셀 파일에는 다음 컬럼들이 반드시 포함되어야 합니다:
        
        - `Listing_Position`: 리스팅 위치 (예: 상단, 하단)
        - `Sentiment_Score`: 감정 점수
        - `Visitor_Review_Count`: 방문자 리뷰 수
        - `Blog_Review_Count`: 블로그 리뷰 수
        - `Keywords_Excl_Food`: 키워드 (음식 제외)
        
        ### 선택 컬럼
        - `Category`: 업종 카테고리 (있으면 추가 분석 제공)
        
        ### 지원 파일 형식
        - `.xlsx` (Excel 2007 이상)
        - `.xls` (Excel 97-2003)
        """)
