var rpio = require('rpio');
var time = require('time');

const trigger = 23;
const echo = 24;

console.log('distance measurement in progress');

rpio.init({
    mapping: 'gpio'
});

rpio.open(trigger, rpio.OUTPUT, rpio.LOW);
rpio.open(echo, rpio.INPUT, rpio.LOW);

console.log('settling...');

rpio.write(trigger, rpio.HIGH);
rpio.sleep(0.00001);
console.log(rpio.read(trigger))
rpio.write(trigger, rpio.LOW);

let pulseStart;
while (!rpio.read(echo)) {
    pulseStart = time.time();
}
let pulseEnd;
while (rpio.read(echo)) {
    pulseEnd = time.time();
}

const pulseDur = pulseEnd - pulseStart;
const distance = pulseDur * 17150

console.log(distance);



