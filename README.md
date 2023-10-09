# PhonesAndAddresses
1. FastAPI Service:
- https://hub.docker.com/layers/d4tremar/addresses-phones/1.0/images/sha256:2b684adf4876a33ab0b78892e8d320d6b4bccf7f3d1420a44ecc09338fc7af1d?uuid=6862290D-6149-46BE-AD92-5E179BC8E860

2. SQL problem:

Подход 1. Чистый SQL запрос:

Представим что у нас есть 2 таблицы. 
```sql
CREATE short_names(
  sh_id SERIAL PRIMARY KEY,
  name VARCHAR(128),
  status INT
);

CREATE full_names(
  fl_id SERIAL PRIMARY KEY,
  name VARCHAR(128),
  status INT
);
```
Если задача состоит в том, чтобы осуществить перенос столбца статусов с таблицы short_names в full_names, то подойдет следующее решение:
```sql
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE split_part(full_names.name, '.', 1) = short_names.name;
``` 
Отбросив расширения файлов в столбце названий и сделав inner join на обеих таблицах, открывается возможность выполнения запроса с хешированием данных.
Таким образом, получается избежать вложенного цикла, как если бы в запросе был использован LIKE.
На моей машине, запрос выполнился за 17.6 сек. без кеширования. 

Подход 2. Скрипт на Python

```python
import psycopg2


if __name__ == '__main__':
    with psycopg2.connect(
        database="postgres",
        user="postgres",
        password="testpassword"
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("select name, status from full_names;")
            data = cursor.fetchall()

            full_names = dict()

            for item in data:
                full_names[item[0]] = item[1]

            cursor.execute("select name, status from short_names;")
            data = cursor.fetchall()

            short_names = dict()

            for item in data:
                short_names[item[0]] = item[1]

            for name in full_names:
                full_names[name] = short_names[name.split('.')[0]]

            data = tuple(f"('{name}', {status})" for name, status in full_names.items())

            query = ("update full_names as fn"
                     " set status = d.status"
                     " from (values {}) as d(name, status)"
                     " where fn.name = d.name;").format(", ".join(data))

            cursor.execute(query)
            conn.commit()
```
Здесь, задача выполнена похожим образом. Однако, у этого решения есть гигантский недостаток - излишнее наполнение ОЗУ на стороне web app. 
В таких ситуациях, выполнение обработки данных на стороне сервиса БД сильно выигрывает перед скриптовой обработкой, т.к. здесь происходит запрос всех данных, их обработка на стороне приложения и их отправка на запись обратно к БД сервису.
Решение неоптимально с точки зрения инфраструктуры сервиса, но использование хэширования данных позволяет выполнить обработку за реалистичное время.
Запрос был выполнен за 23.4 сек. на локальном сервере.


