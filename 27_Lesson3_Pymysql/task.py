with open('blog_list.txt', 'r') as file:
    file_data = file.read()

    my_list = file_data.split('---------------------\n')

    # print(my_list)

new_list = []

for i in  my_list:
    temporary_list = []
    if len(i) != 0:
        id, title, author = i.strip().split("\n")    
        # print(id)
        temporary_list.append(id.split(": ")[1])
        temporary_list.append(title.split(": ")[1])
        temporary_list.append(author.split(": ")[1])
        # print(temporary_list)
        new_list.append(temporary_list)
    
print(new_list)

with connection.cursor()as cursor:
    for i in new_list:
        sql.execute("INSERT INTO blog (id, title, author) VALUES (%s, %s, %s)", (i[0], i[1], i[2]))



