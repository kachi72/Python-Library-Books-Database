from __future__ import print_function
from flask import Flask,request
import controller

app = Flask(__name__)

@app.route('/addbook', methods=['POST'])
def addbook():
    return controller.AddBook(request)

@app.route('/updatestatus', methods=['POST'])
def updatestatus():
    return controller.UpdateStatus(request)

@app.route('/borrowbook', methods=['POST'])
def borrowbook():
    return controller.BorrowBook(request)

@app.route('/returnbook', methods=['POST'])
def returnbook():
    return controller.ReturnBook(request)

@app.route('/displayallbooks', methods=['GET'])
def displayall():
    return controller.DisplayAll()

@app.route('/displayonebook', methods=['GET'])
def displayone():
    return controller.DisplayOne(request)
 
@app.route('/displayavailablebooks', methods=['GET'])
def displayavailable():
    return controller.DisplayAvailableBooks()

@app.route('/displayborrowedbooks', methods=['GET'])
def displayborrowed():
    return controller.DisplayBorrowedBooks()

@app.route('/deletebook', methods=['DELETE'])
def deletebook():
    return controller.DeleteBook(request)


    
if __name__ == '__main__':
    app.run(debug=True,port=5000)