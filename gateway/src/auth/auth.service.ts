import { Injectable } from '@nestjs/common';
import { AuthDto } from './dto/auth.dto';
import bcrypt from 'bcrypt';
import { UserService } from '../user/user.service';

@Injectable()
export class AuthService {
    constructor(private readonly userService: UserService) { }

    async register(payload: AuthDto) {
        const saltRounds = 10;
        const hashPassword = await bcrypt.hash(payload.password, saltRounds);

        const newPayload = {
            displayName: payload.displayName,
            email: payload.email,
            phoneNumber: payload.phoneNumber,
            password: hashPassword
        };

        const newUser = await this.userService.createUser(newPayload);

        return {
            message: 'User registered successfully',
            user: newUser,
        };
    }
}

