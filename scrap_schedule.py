from bs4 import BeautifulSoup


def after_colon(tag):
    return tag.text.split(':', 1)[-1].strip()


def get_slot(slot_div):

    def div_class(clazz):
        return slot_div.find('div', {'class': clazz})

    info_div = div_class('info')
    info = {clazz: after_colon(info_div.find('span', {'class': clazz}))
            for clazz in ['room', 'hour', 'duration']}

    for clazz in ['track', 'title', 'author', 'coauthors']:
        info[clazz] = after_colon(div_class(clazz))

    info['id'] = div_class('more').find('a').attrs['href'].split('/')[-1]

    # get hour by calls attribute
    [hour_attribute] = [c for c in slot_div.attrs['class'] if c.startswith('hour-')]
    hour_in_class = int(hour_attribute[5:])

    hour, minute, second = map(int, info['hour'].split(':'))
    assert (hour, minute, second) == (hour_in_class, 0, 0)

    info['url'] = 'http://schedule.fisl16.softwarelivre.org/#/talk/%s' % info['id']

    return info


def day_slots(day):
    # TODO get from url
    # (with something that processes javascript,
    #  since the DOM is dynamically constructed)
    filename = '%s.html' % day
    with open(filename, 'r') as f:
        content = f.read()
    soup = BeautifulSoup(content)
    rc = soup.find('div', {'class': 'room-column'})
    rc.findAll('header')
    headers = [h.text for h in rc.findAll('div', {'class': 'name'})]
    lines = soup.findAll('div', {'class': 'slot-line'})

    slots = []
    for line in lines:
        line_slots = map(get_slot, line.findAll('div', {'class': 'slot'}))
        line_rooms = {s['room'] for s in line_slots}
        assert len(line_rooms) == 1
        slots += line_slots

    return slots

slots = []
for day in range(8, 12):
    slots += day_slots(day)

tracks = {s['track'] for s in slots}


def search(word):
    return [s for s in slots if word.lower() in s['title'].lower()]


def remove(list):
    for l in list:
        slots.remove(l)
