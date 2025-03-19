import streamlit as st
from utils import fetch_news, analyze_sentiment, text_to_speech, translate_to_hindi

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

            sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

            for idx, article in enumerate(articles):
                article["sentiment"] = analyze_sentiment(article["summary"])
                hindi_summary = translate_to_hindi(article["summary"])
                sentiment_counts[article["sentiment"]] += 1

                with st.expander(f"📰 {idx+1}. {article['title']} ({article['sentiment']})"):
                    st.write(f"**Summary (English):** {article['summary']}")
                    st.write(f"**सारांश (हिन्दी):** {hindi_summary}")
                    st.write(f"**URL:** [Read More]({article['url']})")

            st.subheader("📊 Sentiment Distribution")
            st.bar_chart(sentiment_counts)

            if sentiment_counts["Neutral"] > sentiment_counts["Positive"] and sentiment_counts["Neutral"] > sentiment_counts["Negative"]:
                insight_message = "The news coverage is mostly neutral."
            elif sentiment_counts["Positive"] > sentiment_counts["Negative"]:
                insight_message = "The company is receiving mostly positive news coverage."
            elif sentiment_counts["Positive"] == sentiment_counts["Negative"]:
                insight_message = "The company is receiving mostly balanced news coverage."
            else:
                insight_message = "The company is facing mostly negative news coverage."

            st.subheader("📌 Key Insights")
            hindi_insight = translate_to_hindi(insight_message)
            
            st.write(f"✅ **English:** {insight_message}")
            st.write(f"✅ **हिन्दी:** {hindi_insight}")

            st.subheader("🔊 Listen to the Summary in English & Hindi")
            english_audio = text_to_speech(insight_message, "en", "summary_english.mp3")
            hindi_audio = text_to_speech(hindi_insight, "hi", "summary_hindi.mp3")

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
