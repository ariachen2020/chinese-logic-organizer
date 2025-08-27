# 中文語意邏輯整理器

使用 Google Gemini AI 技術改善中文文本的邏輯結構和表達清晰度的 Streamlit 應用。

## 功能特色

- **智能文本改善**: 使用 Gemini AI 分析並改善中文文本的語意邏輯
- **差異對比**: 清楚顯示修改前後的具體變化
- **修改說明**: 詳細說明每處修改的原因和目的
- **即時處理**: 快速的文本處理和結果展示

## 安裝步驟

1. **克隆專案**
   ```bash
   git clone <your-repo-url>
   cd chinese-logic-organizer
   ```

2. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

3. **設定環境變數**
   ```bash
   cp .env.example .env
   ```
   然後編輯 `.env` 文件，填入您的 Gemini API Key：
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **取得 Gemini API Key**
   - 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
   - 創建新的 API Key
   - 複製 API Key 到 `.env` 文件中

## 執行應用

```bash
streamlit run app.py
```

應用將在瀏覽器中自動開啟，通常在 `http://localhost:8501`

## 使用方式

1. **輸入 API Key**: 在側邊欄輸入您的 Gemini API Key
2. **輸入文本**: 在左側文本框中貼上要改善的中文文字
3. **開始處理**: 點擊「開始整理」按鈕
4. **查看結果**: 
   - 右側顯示改善後的文本
   - 下方顯示修改說明和差異對比

## 檔案結構

```
chinese-logic-organizer/
├── app.py                 # 主要 Streamlit 應用
├── gemini_api.py          # Gemini API 接口模組
├── text_processor.py      # 文字處理和差異比較模組
├── requirements.txt       # Python 依賴列表
├── .env.example          # 環境變數模板
└── README.md             # 專案說明文件
```

## 技術堆疊

- **Frontend**: Streamlit
- **AI Model**: Google Gemini Pro
- **Text Processing**: Python difflib
- **Environment Management**: python-dotenv

## 注意事項

- 需要有效的 Google Gemini API Key
- API 使用可能產生費用，請查看 Google 的定價說明
- 應用僅支援中文文本處理

## 故障排除

### API 連接失敗
- 確認 API Key 正確且有效
- 檢查網路連接
- 確認 API 配額未超出限制

### 文本處理錯誤
- 確認輸入的是有效的中文文本
- 檢查文本長度是否超出 API 限制

## 授權

MIT License