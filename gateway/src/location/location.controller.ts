import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { LocationService } from './location.service';
import { CreateLocationDto } from './dto/create-location.dto';

@Controller('location')
export class LocationController {
  constructor(private readonly locationService: LocationService) {}

  @Post()
  async createLocation(@Body() request: CreateLocationDto) {
    return this.locationService.createLocationFromAiService(request);
  }

  @Post(':name/sync-gis')
  async syncGisData(@Param('name') name: string) {
    return this.locationService.syncGisFeaturesFromAiService(name);
  }

  @Get()
  async getAllLocations() {
    return this.locationService.findAll();
  }

  @Get(':name')
  async getLocationByName(@Param('name') name: string) {
    return this.locationService.findByName(name);
  }
}


