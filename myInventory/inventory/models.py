from django.db import models

# Create your models here.

class product(models.Model):

    # def __init__(self, sku_id, name, mrp, exp_date, qty):
    #     self.sku_id = sku_id
    #     self.name = name
    #     self.mrp = mrp
    #     self.qty = qty
    #     self.exp_date = exp_date

    sku_id = models.IntegerField()
    name = models.CharField(max_length=200)
    mrp = models.DecimalField(max_digits=8, decimal_places=2)
    exp_date = models.DateField()
    qty = models.IntegerField()
