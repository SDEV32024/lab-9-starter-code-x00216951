from django.test import Client, TestCase
from django.urls import reverse
from .models import Book

class BookTests(TestCase):
    
    def setUp(self):
        self.book = Book.objects.create(
            title='Django 4 By Example',
            author='Anthony Mele',
            price='25.00',
            date_publication='2022-08-01'
        )
    
    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Django 4 By Example')
        self.assertEqual(f'{self.book.author}', 'Anthony Mele')
        self.assertEqual(f'{self.book.price}', '25.00')
        self.assertEqual(f'{self.book.date_publication}', '2022-08-01')
    
    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django 4 By Example')
        self.assertTemplateUsed(response, 'books/book_list.html')
    
    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Django 4 By Example')
        self.assertTemplateUsed(response, 'books/book_detail.html')
    
    def test_search_results_view(self):
        response = self.client.get(reverse('search_results'), {'q': 'Django'})
        no_result = self.client.get(reverse('search_results'), {'q': 'Software'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django')
        self.assertEqual(no_result.status_code, 200)
        self.assertNotContains(no_result, 'Software')
    
    def test_book_str_representation(self):
        expected_str = "Django 4 By Example"
        self.assertEqual(str(self.book), expected_str)
    
    def test_get_absolute_url_method(self):
        # Test the get_absolute_url method of Profile
        expected_url = '/books/{}/'.format(self.book.pk)
        self.assertEqual(self.book.get_absolute_url(), expected_url)