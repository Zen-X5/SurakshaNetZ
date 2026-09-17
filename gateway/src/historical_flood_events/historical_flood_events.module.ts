import { Module } from '@nestjs/common';
import { HistoricalFloodEventsService } from './historical_flood_events.service';
import { HistoricalFloodEventsController } from './historical_flood_events.controller';

@Module({
  controllers: [HistoricalFloodEventsController],
  providers: [HistoricalFloodEventsService],
})
export class HistoricalFloodEventsModule {}
