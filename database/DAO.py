from database.DB_connect import DBConnect
from model.interprete import Interprete

class DAO:
    @staticmethod
    def getGenres():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT DISTINCT genre as nome
                FROM genre
                ORDER BY genre"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["nome"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT year AS anno
                   FROM movie
                   ORDER BY year"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        cnx.close()
        return result
    @staticmethod
    def getNodi(genere, anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT n.id, n.name, n.date_of_birth
                   FROM names n, role_mapping rm, movie m, genre g
                   WHERE n.id = rm.name_id
                     AND rm.movie_id = m.id
                     AND m.id = g.movie_id
                     AND rm.category IN ('actor', 'actress')
                     AND g.genre = %s
                     AND m.year = %s"""
        cursor.execute(query, (genere, anno))
        for row in cursor:
            result.append(Interprete(row["id"], row["name"], row["date_of_birth"]))

        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getCoppia(genere, anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT DISTINCT r.name_id AS idP, r.movie_id AS idF
                   FROM role_mapping r, movie m, genre g
                   WHERE r.movie_id = m.id
                     AND m.id = g.movie_id
                     AND g.genre = %s
                     AND m.year = %s"""
        cursor.execute(query, (genere, anno))
        for row in cursor:
            result.append((row["idP"], row["idF"]))

        cursor.close()
        cnx.close()
        return result



