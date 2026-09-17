import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';

export type WeatherReadingDocument = WeatherReading & Document;

@Schema({ timestamps: true, collection: 'weather_readings' })
export class WeatherReading {
    @Prop({ type: Types.ObjectId, ref: 'Location', required: true, index: true })
    locationId: Types.ObjectId;

    @Prop({ required: true, index: true })
    timestamp: Date;

    @Prop({ type: Number })
    rainfallMm?: number;

    @Prop({ type: Number })
    forecastRainfallMm?: number;

    @Prop({ type: Number })
    cumulative1hMm?: number;

    @Prop({ type: Number })
    cumulative3hMm?: number;

    @Prop({ type: Number })
    cumulative6hMm?: number;

    @Prop({ type: Number })
    cumulative24hMm?: number;

    @Prop({ type: Number })
    temperatureC?: number;

    @Prop({ type: Number })
    humidityPct?: number;

    @Prop({ type: Number })
    windSpeedKmph?: number;

    @Prop({ required: true, default: 'openweather' })
    source: string;
}

export const WeatherReadingSchema = SchemaFactory.createForClass(WeatherReading);

WeatherReadingSchema.index({ locationId: 1, timestamp: -1 });