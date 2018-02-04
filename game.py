import requests
from bs4 import BeautifulSoup


class Game(object):
    def __init__(self, team=None):
        self.url = 'http://www.soccernews.nl/livescore/'

        self.team = team or 'FC utrecht'
        self.team_lower = self.team.replace(' ', '_').lower()

        self.game_url = None
        self.at_home = None
        self.opponent = None

    def check_game_today(self):
        soup = self.get_soup(self.url)
        if soup:
            for g in soup.find_all('div', class_='livescore__result'):
                if self.team_lower in g.find('a')['href']:
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


    @staticmethod
    def get_soup(url):
        html = requests.get(url)
        if html.status_code in [200]:
            return BeautifulSoup(html.text, 'html.parser')
        return None


if __name__ == '__main__':
    game = Game()
    if game.check_game_today():
        game.get_stats()
