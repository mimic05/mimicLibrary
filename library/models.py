from django.db import models  # type: ignore
from django.utils import timezone  # Import timezone
import datetime
from django.contrib.auth import get_user_model  # Correct import

User = get_user_model()

# For Book model
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    unique_code = models.CharField(max_length=50, unique=True)  # Unique code
    description = models.TextField(null=True, blank=True)  # Allow null values and blank
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# For Transaction model
class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issued_by = models.CharField(max_length=200)
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  # Allow null and blank values
    fine_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.return_date:  # If return_date is not set
            self.return_date = self.issue_date + datetime.timedelta(days=30)  # Set to 30 days from issue_date
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return f"{self.book.title} issued by {self.issued_by}"

class IssuedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Correct ForeignKey usage for User model
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  # Can be null until returned
    fine_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} issued to {self.user.username}"
