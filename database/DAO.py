from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO:
    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from genre order by Name asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtistsWPopularity():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT ar.ArtistId, ar.Name, SUM(il.Quantity) as Popularity
                FROM artist ar
                JOIN album al ON ar.ArtistId = al.ArtistId
                JOIN track t ON al.AlbumId = t.AlbumId
                JOIN invoiceline il ON t.TrackId = il.TrackId
                GROUP BY ar.ArtistId, ar.Name
                """

        cursor.execute(query)

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArtistsByGenre(selected_genre_id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select a.ArtistId
                from track t
                join album a on a.AlbumId = t.AlbumId
                where t.GenreId = %s"""

        cursor.execute(query, (selected_genre_id,))

        for row in cursor:
            result.append(row['ArtistId'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(selected_genre_id):
        conn = DBConnect.get_connection()

        cursor = conn.cursor()
        query = """
                with artist_invoice as 
                (SELECT ar.ArtistId, ar.Name as ArtistName, t.TrackId, t.Name as TrackName, i.CustomerId 
                FROM artist ar
                JOIN album al ON ar.ArtistId = al.ArtistId
                JOIN track t ON al.AlbumId = t.AlbumId
                JOIN invoiceline il ON t.TrackId = il.TrackId
                JOIN invoice i ON il.InvoiceId = i.InvoiceId
                where t.GenreId = %s
                )
                select least(a1.artistid, a2.artistid), greatest(a1.artistid, a2.artistid), count(*)
                from artist_invoice a1, artist_invoice a2
                where a1.customerid = a2.customerid
                and a1.artistid != a2.artistid
                group by a1.artistid, a2.artistid       
                """

        cursor.execute(query, (selected_genre_id,))

        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result
