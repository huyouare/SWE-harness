import modal
import os
import uuid
from pydantic import BaseModel
import shutil
import sys


stub = modal.Stub("swebench-modal-app")

image = modal.Image.from_registry("huyouare/sweb.base.arm64:latest")


@stub.cls(image=image)
class SWEAgentEval:
    @modal.method()
    def apply_patch(self, patch: str):
        return patch


@stub.function()
@modal.web_endpoint(method="POST")
def endpoint(request: str):
    print("Received data:", request)
    evaluator = SWEAgentEval()
    return evaluator.apply_patch.remote(request)
