import subprocess
from datetime import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AccessLog

@receiver(post_save, sender=AccessLog)
def log_access_creation(sender, instance, created, **kwargs):
    """
    Signal handler that logs when a new AccessLog is created
    Writes to system_events.log using subprocess
    """
    if created:  
        status = "GRANTED" if instance.access_granted else "DENIED"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] - CREATE: Access log created for card {instance.card_id}. Status: {status}.\n"
        
        try:
            subprocess.run(
                ['cmd', '/c', f'echo {log_message} >> system_events.log'],
                shell=False,
                check=True
            )
        except:
            try:
                subprocess.run(
                    ['sh', '-c', f'echo "{log_message}" >> system_events.log'],
                    shell=False,
                    check=True
                )
            except Exception as e:
                print(f"Error writing to log: {e}")


@receiver(post_delete, sender=AccessLog)
def log_access_deletion(sender, instance, **kwargs):
    """
    Signal handler that logs when an AccessLog is deleted
    Writes to system_events.log using subprocess
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] - DELETE: Access log (ID: {instance.id}) for card {instance.card_id} was deleted.\n"
    
    try:
        subprocess.run(
            ['cmd', '/c', f'echo {log_message} >> system_events.log'],
            shell=False,
            check=True
        )
    except:
        try:
            subprocess.run(
                ['sh', '-c', f'echo "{log_message}" >> system_events.log'],
                shell=False,
                check=True
            )
        except Exception as e:
            print(f"Error writing to log: {e}")