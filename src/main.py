from collections.abc import Callable
from typing import Annotated
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import opentelemetry.trace as trace

from fastapi import FastAPI, Depends

app = FastAPI()

tracer = trace.get_tracer(__name__)


def test_dependancy():
    def check() -> int:
        return 1

    return check


@app.get("/")
def read_root(check: Annotated[Callable, Depends(test_dependancy)]):
    with tracer.start_as_current_span("read-root"):
        return {"Hello": "World", "TestDep": check()}


FastAPIInstrumentor.instrument_app(app)
