import pymysql
from typing import List

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



def get_all_blogs():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM TechSpace.Blogs"
        cursor.execute(sql)
        return cursor.fetchall()

# print(get_all_blogs())

def write_to_file(blog_list: List) -> None:
    with open('blog_list.txt', 'w+') as file:
        for blog in blog_list:
            for key, value in blog.items():
                file.write(str(key) + ': ' + str(value) + '\n')
            file.write('---------------------\n')
    
write_to_file(get_all_blogs())

