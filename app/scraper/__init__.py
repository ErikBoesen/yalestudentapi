from app import app, db, celery
from app.models import Person

from app.scraper import sources
from .cache import Cache
import json
import os
from threading import Thread


def scrape_face_book_directory_name_coach(face_book, directory, name_coach):
    people = []
    thread_fb = Thread(target=face_book.pull, args=(people,))
    thread_dir = Thread(target=directory.pull, args=(people,))
    thread_fb.start()
    thread_dir.start()
    thread_fb.join()
    thread_dir.join()
    people = face_book.integrate(people)
    people = directory.integrate(people)
    name_coach.pull(people)
    people = name_coach.integrate(people)


@celery.task
def scrape(face_book_cookie, people_search_session_cookie, csrf_token):
    print('Launching scraper.')
    cache = Cache()

    cache_key = 'scraped_data'
    print('Checking cache...')
    people = cache.get(cache_key)
    if people:
        print('Found people in cache.')
    else:
        print('Initializing sources.')
        directory = sources.Directory(cache, people_search_session_cookie, csrf_token)
        face_book = sources.FaceBook(cache, face_book_cookie, directory)
        name_coach = sources.NameCoach(cache, people_search_session_cookie, csrf_token)
        departmental = sources.Departmental(cache)

        print('Beginning scrape.')
        people = []
        thread_fb_dir_nc = Thread(target=scrape_face_book_directory_name_coach,
                                  args=(face_book, directory, name_coach))
        thread_departmental = Thread(target=departmental.pull, args=(people,))
        thread_fb_dir_nc.start()
        thread_departmental.start()
        thread_fb_dir_nc.join()
        thread_departmental.join()
        # TODO: find a cleaner way to exchange this data
        people = name_coach.people
        people = departmental.integrate(people)
        cache.set(cache_key, people)

    # Store people into database
    print('Inserting new data.')
    Person.query.delete()
    for person_dict in people:
        db.session.add(Person(**{k: v for k, v in person_dict.items() if v or type(v) == bool}))
    db.session.commit()
    print('Done.')
