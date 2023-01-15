import fastapi

from . import exceptions
from . import schemas
from . import controllers


router = fastapi.APIRouter()


@router.post('/opening_hours', response_model=schemas.HumanReadableOpeningHours)
def get_opening_hours(opening_hours: schemas.OpeningHoursQuery):
    """Each day is considered closed by default and each day is presented in the result."""

    try:
        return controllers.parse_opening_hours(opening_hours)
    except exceptions.InvalidOpeningHoursError:
        raise fastapi.HTTPException(status_code=400, detail='Invalid opening hours provided.')
