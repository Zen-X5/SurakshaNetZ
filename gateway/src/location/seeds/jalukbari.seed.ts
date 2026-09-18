import { Location } from '../schemas/location.schema';

export const jalukbariSeedData: Partial<Location> = {
  name: 'Jalukbari',
  wardCode: 'WARD-01',
  city: 'Guwahati',
  state: 'Assam',

  // Real GeoJSON boundary polygon surrounding Jalukbari, Gauhati University & AEC campus area
  boundary: {
    type: 'Polygon',
    coordinates: [
      [
        [91.6500, 26.1550],
        [91.6750, 26.1580],
        [91.6820, 26.1400],
        [91.6700, 26.1300],
        [91.6520, 26.1350],
        [91.6500, 26.1550] // Closed ring
      ]
    ]
  },

  // Centroid point near Jalukbari flyover / GU gate
  centroid: {
    type: 'Point',
    coordinates: [91.6628, 26.1445]
  },

  // Hydrological and physical static features of Jalukbari
  staticFeatures: {
    elevationM: 51.2,
    slopeDegrees: 3.5,
    landCoverType: 'Mixed Educational & Wetland Buffer',
    soilType: 'Alluvial Clay Silt',
    imperviousPct: 62,
    distanceToRiverM: 1200, // ~1.2 km from Deepor Beel wetland channel & Brahmaputra
    drainageDensity: 1.65,
    curveNumber: 82,
    potentialRetentionSMm: 55.75, // S = (25400 / 82) - 254
    sourceNotes: 'Initial seed data for Jalukbari locality (ASDMA / ISRO Bhuvan dataset)'
  }
};
