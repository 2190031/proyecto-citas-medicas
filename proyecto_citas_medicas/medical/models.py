from django.db import models

# Create your models here.
class Seguro(models.Model):
    id_seg = models.AutoField(primary_key=True)
    nom_seg = models.CharField(max_length=30)
    tarifa_seg = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.nom_seg)
    
class Paciente(models.Model):
    id_pac = models.AutoField(primary_key=True)
    nom_pac = models.CharField(max_length=60)
    edad_pac = models.SmallIntegerField()
    sexo_pac = models.CharField(max_length=2) # M, F, MF, FM
    email_pac = models.CharField(max_length=254)
    dni_pac = models.CharField(max_length=11) # No guiones
    tel_per_pac = models.CharField(max_length=11) # No guiones
    tel_dom_pac = models.CharField(max_length=11, null=True) # No guiones
    id_seg = models.ForeignKey(Seguro, on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nom_pac} ({self.email_pac})"
        
class Secretaria(models.Model):
    id_sec = models.AutoField(primary_key=True)
    nom_sec = models.CharField(max_length=60)
    email_sec = models.CharField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.nom_sec)
    
class Especialidad(models.Model):
    id_espec = models.AutoField(primary_key=True)
    nom_espec = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.nom_espec)
    
class Doctor(models.Model):
    id_doc = models.AutoField(primary_key=True)
    nom_doc = models.CharField(max_length=60)
    consult_doc = models.CharField(max_length=30)
    tarifa_doc = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.nom_doc)
    
    
class Doctor_Especialidad(models.Model):
    id_espec = models.ForeignKey(Especialidad, on_delete=models.RESTRICT)
    id_doc = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    
class Doctor_Secretaria(models.Model):
    id_doc = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    id_sec = models.ForeignKey(Secretaria, on_delete=models.RESTRICT)
    
    
class Usuario(models.Model):
    id_usu = models.AutoField(primary_key=True)
    email_usu = models.CharField(max_length=254)
    pass_usu = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
class Usuario_Paciente(models.Model):
    is_usu_pac = models.AutoField(primary_key=True)
    id_usu = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    id_pac = models.ForeignKey(Paciente, on_delete=models.RESTRICT) 
    
    def __str__(self):
        return f"{self.id_pac} - {self.id_pac.email_pac}"
    
class Usuario_Secretaria(models.Model):
    is_usu_sec = models.AutoField(primary_key=True)
    id_usu = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    id_sec = models.ForeignKey(Secretaria, on_delete=models.RESTRICT)
    
    def __str__(self):
        return f"{self.id_sec} - {self.id_sec.email_sec}"

class Cita(models.Model):
    id_sol = models.AutoField(primary_key=True)
    fecha_sol = models.DateField()
    motivo_sol = models.TextField(null=True)
    estado_sol = models.SmallIntegerField(choices=(
        (0, "Pendiente"),
        (1, "Confirmada"),
        (2, "Finalizada")
        ))
    is_doc = models.ForeignKey(Doctor, on_delete=models.RESTRICT)
    is_usu_pac = models.ForeignKey(Usuario_Paciente, on_delete=models.RESTRICT)
    is_usu_sec = models.ForeignKey(Usuario_Secretaria, on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    