# Readme

## Explenation of variables

### KNMI Weather Variables

| Variable | Description | Unit |
|----------|-------------|------|
| YYYYMMDD | Date (Year-Month-Day) | - |
| DDVEC | Vector mean wind direction (360=north, 90=east, 180=south, 270=west, 0=calm/variable) | degrees |
| FHVEC | Vector mean windspeed | 0.1 m/s |
| FG | Daily mean windspeed | 0.1 m/s |
| FHX | Maximum hourly mean windspeed | 0.1 m/s |
| FHXH | Hourly division in which FHX was measured | hour |
| FHN | Minimum hourly mean windspeed | 0.1 m/s |
| FHNH | Hourly division in which FHN was measured | hour |
| FXX | Maximum wind gust | 0.1 m/s |
| FXXH | Hourly division in which FXX was measured | hour |
| TG | Daily mean temperature | 0.1 °C |
| TN | Minimum temperature | 0.1 °C |
| TNH | Hourly division in which TN was measured | hour |
| TX | Maximum temperature | 0.1 °C |
| TXH | Hourly division in which TX was measured | hour |
| T10N | Minimum temperature at 10 cm above surface | 0.1 °C |
| T10NH | 6-hourly division in which T10N was measured (6=0-6 UT, 12=6-12 UT, 18=12-18 UT, 24=18-24 UT) | 6-hour period |
| SQ | Sunshine duration calculated from global radiation (-1 for <0.05 hour) | 0.1 hour |
| SP | Percentage of maximum potential sunshine duration | % |
| Q | Global radiation | J/cm² |
| DR | Precipitation duration | 0.1 hour |
| RH | Daily precipitation amount (-1 for <0.05 mm) | 0.1 mm |
| RHX | Maximum hourly precipitation amount (-1 for <0.05 mm) | 0.1 mm |
| RHXH | Hourly division in which RHX was measured | hour |
| PG | Daily mean sea level pressure calculated from 24 hourly values | 0.1 hPa |
| PX | Maximum hourly sea level pressure | 0.1 hPa |
| PXH | Hourly division in which PX was measured | hour |
| PN | Minimum hourly sea level pressure | 0.1 hPa |
| PNH | Hourly division in which PN was measured | hour |
| VVN | Minimum visibility (0: <100m, 1:100-200m, ..., 50:5-6km, ..., 89: >70km) | coded scale |
| VVNH | Hourly division in which VVN was measured | hour |
| VVX | Maximum visibility (0: <100m, 1:100-200m, ..., 50:5-6km, ..., 89: >70km) | coded scale |
| VVXH | Hourly division in which VVX was measured | hour |
| NG | Mean daily cloud cover (in octants, 9=sky invisible) | octants (0-9) |
| UG | Daily mean relative atmospheric humidity | % |
| UX | Maximum relative atmospheric humidity | % |
| UXH | Hourly division in which UX was measured | hour |
| UN | Minimum relative atmospheric humidity | % |
| UNH | Hourly division in which UN was measured | hour |
| EV24 | Potential evapotranspiration (Makkink) | 0.1 mm |

### KNMI Precipitation and Snow Cover Variables

| Variable | Description | Unit |
|----------|-------------|------|
| STN | Station number | - |
| YYYYMMDD | Date (Year-Month-Day) | - |
| RD | 24-hour precipitation sum from 08:00 UTC previous day to 08:00 UTC current day | 0.1 mm |
| SX | Code for snow cover at 08:00 UTC | coded scale |

#### Snow Cover Codes (SX)

| Code | Snow Cover Description |
|------|------------------------|
| 1-996 | Snow depth in centimeters (e.g., 1 = 1 cm, 996 = 996 cm) |
| 997 | Broken snow cover < 1 cm |
| 998 | Broken snow cover ≥ 1 cm |
| 999 | Snow dunes |
| (5 spaces) | Missing value |
