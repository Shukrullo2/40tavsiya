from django.db import models
from django.contrib.auth.models import User
import uuid
import re
# Create your models here.

class Writer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    # profile_pic = models.ImageField(null=True, blank=True, 
                                    # upload_to="profiles/", 
                                    # default="profiles/default.jpg")
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.CharField(max_length=100, null=True, blank=True)
    # phone_number = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('username', 'twitter')
        
    def __str__(self):
        return self.username or "Unnamed Writer"

class Hack(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, null=True, blank=True, related_name="hack")
    body = models.TextField(max_length=500, null=True, blank=True)
    upvote = models.IntegerField(default=0, null=True, blank=True)
    downvote = models.IntegerField(default=0, null=True, blank=True)
    vote_net = models.IntegerField(default=0, null=True, blank=True)
    comment_count = models.IntegerField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id and self.body:
            clean_text = re.sub(r'[^\w\s]', '', self.body)
            words = clean_text.split()[:10]
            self.id = '-'.join(words).lower()
        super().save(*args, **kwargs)

    @property
    def getVotes(self):
        vote_net = self.upvote - self.downvotes
        self.vote_net = vote_net
        self.save()

    @property
    def countComments(self):
        comments = self.comments.all()
        return comments.count()

    def __str__(self) -> str:
        return self.body[:20]

class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    hack = models.ForeignKey(Hack, on_delete=models.CASCADE, null=True, related_name="comments")
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, 
                               null=True, blank=True, related_name="comment")
    body = models.TextField(max_length=500, null=True, blank=True)
    upvote = models.IntegerField(default=0, null=True, blank=True)
    downvote = models.IntegerField(default=0, null=True, blank=True)
    vote_net = models.IntegerField(default=0, null=True, blank=True)
    reply_count = models.IntegerField(default=0, null=True, blank=True)
    @property
    def getVotes(self):
        votes = self.commentvote_set.all()
        upVotes = votes.filter(value='up').count()
        downVotes = votes.filter(value='down').count()
        vote_net = upVotes - downVotes
        

        self.upvote = upVotes
        self.downvote = downVotes
        self.vote_net= vote_net
        self.save()
        print(upVotes, downVotes, vote_net)
    
    @property
    def countReplies(self):
        replies = self.replies.all()
        return replies.count()

        

    def __str__(self) -> str:
        return self.body[:20]

class Reply(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, 
                                null=True, related_name="replies")
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, 
                               null=True, blank=True, related_name="reply")
    body = models.TextField(max_length=500, null=True, blank=True)
    upvote = models.IntegerField(default=0, null=True, blank=True)
    downvote = models.IntegerField(default=0, null=True, blank=True)
    vote_net = models.IntegerField(default=0, null=True, blank=True)
    @property
    def getVotes(self):
        
        vote_net = self.upvote - self.downvotes

        self.vote_net= vote_net
        self.save()
        # print(upVotes, downVotes, vote_net)

    def __str__(self) -> str:
        return self.body[:20]

class Report(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    hack = models.ForeignKey(Hack, on_delete=models.CASCADE, 
                             null=True, related_name="report")

# r