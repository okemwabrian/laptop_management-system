from django.db import models

class Laptop(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField()  # Detailed description of the laptop
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the laptop
    stock = models.PositiveIntegerField()  # Stock quantity
    image = models.ImageField(upload_to='laptops/', null=True, blank=True)  # Image field for laptop

    def __str__(self):
        return f"{self.brand} {self.model}"

class Sale(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)  # Linking sale to a specific laptop
    customer_name = models.CharField(max_length=100)  # Customer's name
    date = models.DateTimeField(auto_now_add=True)  # Date and time of the sale
    quantity = models.PositiveIntegerField()  # Quantity of laptops sold

    def __str__(self):
        return f"Sale of {self.laptop} to {self.customer_name}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)  # Name of the person sending the message
    email = models.EmailField()  # Email address of the person sending the message
    message = models.TextField()  # Message content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the message was created

    def __str__(self):
        return f"{self.name} - {self.email}"

