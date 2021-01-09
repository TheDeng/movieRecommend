

import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'MovieRecommendation.settings')
django.setup()
import csv


from movie.models import User,Movie,rating



csvfile_path = os.path.join('C:/Users/Think Tank/Desktop/MovieRecommendation/new_users.csv')

# movie_csvfile_path = os.path.join('C:/Users/Think Tank/Desktop/MovieRecommendation/new_movie.csv')
# rating_csvfile_path = os.path.join('C:/Users/Think Tank/Desktop/MovieRecommendation/new_ratings.csv')

with open(csvfile_path,encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        User.objects.update_or_create(
            # field1是字段名，row[0]是csv文件的第1列，以此类推
            user_md5=row[0],
            user_nickname=row[1],

        )

# with open(movie_csvfile_path,encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         Movie.objects.update_or_create(
#             # field1是字段名，row[0]是csv文件的第1列，以此类推
#             movie_id = row[0],
#             name = row[1],
#             alias = row[2],
#             actors = row[3],
#             cover=row[4],
#             directors = row[5],
#             score = row[6],
#             votes = row[7],
#             genres = row[8],
#             languages = row[10],
#             mins = row[11],
#             official_site = row[12],
#             regions = row[13],
#             release_date = row[14],
#             slug = row[15],
#             storyline = row[16],
#             tags = row[17],
#             year = row[18],
#             actor_ids = row[19],
#             director_ids = row[20],
#
#
#         )

# with open(rating_csvfile_path,encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         rating.objects.update_or_create(
#             # field1是字段名，row[0]是csv文件的第1列，以此类推
#             rating_id=row[0],
#             user_md5=row[1],
#             movie_id=row[2],
#             rating=row[3],
#             time= row[4],
#
#
#
#         )