from epics import caget, caput, camonitor
from b22ao.pvs import *
from enum import Enum
from threading import Event
from p4p.client.thread import Context
import numpy
import logging

logger = logging.getLogger('b22ao.aosystem')

class AOSystem:

    def __init__(self):
        self.cam = AreaDetector(AD_PVBASE)
        self.dm = None  # DM of choice

    def select_dm(self, dm):
        logger.info(f'DM {dm} selected')
        self.dm = DeformableMirror(dm)

    def deform(self, mask, dm=None):
        try:
            DeformableMirror(dm).deform(mask)
        except ValueError:  # no dm provided
            try:
                self.dm.deform(mask)
            except AttributeError:
                raise NameError("Call #select_dm(dm) first or specify a DM in #deform(mask, dm)")

    def capture(self):
        return self.cam.acquire()

    def get_metadata(self):
        return {'cam': self.cam.get_metadata(), 'dm': self.dm.get_metadata()}


class DeformableMirror(Enum):

    DM1 = 1
    DM2 = 2

    def deform(self, mask):
        logger.debug('Deforming mirror')
        for actuator in range(len(mask)):
            caput(self._get_pv_base() + DM_ACTUATOR_PREFIX + str(actuator) + DM_ACTUATOR_SETPOINT, mask[actuator])
        caput(self._get_pv_base() + DM_APPLY_MASK, 1)

    def _get_pv_base(self):
        if self is DeformableMirror.DM1:
            return standardise_pv(DM1_PVBASE)
        elif self is DeformableMirror.DM2:
            return standardise_pv(DM2_PVBASE)

    def get_metadata(self):
        return {'mirror': self}


class AreaDetector:

    def __init__(self, pv_base):
        pv_base = standardise_pv(pv_base)
        self.acquisition_allowed = Event()
        self.data_ready = Event()
        self.current_frame = None
        self.frame_counter_pv = pv_base + AD_ARRAY_COUNTER
        self.acquire_pv = pv_base + AD_ACQUIRE
        self.data_pv = pv_base + AD_ARRAY_DATA
        self.gain_pv = pv_base + AD_GAIN
        self.shutter_pv = pv_base + AD_SHUTTER_STATE

        caput(pv_base + AD_IMAGE_MODE, AD_IMAGE_MODE_SINGLE)

        camonitor(self.frame_counter_pv, callback=self.frame_counter_callback)
        camonitor(ALLOW_ACQUISITION, callback=self.allow_acquisition_callback)
        
        # synchronise acquisition_allowed event with current PV value
        self.allow_acquisition_callback(value=caget(ALLOW_ACQUISITION))

        self.pva_ctxt = Context('pva')

    def acquire(self):
        """
        Returns a valid frame
        (acquires and reads shutter state:
        repeats until shutter is open)
        """
        # request frames until shutter is open
        while True:
            self.acquisition_allowed.wait()
            self.request_frame()
            if caget(self.shutter_pv, as_string=True) == "Open":
                break
            logger.debug("Frame received, but shutter closed. Reacquiring...")
        
        # shutter is open; read data
        pvadata = self.pva_ctxt.get(self.data_pv)
        data = numpy.reshape(pvadata.data, pvadata.shape)
        return data

    def request_frame(self):
        """
        Hits the 'Acquire' button and blocks
        until data is ready to be read from Array plugin
        """
        self.current_frame = caget(self.frame_counter_pv)
        logger.debug("Acquiring")
        caput(self.acquire_pv, "Acquire")
        self.data_ready.wait()
        self.data_ready.clear()

    def frame_counter_callback(self, **kwargs):
        try:
            if kwargs['value'] == self.current_frame + 1:
                logger.debug(f'Frame #{kwargs['value']} ready for reading')
                self.data_ready.set()
        except TypeError:
            # callback may be invoked once on initialisation,
            # before request_frame is ever called and so self.current_frame is None
            pass

    def allow_acquisition_callback(self, **kwargs):
        value = kwargs['value']
        if value == 0:
            logger.info("Acquisition disallowed")
            self.acquisition_allowed.clear()
        elif value == 1:
            logger.info("Acquisition allowed")
            self.acquisition_allowed.set()

    def get_metadata(self):
        metadata = dict()
        metadata['gain'] = caget(self.gain_pv)
        return metadata


def standardise_pv(pv):
    return pv if pv.endswith(':') else pv + ':'
