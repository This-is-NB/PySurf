import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QToolBar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
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
        if not self.private_mode:
            self.history.append(url.toString())
            save_preferences(self.preferences)
    
    def add_bookmark(self):
        url = self.browser.url().toString()
        self.bookmarks[url] = "bm"
        save_preferences(self.preferences)
        print(f"Bookmarked {url}")
    
    def show_history(self):
        print("History:")
        for url in self.history:
            print(url)
    
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

app = QApplication(sys.argv)
QApplication.setApplicationName("PySurf")
window = Browser(preferences=preferences)
app.exec_()
