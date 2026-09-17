import { Controller } from '@nestjs/common';
import { WeatherReadingService } from './weather_reading.service';

@Controller('weather-reading')
export class WeatherReadingController {
  constructor(private readonly weatherReadingService: WeatherReadingService) {}
}
