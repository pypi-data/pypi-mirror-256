import os
import sys

def get_fixpoint_api_key():
  if 'FIXPOINT_API_KEY' not in os.environ:
    print("FIXPOINT_API_KEY env variable not set. Exiting...")
    sys.exit(1)
  else:
    return os.environ['FIXPOINT_API_KEY']