import { Module } from '@nestjs/common';
import { WeatherReadingService } from './weather_reading.service';
import { WeatherReadingController } from './weather_reading.controller';

@Module({
  controllers: [WeatherReadingController],
  providers: [WeatherReadingService],
})
export class WeatherReadingModule {}
