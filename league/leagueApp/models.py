from django.db import models

class League(models.Model):
    name = models.CharField(max_length=100)
    # teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    # league = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    position = models.CharField(max_length=50)
    goals = models.IntegerField(default=0)
    
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
    class EventType(models.TextChoices):
        GOL = "GOL"
        AUTOGOL = "AUTOGOL"
        FALTA = "FALTA"
        PENALTY = "PENALTY"
        MANS = "MANS"
        CESSIO = "CESSIO"
        FORA_DE_JOC = "FORA_DE_JOC"
        ASSISTENCIA = "ASSISTENCIA"
        TARGETA_GROGA = "TARGETA_GROGA"
        TARGETA_VERMELLA = "TARGETA_VERMELLA"
    
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    time = models.TimeField()
    event_type = models.CharField(max_length=30,choices=EventType.choices)
    player = models.ForeignKey(Player,null=True,
                    on_delete=models.SET_NULL,
                    related_name="events_fets")
    team = models.ForeignKey(Team,null=True,
                    on_delete=models.SET_NULL)
    
    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        if self.event_type == 'GOL':
            if self.team == self.match.home_team:
                self.match.home_score += 1
                self.match.save()
            elif self.team == self.match.away_team:
                self.match.away_score += 1
                self.match.save()

# class Event(models.Model):
#     match = models.ForeignKey(Match, on_delete=models.CASCADE)
#     player = models.ForeignKey(Player, on_delete=models.CASCADE)
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     event_type = models.CharField(max_length=50, default='goal')
#     time = models.TimeField()

#     def __str__(self):
#         if self.event_type == 'goal':
#             return f'{self.time} - {self.player.name} ({self.team.name}) scored a goal in {self.match}'
#         else:
#             return f'{self.time} - {self.player.name} ({self.team.name}) {self.event_type} in {self.match}'

