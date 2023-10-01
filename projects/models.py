from django.db import models
import uuid
from users.models import Profile

class Project(models.Model):
    class Meta:
        ordering = ["-vote_ratio", "-vote_total", "title"]
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.URLField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tag", blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list("owner__id", flat=True)
        return queryset
    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value="up").count()
        totalVotes = reviews.count()
        ratio = (upVotes/totalVotes) *100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    class Meta:
        unique_together = [["owner", "project"]]
        ordering = ["created"]
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote"),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=4, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return f"{self.project.title} - {self.owner.name} - {self.value}"


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

