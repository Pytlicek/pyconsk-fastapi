import schemathesis
from hypothesis import settings, HealthCheck, Phase, Verbosity
from main import app

schema = schemathesis.from_asgi(
    "/openapi.json", app, validate_schema=True, base_url="http://localhost"
)


@schema.parametrize()
@settings(
    max_examples=5,
    suppress_health_check={HealthCheck(2)},
    phases=[Phase.generate, Phase.shrink],
    verbosity=Verbosity.normal,
    deadline=None,
)
def test_api(case):
    response = case.call_asgi()
    case.validate_response(response)
