from django.db import models

class ModuloIoT(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'En Mantenimiento'),
    ]
    
    empresa = models.ForeignKey(
        'empresas.Empresa', 
        on_delete=models.CASCADE, 
        verbose_name="Empresa"
    )
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Módulo")
    codigo = models.CharField(max_length=100, unique=True, verbose_name="Código del Módulo")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    ubicacion = models.CharField(max_length=200, blank=True, verbose_name="Ubicación")
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='activo',
        verbose_name="Estado"
    )
    fecha_instalacion = models.DateField(null=True, blank=True, verbose_name="Fecha de Instalación")
    ultima_conexion = models.DateTimeField(null=True, blank=True, verbose_name="Última Conexión")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Módulo IoT"
        verbose_name_plural = "Módulos IoT"
        ordering = ['nombre']
       # managed = False # evita que Django intente crear/modificar esta tabla
    
    def __str__(self):
        return f"{self.nombre} - {self.codigo}"


    
class Ruminant(models.Model):
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    ESTADO_PRODUCCION_CHOICES = [
        ('produccion', 'En Producción'),
        ('seca', 'Seca'),
    ]
    
    empresa = models.ForeignKey(
        'empresas.Empresa', 
        on_delete=models.CASCADE, 
        verbose_name="Empresa"
    )
    modulo_iot = models.ForeignKey(
        'ModuloIoT',  # Use string reference to avoid circular import
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Módulo IoT Asignado"
    )
    nombre = models.CharField(max_length=200, blank=True, verbose_name="Nombre")
    codigo = models.CharField(max_length=100, blank=True, verbose_name="Código")
    sexo = models.CharField(
        max_length=10, 
        choices=SEXO_CHOICES, 
        blank=True, 
        verbose_name="Sexo"
    )
    procedencia = models.CharField(max_length=200, blank=True, verbose_name="Procedencia")
    padres = models.CharField(max_length=300, blank=True, verbose_name="Padres")
    raza = models.CharField(max_length=100, blank=True, verbose_name="Raza")
    categoria_reproductiva = models.CharField(max_length=100, blank=True, verbose_name="Categoría Reproductiva")
    categoria_productiva = models.CharField(max_length=100, blank=True, verbose_name="Categoría Productiva")
    fecha_ultimo_parto = models.DateField(null=True, blank=True, verbose_name="Fecha de Último Parto")
    fecha_servicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Servicio")
    fecha_esperada_parto = models.DateField(null=True, blank=True, verbose_name="Fecha Esperada de Parto")
    edad = models.CharField(max_length=50, blank=True, verbose_name="Edad")
    dias_produccion = models.CharField(max_length=50, blank=True, verbose_name="Días de Producción")
    lactancia = models.CharField(max_length=50, blank=True, verbose_name="Lactancia")
    estado_produccion = models.CharField(
        max_length=20, 
        choices=ESTADO_PRODUCCION_CHOICES, 
        blank=True, 
        verbose_name="Estado de Producción"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Ruminant"
        verbose_name_plural = "Ruminants"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.codigo}" if self.nombre else f"Ruminant {self.id}"
    
class IoTData(models.Model):
    modulo_iot = models.ForeignKey(
        'ModuloIoT',
        on_delete=models.CASCADE,
        related_name='iot_data',
        verbose_name="Módulo IoT"
    )
    
    # Core sensor fields (can be null if a reading fails)
    temperatura = models.FloatField(null=True, blank=True, verbose_name="Temperatura (°C)")
    actividad = models.FloatField(null=True, blank=True, verbose_name="Nivel de Actividad")
    latitud = models.FloatField(null=True, blank=True, verbose_name="Latitud")
    longitud = models.FloatField(null=True, blank=True, verbose_name="Longitud")
    
    # Optional metadata
    bateria = models.FloatField(null=True, blank=True, verbose_name="Nivel de Batería (%)")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    raw_data = models.JSONField(default=dict, blank=True, verbose_name="Datos RAW (sin procesar)")
    
    class Meta:
        verbose_name = "Dato IoT"
        verbose_name_plural = "Datos IoT"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.modulo_iot.codigo} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
