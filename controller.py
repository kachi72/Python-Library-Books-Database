import time
import dbconnect

#book validation
def checkbook(bookid):
    db = dbconnect.connection()  
    cursor = db.cursor()
    message = '''SELECT BOOKID FROM BOOKS'''
    cursor.execute(message)
    userid2 = int(bookid)
    result = cursor.fetchall()
    check = any(userid2 in sublist for sublist in result)
    if check:
        return True
    else:
        return False

#add a book to database
def AddBook(request):
    db = dbconnect.connection()
    cursor = db.cursor()
    title = request.form['title']
    author = request.form['author']
    date = time.asctime(time.localtime(time.time()))
    availability = 'Available'
    id = 0

#verifications
    list = []
    if bool(author) != 1:
        list.append('Enter the author of the book')
    if bool(title) != 1:
        list.append('Enter the book title')
    if list:
        return list
    
    
    
    message = '''INSERT INTO BOOKS VALUES(%s,%s,%s,%s,%s)'''
    values = (id,title,author,availability,date)

    try:
        cursor.execute(message,values)
        db.commit()
        return "Successfully added book to library database"
    except:
        db.rollback()
        return "Error uploading book to library database"

#display all books in database
def DisplayAll():
    db = dbconnect.connection()
    cursor = db.cursor()
    message = '''SELECT * FROM BOOKS '''
    list = []
    try:    
        cursor.execute(message)
        result = cursor.fetchall()
        for row in result:
            id = row[0]
            title = row[1]
            author = row[2]
            availability = row[3]
            arrivaldate = row[4]
            iddict = {'ID:': str(id)}
            titledict = {'Title:': str(title)}
            authordict = {'Author:': str(author)}
            availdict = {'Availability:': str(availability)}
            datedict = {'Arrival Date:': str(arrivaldate)}
            list.append(iddict)
            list.append(titledict)
            list.append(authordict)
            list.append(availdict)
            list.append(datedict)
            
        return list
    except:
        return 'Error fetching book inventory'

#display a specific book    
def DisplayOne(request):
    db = dbconnect.connection()
    cursor = db.cursor()
    id = request.form['id']
#validations
    if bool(id) != 1:
        return "Enter the book id"
    if checkbook(id) != 1:
        return "This book id is not in inventory"
    
    message = '''SELECT TITLE,AUTHOR,AVAILABILITY,ARRIVALDATE FROM BOOKS WHERE BOOKID = %s'''
    data = [id]
    list = []
    
    try:    
        cursor.execute(message,data)
        result = cursor.fetchall()
        for row in result:
            title = row[0]
            author = row[1]
            availability = row[2]
            arrivaldate = row[3]
            iddict = {'ID:': str(id)}
            titledict = {'Title:': str(title)}
            authordict = {'Author:': str(author)}
            availdict = {'Availability:': str(availability)}
            datedict = {'Arrival Date:': str(arrivaldate)}
            list.append(iddict)
            list.append(titledict)
            list.append(authordict)
            list.append(availdict)
            list.append(datedict)
            
        return list
    except:
        return 'Error fetching book information from inventory'

#display list of available books   
def DisplayAvailableBooks():
    db = dbconnect.connection()
    cursor = db.cursor()
    message = '''SELECT * FROM BOOKS WHERE AVAILABILITY = 'AVAILABLE' '''
    list = []
    try:
        cursor.execute(message)
        result = cursor.fetchall()
        for row in result:
            id = row[0]
            title = row[1]
            author = row[2]
            availability = row[3]
            arrivaldate = row[4]
            iddict = {'ID:': str(id)}
            titledict = {'Title:': str(title)}
            authordict = {'Author:': str(author)}
            availdict = {'Availability:': str(availability)}
            datedict = {'Arrival Date:': str(arrivaldate)}
            list.append(iddict)
            list.append(titledict)
            list.append(authordict)
            list.append(availdict)
            list.append(datedict)
            
        return list
    except:
        return 'Error fetching available books from inventory'

