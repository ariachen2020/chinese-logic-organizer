import streamlit as st
from gemini_api import GeminiAPI
from text_processor import TextProcessor
import os

st.set_page_config(
    page_title="中文語意邏輯整理器",
    page_icon="📝",
    layout="wide"
)

st.title("📝 中文語意邏輯整理器")
st.markdown("使用 AI 技術改善中文文本的邏輯結構和表達清晰度")

st.session_state.api_key = ""
st.session_state.gemini_api = None

with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value="",
        placeholder="請貼上您的 Gemini API Key",
        help="每次使用都需要重新輸入 API Key"
    )
    
    st.session_state.api_key = api_key
    
    if api_key:
        try:
            os.environ["GEMINI_API_KEY"] = api_key
            st.session_state.gemini_api = GeminiAPI()
            st.success("✅ API 連接成功")
        except Exception as e:
            st.error(f"❌ API 連接失敗: {str(e)}")
            st.session_state.gemini_api = None
    
    st.markdown("---")
    st.markdown("### 📋 使用說明")
    st.markdown("""
    1. 輸入您的 Gemini API Key
    2. 在文本框中貼上要改善的中文文字
    3. 點擊「開始整理」按鈕
    4. 查看改善後的文本和修改說明
    """)

col1, col2 = st.columns([1, 1])

with col1:
    st.header("📄 原始文本")
    input_text = st.text_area(
        "請輸入要整理的中文文字",
        height=300,
        placeholder="在這裡貼上您的中文文字..."
    )

if st.button("🚀 開始整理", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ 請先在側邊欄輸入 Gemini API Key")
    elif not input_text.strip():
        st.error("❌ 請輸入要整理的文字")
    elif st.session_state.gemini_api is None:
        st.error("❌ API 未正確初始化，請檢查 API Key")
    else:
        with st.spinner("🔄 正在使用 AI 整理文字..."):
            try:
                result = st.session_state.gemini_api.improve_chinese_text(input_text)
                
                with col2:
                    st.header("✨ 整理後文本")
                    st.text_area(
                        "改善後的文字",
                        value=result["improved"],
                        height=300,
                        disabled=True
                    )
                    
                    # 複製按鈕區域
                    col_copy1, col_copy2 = st.columns([1, 1])
                    with col_copy1:
                        if st.button("📋 顯示可複製文本", use_container_width=True):
                            st.session_state.show_copyable = True
                    with col_copy2:
                        if st.button("🔄 重新整理", use_container_width=True):
                            st.rerun()
                    
                    # 顯示可選取複製的文本
                    if hasattr(st.session_state, 'show_copyable') and st.session_state.show_copyable:
                        st.markdown("**📋 可選取複製的文本：**")
                        st.text(result["improved"])
                        st.info("💡 請選取上方文本並按 Ctrl+C (Windows) 或 Cmd+C (Mac) 複製")
                
                st.markdown("---")
                
                col_changes, col_diff = st.columns([1, 1])
                
                with col_changes:
                    st.header("📝 修改說明")
                    formatted_changes = TextProcessor.format_changes(result["changes"])
                    st.markdown(formatted_changes)
                
                with col_diff:
                    st.header("🔍 文字差異對比")
                    
                    tab1, tab2 = st.tabs(["標記差異", "統一差異"])
                    
                    with tab1:
                        original_marked, improved_marked = TextProcessor.get_inline_diff(
                            result["original"], result["improved"]
                        )
                        
                        st.markdown("**原文（刪除內容以 ~~刪除線~~ 標示）:**")
                        st.markdown(original_marked)
                        
                        st.markdown("**改善後（新增內容以 **粗體** 標示）:**")
                        st.markdown(improved_marked)
                    
                    with tab2:
                        diff_lines = TextProcessor.get_text_diff(
                            result["original"], result["improved"]
                        )
                        if diff_lines:
                            st.code('\n'.join(diff_lines), language='diff')
                        else:
                            st.info("無明顯差異")
                
                st.success("✅ 文字整理完成！")
                
            except Exception as e:
                st.error(f"❌ 處理過程中發生錯誤: {str(e)}")

with st.expander("💡 功能特色"):
    st.markdown("""
    - **語意邏輯優化**: 改善文章的邏輯結構和表達流暢度
    - **詞彙精確性**: 使用更精確和恰當的詞彙
    - **段落組織**: 優化段落之間的連貫性
    - **差異對比**: 清楚顯示修改前後的具體變化
    - **修改說明**: 詳細說明每處修改的原因和目的
    """)

st.markdown("---")
st.markdown("*由 Google Gemini AI 驅動 • Made with Streamlit*")