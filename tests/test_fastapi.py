from src.main import app, test_dependancy
from fastapi.testclient import TestClient
from tests import trace, span_exporter

tracer = trace.get_tracer(__name__)

client = TestClient(app)


def test_read_main():
    app.dependency_overrides[test_dependancy] = lambda: lambda: 5
    with tracer.start_as_current_span("test"):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World", "TestDep": 5}

    assert "test" in [x.name for x in span_exporter.get_finished_spans()]


def test_read_main_second():
    app.dependency_overrides[test_dependancy] = lambda: lambda: 6
    with tracer.start_as_current_span("test"):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World", "TestDep": 6}

    assert "read-root" in [x.name for x in span_exporter.get_finished_spans()]
