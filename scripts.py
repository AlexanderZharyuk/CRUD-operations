import random

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from datacenter.models import Mark, Chastisement, Schoolkid, Lesson, Commendation


def find_schoolkid(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print('Не найден пользователь')
    except MultipleObjectsReturned:
        print('Найдено больше одного пользователя')
    else:
        return schoolkid


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid):
    chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisement.delete()


def create_commendation(schoolkid_name, subject_name):
    commendations = ['Молодец', 'Отлично', 'Хорошо', 'Гораздо лучше, чем я ожидал',
                     'Ты меня приятно удивил', 'Великолепно', 'Прекрасно',
                     'Ты меня очень обрадовал', 'Именно этого я давно ждал от тебя',
                     'Сказано здорово – просто и ясно',' Ты, как всегда, точен',
                     'Очень хороший ответ', 'Талантливо', 'Ты сегодня прыгнул выше головы',
                     'Я поражен', 'Уже существенно лучше', 'Потрясающе', 'Замечательно', 'Прекрасное начало']
    schoolkid = find_schoolkid(schoolkid_name)
    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                    subject__title=subject_name)[0]
    Commendation.objects.create(text=random.choice(commendations), created=lesson.date,
                                schoolkid=schoolkid, subject=lesson.subject, teacher=lesson.teacher)



