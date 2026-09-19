import { Injectable } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { User, UserDocument } from './schemas/user.schema';
import { SessionService } from 'src/session/session.service';

@Injectable()
export class UserService {
    constructor(@InjectModel(User.name) private userModel: Model<User>) { }

    async createUser(payload: CreateUserDto): Promise<UserDocument> {
        const newPayload = {
            displayName: payload.displayName,
            phoneNumber: payload.phoneNumber,
            email: payload.email,
            passwordHash: payload.password
        }
        const newUser = new this.userModel(newPayload);
        return await newUser.save();
    }

    async findUserById(userId: string) {
        return this.userModel.findById(userId);
    }
    
    async findUserByEmail(email: string) {
        return this.userModel.findOne({ email });
    }

    async findUserByResetToken(token: string) {
        return this.userModel.findOne({ resetPasswordToken: token });
    }
}
