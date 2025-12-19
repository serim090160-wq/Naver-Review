import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Set page config
st.set_page_config(page_title="Naver Review Analysis", layout="wide")

# Title
st.title("📊 Naver Map Review Data Analysis Dashboard")

# File uploader widget
uploaded_file = st.file_uploader(
    "📁 Upload Excel file (Naver Map Visitor Review Data)",
    type=['xlsx', 'xls'],
    help="Please upload preprocessed Naver Map review data file"
)

# Read Excel file
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Data loaded successfully!")
        
        # Data preview
        with st.expander("📋 Data Preview (First 5 rows)", expanded=True):
            st.dataframe(df.head(), use_container_width=True)
        
        # Data information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", len(df))
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric("Columns", ", ".join(df.columns[:3]) + "...")
        
        # Check required columns
        required_cols = ['Listing_Position', 'Sentiment_Score', 'Visitor_Review_Count', 'Blog_Review_Count', 'Keywords_Excl_Food']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
            st.info(f"📌 Required columns: {', '.join(required_cols)}")
            st.info(f"📌 Current file columns: {', '.join(df.columns.tolist())}")
            st.stop()
        
        # Data cleaning
        df['Listing_Position'] = df['Listing_Position'].astype(str)
        
        st.divider()
        
        # ------------------------
        st.header("1️⃣ Average Sentiment Score (Top vs Bottom)")
        avg_sentiment = df.groupby('Listing_Position')['Sentiment_Score'].mean()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(avg_sentiment)
        with col2:
            st.dataframe(avg_sentiment.reset_index().rename(columns={
                'Listing_Position': 'Position',
                'Sentiment_Score': 'Avg Sentiment Score'
            }), use_container_width=True)
        
        st.divider()
        
        # ------------------------
        st.header("2️⃣ Visitor Review Count & Blog Review Count Comparison")
        st.subheader("Boxplot Comparison")
        
        fig1, ax1 = plt.subplots(1, 2, figsize=(14, 5))
        sns.boxplot(data=df, x='Listing_Position', y='Visitor_Review_Count', ax=ax1[0], palette='Set2')
        ax1[0].set_title("📦 Visitor Review Count", fontsize=14, fontweight='bold')
        ax1[0].set_xlabel("Position", fontsize=12)
        ax1[0].set_ylabel("Review Count", fontsize=12)
        
        sns.boxplot(data=df, x='Listing_Position', y='Blog_Review_Count', ax=ax1[1], palette='Set3')
        ax1[1].set_title("📦 Blog Review Count", fontsize=14, fontweight='bold')
        ax1[1].set_xlabel("Position", fontsize=12)
        ax1[1].set_ylabel("Review Count", fontsize=12)
        
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()
        
        st.divider()
        
        # ------------------------
        st.header("3️⃣ Sentiment Score vs Review Count (Scatter Plot)")
        
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
        ax2.set_title("🟣 Sentiment Score vs Visitor Review Count", fontsize=14, fontweight='bold')
        ax2.set_xlabel("Visitor Review Count", fontsize=12)
        ax2.set_ylabel("Sentiment Score", fontsize=12)
        ax2.legend(title='Position')
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()
        
        st.divider()
        
        # ------------------------
        st.header("4️⃣ Keyword-based Word Cloud (Food Keywords Excluded)")
        
        text = " ".join(df["Keywords_Excl_Food"].dropna().astype(str))
        if len(text.strip()) > 0:
            try:
                wordcloud = WordCloud(
                    width=1200,
                    height=600,
                    background_color='white',
                    colormap='viridis',
                    relative_scaling=0.5,
                    min_font_size=10
                ).generate(text)
                
                fig3, ax3 = plt.subplots(figsize=(14, 7))
                ax3.imshow(wordcloud, interpolation='bilinear')
                ax3.axis("off")
                ax3.set_title("Word Cloud - Keywords", fontsize=16, fontweight='bold', pad=20)
                plt.tight_layout()
                st.pyplot(fig3)
                plt.close()
            except Exception as e:
                st.warning(f"⚠️ Error generating word cloud: {str(e)}")
        else:
            st.info("ℹ️ Insufficient or empty keyword data.")
        
        st.divider()
        
        # ------------------------
        if 'Category' in df.columns:
            st.header("5️⃣ Sentiment Score by Category")
            
            fig4, ax4 = plt.subplots(figsize=(12, 6))
            sns.boxplot(data=df, x='Category', y='Sentiment_Score', palette='pastel')
            ax4.set_title("Sentiment Score by Category", fontsize=14, fontweight='bold')
            ax4.set_xlabel("Category", fontsize=12)
            ax4.set_ylabel("Sentiment Score", fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig4)
            plt.close()
            
        # Data download
        st.divider()
        st.header("📥 Download Data")
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="💾 Download as CSV",
            data=csv,
            file_name='naver_review_analysis.csv',
            mime='text/csv',
        )
        
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        st.info("💡 Please check if the Excel file format is correct.")
        
else:
    st.info("👆 Upload an Excel file above to start the analysis.")
    
    # User guide
    with st.expander("📖 How to Use", expanded=True):
        st.markdown("""
        ### Required Columns
        The uploaded Excel file must include the following columns:
        
        - `Listing_Position`: Listing position (e.g., Top, Bottom)
        - `Sentiment_Score`: Sentiment score
        - `Visitor_Review_Count`: Visitor review count
        - `Blog_Review_Count`: Blog review count
        - `Keywords_Excl_Food`: Keywords (food excluded)
        
        ### Optional Columns
        - `Category`: Business category (provides additional analysis if present)
        
        ### Supported File Formats
        - `.xlsx` (Excel 2007 or later)
        - `.xls` (Excel 97-2003)
        """)
