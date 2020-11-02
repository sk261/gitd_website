import sqlite3
from io import BytesIO
from flask import send_file
from random import seed, randint
import time
seed(int(time.time()))

def getConnection():
    _Connection, x = getCommitalConnection()
    return _Connection

def getCommitalConnection():
    _DB_FullPath = 'app/webpages.db'
    _Connection = sqlite3.connect(_DB_FullPath)
    _Cursor = _Connection.cursor()
    return _Cursor, _Connection

def commitChanges(_Connection):
    _Connection.commit()


'''
DB Layout
Key:
PID - PageID
UID - UserID
TID - Thread ID
P_ID - Post ID
DOC - Date of Creation
Icon - Path to Icon image
    PAGES:PID|Name
        PAGES_DATA:PID|Path|LoginReq|Description|Icon
        PAGES_CONTENT:PID|Content
        PAGES_HISTORY:PID|UID|ChangeDTG|Content
    USERS:UID|Username
        USERS_DATA:UID|PW|Email|Verified|DOC|Admin
    FORUM:TID|ThreadName
        FORUM_THREAD_DATA:TID|Visible|DOC|UID|Content
        FORUM_POSTS:TID|P_ID|UID
            FORUM_POST_DATA:P_ID|UID|DOC|Content|Visible
'''

def get_data(table, ID):
    _Cursor = getConnection()
    return _Cursor.execute('SELECT * FROM "' + table + '" WHERE ID IS "' + str(ID) + '"').fetchall()

def _get_page(PID):
    _Cursor = getConnection()
    return _Cursor.execute('SELECT Content FROM "PAGES_CONTENT" WHERE PID = "' + str(PID) + '"').fetchall()[0][0]

def _get_image(PID):
    _Cursor = getConnection()
    return _Cursor.execute('SELECT Image FROM "PAGES_CONTENT" WHERE PID = "' + str(PID) + '"').fetchall()[0][0]

def _get_user(UID, PW):
    # If curosor returns valid user, return true
    return False

def login(UN, PW):
    _Cursor = getConnection()
    _Cursor.execute('SELECT TOP FROM "PAGES_CONTENT" WHERE PID = "' + str(PID) + '"').fetchall()

def pageAccess(UID, PageName, PageType):
    return True

def _page_exists(PageName, PageType):
    return _get_PID(PageName, PageType) != False

def _get_PID(PageName, PageType):
    _Cursor = getConnection()
    try:
        PID = _Cursor.execute('SELECT PID FROM "PAGES" WHERE NAME = "' + PageName + '" AND Type = "' + PageType + '"').fetchall()[0][0]
        return PID
    except:
        return False
    return False


def get_page(PageName, PageType):
    _Cursor = getConnection()
    try:
        PID = _get_PID(PageName, PageType)
        if PID == False:
            return _get_page(_get_PID('404', 'html'))
        elif PageType == 'png':
            img = _get_image(PID)
            return send_file(
                BytesIO(img),
                mimetype='image/png'
            )
        else:
            return _get_page(PID)
    except:
        return _get_page(_get_PID('404', 'html'))

def _getUniquePID():
    _Cursor = getConnection()
    PID = randint(10, 100000)
    exists = (len(_Cursor.execute('SELECT * FROM "PAGES" WHERE PID = ' + str(PID)).fetchall()) != 0)
    return PID

def get_page_files():
    _Cursor = getConnection()
    pages = _Cursor.execute('SELECT PAGES.Name, PAGES_DATA.Path, PAGES_DATA.Description FROM PAGES_DATA JOIN PAGES ON PAGES_DATA.PID = PAGES.PID').fetchall()
    return pages

def save_page(PageName, PageType, Content):
    _Cursor, _Connection = getCommitalConnection()
    if _page_exists(PageName, PageType):
        PID = _get_PID(PageName, PageType)
        # Add current copy to History
        # Add User ID and junk
        # Save New Contents
        _Cursor.execute('DELETE FROM "PAGES_CONTENT" WHERE PID = ' + str(PID))
        _Cursor.execute('INSERT INTO "PAGES_CONTENT" (PID, Content) VALUES(' + str(PID) + ', "' + Content.replace("\"", "\"\"") + '")')
        commitChanges(_Connection)
    else:
        PID = _getUniquePID()
        _Cursor.execute('INSERT INTO "PAGES" (PID, Name, Type) VALUES(' + PID + ', "' + PageName + '", "' + PageType + '")')
        _Cursor.execute('INSERT INTO "PAGES_CONTENT" (PID, Content) VALUES(' + PID + ', "' + Content.replace("\"", "\"\"") + '")')
        commitChanges(_Connection)

    