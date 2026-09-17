import { Module } from '@nestjs/common';
import { SensorReadingsService } from './sensor_readings.service';
import { SensorReadingsController } from './sensor_readings.controller';

@Module({
  controllers: [SensorReadingsController],
  providers: [SensorReadingsService],
})
export class SensorReadingsModule {}
