import { Controller } from '@nestjs/common';
import { HistoricalFloodEventsService } from './historical_flood_events.service';

@Controller('historical-flood-events')
export class HistoricalFloodEventsController {
  constructor(private readonly historicalFloodEventsService: HistoricalFloodEventsService) {}
}
