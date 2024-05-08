from django.db import models

# Create your models here.

class Record(models.Model):  
    company_name = models.CharField(max_length=100,null=False,blank=False)  
    email = models.EmailField()  
    company_code = models.CharField(max_length=100,null=False,blank=False) 
    strength = models.CharField(max_length=100,null=False,blank=False)
    website = models.CharField(max_length=100,null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True,null=False,blank=False)
    
    class Meta:  
        db_table = "company_record_table"