export enum RiskLevel {
    LOW = 'low',
    MODERATE = 'moderate',
    HIGH = 'high',
    SEVERE = 'severe',
}

export enum ReportSeverity {
    NO_FLOODING = 'no_flooding',
    WATERLOGGING = 'waterlogging',
    MODERATE = 'moderate',
    SEVERE = 'severe',
}

export enum CorroborationStatus {
    UNVERIFIED = 'unverified',
    CORROBORATED = 'corroborated',
    DISPUTED = 'disputed',
}

export enum SensorReadingType {
    WATER_LEVEL = 'water_level',
    RAIN_GAUGE = 'rain_gauge',
    FLOW = 'flow',
    PRESSURE = 'pressure',
}

export enum AlertChannel {
    PUSH = 'push',
    SMS = 'sms',
    DASHBOARD = 'dashboard',
    EMAIL = 'email',
}

export enum UserRole {
    CITIZEN = 'citizen',
    NGO = 'ngo',
    GOVERNMENT = 'government',
    ADMIN = 'admin',
}