var cnIpRange = __IP_LIST__;

var fakeIpRange = __FAKE_IP_LIST__;

var subnetIpRange = {
167772160:16777216,	//10.0.0.0/8
2886729728:1048576,	//172.16.0.0/12
3232235520:65536,	//192.168.0.0/16
2130706432:256		//127.0.0.0/24
};

var wall_proxy = __PROXY__;
var nowall_proxy = "DIRECT;";

var direct = "DIRECT;";

var hasOwnProperty = Object.hasOwnProperty;

function convertAddress(ipchars) {
	var bytes = ipchars.split('.');
	var result = (bytes[0] << 24) |
	(bytes[1] << 16) |
	(bytes[2] << 8) |
	(bytes[3]);
	return result >>> 0;
};
function isInRange(ipRange, intIp) {
	for ( var range = 256; range <= 8388608; range*=2 ) {
		var sub = intIp & (range-1);
		var masterIp = intIp - sub;
		if ( hasOwnProperty.call(ipRange, masterIp) )
			continue;
		if ( sub <= ipRange[masterIp] )
			return 1;
		return 0;
	}
	return 0;
}

function FindProxyForURL(url, host) {

	if ( isPlainHostName(host) === true ) {
		return direct;
	}

	var strIp = dnsResolve(host);
	if (!strIp) {
		return wall_proxy;
	}
	
	var intIp = convertAddress(strIp);
	if ( isInRange(fakeIpRange, intIp) ) {
		return wall_proxy;
	}
	if ( isInRange(subnetIpRange, intIp) ) {
		return direct;
	}
	if ( isInRange(cnIpRange, intIp) ) {
		return nowall_proxy;
	}
	return wall_proxy;
}

