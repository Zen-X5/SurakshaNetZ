import { Controller } from '@nestjs/common';
import { CitizenReportsService } from './citizen_reports.service';

@Controller('citizen-reports')
export class CitizenReportsController {
  constructor(private readonly citizenReportsService: CitizenReportsService) {}
}
