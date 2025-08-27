import google.generativeai as genai
from typing import Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiAPI:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def improve_chinese_text(self, text: str) -> Dict[str, str]:
        prompt = f"""
請分析以下中文文本，並提供改進版本。請專注於：
1. 語意邏輯的清晰性
2. 句子結構的流暢性
3. 詞彙選擇的精確性
4. 段落組織的連貫性
5. 字詞的正確性

原文：
{text}

請以JSON格式回覆，包含以下欄位：
{{
  "original": "原始文本",
  "improved": "改進後的文本",
  "changes": "具體修改說明"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            import json
            
            response_text = response.text.strip()
            
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()
            
            result = json.loads(response_text)
            
            return {
                "original": result.get("original", text),
                "improved": result.get("improved", text),
                "changes": result.get("changes", "無修改")
            }
        
        except Exception as e:
            return {
                "original": text,
                "improved": text,
                "changes": f"處理錯誤: {str(e)}"
            }