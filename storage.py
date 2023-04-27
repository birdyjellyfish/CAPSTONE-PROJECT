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
                WHERE ? = ?;
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
            return False

        # retrieve class_id
        query = """SELECT 'class_id'
                FROM 'Classes'
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
        # check if student exists
        if not self._is_exist("Students", "student_name", student_name):
            return False
        
        # retrieve student record
        query = f"""
                SELECT *
                FROM '{self._tblname}'
                WHERE student_name = ?;
                """
        values = tuple(student_name)
        row = self._return(query, values, multi=False)

        # retrieve class_name
        query = f"""
                SELECT 'class_name'
                FROM 'Classes'
                WHERE class_id = ?;
                """
        values = tuple(row["class_id"])
        row2 = self._return(query, values, multi=False)
        class_name = row2["class_name"]
        del row["class_id"]
        row["class_name"] = class_name

        # convert data to dictionary
        field_names = row.keys()
        data = {}
        for i, elem in enumerate(field_names):
            data[elem] = row[i]
        return data

    def update(self, record):
        """Updates student record in database."""
        # check if student exists
        if self._is_exist(self._tblname, "student_name", record["student_name"]:
            return False
            
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
            return "does not exist"

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
    add(record)
    get_all(class_name)
    update(record)
    """
    def __init__(self):
        super().__init__("Classes")

    def add(self, record):
        """Adds a class record to the database."""
        # check if class exists
        if self._is_exist(self._tblname, "class_name", record["class_name"]):
            return False

        # add class record
        query = f"""
                INSERT INTO '{self._tblname}' VALUES (:class_name, :level);
                """
        self._execute(query, record)
        return

    def get_all(self, class_name):
        """Returns all students in the corresponding class."""
        # check if class exists
        if not self._is_exist("Classes", "class_name", class_name):
            return False

        # retrieve class_id
        query = f"""
                SELECT 'class_id'
                FROM '{self._tblname}'
                WHERE class_name = ?;
                """
        values = tuple(class_name)
        row = self._return(query, values, multi=False)
        class_id = row["class_id"]
        
        # retrieve student_id and student_name
        query = """
                SELECT 'student_id', 'student_name'
                FROM 'Students'
                WHERE class_id = ?
                ORDER BY 'student_id' ASC;
                """
        values = tuple(class_id)
        row = self._return(query, values, multi=True)

        # convert data to dictionary (key=id, value=student_name)
        data = {}
        for item in row:
            data[item["student_id"]] = item["student_name"]
        return data

    def update(self, record):
        """Updates class record in the database."""
        # check if class exists
        if not self._is_exist(self._tblname, "class_name", record["class_name"]):
            return False

        # update class record
        query = f"""
                UPDATE '{self._tblname}' SET
                    'level' = ?
                WHERE class_name = ?;
                """
        values = tuple(record["level"], record["class_name"])
        self._execute(query, values)
        return


class Subjects(Collection):
    """
    Subjects Collection
    """
    def __init__(self):
        super().__init__("Subjects")
        

class CCAs(Collection):
    """
    CCAs Collection

    Methods:
    --------
    add(record)
    get(student_name)
    get_all(cca_name)
    """
    def __init__(self):
        super().__init__("CCAs")

    def add(self, record):
        """Adds a CCA record to the database."""
        # check if CCA exists
        if self._is_exist(self._tblname, "cca_name", record["cca_name"]):
            return False

        # add CCA record
        query = f"""
                INSERT INTO '{self._tblname}' VALUES (:cca_name, :type);
                """
        self._execute(query, record)
        return

    def get(self, student_name):
        """Returns a student's CCA."""
        # check if student exists
        if not self._is_exist("Students", "student_name", student_name):
            return False
            
        # retrieve student_id
        query = """
                SELECT 'student_id'
                FROM 'Students'
                WHERE student_name = ?;
                """
        values = tuple(student_name)
        row = self._return(query, values, multi=False)
        student_id = row["student_id"]
        
        # retrieve cca_id and role
        query = """
                SELECT 'cca_id', 'role'
                FROM 'Students-CCAs'
                WHERE student_id = ?
                """
        values = tuple(student_id)
        row = self._return(query, values, multi=True)
        cca_id = row["cca_id"]
        role = row["role"]

         # check if CCA exists
        if not self._is_exist("CCAs", "cca_id", cca_id):
            return False
            
        # retrive cca_name
        query = """
                SELECT 'cca_name'
                FROM 'CCAs'
                WHERE cca_id = ?
                """
        values = tuple(cca_id)
        row = self._return(query, values)
        cca_name = row["cca_name"]

        # convert data into dictionary
        data = {}
        data["student_name"] = student_name
        data["cca_name"] = cca_name
        data["role"] = role
        return

    def get_all(self, cca_name):
        """Returns a CCA's details."""
         # check if CCA exists
        if not self._is_exist("CCAs", "cca_name", cca_name):
            return None
            
        # retrieve CCA record
        query = """
                SELECT *
                FROM 'CCAs'
                WHERE cca_name = ?;
                """
        values = tuple(cca_name)
        row = self._return(query, values, multi=False)
        
        # convert data to dictionary
        field_names = row.keys()
        data = {}
        for i, elem in enumerate(field_names):
            data[elem] = row[i]
        return data


class Activities(Collection):
    """
    Activities Collection.

    Methods:
    --------
    add(record)
    """
    def __init__(self):
        super().__init__("Activities")


    def add(self, record):
        """Adds an activity record into the database."""
        # check if activity exists
        if self._is_exist(self._tblname, "activity_name", record["activity_name"]):
            return False

        # add activity record
        query = f"""
                INSERT INTO '{self._tblname}' VALUES (?, ?, ?, ?);
                """
        

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