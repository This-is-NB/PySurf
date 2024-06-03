import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QToolBar, QCompleter,QListWidget, QDialog, QVBoxLayout, QMenu, QToolButton, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtCore import QUrl, QStringListModel
from PyQt5.QtGui import QIcon, QFont
import json

preferences = json.load(open('preference.json', 'r'))

#Global Preferences

# zoom_factor = preferences['settings']['zoom_factor']
# home = preferences['settings']['home']
# bookmarks = preferences['bookmarks']['bookmarks']
# history = preferences['history']['history']

# Functions
def save_preferences( pref): 
    # print(json.dumps(pref, indent = 4))
    json.dump(pref, open('preference.json', 'w'), indent = 4)

class HistoryWindow(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Browsing History")
        self.setGeometry(self.parent().screen.size().width() - 650,170, 600, 1000)
        layout = QVBoxLayout()
        self.history_list = QListWidget()
        self.history_list.addItems(reversed(history))
        self.history_list.itemDoubleClicked.connect(self.navigate_to_history_item)
        layout.addWidget(self.history_list)
        self.setLayout(layout)
    
    def navigate_to_history_item(self, item):
        url = item.text()
        self.parent().browser.setUrl(QUrl(url))
        self.close()


class Browser(QMainWindow):
    def __init__(self,preferences = preferences):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.setWindowIcon(QIcon('Icons/browser.gif'))
        self.setWindowTitle("PySurf")
        self.preferences = preferences
        self.zoom_factor = self.preferences['settings']['zoom_factor']
        self.home = self.preferences['settings']['home']
        self.bookmarks = self.preferences['bookmarks']['bookmarks']
        self.history = self.preferences['history']['history']
        self.screen = QApplication.primaryScreen()
        
        # Setup profile for ad blocking
        self.setup_profile()
        
        # Navigation bar
        nav_bar = QToolBar()
        self.addToolBar(nav_bar)
        
        # Back button
        back_btn = QAction(QIcon('Icons/back.png'),'Back', self)
        back_btn.triggered.connect(self.browser.back)
        nav_bar.addAction(back_btn)
        
        # Forward button
        forward_btn = QAction(QIcon('Icons/forward.png'),'Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        nav_bar.addAction(forward_btn)
        
        # Reload button
        reload_btn = QAction(QIcon('Icons/reload.png'),'Reload', self)
        reload_btn.triggered.connect(self.reload_page)
        nav_bar.addAction(reload_btn)
        
        # Home button
        home_btn = QAction(QIcon('Icons/home.png'),'Home', self)
        home_btn.triggered.connect(lambda:self.navigate_to_url(home = True))
        nav_bar.addAction(home_btn)
        
        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setMinimumHeight(50)
        self.url_bar.setFont(QFont('Arial', 12))
        self.url_bar.setClearButtonEnabled(True)

        # Initialize completer with empty list
        self.completer = QCompleter()
        self.model = QStringListModel()
        self.completer.setModel(self.model)
        self.url_bar.setCompleter(self.completer)
        nav_bar.addWidget(self.url_bar)

        # Zoom in button
        zoom_in_btn = QAction(QIcon('Icons/zoom-in.png'),'Zoom In', self)
        zoom_in_btn.triggered.connect(self.zoom_in)
        nav_bar.addAction(zoom_in_btn)
        
        # Zoom out button
        zoom_out_btn = QAction(QIcon('Icons/zoom-out.png'),'Zoom Out', self)
        zoom_out_btn.triggered.connect(self.zoom_out)
        nav_bar.addAction(zoom_out_btn)
        
        # Bookmark button
        bookmark_btn = QAction(QIcon('Icons/bookmark.png'),'Bookmark', self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        nav_bar.addAction(bookmark_btn)
        
        # History button
        history_btn = QAction(QIcon('Icons/history.png'),'History', self)
        history_btn.triggered.connect(self.show_history)
        nav_bar.addAction(history_btn)

        # Private browsing toggle
        self.private_mode = False
        private_btn = QAction(QIcon('Icons/private.png'),'Private Mode', self)
        private_btn.setCheckable(True)
        private_btn.triggered.connect(self.toggle_private_mode)
        nav_bar.addAction(private_btn)

        # Dark mode toggle
        self.dark_mode = False
        dark_mode_btn = QAction('Dark Mode', self)
        dark_mode_btn.setCheckable(True)
        dark_mode_btn.triggered.connect(self.toggle_dark_mode_css)
        nav_bar.addAction(dark_mode_btn)
        
        # self.history = []
        # self.bookmarks = []
        
        # Update URL bar
        self.browser.urlChanged.connect(self.update_url)


        # Connect loadFinished signal to reapply zoom factor
        self.browser.loadFinished.connect(self.apply_zoom_factor)

    def setup_profile(self):
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent("MyCustomUserAgent")
        profile.setHttpCacheType(QWebEngineProfile.NoCache)
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
    
    def navigate_to_url(self, home = False):
        if home:
            url = self.home
        else:
            url = self.url_bar.text()
        if url.startswith('http') or url.startswith('https'):
            self.browser.setUrl(QUrl(url))
        else:
            if not url.startswith('www.'):
                url =  'www.' + url
            self.browser.setUrl(QUrl('http://' + url))

        self.browser.setUrl(QUrl(url if url.startswith('http') else 'http://' + url))
    
    def update_url(self, url):
        self.url_bar.setText(url.toString())
        self.update_completer()
        if not self.private_mode:
            self.history.append(url.toString())
            save_preferences(self.preferences)
    
    def add_bookmark(self):
        url = self.browser.url().toString()
        self.bookmarks[url] = "bm"
        self.update_completer()
        save_preferences(self.preferences)
        print(f"Bookmarked {url}")
    
    def show_history(self):
        self.history_window = HistoryWindow(self.history, self)
        self.history_window.show()
        # self.history_btn.showMenu()
        # print("History:")
        # for url in self.history:
            # print(url)
    
    def toggle_private_mode(self):
        self.private_mode = not self.private_mode
        print("Private Mode:", "On" if self.private_mode else "Off")

    def zoom_in(self):
        self.preferences['settings']['zoom_factor'] += 0.1
        save_preferences(self.preferences)
        self.browser.setZoomFactor(self.preferences['settings']['zoom_factor'])
    
    def zoom_out(self):
        self.preferences['settings']['zoom_factor'] -= 0.1
        save_preferences(self.preferences)
        self.browser.setZoomFactor(self.preferences['settings']['zoom_factor'])

    def reload_page(self):
        self.browser.reload()
    
    def apply_zoom_factor(self):
        self.browser.setZoomFactor(self.zoom_factor)
    
    def update_completer(self):
        all_urls = list(set(self.history + list(self.bookmarks.keys())))
        all_urls_without_protocol = [url.split('//')[1] for url in all_urls]
        all_urls_without_www = [url.replace('www.', '') for url in all_urls_without_protocol]
        self.model.setStringList(list(set(all_urls + all_urls_without_protocol + all_urls_without_www)))
    def toggle_dark_mode_css(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet("""
                QToolBar { background-color: #555; color: white; border: none; }
                QLineEdit { background-color: #666; color: white; border: 1px solid #888; border-radius: 5px; }
                QPushButton { background-color: #777; color: white; border: 1px solid #888; border-radius: 5px; }
                QListWidget { background-color: #666; color: white; border: 1px solid #888; border-radius: 5px; }
                QScrollBar:vertical { border: 1px solid #888; background: #555; width: 15px; margin: 15px 0 15px 0; }
                QScrollBar::handle:vertical { background-color: #888; border-radius: 7px; min-height: 30px; }
                QScrollBar::handle:vertical:hover { background-color: #999; }
                QScrollBar::add-line:vertical { border: none; background: none; }
                QScrollBar::sub-line:vertical { border: none; background: none; }
                QScrollBar::add-page:vertical { background: none; }
                QScrollBar::sub-page:vertical { background: none; }
            """)
            dark_mode_css = """
                html, body { background-color: #333; color: #fff; }
                a { color: #c7f0db; }
                /* Add more CSS rules for dark mode as needed */
            """
            # Inject the CSS into the webpage
            self.browser.page().runJavaScript(f"""
                var darkModeStyle = document.createElement('style');
                darkModeStyle.textContent = `{dark_mode_css}`;
                document.head.append(darkModeStyle);
            """)
        else:
            self.setStyleSheet("")
            self.browser.page().runJavaScript("document.getElementsByTagName('style')[0].remove()")


app = QApplication(sys.argv)
QApplication.setApplicationName("PySurf")
window = Browser(preferences=preferences)
app.exec_()
