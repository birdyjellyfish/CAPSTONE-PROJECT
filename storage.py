import sqlite3
DBNAME = "webapp_database"

class Collection:
    """
    Collection class acts as an interface with the database and its tables.
    """
    def __init__(self, tblname):
        self._dbname = DBNAME
        self._tblname = tblname

    def __repr__(self):
        pass

    def _execute(self, query, values=None):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        c.execute(query, values)
        conn.commit()
        conn.close()

    def _return(self, query, values=None):
        conn = sqlite3.connect(self._dbname)
        c = conn.cursor()
        c.execute(query, values)
        rows = c.fetchall() 
        conn.close()
        return rows


class Students(Collection):
    """
    Student Collection
    Methods:
    --------
    add(record)
    get(student_name)
    update(student_name, record)
    delete(student_name)
    """
    def __init__(self):
        super().__init__("Students")

    def add(self, record: dict):
        """
        Adds a student record into the database.
        Record includes
        """
        query = f"""
                INSERT INTO {self._tblname} VALUES (?, ?, ?, ?, ?, ?, ?)
                """
        values = tuple(record.values())
        self._execute(query, values)

    def get(self, student_name):
        """Returns record of student."""
        query = f"""
                SELECT *
                FROM {self._tblname}
                """

    def update(self, student_name, record):
        """Updates student record in database."""
        pass

    def delete(self, student_name):
        """Deletes student record from database."""
        pass


class Classes(Collection):
    """
    Classes Collection
    Methods:
    --------
    add()
    get_all(class_name)
    update()
    delete()
    """
    def __init__(self):
        super().__init__("Classes")

    def add(self, name):
        """"""
        pass

    def get_all(self, class_name):
        """Returns all students in the corresponding class."""
        # check if class exists
            
        # retrieve class_id
        query = f"""
                SELECT 'class_id'
                FROM '{self._tblname}'
                WHERE class_name = ?
                """
        values = tuple(class_name)
        rows = self._return(query, values)
        class_id = rows[0]    # tuple
        
        # retrieve student_id and student_name
        query = f"""
                SELECT 'student_Id', 'student_name'
                FROM 'Students-Classes'
                WHERE class_id = ?
                ORDER BY 'student_id' ASC
                """
        values = class_id
        rows = self._return(query, values)
        
        data = {}
        for item in rows:
            data[item[0]] = item[1]
        return data    # dictionary(key=id, value=student_name)

    def update(self):
        """"""
        pass

    def delete(self, class_name):
        """"""
        pass


class Subjects(Collection):
    """
    Subjects Collection
    """
    def __init__(self):
        super().__init__("Subjects")


class CCAs(Collection):
    """
    CCAs Collection
    """
    def __init__(self):
        super().__init__("CCAs")

    def add(self, cca_name):
        """"""
        pass

    def search(self, student_name):
        """Returns a student's CCA."""
        # retrieve student_id
        query = """
                SELECT 'student_id'
                FROM 'Students'
                WHERE student_name = ?
                """
        values = tuple(student_name)
        rows = self._return(query, values)
        student_id = rows[0]    # tuple

        # retrieve cca_id
        query = """
                SELECT 'cca_id'
                FROM 'Students-CCAs'
                WHERE student_id = ?
                """
        values = student_id
        rows = self._return(query, values)
        cca_id = rows[0]    # tuple

        # retrive cca_name
        query = """
                SELECT 'cca_name'
                FROM 'Ccas'
                WHERE cca_id = ?
                """
        values = cca_id
        rows = self._return(query, values)
        cca_name = rows[0][0]

        data = {}
        data[student_name] = cca_name
        return data    # dictionary(key=student_name, value=cca_name)

    def get_all(self, cca_name):
        """Returns a CCA's details."""
        query = """
                SELECT *
                FROM 'CCAs'
                WHERE cca_name = ?
                """
        values = tuple(cca_name)
        rows = self._return(query, values)
        ##############################


    # get_all method returns cca info

class Activities(Collection):
    """
    Activities Collection
    """
    def __init__(self):
        super().__init__("Activies")

    # search method return dictionary {kaelin: activity}
    # get_all method returns activity info