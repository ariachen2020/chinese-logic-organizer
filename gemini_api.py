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
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    def improve_chinese_text(self, text: str) -> Dict[str, str]:
        prompt = f"""
請用繁體中文分析以下中文文本並提供改進版本。重點改善：
1. 邏輯結構和條理性
2. 表達流暢性和可讀性
3. 詞彙選擇的準確性
4. 句式結構的優化

原文：
{text}

請用JSON格式回覆，所有內容都必須使用繁體中文：
{{
  "original": "原始文本",
  "improved": "改進後的文本",
  "changes": "修改說明"
}}
"""
        
        try:
            # 配置生成參數
            generation_config = {
                "temperature": 0,
                "max_output_tokens": 65536,
            }
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            import json
            
            # 處理回應文本
            response_text = ""
            if hasattr(response, 'text') and response.text:
                if isinstance(response.text, list):
                    response_text = ' '.join(str(item) for item in response.text)
                else:
                    response_text = str(response.text)
            else:
                # 備用方法：從 candidates 獲取
                if response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'text'):
                                response_text += str(part.text)
            
            response_text = response_text.strip()
            
            # 清理 JSON 格式
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
        
        except json.JSONDecodeError as e:
            return {
                "original": text,
                "improved": text,
                "changes": f"JSON 解析錯誤: {str(e)}。請檢查 API 回應格式。"
            }
        except Exception as e:
            error_msg = str(e)
            if "500" in error_msg:
                return {
                    "original": text,
                    "improved": text,
                    "changes": "API 服務暫時不可用，請稍後重試。可能原因：API 配額用盡或服務器過載。"
                }
            else:
                return {
                    "original": text,
                    "improved": text,
                    "changes": f"處理錯誤: {error_msg}"
                }