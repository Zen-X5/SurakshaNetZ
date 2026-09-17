import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';
import { ReportSeverity, CorroborationStatus } from '../../common/enums/flood-system.enum';

export type CitizenReportDocument = CitizenReport & Document;

@Schema({ _id: false })
export class GeoPoint {
    @Prop({ type: String, enum: ['Point'], required: true, default: 'Point' })
    type: string;

    @Prop({ type: [Number], required: true }) // [lng, lat] — device GPS, not EXIF
    coordinates: number[];
}

@Schema({ timestamps: true, collection: 'citizen_reports' })
export class CitizenReport {
    @Prop({ type: Types.ObjectId, ref: 'User' })
    userId?: Types.ObjectId;

    @Prop({ type: Types.ObjectId, ref: 'Location', index: true })
    locationId?: Types.ObjectId; // nearest matched ward, resolved server-side

    @Prop({ type: GeoPoint, required: true })
    reportedPoint: GeoPoint; // exact device GPS at submission time

    @Prop({ required: true, default: () => new Date(), index: true })
    timestamp: Date;

    @Prop({ required: true })
    imageUrl: string;

    @Prop({ type: String, enum: ReportSeverity })
    classifierSeverity?: ReportSeverity;

    @Prop({ type: Number, min: 0, max: 1 })
    classifierConfidence?: number;

    @Prop({
        type: String,
        enum: CorroborationStatus,
        required: true,
        default: CorroborationStatus.UNVERIFIED,
        index: true,
    })
    corroborationStatus: CorroborationStatus;

    @Prop({ type: [Types.ObjectId], ref: 'CitizenReport', default: [] })
    corroboratedWith: Types.ObjectId[];
}

export const CitizenReportSchema = SchemaFactory.createForClass(CitizenReport);

CitizenReportSchema.index({ reportedPoint: '2dsphere' });
CitizenReportSchema.index({ locationId: 1, timestamp: -1 });