import { Controller, Get, Param, Post } from '@nestjs/common';
import { LocationService } from './location.service';

@Controller('location')
export class LocationController {
  constructor(private readonly locationService: LocationService) {}

  @Post('seed/jalukbari')
  async seedJalukbari() {
    return this.locationService.seedJalukbari();
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

