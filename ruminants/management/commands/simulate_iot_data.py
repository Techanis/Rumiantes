from django.core.management.base import BaseCommand
from ruminants.models import IoTData, ModuloIoT
import random
from datetime import datetime

class Command(BaseCommand):
    help = "Genera datos simulados para módulos IoT"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Número de registros por módulo')

    def handle(self, *args, **options):
        count = options['count']
        modulos = ModuloIoT.objects.all()

        if not modulos.exists():
            self.stdout.write(self.style.ERROR("❌ No hay módulos IoT registrados."))
            return

        total = 0
        for modulo in modulos:
            for _ in range(count):
                # Simulate random sensor values
                temperatura = round(random.uniform(35.0, 40.0), 2)
                actividad = round(random.uniform(0, 100), 2)
                latitud = round(random.uniform(-12.1, -12.0), 6)
                longitud = round(random.uniform(-77.1, -77.0), 6)
                bateria = round(random.uniform(30, 100), 1)

                IoTData.objects.create(
                    modulo_iot=modulo,
                    temperatura=temperatura,
                    actividad=actividad,
                    latitud=latitud,
                    longitud=longitud,
                    bateria=bateria,
                    raw_data={
                        "simulated": True,
                        "timestamp": datetime.now().isoformat(),
                    },
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Generados {total} registros IoT simulados para {modulos.count()} módulos."))
