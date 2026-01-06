from django.db import models

class AccessLog(models.Model):

    card_id = models.CharField(max_length=50, help_text="Unique card identifier")
    door_name = models.CharField(max_length=100, help_text="Name of the door")
    access_granted = models.BooleanField(help_text="Whether access was granted")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When the log was created")
    
    class Meta:
        ordering = ['-timestamp'] 
        
    def __str__(self):
        status = "GRANTED" if self.access_granted else "DENIED"
        return f"{self.card_id} - {self.door_name} - {status}"