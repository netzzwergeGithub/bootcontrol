import threading
import time

try:
        import RPi.GPIO as GPIO
except RuntimeError:
        print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

GPIO.setmode(GPIO.BCM)


class GPIOInputThread(object):
    """ The  class which call a callback function regularily on an interval passing the input value on the defined pin.
    class construction thanks to:
    https://gist.github.com/sebdah/832219525541e059aefa
    """

    def __init__(self, bcm_pin_nr, call_back, check_interval=1 ):
        """ Constructor
        :type check_interval: int
        :param bcm_pin_nr: GPIO Number in BCM layout
        :param call_back: a callback function with on parameter . Will called regularily on check_interval with the current value on the gpio-pin as parameter.
        :param check_interval: Check interval, in seconds
        """
        self.check_interval = check_interval
        self.bcm_pin_nr = bcm_pin_nr
        self.call_back = call_back
        GPIO.setup(self.bcm_pin_nr, GPIO.IN)

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            state = GPIO.input(self.bcm_pin_nr)
            # print('checking input on PIN: {}: {} => callback: {} '.format(self.bcm_pin_nr, state , self.call_back))
            if self.call_back:
                self.call_back(state)

            time.sleep(self.check_interval)
