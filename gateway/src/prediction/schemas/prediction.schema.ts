import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';
import { RiskLevel } from '../../common/enums/flood-system.enum';

export type PredictionDocument = Prediction & Document;

@Schema({ timestamps: true, collection: 'predictions' })
export class Prediction {
    @Prop({ type: Types.ObjectId, ref: 'Location', required: true, index: true })
    locationId: Types.ObjectId;

    @Prop({ required: true, default: () => new Date(), index: true })
    timestamp: Date;

    @Prop({ required: true })
    modelVersion: string; // e.g. 'xgb-v0.3'

    @Prop({ required: true, min: 0, max: 1 })
    riskScore: number; // ML probability

    @Prop({ type: String, enum: RiskLevel, required: true, index: true })
    riskLevel: RiskLevel; // bucketed, possibly overridden by rules

    @Prop({ required: true, default: false })
    ruleOverrideTriggered: boolean;

    @Prop({ type: Object })
    topFeatures?: Record<string, number>;

    @Prop({ type: Types.ObjectId, ref: 'HydrologySnapshot' })
    hydrologySnapshotId?: Types.ObjectId;
}

export const PredictionSchema = SchemaFactory.createForClass(Prediction);

PredictionSchema.index({ locationId: 1, timestamp: -1 });