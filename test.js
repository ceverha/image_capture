var usonic = require('r-pi-usonic');
usonic.init((err) => {
    if (err) {
	console.log(err);
	return;
    } else {
	
    }
});

var sensor = usonic.createSensor(24, 23, 450);

console.log(sensor());
