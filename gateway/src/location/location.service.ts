import { Injectable, Logger } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Location, LocationDocument } from './schemas/location.schema';
import { CreateLocationDto } from './dto/create-location.dto';

@Injectable()
export class LocationService {
  private readonly logger = new Logger(LocationService.name);
  private readonly aiServiceUrl = process.env.AI_SERVICE_URL || 'http://localhost:8000';

  constructor(
    @InjectModel(Location.name) private readonly locationModel: Model<LocationDocument>,
  ) {}

  async findAll(): Promise<Location[]> {
    return this.locationModel.find().exec();
  }

  async findByName(name: string): Promise<LocationDocument | null> {
    return this.locationModel.findOne({ name: new RegExp(`^${name}$`, 'i') }).exec();
  }

  async createLocationFromAiService(request: CreateLocationDto): Promise<LocationDocument> {
    return this.fetchAndUpsertGisData(request.name, request.city, request.state);
  }

  /**
   * Connects to Python AI-Service (Port 8000) to fetch live GIS features
   * and syncs them into MongoDB for the specified location.
   */
  async syncGisFeaturesFromAiService(name: string): Promise<LocationDocument | null> {
    return this.fetchAndUpsertGisData(name);
  }

  private async fetchAndUpsertGisData(
    name: string,
    city = 'Guwahati',
    state = 'Assam',
  ): Promise<LocationDocument> {
    try {
      const url = `${this.aiServiceUrl}/api/v1/gis/locations`;
      this.logger.log(`Calling Python AI-Service at: ${url}`);
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, city, state }),
      });
      if (!response.ok) {
        throw new Error(`AI-Service returned HTTP status ${response.status}`);
      }

      const gisData = await response.json();
      this.logger.log(`Received live GIS payload from Python AI-Service for ${name}`);

      const staticFeatures = gisData.static_features || {};
      return this.locationModel.findOneAndUpdate(
        { name: gisData.location_name || name, city: gisData.city || city },
        {
          name: gisData.location_name || name,
          city: gisData.city || city,
          state: gisData.state || state,
          wardCodes: Array.isArray(gisData.ward_codes) ? gisData.ward_codes : [],
          boundary: gisData.boundary,
          centroid: gisData.centroid,
          staticFeatures: {
            elevationM: staticFeatures.elevation_m,
            slopeDegrees: staticFeatures.slope_degrees,
            landCoverType: staticFeatures.land_cover_type,
            soilType: staticFeatures.soil_type,
            imperviousPct: staticFeatures.impervious_pct,
            distanceToRiverM: staticFeatures.distance_to_river_m,
            drainageDensity: staticFeatures.drainage_density,
            curveNumber: staticFeatures.curve_number,
            potentialRetentionSMm: staticFeatures.potential_retention_s_mm,
            sourceNotes: staticFeatures.source || 'Synced from Python AI-Service',
          },
        },
        { new: true, upsert: true, setDefaultsOnInsert: true },
      ).exec() as Promise<LocationDocument>;
    } catch (error: any) {
      this.logger.error(`Failed to sync with Python AI-Service: ${error.message}`);
      throw error;
    }
  }

}



