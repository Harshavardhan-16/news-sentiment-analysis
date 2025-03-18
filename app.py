import streamlit as st
from utils import fetch_news, analyze_sentiment, comparative_sentiment_analysis, text_to_speech, translate_to_hindi

st.set_page_config(page_title="News Sentiment Analysis", layout="wide")
st.title("🔍 Company News Sentiment Analysis")
st.write("Enter a company name to fetch the latest news, analyze sentiment, and generate English and Hindi speech summaries.")

company_name = st.text_input("Enter Company Name:", "")

if st.button("Fetch News"):
    if company_name:
        with st.spinner(f"Fetching latest news for {company_name}..."):
            articles = fetch_news(company_name)

        if "error" in articles:
            st.error("Failed to fetch news. Please try again.")
        else:
            st.success("News articles fetched successfully!")

            for idx, article in enumerate(articles):
                sentiment = analyze_sentiment(article["summary"])
                hindi_summary = translate_to_hindi(article["summary"])
                
                with st.expander(f"📰 {idx+1}. {article['title']} ({sentiment})"):
                    st.write(f"**Summary (English):** {article['summary']}")
                    st.write(f"**सारांश (हिन्दी):** {hindi_summary}")
                    st.write(f"**URL:** [Read More]({article['url']})")

            analysis_results = comparative_sentiment_analysis(articles)

            st.subheader("📊 Sentiment Distribution")
            st.bar_chart(analysis_results["sentiment_distribution"])

            st.subheader("📌 Key Insights")
            insights_english = analysis_results["insights"]
            insights_hindi = [translate_to_hindi(insight) for insight in insights_english]

            for eng, hin in zip(insights_english, insights_hindi):
                st.write(f"✅ **English:** {eng}")
                st.write(f"✅ **हिन्दी:** {hin}")

            st.subheader("🔊 Listen to the Summary in English & Hindi")
            english_summary = ". ".join(insights_english)
            hindi_summary = ". ".join(insights_hindi)

            english_audio = text_to_speech(english_summary, "en", "summary_english.mp3")
            hindi_audio = text_to_speech(hindi_summary, "hi", "summary_hindi.mp3")

            col1, col2 = st.columns(2)
            with col1:
                st.write("🎧 English Summary")
                if english_audio:
                    st.audio(english_audio, format="audio/mp3", start_time=0)
            with col2:
                st.write("🎧 Hindi Summary")
                if hindi_audio:
                    st.audio(hindi_audio, format="audio/mp3", start_time=0)

            st.success("✅ Audio summaries are ready!")
    else:
        st.warning("Please enter a company name.")
