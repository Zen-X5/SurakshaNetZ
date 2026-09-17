import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { UserModule } from './user/user.module';
import { AuthModule } from './auth/auth.module';
import { LocationModule } from './location/location.module';
import { WeatherReadingModule } from './weather_reading/weather_reading.module';
import { HydrologySnapshotsModule } from './hydrology_snapshots/hydrology_snapshots.module';
import { HistoricalFloodEventsModule } from './historical_flood_events/historical_flood_events.module';
import { SensorReadingsModule } from './sensor_readings/sensor_readings.module';
import { CitizenReportsModule } from './citizen_reports/citizen_reports.module';
import { PredictionModule } from './prediction/prediction.module';
import { AlertsModule } from './alerts/alerts.module';
import { ConfigModule } from '@nestjs/config';
import { MongooseModule } from '@nestjs/mongoose';
import { SessionModule } from './session/session.module';

@Module({
  imports: [UserModule, AuthModule, LocationModule, WeatherReadingModule, HydrologySnapshotsModule, HistoricalFloodEventsModule, SensorReadingsModule, CitizenReportsModule, PredictionModule, AlertsModule, ConfigModule.forRoot({ isGlobal: true }), MongooseModule.forRoot(process.env.MONGO_URL as string), SessionModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule { }
