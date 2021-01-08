import datetime as dt
import requests
import time
import pytz
import os


"""
     "The concept of waiting bewilders me. There are always
     deadlines. There are always ticking clocks. That's why
                                 you must manage your time"

                                                - Whiterose

"""

FORMATS = ("%Y/%m/%dT%H:%M:%S", '%Y/%m/%d')
TIMEZONES = {
    "MX": "Mexico/General",
    "UTC": "Universal"
}

"""
    localtime() = time.struct_time
    today('UTC|MX') UTC = 2020/12/18T22:24:58
                    MX = 2020/12/18T16:24:58
"""

def localtime():

    """ Returns struct_time """

    return time.localtime(time.time())


def today(tzinfo=TIMEZONES['UTC']):

    """ Get current datetime. Timezone aware

    Keyword Arguments:
        tzinfo {str} -- [description] (default: {"UTC"})

    Returns:
        {str} Datetime string, format %Y/%m/%dT%H:%M:%S

        today(UTC) = 2020/12/18T22:01:45
        today(MX) = 2020/12/18T16:01:45
    """

    tzdt = dt.datetime.now(pytz.timezone(tzinfo))
    return dt.datetime.strftime(tzdt, FORMATS[0])


class Epoch:

    """ Unix time manager class """

    timezone = TIMEZONES['UTC']

    """
    Epoch.dump(2020, 12, 18, 16) = 1608328800.0
    Epoch.load(epoch) = 2020-12-18 16:24:58.109826 Type: <class 'datetime.datetime'>
    Epoch.now()=1608330298.110156 Type: <class 'float'>
    Epoch.strfload(epoch, datetime=True|False) T = 2020/12/18T16:24:58
                                               F = 2020/12/18 Type: <class 'str'>
    """

    @classmethod
    def dump(cls, year, month, day, hr=None, tz=None):

        """ Dump unix timestamp (EPOCH)
        """

        dtt = dt.datetime(year, month, day, hr, 0, 0, 0,
                          tzinfo=pytz.timezone(cls.timezone))
        if bool(tz):
            tgt_timezone = pytz.timezone(TIMEZONES[tz])
            dtt = dtt.astimezone(tgt_timezone)

        dtt = dt.datetime.strptime(dtt.strftime(FORMATS[0]), FORMATS[0])
        return dtt.timestamp()

    @classmethod
    def now(cls, tz=None):

        """ Returns current datetime epoch. Timezone aware

        Returns:
            <class 'float'>
        """
        tzinfo = TIMEZONES[tz] if bool(tz) else cls.timezone
        tgt_timezone = pytz.timezone(tzinfo)
        dtime = dt.datetime.now(tgt_timezone)
        return dtime.timestamp()

    @classmethod
    def load(cls, epoch):

        """ load datetime from unix timestamp

        Arguments:
            epoch <class 'float'> -- Unix timestamp e.g. 1608328905.92277

        Returns:
            <class 'datetime.datetime'>
        """
        return dt.datetime.fromtimestamp(epoch)

    @classmethod
    def strfload(cls, epoch, datetime=True):

        """ load string datetime from unix timestamp

        Arguments:
            epoch <class 'float'> -- Unix timestamp e.g. 1608328905.92277
            datetime <class 'boolean'> -- if true returns: 2020/12/18T16:01:45
                                          if false returns: 2020/12/18

        Returns:
            <class 'string'> Datetime string: 2020/12/18(T16:01:45)
        """
        fmt = FORMATS[0] if datetime else FORMATS[1]
        dt = cls.load(epoch)
        return str(dt.strftime(fmt))


class Benchmark:

    """ Code benchmark class """

    def start(self):
        self.t1 = time.time()

    def stop(self, message):
        self.t2 = time.time()
        self.rst = self.t2 - self.t1
        self.t2 = self.t1 = 0

        print("%s: %s" % (message, str(self.rst)))
