import re
import textacy
import spacy

class QuoteExtractor:
    """استخراج الاقتباسات والتعاريف من النصوص"""
    
    def __init__(self):
        # تحميل نموذج اللغة العربية إذا كان متوفراً، وإلا استخدم الإنجليزية
        try:
            self.nlp = spacy.load('ar_core_news_sm')
        except:
            self.nlp = spacy.load('en_core_web_sm')
    
    def extract_quotes(self, text):
        """استخراج الاقتباسات بين علامات التنصيص"""
        # اقتباسات مباشرة
        patterns = [
            r'["「](.*?)["」]',           # علامات تنصيص
            r'«(.*?)»',                   # علامات تنصيص فرنسية/عربية
            r'“([^”]*)”',                 # علامات تنصيص ذكية
        ]
        quotes = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            quotes.extend(matches)
        
        # استخدام textacy لاستخراج اقتباسات أكثر دقة
        doc = self.nlp(text)
        # textacy.extract.direct_quotations(doc)  # إذا كانت spaCy مدعومة
        
        return list(set(quotes))  # إزالة التكرار
    
    def extract_definitions(self, text):
        """استخراج التعاريف (جمل تحتوي على 'هو'، 'تعريف'، 'تعني'...)"""
        definition_patterns = [
            r'([^.]*?(?:يعرف|تعريف|هو|هي|تعني|مصطلح)[^.]*\.)',
            r'([^.]*?(?:definition|is defined as|means)[^.]*\.)',
        ]
        definitions = []
        for pattern in definition_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            definitions.extend(matches)
        return definitions
    
    def extract_key_points(self, text):
        """استخراج نقاط رئيسية (جمل تبدأ بنقاط أو أرقام)"""
        point_patterns = [
            r'[•\-*]\s*([^.\n]+)',          # نقاط عادية
            r'\d+[\.\)]\s*([^.\n]+)',        # نقاط مرقمة
        ]
        points = []
        for pattern in point_patterns:
            matches = re.findall(pattern, text)
            points.extend(matches)
        return points
    
    def process_document(self, filepath):
        """معالجة ملف كامل واستخراج كل شيء"""
        # قراءة الملف حسب نوعه (PDF، EPUB، TXT)
        text = self._read_file(filepath)
        return {
            'quotes': self.extract_quotes(text),
            'definitions': self.extract_definitions(text),
            'key_points': self.extract_key_points(text)
        }
    
    def _read_file(self, filepath):
        """قراءة محتوى الملف حسب الامتداد"""
        ext = filepath.split('.')[-1].lower()
        if ext == 'pdf':
            return self._read_pdf(filepath)
        elif ext == 'epub':
            return self._read_epub(filepath)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
    
    def _read_pdf(self, filepath):
        # استخدام PyPDF2 أو pdfplumber
        pass
    
    def _read_epub(self, filepath):
        # استخدام ebooklib
        pass
