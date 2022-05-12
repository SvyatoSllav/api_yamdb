import os
import csv

from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, GenreTitle

path = 'api_yamdb/static/data/'
os.chdir(path)

"""Импорт Category"""
with open('category.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row_import = Category(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
        row_import.save()

"""Импорт Genre"""
with open('genre.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row_import = Genre(
            id=row['id'],
            name=row['name'],
            slug=row['slug'],
        )
        row_import.save()

"""Импорт Title"""
with open('titles.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row_import = Title(
            id=row['id'],
            name=row['name'],
            year=row['year'],
            category=get_object_or_404(Category, pk=row['category'])
        )
        row_import.save()


"""Импорт GENRE_TITLE"""
with open('genre_title.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row_import = GenreTitle(
            id=row['id'],
            title_id=get_object_or_404(Title, pk=row['title_id']),
            genre_id=get_object_or_404(Genre, pk=row['genre_id'])
        )
        row_import.save()
