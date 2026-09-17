import { Controller } from '@nestjs/common';
import { HydrologySnapshotsService } from './hydrology_snapshots.service';

@Controller('hydrology-snapshots')
export class HydrologySnapshotsController {
  constructor(private readonly hydrologySnapshotsService: HydrologySnapshotsService) {}
}
