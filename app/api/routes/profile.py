from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)
from fastapi import Request
from app.core.limiter import limiter
from sqlmodel import Session

from app.db.session import get_session
from app.api.deps import get_current_user

from app.schemas.profile import ProfileUpdate
from app.schemas.tutor_profile import (
    TutorProfileCreate,
    TutorProfileUpdate
)
from app.schemas.learner_profile import (
    LearnerProfileCreate,
    LearnerProfileUpdate
)

from app.services.profile_service import (
    get_my_profile,
    get_profile_by_user_id,
    update_profile
)

from app.services.tutor_profile_service import (
    create_tutor_profile,
    get_tutor_profile,
    update_tutor_profile
)

from app.services.learner_profile_service import (
    create_learner_profile,
    get_learner_profile,
    update_learner_profile
)

from app.services.storage_service import (
    upload_image,
    delete_file,
    get_file_url
)


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get("/me")
@limiter.limit("10/minute")
def my_profile(
    request: Request,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    try:

        return get_my_profile(
            db,
            current_user.id
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    


@router.get("/{user_id}")
@limiter.limit("10/minute")
def public_profile(
    request: Request,
    user_id: int,
    db: Session = Depends(get_session)
):

    try:

        return get_profile_by_user_id(
            db,
            user_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )   
    
@router.put("/me")
@limiter.limit("10/minute")
async def update_my_profile(
    request: Request,
    full_name: str | None = Form(None),
    headline: str | None = Form(None),
    bio: str | None = Form(None),
    city: str | None = Form(None),
    country: str | None = Form(None),
    college: str | None = Form(None),
    github_url: str | None = Form(None),
    linkedin_url: str | None = Form(None),
    website_url: str | None = Form(None),

    photo: UploadFile | None = File(None),

    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)

):

    profile_picture = None

    if photo:

        profile = get_my_profile(
        db,
        current_user.id
        )

        if profile.profile_picture:

           delete_file(
            profile.profile_picture
        )

        object_name = upload_image(

        file=photo,

        folder="profile-images"

        )

        profile_picture = object_name

    data = ProfileUpdate(

        full_name=full_name,
        headline=headline,
        bio=bio,
        city=city,
        country=country,
        college=college,
        github_url=github_url,
        linkedin_url=linkedin_url,
        website_url=website_url

    )

    return update_profile(

        db=db,
        user_id=current_user.id,
        data=data,
        profile_picture=profile_picture

    )


@router.post("/tutor")
@limiter.limit("10/minute")
def create_tutor(
    request: Request,
    data: TutorProfileCreate,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    return create_tutor_profile(

        db,
        current_user.id,
        data

    )

@router.get("/tutor")
def tutor_profile(

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    return get_tutor_profile(

        db,
        current_user.id

    )

@router.put("/tutor")
@limiter.limit("10/minute")
def update_tutor(

    request: Request,
    data: TutorProfileUpdate,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    return update_tutor_profile(

        db,
        current_user.id,
        data

    )

@router.post("/learner")
@limiter.limit("10/minute")
def create_learner(
    request: Request,

    data: LearnerProfileCreate,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    return create_learner_profile(

        db,
        current_user.id,
        data

    )

@router.get("/learner")
def learner_profile(

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    return get_learner_profile(

        db,
        current_user.id

    )
@router.put("/learner")
@limiter.limit("10/minute")
def update_learner(

    request: Request,
    data: LearnerProfileUpdate,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    return update_learner_profile(

        db,
        current_user.id,
        data

    )