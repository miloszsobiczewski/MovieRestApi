import unittest
import movies.utils as ut
import datetime
import requests as r


class MovieRestApiUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.correct_movie_title = 'Django'
        self.incorrect_movie_title = 'Humbeleulagula'
        self.movies_url = 'http://0.0.0.0:8000/movies/'
        self.comments_url = 'http://0.0.0.0:8000/comments/'
        self.top_url = 'http://0.0.0.0:8000/top/'
        self.correct_date = '1.4.2019'
        self.incorrect_date = '2019.4.1'
        self.test_comment = 'Test Comment'
        self.movies_list = ['Predator', 'Predator 2', 'Predators', 'Alien']

    def test_001_get_date(self):
        """
        Checks if function returns date and the date is in correct format:
        'dd.mm.yyyy'
        :return:
        """
        date = ut.get_date(self.correct_date)
        self.assertTrue(isinstance(date, datetime.date))
        self.assertGreaterEqual(date.year, 2019)

    def test_002_get_omdb_data(self):
        """
        Checks if function returns correct responses depending on the movie
        existence in OMDb
        :return:
        """
        data = ut.get_omdb_data(self.correct_movie_title)
        self.assertTrue(bool(data['Response'] == 'True')) ## TODO czy trzeba robic bool()???

        data = ut.get_omdb_data(self.incorrect_movie_title)
        self.assertFalse(bool(data['Response'] == 'True'))

    def test_003_post_movie(self):
        """
        Post new movie, retrieve from api, compare and delete
        :return:
        """
        parameters = {"movie_title": self.correct_movie_title}

        # POST movie
        response = r.post(self.movies_url, data=parameters)
        post = response.json()

        movie_id = post['id']
        url = self.movies_url + str(movie_id) + '/'

        # GET movie
        response = r.get(url, data={"id": movie_id})
        get = response.json()
        self.assertEqual(post['movie_title'], get['movie_title'])

        # DELETE movie
        r.delete(url, data={"id": movie_id})

    def test_004_post_comment(self):
        """
        Post new movie, Post new comment, retrieve from api, compare and delete
        movie with comments
        :return:
        """
        movie_parameters = {"movie_title": self.correct_movie_title}

        # POST movie
        response = r.post(self.movies_url, data=movie_parameters)
        post = response.json()

        movie_id = post['id']
        movie_url = self.movies_url + str(movie_id) + '/'

        comment_parameters = {"movie_id": movie_id,
                              "comment_txt": self.test_comment}

        # POST comment
        response = r.post(self.comments_url, data=comment_parameters)
        post = response.json()

        comment_id = post['id']
        comment_url = self.comments_url + str(comment_id) + '/'

        # GET comment
        response = r.get(comment_url, data={"id": comment_id})
        get = response.json()

        self.assertEqual(post['comment_txt'], get['comment_txt'])

        # DELETE movie, DELETE comment cascade
        r.delete(movie_url, data={"id": movie_id})

    def test_005_get_top(self):
        """
        Post new movies and comments, Check if returned list is appropriate
        :return:
        """
        movies_id_list = []

        # POST movies
        for m in self.movies_list:
            response = r.post(self.movies_url, data={"movie_title": m})
            movies_id_list.append(response.json()['id'])

        # POST comments
        for c in range(4):
            r.post(self.comments_url, data={"movie_id": movies_id_list[0],
                                            "comment_txt": self.test_comment})
        for c in range(2):
            r.post(self.comments_url, data={"movie_id": movies_id_list[1],
                                            "comment_txt": self.test_comment})
            r.post(self.comments_url, data={"movie_id": movies_id_list[2],
                                            "comment_txt": self.test_comment})
        # GET top
        response = r.get(self.top_url)
        get = response.json()
        ranks = [d.get('rank') for d in get]
        total_comments = [d.get('total_comments') for d in get]

        self.assertEqual(ranks, [1, 2, 2, 3])
        self.assertEqual(total_comments, [4, 2, 2, 0])

        # DELETE movies, DELETE comments cascade
        for i in movies_id_list:
            movie_url = self.movies_url + str(i) + '/'
            r.delete(movie_url, data={"id": i})

    @classmethod
    def tearDownClass(self):
        """
        Delete saved movies and comments
        :return:
        """
        pass


if __name__ == '__main__':
    unittest.main()
