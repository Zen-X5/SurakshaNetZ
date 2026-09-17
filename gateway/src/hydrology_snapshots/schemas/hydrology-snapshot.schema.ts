import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';

export type HydrologySnapshotDocument = HydrologySnapshot & Document;

@Schema({ timestamps: true, collection: 'hydrology_snapshots' })
export class HydrologySnapshot {
    @Prop({ type: Types.ObjectId, ref: 'Location', required: true, index: true })
    locationId: Types.ObjectId;

    @Prop({ type: Types.ObjectId, ref: 'WeatherReading' })
    weatherReadingId?: Types.ObjectId;

    @Prop({ required: true, index: true })
    timestamp: Date;

    @Prop({ required: true })
    rainfallInputMm: number; // P used in the calc

    @Prop({ type: Number, min: 1, max: 3 })
    antecedentMoistureCondition?: number; // 1=dry (AMC I), 2=normal (AMC II), 3=wet (AMC III)

    @Prop({ required: true })
    curveNumberUsed: number;

    @Prop({ required: true })
    runoffDepthQMm: number; // Q = (P - 0.2S)^2 / (P + 0.8S)
}

export const HydrologySnapshotSchema = SchemaFactory.createForClass(HydrologySnapshot);

HydrologySnapshotSchema.index({ locationId: 1, timestamp: -1 });