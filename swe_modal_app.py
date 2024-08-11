import modal
import os
import uuid
from pydantic import BaseModel
import shutil
import sys


stub = modal.Stub("swebench-modal-app")

image = (
    modal.Image.from_registry("exploiter007/swebench:sweb.eval.x86_64.astropy__astropy-12907")
)


class AgentEvalRequest(BaseModel):
    patch: str

@stub.cls(image=image)
class SWEAgentEval:
    @modal.method()
    def apply_patch(self, patch: str):
        return patch


@stub.function()
@modal.web_endpoint(method="POST")
def endpoint(request: AgentEvalRequest):
    print("Received data:", request)
    evaluator = SWEAgentEval()
    return evaluator.apply_patch.remote(request.patch)


if __name__ == "__main__":
    stub.serve()