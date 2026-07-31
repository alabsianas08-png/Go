from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import threading

from search_engine import AcademicSearchEngine
from downloader import DownloadEngine
from quote_extractor import QuoteExtractor

class ResearchApp(App):
    def build(self):
        self.search_engine = AcademicSearchEngine()
        self.downloader = DownloadEngine()
        self.quote_extractor = QuoteExtractor()
        
        # الواجهة الرئيسية
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # حقل البحث
        self.search_input = TextInput(
            hint_text='أدخل موضوع البحث (مثل: الذكاء الاصطناعي)',
            size_hint_y=None,
            height=50,
            font_size='16sp'
        )
        main_layout.add_widget(self.search_input)
        
        # أزرار التحكم
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.search_btn = Button(text='🔍 بحث', on_press=self.start_search)
        self.download_btn = Button(text='📥 تنزيل', on_press=self.start_download, disabled=True)
        self.quote_btn = Button(text='📝 استخراج الاقتباسات', on_press=self.start_quote_extraction, disabled=True)
        btn_layout.add_widget(self.search_btn)
        btn_layout.add_widget(self.download_btn)
        btn_layout.add_widget(self.quote_btn)
        main_layout.add_widget(btn_layout)
        
        # منطقة عرض النتائج (قابلة للتمرير)
        self.results_container = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.results_container.bind(minimum_height=self.results_container.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.results_container)
        main_layout.add_widget(scroll)
        
        # شريط الحالة
        self.status_label = Label(text='جاهز', size_hint_y=None, height=30)
        main_layout.add_widget(self.status_label)
        
        return main_layout
    
    def start_search(self, instance):
        self.status_label.text = 'جاري البحث...'
        self.search_btn.disabled = True
        threading.Thread(target=self._do_search, daemon=True).start()
    
    def _do_search(self):
        query = self.search_input.text.strip()
        if not query:
            Clock.schedule_once(lambda dt: self.update_status('الرجاء إدخال نص للبحث'))
            return
        
        results = self.search_engine.search(query, max_results=15)
        Clock.schedule_once(lambda dt: self.display_results(results))
        Clock.schedule_once(lambda dt: self.update_status(f'تم العثور على {len(results)} نتيجة'))
        Clock.schedule_once(lambda dt: setattr(self.download_btn, 'disabled', False))
        Clock.schedule_once(lambda dt: setattr(self.quote_btn, 'disabled', False))
        Clock.schedule_once(lambda dt: setattr(self.search_btn, 'disabled', False))
    
    def display_results(self, results):
        self.results_container.clear_widgets()
        for i, paper in enumerate(results):
            # عرض كل نتيجة كبطاقة
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=150, 
                           padding=10, spacing=5)
            card.add_widget(Label(text=f"{i+1}. {paper.get('title', 'بدون عنوان')}", 
                                 bold=True, size_hint_y=None, height=30))
            card.add_widget(Label(text=f"المؤلفون: {', '.join(paper.get('authors', [])[:3])}", 
                                 size_hint_y=None, height=25))
            card.add_widget(Label(text=f"المصدر: {paper.get('source', 'غير معروف')} | {paper.get('year', '')}", 
                                 size_hint_y=None, height=25))
            # زر لتنزيل هذا البحث تحديداً
            download_btn = Button(text='تنزيل', size_hint_y=None, height=30)
            download_btn.bind(on_press=lambda btn, p=paper: self.download_single(p))
            card.add_widget(download_btn)
            self.results_container.add_widget(card)
    
    def download_single(self, paper):
        url = paper.get('pdf_url')
        if url:
            threading.Thread(target=self._do_download, args=(url,), daemon=True).start()
    
    def start_download(self, instance):
        self.status_label.text = 'جاري تنزيل الكتب...'
        # تنزيل جميع النتائج المعروضة
        for child in self.results_container.children:
            # استخراج رابط PDF من كل بطاقة
            pass
    
    def _do_download(self, url):
        result = self.downloader.download_pdf(url)
        Clock.schedule_once(lambda dt: self.update_status(f'تم التنزيل: {result}'))
    
    def start_quote_extraction(self, instance):
        self.status_label.text = 'جاري استخراج الاقتباسات...'
        threading.Thread(target=self._do_quote_extraction, daemon=True).start()
    
    def _do_quote_extraction(self):
        # استخراج الاقتباسات من الملفات التي تم تنزيلها
        import glob
        files = glob.glob('downloads/*.pdf')
        all_quotes = []
        for f in files:
            quotes = self.quote_extractor.process_document(f)
            all_quotes.extend(quotes.get('quotes', []))
        
        Clock.schedule_once(lambda dt: self.display_quotes(all_quotes))
    
    def display_quotes(self, quotes):
        self.results_container.clear_widgets()
        for q in quotes[:20]:
            self.results_container.add_widget(
                Label(text=f'📝 {q}', size_hint_y=None, height=40, text_size=(self.width, None))
            )
    
    def update_status(self, msg):
        self.status_label.text = msg

if __name__ == '__main__':
    ResearchApp().run()
