import { IsOptional, IsString, Length } from 'class-validator';

export class CreateLocationDto {
  @IsString()
  @Length(2, 120)
  name = '';

  @IsOptional()
  @IsString()
  @Length(2, 120)
  city?: string;

  @IsOptional()
  @IsString()
  @Length(2, 120)
  state?: string;
}