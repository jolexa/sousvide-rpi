# sousvide-rpi
Controlling a Sous Vide Cooker with a Raspberry Pi. Heavily inspired by Chris Swan's [work](https://github.com/cpswan/RPi_sousvide)

This was an attempt, it is now abondonware. I have just bought a commercial Sous Vide Cooker after trying to manually tune this algorithm and deciding that I didn't want to spend so much time on it to get it right. I also found that using a Crock Pot for this task was not ideal because the heating time was so slow.

Bias of 40 seconds seems like a good start, the defaults seemed to almost work except it wasn't making up ground on the temp. I was then playing with the divisors to get a bigger change to `power` level based on the error. I think it would have worked eventually.

![example](https://raw.githubusercontent.com/jolexa/sousvide-rpi/master/default.png)


Attempted a P and I of 1 to see what would happen and the temp was getting progressively worse as there was no damping on the error levels.
![example](https://raw.githubusercontent.com/jolexa/sousvide-rpi/master/no-constants.png)

Good Luck!



# Disclaimer
Though I make this available and it works for me, this is dealing with electronics and I am not responsible for a) wrecking your Raspberry Pi, b) Burning down your house, or c) anything else
