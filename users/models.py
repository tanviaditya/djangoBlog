from django.db import models
from django.contrib.auth.models import User

from PIL import Image
# Create your models here.

class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	image=models.ImageField(default='default.jpg',upload_to='profile_pics')
	firstname=models.CharField(max_length=10,default='First name')
	lastname=models.CharField(max_length=10,default='Last name')
	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self ,*args, **kwargs):
		#overiding self method
		super().save()
		img=Image.open(self.image.path)
		if img.height >300 or img.width >300:
			output_size=(300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)

class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='follower',on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following',on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
        )