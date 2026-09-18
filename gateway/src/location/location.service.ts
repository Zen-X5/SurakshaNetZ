import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Location, LocationDocument } from './schemas/location.schema';
import { jalukbariSeedData } from './seeds/jalukbari.seed';

@Injectable()
export class LocationService {
  constructor(
    @InjectModel(Location.name) private readonly locationModel: Model<LocationDocument>,
  ) {}

  async seedJalukbari(): Promise<Location> {
    const existing = await this.locationModel.findOne({ name: 'Jalukbari' }).exec();
    if (existing) {
      return existing;
    }
    const newLocation = new this.locationModel(jalukbariSeedData);
    return newLocation.save();
  }

  async findAll(): Promise<Location[]> {
    return this.locationModel.find().exec();
  }

  async findByName(name: string): Promise<Location | null> {
    return this.locationModel.findOne({ name: new RegExp(name, 'i') }).exec();
  }
}

