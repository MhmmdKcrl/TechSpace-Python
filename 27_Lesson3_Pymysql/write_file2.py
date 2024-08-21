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



def insert_blog_data(blog_list):
   
    
    try:
        with connection.cursor() as cursor:
            # Məlumatların verilənlər bazasına yazılması üçün SQL sorğusu
            sql = "INSERT INTO blogs (id, title, author_name) VALUES (%s, %s, %s)"
            
            # Hər bir blog üçün məlumatları əlavə edirik
            for blog in blog_list:
                cursor.execute(sql, (blog['id'], blog['title'], blog['author_name']))
            
            # Dəyişiklikləri tətbiq edirik
            connection.commit()
            print("Məlumatlar verilənlər bazasına yazıldı.")
    
    finally:
        # Bağlantını bağlayırıq
        connection.close()

def read_blog_data_from_file(file_path):
    blog_list = []
    with open(file_path, 'r') as file:
        blog_data = {}
        for line in file:
            if "id:" in line:
                blog_data['id'] = int(line.split(":")[1].strip())
            elif "title:" in line:
                blog_data['title'] = line.split(":")[1].strip()
            elif "author_name:" in line:
                blog_data['author_name'] = line.split(":")[1].strip()
            elif "---------------------" in line:
                blog_list.append(blog_data)
                blog_data = {}
    return blog_list

# Fayldan məlumatları oxuyuruq
blog_list = read_blog_data_from_file('./blog_list.txt')

# Məlumatları verilənlər bazasına yazırıq
insert_blog_data(blog_list)