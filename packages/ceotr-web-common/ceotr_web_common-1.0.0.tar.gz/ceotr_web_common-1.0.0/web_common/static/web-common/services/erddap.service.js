function ErddapService() {

    this.generateDataUrl = generateDataUrl;
    this.generateMetadataUrl = generateMetadataUrl;

    function generateDataUrl(datasetId, variables, fileFormat, dateRange) {
        var result = "http://ceotr.ocean.dal.ca/erddap/tabledap/" + datasetId + fileFormat + "?" + percentEncode(variables.toString());
        if(dateRange) {
            result += "&time>=" + getDateString(dateRange.min) + "&time<=" + getDateString(dateRange.max);
        }
        return result;
    }

    function getDateString(date) {
        let date_str = date.getFullYear() + "-";
        if(date.getMonth() < 9) {
            date_str += "0";
        }
        date_str += (date.getMonth()+1) + "-";
        if(date.getDate() < 10) {
            date_str += "0";
        }
        date_str += date.getDate();
        return date_str;
    }

    function generateMetadataUrl(datasetId, fileFormat) {
        var result = "http://ceotr.ocean.dal.ca/erddap/info/" + datasetId + "/index" + fileFormat;
        return result;
    }

    //TODO: review and probably replace, taken from ERDDAP site
    function percentEncode(s) {
        var s2 = "";
        for (var i = 0; i < s.length; i++) {
            var ch = s.charAt(i);
            if (ch == "\xA0") {
                s2 += "%20";
            }
            else {
                s2 += encodeURIComponent(ch);
            }
        }
        return s2;
    }

}