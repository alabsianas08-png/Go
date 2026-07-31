import requests
import os
from pathlib import Path

class DownloadEngine:
    """محرك تنزيل الملفات من الروابط"""
    
    def __init__(self, download_folder='downloads'):
        self.folder = Path(download_folder)
        self.folder.mkdir(exist_ok=True)
    
    def download_pdf(self, url, filename=None):
        """تنزيل ملف PDF"""
        if not filename:
            filename = url.split('/')[-1] or 'paper.pdf'
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        
        filepath = self.folder / filename
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return str(filepath)
        except Exception as e:
            return f"خطأ في التنزيل: {e}"
    
    def download_epub(self, url, filename=None):
        """تنزيل كتاب EPUB"""
        # مشابه لـ download_pdf
        pass
    
    def download_from_doi(self, doi):
        """تنزيل عبر DOI باستخدام Unpaywall"""
        # استخدام Unpaywall API للحصول على PDF مفتوح
        pass
