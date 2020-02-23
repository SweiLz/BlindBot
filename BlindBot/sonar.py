import time

import pigpio


class Sonar:
    """
    This class encapsulates a sonar device with separate
    trigger and echo pins.
    A pulse on the trigger initiates the sonar ping and shortly
    afterwards a sonar pulse is transmitted and the echo pin
    goes high.  The echo pins stays high until a sonar echo is
    received (or the response times-out).  The time between
    the high and low edges indicates the sonar round trip time.
    """

    def __init__(self, pi, trigger, echo):
        """
        The class is instantiated with the Pi to use and the
        gpios connected to the trigger and echo pins.
        """
        self.pi = pi
        self._trig = trigger
        self._echo = echo

        self._ping = False
        self._high = None
        self._time = None

        self._triggered = False
        self._trig_mode = self.pi.get_mode(self._trig)
        self._echo_mode = self.pi.get_mode(self._echo)

        self.pi.set_mode(self._trig, pigpio.OUTPUT)
        self.pi.set_mode(self._echo, pigpio.INPUT)

        self._cb = self.pi.callback(self._trig, pigpio.EITHER_EDGE, self._cbf)
        self._cb = self.pi.callback(self._echo, pigpio.EITHER_EDGE, self._cbf)

        self._inited = True

    def _cbf(self, gpio, level, tick):
        if gpio == self._trig:
            if level == 0:
                self._triggered = True
                self._high = None
        else:
            if self._triggered:
                if level == 1:
                    self._high = tick
                else:
                    if self._high is not None:
                        self._time = tick-self._high
                        self._high = None
                        self._ping = True

    def read(self):
        """
        Triggers a reading.  The returned reading is the number
        of microseconds for the sonar round-trip.
        round trip cms = round trip time / 1000000.0 * 34030
        """
        if self._inited:
            self._ping = False
            self.pi.gpio_trigger(self._trig)
            start = time.time()
            while not self._ping:
                if (time.time()-start) > 5.0:
                    return 20000
                time.sleep(0.001)
            return self._time
        else:
            return None

    def getDist(self):
        """
        Read a distance,
        Return float number in cm.
        """
        if self._inited:
            stime = self.read()
            distance = round(stime/29/2, 2)
            return distance
        else:
            return None

    def cancel(self):
        """
        Cancels the ranger and returns the gpios to their
        original mode.
        """
        if self._inited:
            self._inited = False
            self._cb.cancel()
            self.pi.set_mode(self._trig, self._trig_mode)
            self.pi.set_mode(self._echo, self._echo_mode)


# if __name__ == "__main__":
#     pi = pigpio.pi()

#     sonar = Sonar(pi, 27, 22)
#     end_time = time.time() + 60
#     while time.time() < end_time:
#         print(sonar.getDist())
#         time.sleep(0.03)

#     sonar.cancel()
#     pi.stop()
