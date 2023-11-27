from os.path import isfile as file_exists, isdir as directory_exists
from os import mkdir, chdir
from helper import get_request, image_link_to_fname
from helper import write_file, read_file, escape_folder_name
from json import loads as json_loads


def mkdir_and_cd(folder):
    mkdir(folder)
    chdir(folder)


json_file = 'chess.json'
download_folder = 'downloaded'
if not file_exists(json_file):
    print('File {} does not exist! Please, generate it by executing chess_json_generator.py'.format(json_file))
    exit()
if directory_exists(download_folder):
    print('Folder {} already exists! Please, remove or rename it before starting the script'.format(download_folder))
    exit()
data = read_file(json_file, 'r', 'UTF-8')
levels = json_loads(data)['levels']
mkdir_and_cd(download_folder)
level_counter = 1
try:
    for level in levels:
        print('Downloading level "{}"...'.format(level['name']))
        mkdir_and_cd('{}. {}'.format(level_counter, escape_folder_name(level['name'])))
        course_counter = 1
        for course in level['courses']:
            print('{}. Course "{}"'.format(course_counter, course['name']))
            mkdir_and_cd('{}. {}'.format(course_counter, escape_folder_name(course['name'])))
            write_file('short_description.txt', 'w', course['short_description'], 'UTF-8')
            write_file('description.txt', 'w', course['description'], 'UTF-8')
            write_file('short_description.txt', 'w', course['short_description'], 'UTF-8')
            write_file(image_link_to_fname(course['image']), 'wb', get_request(course['image'], host='images.chesscomfiles.com').content)
            lessons_len = len(course['lessons'])
            if lessons_len:
                print('Downloading lessons ({}) ...'.format(lessons_len))
                mkdir_and_cd('Lessons')
                lesson_counter = 1
                for lesson in course['lessons']:
                    mkdir_and_cd('{}. {}'.format(lesson_counter, escape_folder_name(lesson['name'])))
                    if lesson.get('image'):
                        write_file(image_link_to_fname(lesson['image']), 'wb', get_request(lesson['image'], host='images.chesscomfiles.com').content)
                    write_file('description.txt', 'w', lesson['description'], 'UTF-8')
                    write_file('video.mp4', 'wb', get_request(lesson['video_url'], host='media.chesscomfiles.com').content)
                    print('Downloaded lesson ({}/{}) "{}" successfully!'.format(lesson_counter, lessons_len, lesson['name']))
                    lesson_counter += 1
                    chdir('..')
                chdir('..')
            print()
            course_counter += 1
            chdir('..')
        print()
        level_counter += 1
        chdir('..')
    chdir('..')
    print('Everything has been downloaded successfully!')
except KeyboardInterrupt:
    print('Download interrupted!')
    exit()
