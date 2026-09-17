import { Module } from '@nestjs/common';
import { CitizenReportsService } from './citizen_reports.service';
import { CitizenReportsController } from './citizen_reports.controller';

@Module({
  controllers: [CitizenReportsController],
  providers: [CitizenReportsService],
})
export class CitizenReportsModule {}
