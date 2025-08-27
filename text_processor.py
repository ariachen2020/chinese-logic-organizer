import difflib
from typing import List, Tuple
import re

class TextProcessor:
    @staticmethod
    def get_text_diff(original: str, improved: str) -> List[str]:
        original_lines = original.splitlines(keepends=True)
        improved_lines = improved.splitlines(keepends=True)
        
        diff = list(difflib.unified_diff(
            original_lines, 
            improved_lines,
            fromfile='原文',
            tofile='修改後',
            lineterm=''
        ))
        
        return diff
    
    @staticmethod
    def get_inline_diff(original: str, improved: str) -> Tuple[str, str]:
        original_words = re.findall(r'[\u4e00-\u9fff]+|[^\u4e00-\u9fff\s]+|\s+', original)
        improved_words = re.findall(r'[\u4e00-\u9fff]+|[^\u4e00-\u9fff\s]+|\s+', improved)
        
        diff = list(difflib.ndiff(original_words, improved_words))
        
        original_marked = []
        improved_marked = []
        
        for line in diff:
            if line.startswith('  '):
                word = line[2:]
                original_marked.append(word)
                improved_marked.append(word)
            elif line.startswith('- '):
                word = line[2:]
                original_marked.append(f"~~{word}~~")
            elif line.startswith('+ '):
                word = line[2:]
                improved_marked.append(f"**{word}**")
        
        return ''.join(original_marked), ''.join(improved_marked)
    
    @staticmethod
    def format_changes(changes: str) -> str:
        if changes == "無修改":
            return changes
        
        lines = changes.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                if not line.startswith('•') and not line.startswith('-') and not line.startswith('*'):
                    formatted_lines.append(f"• {line}")
                else:
                    formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)