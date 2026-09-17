import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';
import { ReportSeverity } from '../../common/enums/flood-system.enum';

export type HistoricalFloodEventDocument = HistoricalFloodEvent & Document;

@Schema({ timestamps: true, collection: 'historical_flood_events' })
export class HistoricalFloodEvent {
    @Prop({ type: Types.ObjectId, ref: 'Location', required: true, index: true })
    locationId: Types.ObjectId;

    @Prop({ required: true, index: true })
    eventDate: Date;

    @Prop({ type: Number })
    rainfallMmEstimate?: number;

    @Prop({ type: String, enum: ReportSeverity })
    severity?: ReportSeverity;

    @Prop() // e.g. 'ASDMA report 2022', 'Cloud to Street GFD id'
    sourceReference?: string;

    @Prop({ type: Number, min: 0, max: 1 })
    geocodeConfidence?: number; // how confident we are in the location match

    @Prop()
    notes?: string;
}

export const HistoricalFloodEventSchema = SchemaFactory.createForClass(HistoricalFloodEvent);

HistoricalFloodEventSchema.index({ locationId: 1, eventDate: -1 });