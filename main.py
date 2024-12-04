import sqlite3
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget

from book_info import Ui_MainWindow as Ui_BookInfo
from library_des import Ui_MainWindow

connet = sqlite3.connect('library_db')
cursor = connet.cursor()
sql_query = '''SELECT title, author, year, genre, path 
                FROM Books JOIN Authors ON Books.author_id=Authors.id JOIN Genres ON Books.genre_id = Genres.id 
                '''


class SearchWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Каталог библиотеки')
        self.items = {'Автор': "author", "Название": "name"}
        self.query_box.addItems(self.items.keys())
        self.find_btn.clicked.connect(self.result_search)

    def result_search(self):
        query_text = self.searchEdit.text().lower()
        if query_text:
            _sql = sql_query + f"""WHERE {self.items[self.query_box.currentText()]} LIKE '%{query_text}%'"""
            data = cursor.execute(_sql).fetchall()
            names = [i[0] for i in data]
            self.result_table.setRowCount(len(names))
            self.result_table.setColumnCount(1)
            self.result_table.verticalHeader().hide()
            self.result_table.horizontalHeader().hide()

            for i in range(len(names)):
                btn = QPushButton()
                btn.setText(names[i])
                btn.setFixedWidth(591)
                btn.clicked.connect(self.create_window)
                self.result_table.setCellWidget(i, 0, btn)

    def create_window(self):
        name = self.sender().text()
        _sql = sql_query + """WHERE title = ?"""
        _, author, year, genre, path = cursor.execute(_sql, (name,)).fetchone()
        self.book = ShowBook(name, author, year, genre, path)
        self.book.show()


class ShowBook(QWidget, Ui_BookInfo):
    def __init__(self, book, author, year, genre, path):
        super(ShowBook, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Информация о книге')
        self.book, self.author, self.year, self.genre, self.path = book, ' '.join(
            i.capitalize() for i in author.split()), year, genre, path
        self.show_info()

    def show_info(self):
        pixmap = QPixmap(self.path)
        self.photo.setPixmap(pixmap)
        self.name_lbl_3.setText(f'<html><head/><body><p align="center">{self.book} </p></body></html>')
        self.year_lbl_3.setText(f'<html><head/><body><p align="center">{str(self.year)} </p></body></html>')
        self.author_lbl_3.setText(f'<html><head/><body><p align="center">{self.author} </p></body></html>')
        self.genre_lbl_3.setText(f'<html><head/><body><p align="center">{self.genre} </p></body></html>')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchWindow()
    ex.show()
    sys.exit(app.exec())
