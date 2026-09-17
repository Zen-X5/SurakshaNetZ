import { Controller } from '@nestjs/common';
import { SensorReadingsService } from './sensor_readings.service';

@Controller('sensor-readings')
export class SensorReadingsController {
  constructor(private readonly sensorReadingsService: SensorReadingsService) {}
}