#display list of borrowed books     
def DisplayBorrowedBooks():
    db = dbconnect.connection()
    cursor = db.cursor()
    message = '''SELECT BOOKID,TITLE,BORROWEDDATE,RETURNDATE FROM BORROWED'''
    list = []
    try:
        cursor.execute(message)
        result = cursor.fetchall()
        for row in result:
            id = row[0]
            title = row[1]
            borroweddate = row[2]
            returndate = row[3]
            iddict = {'ID:': str(id)}
            titledict = {'Title:': str(title)}
            borrowdict = {'Borrowed Date:': str(borroweddate)}
            datedict = {'Return Date:': str(returndate)}
            list.append(iddict)
            list.append(titledict)
            list.append(borrowdict)
            list.append(datedict)
            
        return list
    except:
        return 'Error fetching list of borrowed books'

#delete a book from database   
def DeleteBook(request):
    db = dbconnect.connection()
    cursor = db.cursor()
    id = request.form['id']
    #password = request.form['password']
    #validations
    list = []
    if bool(id)!= 1:
        list.append('Enter the bookid')
    #if bool(password)!= 1:
            #list.append('Enter the librarian\'s password')
    if list:
        return list
    if checkbook(id) != 1:
        return 'This bookid is not in the inventory'
    
    message = '''DELETE FROM BOOKS WHERE ID = %s'''
    data = (id)
    try:
        cursor.execute(message,data)
        db.commit()
    except:
        db.rollback()
        return "Error deleting book from inventory"

#return a borrowed book
def ReturnBook(request):
    db = dbconnect.connection()
    cursor = db.cursor()
    id = request.form['id']

    #validations
    if bool(id) != 1:
        return 'Enter the book id'
    if checkbook(id) != 1:
        return "This book id is not in inventory"
    
    message1 = '''SELECT TITLE,AVAILABILITY FROM BOOKS WHERE BOOKID = %s'''
    data = [id]
    cursor.execute(message1,data)
    result = cursor.fetchall()
    for row in result:
        title = row[0]
        avail = row[1]

    if (avail.lower()) == 'available':
        return 'This book is already in the library'
    message = '''UPDATE BOOKS SET AVAILABILITY = 'Available' WHERE BOOKID = %s'''

    update = 'Successfully returned ' + title + ' to the library'
    try:
        cursor.execute(message,data)
        db.commit()
        return update
    except:
        return 'Error returning book to library'

#borow a book from library
def BorrowBook(request):
    db = dbconnect.connection()
    cursor = db.cursor()
    id = request.form['id']
    date = time.asctime(time.localtime(time.time()))
    returndate = request.form['return date']
    #validations
    list = []
    if bool(id) != 1:
       list.append('Enter the book id')
    if bool(returndate) != 1:
        list.append("Enter return date")
    if checkbook(id) != 1:
        return 'This book id is not in inventory'
    message1 = '''SELECT TITLE,AVAILABILITY FROM BOOKS WHERE BOOKID = %s'''
    data1 = [id]
    
    cursor.execute(message1,data1)
    result = cursor.fetchall()
    for row in result:
        title = row[0]
        avail = row[1]
    
    if (avail.lower()) == 'borrowed':
        return "This book has already been borrowed out"
    
    message2 = '''INSERT INTO BORROWED VALUES(%s,%s,%s,%s,%s)'''
    id2 = 0
    data2 = [id2,id,title,date,returndate]
    message = '''UPDATE BOOKS SET AVAILABILITY = 'Borrowed' WHERE BOOKID = %s'''

    update = 'Successfully borrowed ' + title + ' from the library' 
    '''
    try:
        cursor.execute(message2,data2)
        cursor.execute(message,data1)
        db.commit()
        return update
    except:
        db.rollback()
        return "Error occurred while attempting to borrow book"
    '''
    cursor.execute(message2,data2)
    cursor.execute(message,data1)
    db.commit()
    return update