DRIVER_PATH = 'absolute/path/to/your/chromedriver'
MOOC_ADDRESS = 'http://i.mooc.mooc.whu.edu.cn/'
DOUBLE_RATE = True
IMPLICITLY_WAIT = 5

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from time import sleep

to_zh = {
    '{}': '{}',
    'Please login and then press enter.': '请登录并在此之后按下回车',
    '{} courses found in total:': '共发现{}门课程：',
    '({}): {}': '({}): {}',
    'Press the index of the course to be finished:': '请输入目标课程的序号：',
    'The selected course has been finished.': '已成功刷完选定课程',
    'Handling {0} taught by {1}': '正在处理{0}, {1}...',
    '{0} taught by {1}': '{0}, {1}',
    '{} lessons found in total:': '共发现{}节未完成章节：',
    'Currently working on {}...': '正在处理{}...',
    'Done.': '完毕',
    'Skipped.': '非视频章节，跳过',
}

def output(content, *args, wait = False):
    content = to_zh[content].format(*args)
    return input(content) if wait else print(content)

class Lesson:
    def __init__(self, name, link, driver):
        self.name = name
        self.link = link
        self.driver = driver
    
    def __repr__(self):
        return 'Lesson({}, {})'.format(*map(repr, (self.name, self.link)))
    
    def __str__(self):
        return self.name

    def handle(self):
        driver = self.driver
        driver.get(self.link)
        driver.switch_to.frame('iframe')
        driver.switch_to.frame(0)

        if not driver.find_elements(By.CSS_SELECTOR, '#video_html5_api'):
            return False

        driver.find_element(By.CSS_SELECTOR, 'button[class="vjs-big-play-button"]').click()
        if DOUBLE_RATE:
            for _ in range(3):
                driver.find_element(By.CSS_SELECTOR, '.vjs-playback-rate.vjs-menu-button.vjs-menu-button-popup.vjs-button[type="button"]').click()

        while not driver.find_elements(By.CSS_SELECTOR, '.video-js.vjs-ended'):
            sleep(20)
        return True

class Course:
    def __init__(self, course_name, course_teacher, link, driver):
        self.course_name = course_name
        self.course_teacher = course_teacher
        self.link = link
        self.driver = driver
    
    def __repr__(self):
        return 'Course({}, {}, {})'.format(*map(repr, (self.course_name, self.course_teacher, self.link)))
    
    def __str__(self):
        return to_zh['{0} taught by {1}'].format(self.course_name, self.course_teacher)
    
    def handle(self):
        output('Handling {0} taught by {1}', self.course_name, self.course_teacher)
        driver = self.driver
        driver.get(self.link)
        
        lessons = list(map(lambda ele:element_to_lesson(ele, driver), filter(is_locked, driver.find_elements(By.CSS_SELECTOR, '.leveltwo > .clearfix > a'))))
        
        output('{} lessons found in total:', len(lessons))
        for lesson in lessons:
            output('{}', lesson)
        for lesson in lessons:
            output('Currently working on {}...', lesson)
            if lesson.handle():
                output('Done.')
            else:
                output('Skipped.')

def is_locked(element):
    return element.find_element(By.CSS_SELECTOR, '.icon > em').get_attribute('class')=='orange'

def element_to_lesson(element, driver):
    return Lesson(element.get_attribute('aria-label'), element.get_attribute('href'), driver)

def element_to_course(web_element, driver):
    link = web_element.find_element(By.CSS_SELECTOR, '.inlineBlock > a').get_attribute('href')
    course_name = web_element.find_element(By.CSS_SELECTOR, '.inlineBlock > a > .course-name').get_attribute('title')
    course_teacher = web_element.find_element(By.CSS_SELECTOR, '.line2:nth-of-type(2)').get_attribute('title')
    return Course(course_name, course_teacher, link, driver)

def run():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--mute-audio")

    wd = webdriver.Chrome(options=options, service=Service(DRIVER_PATH))
    wd.implicitly_wait(IMPLICITLY_WAIT)
    wd.get(MOOC_ADDRESS)
    output('Please login and then press enter.', wait = True)

    wd.switch_to.frame('frame_content')
    if wd.find_element(By.CSS_SELECTOR, '.tab-item.current').get_attribute('coursetype') == '0':
        wd.find_element(By.CSS_SELECTOR, '.tab-item[coursetype="1"]').click()
    courses = list(map(lambda ele:element_to_course(ele, wd), wd.find_elements(By.CSS_SELECTOR, '.content .course > .course-info')))

    output('{} courses found in total:', len(courses))
    for i in range(len(courses)):
        output('({}): {}', i + 1, courses[i])
    
    while True:
        courses[int(output('Press the index of the course to be finished:', wait=True)) - 1].handle()
        output('The selected course has been finished.')

if __name__ == '__main__':
    run()