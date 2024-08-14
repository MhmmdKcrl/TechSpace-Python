import pymysql

# Connect to the database
connection = pymysql.connect(   
    host = '127.0.0.1',
    user = 'root',
    password= '12345',
    db='TechSpace',
    port = 3306,
    charset = 'utf8mb4', 
    cursorclass= pymysql.cursors.DictCursor
)

# print(connection.host_info)

# create a table
def create_blog():
    with connection:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE if not exists TechSpace.Blogs3 (
                        id INT AUTO_INCREMENT PRIMARY KEY, 
                        title VARCHAR(100), 
                        author_name varchar(100)
                        );"""
            cursor.execute(sql)
        connection.commit()

# create_blog()


# insert data into the table
def insert_into_blog(title, author):
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO TechSpace.Blogs (title, author_name) VALUES (%s, %s)"
            cursor.execute(sql, (title, author))
        connection.commit()

# insert_into_blog('Python3', 'John Doe')
# insert_into_blog('Java3', 'Jane Doe')


# # get all the blogs
def get_all_blogs():
    with connection.cursor() as cursor:
            sql = "SELECT * FROM TechSpace.Blogs"
            cursor.execute(sql)
            print(cursor.fetchall())

# print(get_all_blogs())


# update a blog
def update_blog(id, title):
    with connection:
        with connection.cursor() as cursor:
            sql = f"UPDATE TechSpace.Blogs SET title = %s WHERE id = %s"
            cursor.execute(sql, (title, id))
        connection.commit()

# update_blog(9, 'Python6')




# get a single blog
def get_single_blog(id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM TechSpace.Blogs WHERE id = %s"
        cursor.execute(sql, (id))
        return cursor.fetchone()

# print(get_single_blog(5))




# filter by blog name
def filter_by_name(title):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM TechSpace.Blogs WHERE title like '%{title}%' "
        cursor.execute(sql)
        return cursor.fetchall()

# print(filter_by_name('Python'))

# delete a blog
def delete_single_blog(id):
    with connection:
        with connection.cursor() as cursor:
            sql = """DELETE FROM TechSpace.Blogs 
                WHERE id = %s"""
            cursor.execute(sql, (id))
        connection.commit()

# delete_single_blog(3)


class Blog(models.Model):
    title = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)

# Blog.objects.filter_by(title="Python")
