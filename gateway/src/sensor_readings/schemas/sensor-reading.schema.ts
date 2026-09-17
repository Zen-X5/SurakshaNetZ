import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';
import { SensorReadingType } from '../../common/enums/flood-system.enum';

export type SensorReadingDocument = SensorReading & Document;

@Schema({ timestamps: true, collection: 'sensor_readings' })
export class SensorReading {
    @Prop({ required: true, index: true })
    sensorId: string; // device identifier (ESP32 MAC/id, or 'sim-01')

    @Prop({ type: Types.ObjectId, ref: 'Location', required: true, index: true })
    locationId: Types.ObjectId;

    @Prop({ required: true, index: true })
    timestamp: Date;

    @Prop({ type: String, enum: SensorReadingType, required: true })
    readingType: SensorReadingType;

    @Prop({ required: true })
    value: number; // cm for water_level, mm for rain_gauge, etc.

    @Prop({ required: true })
    unit: string;

    @Prop({ required: true, default: true })
    isSimulated: boolean;

    @Prop({ required: true, default: false })
    faultFlag: boolean;
}

export const SensorReadingSchema = SchemaFactory.createForClass(SensorReading);

SensorReadingSchema.index({ locationId: 1, timestamp: -1 });
SensorReadingSchema.index({ sensorId: 1, timestamp: -1 });