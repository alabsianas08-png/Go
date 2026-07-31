import arxiv
import requests
from pyalex import Works
import re

class AcademicSearchEngine:
    """محرك بحث متعدد المصادر للدراسات والكتب"""
    
    def __init__(self):
        self.sources = {
            'arxiv': self._search_arxiv,
            'openalex': self._search_openalex,
            'pubmed': self._search_pubmed,
            # يمكن إضافة Google Scholar عبر Selenium أو APIs مدفوعة
        }
    
    def search(self, query, source='all', max_results=20):
        """البحث في المصادر المحددة"""
        results = []
        if source == 'all':
            for src_name, src_func in self.sources.items():
                try:
                    results.extend(src_func(query, max_results // len(self.sources)))
                except Exception as e:
                    print(f"خطأ في {src_name}: {e}")
        else:
            results = self.sources[source](query, max_results)
        return results
    
    def _search_arxiv(self, query, max_results):
        """البحث في arXiv"""
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
        papers = []
        for paper in client.results(search):
            papers.append({
                'title': paper.title,
                'authors': [a.name for a in paper.authors],
                'abstract': paper.summary,
                'pdf_url': paper.pdf_url,
                'source': 'arXiv',
                'year': paper.published.year
            })
        return papers
    
    def _search_openalex(self, query, max_results):
        """البحث في OpenAlex"""
        works = Works().search(query).paginate(per_page=max_results)
        papers = []
        for work in works:
            papers.append({
                'title': work.get('title', ''),
                'authors': [a.get('author', {}).get('display_name', '') for a in work.get('authorships', [])],
                'abstract': work.get('abstract', ''),
                'pdf_url': self._get_openalex_pdf(work),
                'source': 'OpenAlex',
                'year': work.get('publication_year')
            })
        return papers
    
    def _get_openalex_pdf(self, work):
        """استخراج رابط PDF من OpenAlex"""
        for location in work.get('locations', []):
            if location.get('pdf_url'):
                return location['pdf_url']
            if location.get('landing_page_url'):
                return location['landing_page_url']
        return None
    
    def _search_pubmed(self, query, max_results):
        """البحث في PubMed عبر Entrez"""
        # استخدام Biopython أو requests مع Entrez API
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json'
        }
        response = requests.get(base_url, params=params)
        # معالجة النتيجة وعرضها...
        return []
