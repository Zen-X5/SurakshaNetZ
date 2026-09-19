import { Injectable } from '@nestjs/common';
import { AuthDto } from './dto/auth.dto';
import bcrypt from 'bcrypt';
import { UserService } from '../user/user.service';
import { SessionService } from 'src/session/session.service';

@Injectable()
export class AuthService {
    constructor(private readonly userService: UserService,private readonly sessionService:SessionService) { }

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
        const accessToken = await this.sessionService.findTokenByUserId(newUser._id.toString(),"Browser","SurakshaNetZ")

        return {
            message: 'User registered successfully',
            token: accessToken,
        };
    }
}

