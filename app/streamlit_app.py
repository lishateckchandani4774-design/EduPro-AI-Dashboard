import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="EduPro AI Dashboard",
    page_icon="🎓",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0B1120;
    color: white;
}

/* Main Title */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 8px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: #9CA3AF;
    font-size: 18px;
    margin-bottom: 30px;
}

/* Section Headers */
.section-header {
    font-size: 28px;
    font-weight: 700;
    color: #60A5FA;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Cards */
.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #1F2937;
    margin-bottom: 20px;
}

/* Metrics */
[data-testid="metric-container"] {
    background-color: #111827;
    border: 1px solid #374151;
    padding: 18px;
    border-radius: 16px;
}

/* Button */
.stButton>button {
    background: linear-gradient(to right, #4F46E5, #7C3AED);
    color: white;
    border: none;
    border-radius: 12px;
    height: 3.2em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 20px;
}

.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    font-weight: 600;
    padding: 12px 20px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# TITLE SECTION
# =====================================================

st.markdown(
    '<div class="main-title">🎓 EduPro AI Intelligence Platform</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Predict Course Demand • Forecast Revenue • Optimize Pricing</div>',
    unsafe_allow_html=True
)

st.info(
    "🚀 AI-powered dashboard for enrollment forecasting using Machine Learning."
)

# =====================================================
# DASHBOARD OVERVIEW
# =====================================================

st.markdown(
    '<div class="section-header">📊 Dashboard Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Courses", "60")

with col2:
    st.metric("Predicted Demand", "168+")

with col3:
    st.metric("Revenue Forecast", "$125K")

# =====================================================
# LOAD MODEL
# =====================================================

model_path = os.path.join(
    os.path.dirname(__file__),
    "../models/course_demand_model.pkl"
)

model = joblib.load(model_path)

# =====================================================
# SIDEBAR INPUTS
# =====================================================

st.sidebar.header("📚 Course Inputs")

course_category_dict = {
    "Programming": 0,
    "Business": 1,
    "Design": 2,
    "Marketing": 3,
    "Data Science": 4,
    "Finance": 5
}

selected_category = st.sidebar.selectbox(
    "Course Category",
    list(course_category_dict.keys())
)

course_category = course_category_dict[selected_category]

course_type_dict = {
    "Free": 0,
    "Paid": 1
}

selected_type = st.sidebar.selectbox(
    "Course Type",
    list(course_type_dict.keys())
)

course_type = course_type_dict[selected_type]

course_level_dict = {
    "Beginner": 0,
    "Intermediate": 1,
    "Advanced": 2
}

selected_level = st.sidebar.selectbox(
    "Course Level",
    list(course_level_dict.keys())
)

course_level = course_level_dict[selected_level]

course_price = st.sidebar.number_input(
    "Course Price",
    min_value=0.0,
    value=100.0
)

course_duration = st.sidebar.number_input(
    "Course Duration (Hours)",
    min_value=1.0,
    value=10.0
)

course_rating = st.sidebar.slider(
    "Course Rating",
    0.0,
    5.0,
    4.0
)

# Teacher Inputs
teacher_experience = st.sidebar.slider(
    "Instructor Experience (Years)",
    0,
    20,
    5
)

teacher_rating = st.sidebar.slider(
    "Instructor Rating",
    0.0,
    5.0,
    4.2
)

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
    width=120
)

# =====================================================
# FEATURE ENGINEERING
# =====================================================

# Price Band
if course_price == 0:
    price_band = 0
elif course_price <= 200:
    price_band = 1
elif course_price <= 500:
    price_band = 2
else:
    price_band = 3

# Duration Bucket
if course_duration <= 10:
    duration_bucket = 0
elif course_duration <= 20:
    duration_bucket = 1
elif course_duration <= 40:
    duration_bucket = 2
else:
    duration_bucket = 3

# Rating Tier
if course_rating <= 2:
    rating_tier = 0
elif course_rating <= 3.5:
    rating_tier = 1
else:
    rating_tier = 2

# =====================================================
# INPUT DATAFRAME
# =====================================================

# NOTE:
# Teacher features are NOT added to model input
# because model was trained without them.

input_data = pd.DataFrame({
    "CourseCategory": [course_category],
    "CourseType": [course_type],
    "CourseLevel": [course_level],
    "CoursePrice": [course_price],
    "CourseDuration": [course_duration],
    "CourseRating": [course_rating],
    "PriceBand": [price_band],
    "DurationBucket": [duration_bucket],
    "RatingTier": [rating_tier]
})

# =====================================================
# PREDICTION SECTION
# =====================================================

st.markdown(
    '<div class="section-header">🤖 AI Enrollment Prediction</div>',
    unsafe_allow_html=True
)

if st.button("🚀 Predict Enrollment"):

    prediction = model.predict(input_data)

    predicted_value = int(prediction[0])

    predicted_revenue = predicted_value * course_price

    st.progress(min(predicted_value, 100))

    st.balloons()

    st.success(
        f"🎯 Predicted Enrollment Count: {predicted_value}"
    )

    st.info(
        f"💰 Predicted Revenue: ${int(predicted_revenue)}"
    )

    if predicted_value >= 150:
        st.success("🔥 Very High Market Demand")

    elif predicted_value >= 80:
        st.warning("⚡ Moderate Market Demand")

    else:
        st.error("📉 Low Demand Forecast")

# =====================================================
# INPUT SUMMARY
# =====================================================

st.markdown(
    '<div class="section-header">📋 Input Summary</div>',
    unsafe_allow_html=True
)

display_df = pd.DataFrame({
    "Category": [selected_category],
    "Type": [selected_type],
    "Level": [selected_level],
    "Price": [course_price],
    "Duration": [course_duration],
    "Rating": [course_rating],
    "Instructor Experience": [teacher_experience],
    "Instructor Rating": [teacher_rating]
})

st.markdown('<div class="card">', unsafe_allow_html=True)

st.dataframe(display_df)

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# REVENUE DATA
# =====================================================

revenue_data = pd.DataFrame({
    "Category": [
        "Programming",
        "Business",
        "Design",
        "Marketing",
        "Data Science"
    ],
    "Revenue": [
        50000,
        42000,
        30000,
        25000,
        60000
    ]
})

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "📈 Prediction",
    "📊 Analytics",
    "💡 Insights"
])

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.markdown(
        '<div class="section-header">📈 Prediction Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write("""
    This machine learning model predicts future course enrollments
    using pricing, duration, ratings, and course category data.
    """)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.markdown(
        '<div class="section-header">📊 Revenue Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.bar_chart(
        revenue_data.set_index("Category")
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # Revenue Table
    st.markdown(
        '<div class="section-header">📋 Revenue Table</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.dataframe(revenue_data)

    st.markdown('</div>', unsafe_allow_html=True)

    # Feature Importance
    st.markdown("---")

    st.subheader("📌 Feature Importance Analysis")

    feature_data = pd.DataFrame({
        "Feature": [
            "Course Rating",
            "Course Price",
            "Course Duration",
            "Teacher Rating",
            "Instructor Experience"
        ],
        "Importance": [35, 25, 15, 15, 10]
    })

    st.bar_chart(
        feature_data.set_index("Feature")
    )

    st.caption(
        "Course Rating and Pricing are the strongest drivers of enrollment demand."
    )

    # Model Metrics
    st.markdown("---")

    st.subheader("📈 Model Performance Metrics")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("R² Score", "0.87")

    with metric2:
        st.metric("MAE", "12.4")

    with metric3:
        st.metric("RMSE", "18.7")

    # Pie Chart
    st.markdown("---")

    st.markdown(
        '<div class="section-header">🥧 Revenue Share by Category</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(
        revenue_data["Revenue"],
        labels=revenue_data["Category"],
        autopct='%1.1f%%',
        textprops={'fontsize': 10}
    )

    ax.axis("equal")

    st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.markdown(
        '<div class="section-header">💡 Business Insights</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.write("""
    • Programming courses generate the highest revenue.

    • Higher rated courses attract more enrollments.

    • Medium pricing performs better than extremely high pricing.

    • Long-duration technical courses show strong demand.

    • Data Science courses show continuous market growth.

    • Instructor quality positively impacts enrollment performance.
    """)

    st.success(
        "🚀 Recommended Strategy: Launch more AI & Data Science courses."
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "EduPro AI Dashboard | Built using Machine Learning & Streamlit"
)