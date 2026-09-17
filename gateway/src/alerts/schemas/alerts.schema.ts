import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';
import { RiskLevel, AlertChannel } from '../../common/enums/flood-system.enum';

export type AlertDocument = Alert & Document;

@Schema({ timestamps: true, collection: 'alerts' })
export class Alert {
    @Prop({ type: Types.ObjectId, ref: 'Location', required: true, index: true })
    locationId: Types.ObjectId;

    @Prop({ type: Types.ObjectId, ref: 'Prediction' })
    predictionId?: Types.ObjectId;

    @Prop({ required: true, default: () => new Date(), index: true })
    timestamp: Date;

    @Prop({ type: String, enum: RiskLevel, required: true })
    riskLevel: RiskLevel;

    @Prop({ type: String, enum: AlertChannel, required: true })
    channel: AlertChannel;

    @Prop({ required: true })
    message: string;

    @Prop({ required: true, default: 1 })
    escalationLevel: number; // 1 = first notice, 2 = escalated, ...

    @Prop({ type: Types.ObjectId, ref: 'CitizenReport' })
    triggeredByReport?: Types.ObjectId;
}

export const AlertSchema = SchemaFactory.createForClass(Alert);

AlertSchema.index({ locationId: 1, timestamp: -1 });