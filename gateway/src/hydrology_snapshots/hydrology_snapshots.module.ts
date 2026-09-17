import { Module } from '@nestjs/common';
import { HydrologySnapshotsService } from './hydrology_snapshots.service';
import { HydrologySnapshotsController } from './hydrology_snapshots.controller';

@Module({
  controllers: [HydrologySnapshotsController],
  providers: [HydrologySnapshotsService],
})
export class HydrologySnapshotsModule {}
