import sqlite3
DBNAME = "webapp_database.db"

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
        if values is None:
            c.execute(query)
        else:
            c.execute(query, values)
        conn.commit()
        conn.close()

    def _return(self, query, values=None, multi=False):
        conn = sqlite3.connect(self._dbname)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        if values is None:
            c.execute(query)
        else:
            c.execute(query, values)
        if multi:
            row = c.fetchall()
        else:
            row = c.fetchone()
        conn.close()
        return row # sqlite3.Row object (supports both numerical and key indexing)

    def _is_exist(self, key, value, tblname):
        """Checks whether a record exists in a table."""
        query = """
                SELECT *
                FROM ?
                WHERE ? = ?
                """
        values = tuple(tblname, key, value)
        row = self._execute(query, values)

        if row is None:
            return False
        return True
        

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

    def add(self, record):
        """Adds a student record into the database."""
        # check if student exists
        if self._is_exist(self._tblname, "student_name", record["student_name"]):
            return "exists"

        # retrieve class_id
        query = """SELECT 'class_id'
                FROM "Classes"
                WHERE class_name = ?;
                """
        values = tuple(record["class_name"])
        row = self._return(query, values, multi=False)
        class_id = row["class_id"]
        record["class_id"] = class_id
        
        # add student record
        query = f"""
                INSERT INTO '{self._tblname}' VALUES (:student_name, :age, :year_enrolled, :grad_year, :class_id);
                """
        self._execute(query, record)
        return
        
    def get(self, student_name):
        """Returns a student's record."""
        query = f"""
                SELECT *
                FROM '{self._tblname}'
                WHERE student_name = ?
                """
        values = tuple(student_name)
        row = self._return(query, values, False)

        # check if student exists
        if not self._is_exist("Students", "student_name", student_name):
            return None

        # 
        field_names = row.keys()
        data = {}
        for i, elem in enumerate(field_names):
            data[elem] = row[i]
        return data

    def update(self, record):
        """Updates student record in database."""
        # check if student exists
        if self._is_exist(self._tblname, "student_name", record["student_name"]:
            raise KeyError("Student already exists.")
            
        # retrieve class_id
        query = f"""
                SELECT 'class_id'
                FROM 'Classes'
                WHERE class_name = ?;
                """
        values = tuple(record["class_name"])
        row = self._return(query, values, False)
        class_id = row["class_id"]
        
        # update student record
        query = f"""
                UPDATE '{self._tblname}' SET
                    "age" = ?,
                    "year_enrolled" = ?,
                    "grad_year" = ?,
                    "class_id" = ?,
                WHERE student_name = ?;
                """
        values = tuple(record["age"], record["year_enrolled"], record["grad_year"], class_id, record["student_name"])
        self._execute(query, values)
        return
        
    def delete(self, student_name):
        """Deletes student record from database."""
        # check if student exists
        if not self._is_exist(self._tblname, "student_name", student_name):
            raise KeyError("Student does not exist.")

        # retrieve student_id
        query = """
                SELECT 'student_id'
                FROM 'Students'
                WHERE student_name = ?;
                """
        values = tuple(student_name)
        row = self._return(row, values, False)
        student_id = row["student_id"]
        
        # delete from Students-Activities, Students-CCAs, Students-Subjects and Students table
        tblnames = ["Students-Activites", "Students-CCAs", "Students-Subjects", "Students"]
        for tblname in tblnames:
            query = f"""
                    DELETE FROM '{tblname}'
                    WHERE student_id = ?;
                    """
            values = tuple(student_id)
            self._execute(query, values)
        return


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
        if not self._is_exist("Classes", "class_name", class_name):
            return None
        
        # retrieve student_id and student_name
        query = """
                SELECT 'student_id', 'student_name'
                FROM 'Students'
                WHERE class_name = ?
                ORDER BY 'student_id' ASC
                """
        values = tuple(class_name)
        row = self._return(query, values)
        
        data = {}
        for item in row:
            data[item["student_id"]] = item["student_name"]
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

    def get(self, student_name):
        """Returns a student's CCA."""
        # retrieve student_id
        query = """
                SELECT 'student_id'
                FROM 'Students'
                WHERE student_name = ?
                """
        values = tuple(student_name)
        row = self._return(query, values)
        student_id = row["student_id"]

        # check if student exists
        if not self._is_exist("Students", "student_name", student_name):
            return None
        
        # retrieve cca_id
        query = """
                SELECT 'cca_id'
                FROM 'Students-CCAs'
                WHERE student_id = ?
                """
        values = tuple(student_id)
        row = self._return(query, values)
        cca_id = row["cca_id"]

        # retrive cca_name
        query = """
                SELECT 'cca_name'
                FROM 'CCAs'
                WHERE cca_id = ?
                """
        values = tuple(cca_id)
        row = self._return(query, values)
        cca_name = row["cca_name"]

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
        row = self._return(query, values)

        # check if CCA exists
        if not self._is_exist("CCAs", "cca_name", cca_name):
            return None
        
        field_names = row.keys()
        data = {}
        for i, elem in enumerate(field_names):
            data[elem] = row[i]
        return data # dictionary


class Activities(Collection):
    """
    Activities Collection.
    """
    def __init__(self):
        super().__init__("Activies")

    def search(self, student_name):
        """Returns a student's activity."""
        # retrieve student_id
        query = """
                SELECT 'student_id'
                FROM 'Students'
                WHERE student_name = ?
                """
        values = tuple(student_name)
        row = self._execute(query, values)
        student_id = row["student_id"]

        # check if student exists
        if not self._is_exist("Students", "student_name", student_name):
            return None

        # retrieve activity_id
        query = """
                SELECT 'activity_id'
                FROM 'Students-Activities'
                WHERE student_id = ?
                """
        values = tuple(student_id)
        row = self._execute(query, values)
        activity_id = row["activity_id"]

        # retrieve activity_name
        query = f"""
                SELECT 'activity_name'
                FROM '{self._tblname}'
                WHERE activity_id = ?
                """
        values = tuple(activity_id)
        row = self._execute(query, values)
        activity_name = row["activity_name"]

        data = {}
        data[student_name] = activity_name
        return data # dictionary(key=student_name, value=activity_name)

    def get_all(self, activity_name):
        """Returns an activity's details."""
        query = f"""
                SELECT *
                FROM '{self._tblname}'
                WHERE activity_name = ?
                """
        values = tuple(activity_name)
        row = self._execute(query, values)

        # check if activity exists
        if not self._is_exist("Activities", "activity_name", activity_name):
            return None

        field_names = row.keys()
        data = {}
        for i, elem in enumerate(field_names):
            data[elem] = row[i]
        return data