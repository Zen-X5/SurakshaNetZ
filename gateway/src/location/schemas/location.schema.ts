import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';

export type LocationDocument = Location & Document;

@Schema({ _id: false })
export class GeoPolygon {
    @Prop({ type: String, enum: ['Polygon'], required: true, default: 'Polygon' })
    type: string;

    @Prop({ type: [[[Number]]], required: true })
    coordinates: number[][][];
}

@Schema({ _id: false })
export class GeoPoint {
    @Prop({ type: String, enum: ['Point'], required: true, default: 'Point' })
    type: string;

    @Prop({ type: [Number], required: true })
    coordinates: number[];
}

@Schema({ _id: false })
export class StaticFeatures {
    @Prop({ type: Number })
    elevationM?: number;

    @Prop({ type: Number })
    slopeDegrees?: number;

    @Prop({ type: String })
    landCoverType?: string;

    @Prop({ type: String })
    soilType?: string;

    @Prop({ type: Number, min: 0, max: 100 })
    imperviousPct?: number;

    @Prop({ type: Number })
    distanceToRiverM?: number;

    @Prop({ type: Number })
    drainageDensity?: number;

    @Prop({ type: Number })
    curveNumber?: number;

    @Prop({ type: Number })
    potentialRetentionSMm?: number; // S = (25400 / CN) - 254, precomputed

    @Prop({ type: String })
    sourceNotes?: string;
}

@Schema({ timestamps: true, collection: 'locations' })
export class Location {
    @Prop({ required: true })
    name: string; // e.g. 'Beltola', 'Six Mile'

    @Prop()
    wardCode?: string;

    @Prop({ required: true, default: 'Guwahati' })
    city: string;

    @Prop({ required: true, default: 'Assam' })
    state: string;

    @Prop({ type: GeoPolygon, required: true })
    boundary: GeoPolygon;

    @Prop({ type: GeoPoint, required: true })
    centroid: GeoPoint;

    @Prop({ type: StaticFeatures, default: {} })
    staticFeatures: StaticFeatures;
}

export const LocationSchema = SchemaFactory.createForClass(Location);

LocationSchema.index({ boundary: '2dsphere' });
LocationSchema.index({ centroid: '2dsphere' });
LocationSchema.index({ name: 1, city: 1 });