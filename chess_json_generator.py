from lxml import html
from re import sub as re_sub
from helper import get_request
from json import loads as json_loads, dump as json_dump


try:
    response = get_request('https://www.chess.com/lessons/guide')
    tree = html.fromstring(response.text)
    level_components = tree.xpath('.//div[contains(@id, "panel-guide")] //div[contains(@class, "level-component")]')
    data = {'levels': []}
    len_levels = len(level_components)
    done_level_count = 0
    print(f'Found {len_levels} levels!')
    for lc in level_components:
        lc_name = re_sub(r' {2,}', ' ', lc.xpath('.//h2')[0].text_content().replace('\n', '').strip())
        lc_courses = [{
            'name': course.xpath('.//h3[contains(@class, "course-title")]')[0].text_content().strip(),
            'short_description': course.xpath('.//p[contains(@class, "course-desc")]')[0].text_content().strip(),
            'link': course.xpath('.//a')[0].attrib['href'],
        } for course in lc.xpath('.//div[contains(@class, "course-component")]')]
        for i in range(len(lc_courses)):
            course_tree = html.fromstring(get_request(lc_courses[i]['link']).text)
            lc_courses[i]['image'] = course_tree.xpath('//img[contains(@class, "course-header-image")]')[0].attrib['src']
            lc_courses[i]['description'] = course_tree.xpath('//div[contains(@class, "course-header-description")]')[0].text_content().strip()
            lessons = []
            lessons_els = course_tree.xpath('//div[contains(@class, "lesson-component") or contains(@class, "lesson-board-preview-component")]')
            for lesson_el in lessons_els:
                lesson = {
                    'name': lesson_el.xpath('.//div[contains(@class, "lesson-content")] //h3')[0].text_content().strip(),
                    'link': lesson_el.xpath('.//div[contains(@class, "lesson-content")] //h3/a')[0].attrib['href'],
                }
                image = lesson_el.xpath('.//img[contains(@class, "lesson-preview-img")]')
                if len(image):
                    lesson['image'] = image[0].attrib['data-src']
                lessons.append(lesson)
            for j in range(len(lessons)):
                lesson_tree = html.fromstring(get_request(lessons[j]['link']).text)
                lesson_data = json_loads(lesson_tree.xpath('//div[contains(@id, "lessons-upgrade-modal")]')[0].attrib['data-lesson'])
                lessons[j]['description'] = lesson_data['description']
                lessons[j]['video_url'] = lesson_data['video_url']
            lc_courses[i]['lessons'] = lessons
        data['levels'].append({
            'name': lc_name,
            'courses': lc_courses,
        })
        done_level_count += 1
        print(f'Level {done_level_count}/{len_levels} done')
    print('Generating json...')
    with open('chess.json', 'w', encoding='UTF-8') as outfile: 
        json_dump(data, outfile, indent=4, ensure_ascii=False)
    print('chess.json generated successfully!')
except KeyboardInterrupt:
    print('JSON generation interrupted!')
    exit()