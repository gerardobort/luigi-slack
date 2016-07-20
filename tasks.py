from __future__ import print_function
import json
import luigi
from luigi.format import UTF8

@luigi.Task.event_handler(luigi.Event.SUCCESS)
def celebrate_success(task):
    """Will be called directly after a successful execution
       of `run` on any Task subclass (i.e. all luigi Tasks)
    """
    print("YAY! :D")

@luigi.Task.event_handler(luigi.Event.FAILURE)
def mourn_failure(task, exception):
    """Will be called directly after a failed execution
       of `run` on any JobTask subclass
    """
    print("OUGH! :(")

from slack import *

if __name__ == "__main__":
    luigi.run()

