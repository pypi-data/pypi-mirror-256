import os
import sys

from dotenv import load_dotenv

# Fixes imports for generated grpc code, see https://github.com/protocolbuffers/protobuf/issues/4546
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f"{dir_path}")

from . import io, llm, core, agent, util

from .core.config import ENV_FILE

load_dotenv(ENV_FILE)

workflow = core.workflow
action = core.action
