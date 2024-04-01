from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author


class AuthorCRUDTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_author(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'about': 'A famous author'
        }

        image_path = 'media/author_images/3_XEQvXoj.jpeg'  # Update the path as needed
        image_file = SimpleUploadedFile("3_XEQvXoj.jpeg", open(image_path, 'rb').read(), content_type="image/jpeg")
        data['image'] = image_file

        response = self.client.post('/books/author/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Author.objects.filter(name='Doe John').exists())

    def test_read_author(self):
        author = Author.objects.create(
            first_name='Jane',
            last_name='Doe',
            about='Another author',
            image='media/authors/3.jpeg'
        )
        response = self.client.get(f'/books/author/{author.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane')
        self.assertEqual(response.data['last_name'], 'Doe')

    def test_update_author(self):
        author = Author.objects.create(
            first_name='Old',
            last_name='Author',
            about='An old author',
            image='media/author_images/3.jpeg'
        )
        
        data = {
            'first_name': 'New',
            'last_name': 'Author',
            'about': 'An updated author'
        }

        updated_image_path = 'media/author_images/3_XEQvXoj.jpeg' 
        updated_image_file = SimpleUploadedFile("new_image.jpeg", open(updated_image_path, 'rb').read(), content_type="image/jpeg")
        data['image'] = updated_image_file

        response = self.client.put(f'/books/author/{author.slug}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        author.refresh_from_db()
        self.assertEqual(author.first_name, 'New')
        self.assertEqual(author.about, 'An updated author')

    def test_delete_author(self):
        author = Author.objects.create(
            first_name='To',
            last_name='Be Deleted',
            about='An author to be deleted',
            image='media/authors/3_XEQvXoj.jpeg'
        )
        response = self.client.delete(f'/books/author/{author.slug}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(slug=author.slug).exists())
