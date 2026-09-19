import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document, Types } from 'mongoose';
import { UserRole } from '../../common/enums/flood-system.enum';

export type UserDocument = User & Document;

@Schema({ _id: false })
export class NotificationPrefs {
    @Prop({ default: true })
    push!: boolean;

    @Prop({ default: false })
    sms!: boolean;

    @Prop({ default: false })
    email!: boolean;
}

@Schema({ timestamps: true, collection: 'users' })
export class User {
    @Prop({ type: String, enum: UserRole, required: true, default: UserRole.CITIZEN })
    role!: UserRole;

    @Prop()
    displayName?: string;

    @Prop({ index: true, sparse: true, unique: true })
    phoneNumber?: string;

    @Prop({ index: true, sparse: true, unique: true, lowercase: true })
    email?: string;

    @Prop({ type: Types.ObjectId, ref: 'Location' })
    xhomeLocationId?: Types.ObjectId;

    @Prop({ type: NotificationPrefs, default: {} })
    notificationPrefs!: NotificationPrefs;

    @Prop({ select: false })
    passwordHash?: string;
}

export const UserSchema = SchemaFactory.createForClass(User);