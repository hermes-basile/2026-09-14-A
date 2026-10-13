from database.DB_connect import DBConnect
from model.actor import Actor


class DAO:
    @staticmethod
    def getAllMovies():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select * from movie m """

        cursor.execute(query)

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllActor():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.*
                    from names n , role_mapping rm 
                    where rm.name_id = n.id 
                    and (rm.category = 'actor' or rm.category = 'actress')
                 """

        cursor.execute(query)

        for row in cursor:
            results.append(
                Actor(**row)
            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(rangeA, rangeB):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct rm.name_id as actor_id
                    from names n , role_mapping rm, ratings r 
                    where rm.name_id = n.id and r.movie_id = rm.movie_id 
                    and (rm.category = 'actor' or rm.category = 'actress')
                    and r.avg_rating >= %s
                    and r.avg_rating  <= %s
                    order by rm.name_id asc
                     """

        cursor.execute(query,(rangeA, rangeB))

        for row in cursor:
            results.append(
                row["actor_id"]
            )

        cursor.close()
        conn.close()
        return results



    @staticmethod
    def getArchi(rangeA, rangeB):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select rm.name_id as u, rm2.name_id as v, count(r.movie_id) as peso
                    from names n , role_mapping rm, ratings r, role_mapping rm2 
                    where rm.name_id = n.id and r.movie_id = rm.movie_id and rm2.movie_id = r.movie_id 
                    and (rm.category = 'actor' or rm.category = 'actress')
                    and r.avg_rating >= %s
                    and r.avg_rating  <= %s
                    and rm.name_id < rm2.name_id 
                    group by rm.name_id, rm2.name_id 
                        """

        cursor.execute(query, (rangeA, rangeB))

        for row in cursor:
            results.append(
                (row["u"],row["v"],row["peso"])
            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAttoreFilm(rangeA, rangeB):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct rm.name_id as id_actor, rm.movie_id as id_movie
                    from names n , role_mapping rm, ratings r 
                    where rm.name_id = n.id and r.movie_id = rm.movie_id 
                    and (rm.category = 'actor' or rm.category = 'actress')
                    and r.avg_rating >= %s
                    and r.avg_rating  <= %s
                    order by rm.name_id asc 
                           """

        cursor.execute(query, (rangeA, rangeB))

        for row in cursor:
            results.append(
                (row["id_actor"], row["id_movie"])
            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getFilmAttore(rangeA, rangeB):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct rm.movie_id , rm.name_id 
                    from names n , role_mapping rm, ratings r 
                    where rm.name_id = n.id and r.movie_id = rm.movie_id 
                    and (rm.category = 'actor' or rm.category = 'actress')
                    and r.avg_rating >= %s 
                    and r.avg_rating  <= %s
                    order by rm.movie_id asc 
                              """

        cursor.execute(query, (rangeA, rangeB))

        for row in cursor:
            results.append(
                (row["movie_id"], row["name_id"])
            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getFilmforActor(attore, rangeA, rangeB):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select  m.id ,m.title , m.`year` ,r.avg_rating 
                    from role_mapping rm ,movie m ,ratings r 
                    where rm.movie_id = m.id and r.movie_id = rm.movie_id 
                    and (rm.category = 'actor' or rm.category = 'actress')
                    and rm.name_id = %s
                    and r.avg_rating >= %s
                    and r.avg_rating <= %s
                                  """

        cursor.execute(query, (attore.id, rangeA,rangeB))

        lista_film_DAO = []
        for row in cursor:
           lista_film_DAO.append({
                "movie_id" : row["id"],
                "title" : row["title"],
                "year" : row["year"],
                "avg_rating" : float(row["avg_rating"])
            })

        cursor.close()
        conn.close()
        attore.lista_film = lista_film_DAO


