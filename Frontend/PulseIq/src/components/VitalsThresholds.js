export const thresholds = {
  glucose: {
    warning: { min: 140, max: 180 },
    danger: { min: 181, max: 999 }
  },

  systolic: {
    warning: { min: 120, max: 139 },
    danger: { min: 140, max: 300 }
  },

  diastolic: {
    warning: { min: 80, max: 89 },
    danger: { min: 90, max: 200 }
  },

  heart_rate: {
    warning: { min: 100, max: 120 },
    danger: { min: 121, max: 300 }
  },

  cholesterol: {
    warning: { min: 200, max: 239 },
    danger: { min: 240, max: 600 }
  },

  spo2: {
    warning: { min: 94, max: 96 },
    danger: { min: 0, max: 93 }
  },

  bmi: {
    warning: { min: 25, max: 29 },
    danger: { min: 30, max: 60 }
  }
};
