from django.db import models
from multiselectfield import MultiSelectField

# Create your models here.

class worker(models.Model):
    code = models.CharField(max_length=20, verbose_name="Codigo", unique=True)
    name = models.CharField(max_length=20, verbose_name="Nombre")

    class Meta:
        ordering = ['name']
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

    def __str__(self):
        return self.name

class design(models.Model):

    gestion_choice = (
        ("Serigrafia", "Serigrafia"),
        ("Sublimacion", "Sublimacion"),
        ("Vinil", "Vinil"),
        ("Vinil Imprim", "Vinil Imprim"),
        ("Bordado", "Bordado"),
        ("Laser", "Laser"),
        ("Bosquejo", "Bosquejo"),
    )

    color_choice = (
        ("Jersey", "Jersey"),
        ("Dryfit", "Dryfit"),
        ("Hidrotech","Hidrotech"),
        ("Algodon Subli.", "Algodon Subli."),
        ("Algodon Chino", "Algodon Chino"),
        ("Adidas", "Adidas"),
    )

    ot = models.CharField(max_length=10, verbose_name = "Orden De Trabajo", unique=True)
    worker = models.ManyToManyField(worker, verbose_name = "Trabajador")
    date = models.DateField(verbose_name = "Fecha")
    houri = models.TimeField(verbose_name = "Hora Inicial")
    hourf = models.TimeField(verbose_name = "Hora Final")
    observations = models.TextField(verbose_name = "Observaciones")
    gestion = MultiSelectField(choices = gestion_choice, verbose_name = "Gestion")
    mts = models.CharField(max_length=10, verbose_name = "Metros")
    color = MultiSelectField(choices = color_choice, verbose_name = "Color")

    class Meta:
        ordering = ['date']
        verbose_name = "Diseño"
        verbose_name_plural = "Diseños"

    def __str__(self):
        return self.ot