import datetime

import requests
from bs4 import BeautifulSoup


class Game(object):
    def __init__(self, team=None):
        self.url = 'http://www.soccernews.nl/livescore/'

        self.team = team or 'FC Utrecht'
        self.team_lower = self.team.replace(' ', '_').lower()

        self.game_url = None
        self.competition = None
        self.at_home = None
        self.opponent = None
        self.time = None
        self.scores = []

    def check_game_today(self):
        soup = self.get_soup(self.url)
        if soup:
            for g in soup.find_all('div', class_='livescore livescore--off'):
                if self.team_lower in g.find('a')['href']:
                    self.competition = g.find_previous_sibling('h3').text.split(' - ')[0].strip()
                    self.game_url = self.url + g.find('a')['href']
                    return True
        return False

    def get_stats(self):
        soup = self.get_soup(self.game_url)
        if soup:
            # Get opponent and location
            teams = [t.text for t in soup.find_all('h2', class_='score__team-title')]
            self.at_home = True if teams.index(self.team) == 0 else False
            self.opponent = teams[1] if self.at_home else teams[0]

            # Time
            raw_time = list(map(int, soup.find('time', class_='score__date').text.split(' om ')[1].split(':')))
            self.time = datetime.datetime.now().replace(hour=raw_time[0], minute=raw_time[1], second=0)

    def notify_game_today(self):
        game_time = self.time.strftime('%H:%M')
        location = 'thuis' if self.at_home else 'uit'
        message_template = "Ons cluppie moet vandaag om {} {} voetballen tegen {} ({})"
        message = message_template.format(game_time, location, self.opponent, self.competition)
        return message

    def get_score(self):
        soup = self.get_soup(self.game_url)
        if soup:
            for event in soup.find_all('div', class_='livescore'):
                goal = event.find('div', class_='livescore__stand')
                if len(goal.text) and goal.text not in self.scores:
                    self.scores.append(goal.text)
                    time = event.find('div', class_='livescore__position').text.strip()
                    player = event.find('strong')
                    player_name = event.find('strong').text.strip()
                    our_team = ('livescore__player' in player.parent.get('class', '')) == self.at_home
                    if our_team:
                        return self.goal_for_us(goal.text, time, player_name)
                    else:
                        return self.goal_for_them(goal.text, time, player_name)

    def goal_for_us(self, goal, time, player):
        template = 'UUUUUUUU!!!! {} scoort voor {} en de stand is nu {} ({}). UUUUUU!!!'
        return template.format(player, self.team, goal, time)

    def goal_for_them(self, goal, time, player):
        template = 'NEEEE!!!! {} scoort voor {} en de stand is nu {} ({}). SHEMALES!!!'
        return template.format(player, self.opponent, goal, time)

    @staticmethod
    def get_soup(url):
        html = requests.get(url)
        if html.status_code in [200]:
            return BeautifulSoup(html.text, 'html.parser')
        return None

if __name__ == '__main__':
    game = Game(team='Sparta Rotterdam')
    if game.check_game_today():
        game.get_stats()
        message = game.get_score()
