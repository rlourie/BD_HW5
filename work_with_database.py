from pprint import pprint
import sqlalchemy

db = 'postgresql://azvezdin:***********!@localhost:5432/hw_2'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()
sel = connection.execute("""
    SELECT g.title, COUNT(s.singer_name)
    FROM genre AS g
    LEFT JOIN genre_singer AS gs ON g.id = gs.id_genre
    LEFT JOIN singer AS s ON gs.id_singer = s.id
    GROUP BY g.title
    ORDER BY COUNT(s.id) DESC
""").fetchall()
print("Kоличество исполнителей в каждом жанре;")
pprint(sel)
print()

sel = connection.execute("""
    SELECT t.title, a.year_issue
    FROM album AS a
    LEFT JOIN track AS t ON t.id_album = a.id
    WHERE (a.year_issue >= 2019) AND (a.year_issue <= 2020)
""").fetchall()
print("Kоличество треков, вошедших в альбомы 2019-2020 годов;")
pprint(sel)
print()

sel = connection.execute("""
    SELECT a.title, AVG(t.duration)
    FROM album as a
    LEFT JOIN track as t on t.id_album = a.id
    GROUP BY a.title
    ORDER BY AVG(t.duration)
""").fetchall()
print("Cредняя продолжительность треков по каждому альбому;")
pprint(sel)
print()

sel = connection.execute("""
SElECT DISTINCT s.singer_name
FROM singer as s
WHERE s.singer_name NOT IN (
    SELECT DISTINCT s.singer_name
    FROM singer AS s
    LEFT JOIN singer_album AS sa on s.id = sa.id
    LEFT JOIN album AS a on a.id = sa.id_album
    WHERE a.year_issue = 2020
)
ORDER BY s.singer_name
""").fetchall()
print("Все исполнители, которые не выпустили альбомы в 2020 году;")
pprint(sel)
print()

sel = connection.execute("""
SELECT DISTINCT c.title
FROM collection AS c
LEFT JOIN collection_track AS ct ON c.id = ct.id
LEFT JOIN track AS t ON t.id = ct.id_track
LEFT JOIN album AS a ON a.id = t.id_album
LEFT JOIN singer_album AS sa ON sa.id_album = a.id
LEFT JOIN singer AS s ON s.id = sa.id_singer
WHERE s.singer_name LIKE '%%Lili%%'
ORDER BY c.title
""").fetchall()
print("Названия сборников, в которых присутствует конкретный исполнитель (выберите сами);")
pprint(sel)
print()

sel = connection.execute("""
SELECT a.title
FROM album AS a
LEFT JOIN singer_album AS sa ON a.id = sa.id_album
LEFT JOIN singer AS s ON s.id = sa.id_singer
LEFT JOIN genre_singer AS gs ON s.id = gs.id_singer
LEFT JOIN genre AS g ON g.id = gs.id_genre
GROUP BY a.title
HAVING COUNT(DISTINCT g.title) > 1
ORDER BY a.title
""").fetchall()
print("Название альбомов, в которых присутствуют исполнители более 1 жанра;")
pprint(sel)
print()

sel = connection.execute("""
SELECT t.title
FROM track AS t
LEFT JOIN collection_track AS ct ON t.id = ct.id_track
WHERE ct.id_track IS NULL
""").fetchall()
print("Наименование треков, которые не входят в сборники;")
pprint(sel)
print()

sel = connection.execute("""
SELECT s.singer_name, t.duration
FROM track AS t
LEFT JOIN album AS a ON a.id = t.id_album
LEFT JOIN singer_album AS sa ON sa.id_album = a.id
LEFT JOIN singer AS s ON s.id = sa.id_singer
GROUP BY s.singer_name, t.duration
HAVING t.duration = (SELECT MIN(duration) FROM track)
ORDER BY s.singer_name
""").fetchall()
print(
    "Исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);")
pprint(sel)
print()

sel = connection.execute("""
SELECT DISTINCT a.title
FROM album AS a
LEFT JOIN track AS t ON t.id_album = a.id
WHERE t.id_album IN (
    SELECT id_album
    FROM track
    GROUP BY id_album
    HAVING COUNT(id) = (
        SELECT COUNT(id)
        FROM track
        GROUP BY id_album
        ORDER BY COUNT
        LIMIT 1
    )
)
ORDER BY a.title
""").fetchall()
print("Название альбомов, содержащих наименьшее количество треков.")
pprint(sel)
print()
