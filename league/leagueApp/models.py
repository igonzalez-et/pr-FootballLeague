from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    league = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    position = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    date = models.DateField()
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    
    def __str__(self):
        return f'{self.home_team} vs {self.away_team}'


class Event(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, default='goal')
    time = models.TimeField()
    
    def __str__(self):
        return f'{self.event_type} - {self.player} ({self.team})'
