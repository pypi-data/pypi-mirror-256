// Not using prototype because leaflet library incorrectly using array as an object and chokes on additional properties

Array.indexOfByProperty = function(arr, val, property) {
	for(var i=0; i<arr.length; i++) {
		if(arr[i] && arr[i][property] === val) {
			return i;
		}
	}
	return -1;
};

Array.getByProperty = function(arr, val, property) {
    var index = Array.indexOfByProperty(arr, val, property);
    if(index < 0) {
        return null;
    }
    return arr[index];
};

Array.unique = function(arr, key) {
	var result = [];
    for(var i = 0; i < arr.length; i++) {
    	var item = key ? arr[i] && arr[i][key] : arr[i];
        if(item && (key ? result.indexOfByProperty(item, key) < 0 : result.indexOf(item) < 0)) {
            result.push(arr[i]);
        }
    }
    return result;
};

Array.contains = function(arr, val) {
	return arr.indexOf(val) >= 0;
};

String.prototype.equalsIgnoreCase = function(second) {
	var first = this;
	if(!first.toLowerCase) {
		return first == second;
	}
	if(!second.toLowerCase) {
		return false;
	}

	return first.toLowerCase() == second.toLowerCase();
};

/**
 * Get the current timezone in long format (e.g. "Atlantic Standard Time"/"Atlantic Daylight Time").
 * @returns {*}
 */
Date.getLongTimezone = function() {
	var matches = new Date().toLocaleTimeString('en-us',{timeZoneName:'long'}).match(/^\d+:\d+:\d+\s[AP]M\s([a-zA-Z0-9 ]+)$/);
	if(matches && matches.length == 2) {
	    return matches[1];
    }
    return null;
};

/**
 * Get the current timezone in short format (e.g. "AST"/"ADT").
 * @returns {*}
 */
Date.getShortTimezone = function() {
	var matches = new Date().toLocaleTimeString('en-us',{timeZoneName:'short'}).match(/^\d+:\d+:\d+\s[AP]M\s([a-zA-Z0-9 ]+)$/);
	if(matches && matches.length == 2) {
	    return matches[1];
    }
    var longTimezone = Date.getLongTimezone();
	if(longTimezone) {
		var obj = Array.getByProperty(Timezones, longTimezone, 'Name');
		if(obj) {
			return obj.Abbreviation;
		}
	}
    return null;
};
