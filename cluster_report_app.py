import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
from collections import Counter
import base64

# Cấu hình trang
st.set_page_config(
    page_title="📊 Báo Cáo Cluster Survey",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh để làm web đẹp hơn
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cluster-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #1e3c72;
    }
    .summary-text {
        background: #f8f9fa;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        font-weight: 500;
    }
    .sidebar-content {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    .tab-content {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📊 Báo Cáo Tóm Tắt Cluster Survey</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("## ⚙️ Cấu Hình")
    
    # Dark mode toggle
    dark_mode = st.checkbox("🌙 Dark Mode", value=False)
    
    # API key (tùy chọn)
    api_key = st.text_input("🔑 API Key (tùy chọn):", type="password", 
                          help="Để trống nếu không sử dụng API")
    
    # File upload
    uploaded_file = st.file_uploader("📁 Upload File Excel:", type=["xlsx", "csv"],
                                   help="File phải có cột 'Cluster' và 'Content'")
    
    st.markdown("---")
    st.markdown("### 📋 Hướng Dẫn")
    st.markdown("""
    1. **Upload file**: Excel/CSV với cột Cluster và Content
    2. **API Key**: Tùy chọn, để trống dùng tóm tắt local
    3. **Xem báo cáo**: Phân tích và tóm tắt tự động
    4. **Export**: Tải kết quả về máy
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Hàm tóm tắt nội dung
def summarize_content(content):
    """Tóm tắt nội dung cluster một cách thông minh"""
    text = str(content).strip()
    if not text:
        return "(Không có nội dung)"

    # Làm sạch text
    text = re.sub(r'\s+', ' ', text)
    
    # Tách câu
    sentences = re.split(r'(?:[.!?]+\s+|\n)', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Chọn câu đại diện (ưu tiên câu dài, có ý nghĩa)
    meaningful_sentences = []
    for sent in sentences:
        words = sent.split()
        if len(words) >= 6:  # Câu có ít nhất 6 từ
            meaningful_sentences.append(sent)
    
    if not meaningful_sentences:
        meaningful_sentences = sentences[:3] if sentences else [text]
    
    # Ghép và rút gọn
    combined = ' '.join(meaningful_sentences[:2])
    words = combined.split()
    
    # Loại bỏ từ lặp
    seen = set()
    filtered_words = []
    for word in words:
        word_lower = word.lower().strip('.,!?')
        if word_lower not in seen and len(word_lower) > 1:
            filtered_words.append(word)
            seen.add(word_lower)
    
    # Giới hạn độ dài
    summary_words = filtered_words[:20]
    summary = ' '.join(summary_words)
    
    if len(filtered_words) > 20:
        summary = summary.rstrip('.,!?') + '...'
    
    return summary.capitalize()

# Hàm tạo biểu đồ
def create_cluster_chart(df):
    """Tạo biểu đồ phân bố cluster"""
    cluster_counts = df['Cluster'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', 'Số lượng']
    
    fig = px.bar(cluster_counts, 
                 x='Cluster', 
                 y='Số lượng',
                 title='📊 Phân Bố Số Lượng Theo Cluster',
                 color='Số lượng',
                 color_continuous_scale='Blues')
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    return fig

# Hàm tạo word cloud data
def get_word_frequencies(text):
    """Lấy tần suất từ để tạo word cloud"""
    words = re.findall(r'\b\w+\b', text.lower())
    # Loại bỏ stop words cơ bản
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'}
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    return Counter(filtered_words).most_common(20)

# Hàm export kết quả
def create_download_link(df_results, filename="cluster_report.xlsx"):
    """Tạo link download cho kết quả"""
    output = pd.DataFrame(df_results)
    csv = output.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Tải Xuống Báo Cáo</a>'
    return href

# Main content
if uploaded_file is not None:
    try:
        # Đọc file
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        
        # Kiểm tra cột cần thiết
        required_cols = ['Cluster', 'Content']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ File thiếu các cột bắt buộc: {', '.join(missing_cols)}")
            st.stop()
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Tổng Quan", "📋 Chi Tiết Cluster", "📈 Thống Kê", "💾 Export"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.markdown("## 📊 Tổng Quan Dữ liệu")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📁 Tổng Records</h3>
                    <h2>{len(df)}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🎯 Số Cluster</h3>
                    <h2>{df['Cluster'].nunique()}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📝 Trung bình/Cluster</h3>
                    <h2>{len(df)//df['Cluster'].nunique() if df['Cluster'].nunique() > 0 else 0}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⏰ Thời gian xử lý</h3>
                    <h2>< 5s</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Biểu đồ phân bố
            st.markdown("### 📊 Phân Bố Cluster")
            fig = create_cluster_chart(df)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.markdown("## 📋 Chi Tiết Tóm Tắt Cluster")
            
            # Group by cluster
            grouped = df.groupby('Cluster')['Content'].apply(
                lambda x: '\n'.join(x.dropna().astype(str))
            ).reset_index()
            
            if st.button("🚀 Tạo Báo Cáo Tóm Tắt", type="primary"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = []
                
                for i, (_, row) in enumerate(grouped.iterrows()):
                    cluster_name = row['Cluster']
                    content = row['Content']
                    
                    status_text.text(f"Đang xử lý Cluster: {cluster_name}...")
                    progress_bar.progress((i + 1) / len(grouped))
                    
                    # Tóm tắt
                    summary = summarize_content(content)
                    
                    # Hiển thị kết quả
                    st.markdown(f"""
                    <div class="cluster-card">
                        <h3>🎯 Cluster: {cluster_name}</h3>
                        <div class="summary-text">
                            <strong>Tóm tắt ý nghĩa chủ đề:</strong><br>
                            {summary}
                        </div>
                        <small>📊 Dựa trên {len(content.split())} từ</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    results.append({
                        'Cluster': cluster_name,
                        'Tóm tắt': summary,
                        'Số từ': len(content.split()),
                        'Thời gian': datetime.now().strftime("%H:%M:%S")
                    })
                
                progress_bar.empty()
                status_text.empty()
                st.success("✅ Hoàn thành tóm tắt tất cả cluster!")
                
                # Lưu kết quả vào session state
                st.session_state.results = results
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.markdown("## 📈 Thống Kê Chi Tiết")
            
            if 'results' in st.session_state:
                results_df = pd.DataFrame(st.session_state.results)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Thống Kê Từ Khóa")
                    all_text = ' '.join(df['Content'].dropna().astype(str))
                    word_freq = get_word_frequencies(all_text)
                    
                    if word_freq:
                        words_df = pd.DataFrame(word_freq, columns=['Từ', 'Tần suất'])
                        st.dataframe(words_df, use_container_width=True)
                
                with col2:
                    st.markdown("### 📈 Độ Dài Tóm Tắt")
                    fig = px.histogram(results_df, x='Số từ', 
                                     title='Phân Bố Độ Dài Nội Dung Cluster',
                                     color_discrete_sequence=['#1e3c72'])
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📋 Hãy tạo báo cáo tóm tắt trước để xem thống kê!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.markdown("## 💾 Export Kết Quả")
            
            if 'results' in st.session_state:
                results_df = pd.DataFrame(st.session_state.results)
                st.dataframe(results_df, use_container_width=True)
                
                # Download buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    csv_data = results_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Tải CSV",
                        data=csv_data,
                        file_name="cluster_report.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    excel_data = results_df.to_excel(index=False, engine='openpyxl')
                    st.download_button(
                        label="📊 Tải Excel",
                        data=excel_data,
                        file_name="cluster_report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.info("📋 Hãy tạo báo cáo tóm tắt trước để export!")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Lỗi xử lý file: {str(e)}")
        st.info("💡 Đảm bảo file Excel có định dạng đúng với cột 'Cluster' và 'Content'")

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2>🎯 Chào mừng đến với Báo Cáo Cluster Survey</h2>
        <p style="font-size: 18px; color: #666;">
            Upload file Excel/CSV để tạo báo cáo tóm tắt ý nghĩa chủ đề của các cluster một cách thông minh và đẹp mắt!
        </p>
        <div style="background: linear-gradient(45deg, #1e3c72, #2a5298); color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3>✨ Tính Năng Nổi Bật</h3>
            <ul style="text-align: left; display: inline-block;">
                <li>📊 Phân tích thống kê chi tiết</li>
                <li>🎨 Giao diện đẹp với biểu đồ</li>
                <li>⚡ Xử lý nhanh chóng</li>
                <li>💾 Export nhiều định dạng</li>
                <li>🔍 Tóm tắt thông minh</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>📊 Báo Cáo Cluster Survey - Phiên bản 2.0 | Phát triển với ❤️ bởi AI Assistant</p>
</div>
""", unsafe_allow_html=True)