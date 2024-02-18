// https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
export function getDistanceFromLatLonInKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
	var R = 6371; // Radius of the earth in km
	var dLat = deg2rad(lat2 - lat1);  // deg2rad below
	var dLon = deg2rad(lon2 - lon1);
	var a =
		Math.sin(dLat/2) * Math.sin(dLat/2) +
		Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
		Math.sin(dLon/2) * Math.sin(dLon/2)
	;
	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
	var d = R * c; // Distance in km
	return d;
}

export function deg2rad(deg: number): number {
  return deg * (Math.PI/180)
}

/**
 * Round value to the specified number of decimal places
 * @param value
 * @param decimalPlaces
 * @returns {number}
 */
export function roundTo(value: number, decimalPlaces: number): number {
    var factor = 1;
    for(var i=0; i<decimalPlaces; i++) {
        factor *= 10;
    }
    var result = Math.round(value * factor) / factor;
    return result;
}

let x = 8;