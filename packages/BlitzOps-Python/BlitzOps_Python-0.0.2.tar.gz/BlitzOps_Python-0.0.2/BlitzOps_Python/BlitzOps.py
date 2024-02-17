from logging import Logger
import requests
import json
import time

class BlitzOps(Logger):

    def __init__(self, workflow_id:str, tracker_address:str, run_id:str):
        self.workflow_id = workflow_id
        self.tracker_address = tracker_address
        self.run_id = run_id

    def checkpoint(self, checkpoint_id:str=None):
        self._sendCall(checkpoint_id=checkpoint_id)

    ### Utils ###

    def _generateTimestamp(self):
        return time.time()
    
    def _sendCall(self, checkpoint_id:str):
        payload = {
            "workflow_id": self.workflow_id,
            "run_id": self.run_id,
            "checkpoint_id": checkpoint_id,
            "timestamp": self._generateTimestamp()
        }

        r = requests.post(url=self.tracker_address, data=json.dumps(payload))
        print("Status code: ", r.status_code)
        print("Resp: ", r.text)

    ### Trackers ###

    