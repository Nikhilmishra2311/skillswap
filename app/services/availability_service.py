from sqlmodel import Session, select

from app.models.availability import AvailabilitySlot


# =====================================
# CREATE AVAILABILITY
# =====================================

def create_availability(
    db: Session,
    user_id: int,
    day: str,
    start_time: str,
    end_time: str
):

    # Prevent overlapping slots

    existing_slots = db.exec(
        select(AvailabilitySlot).where(
            AvailabilitySlot.user_id == user_id,
            AvailabilitySlot.day == day,
            AvailabilitySlot.is_active == True
        )
    ).all()

    for slot in existing_slots:

        if (
            start_time < slot.end_time
            and
            end_time > slot.start_time
        ):
            raise Exception(
                "Time slot overlaps with existing availability"
            )

    availability_slot = AvailabilitySlot(
        user_id=user_id,
        day=day,
        start_time=start_time,
        end_time=end_time,
        is_active=True
    )

    db.add(availability_slot)

    db.commit()

    db.refresh(availability_slot)

    return availability_slot


# =====================================
# GET MY AVAILABILITY
# =====================================

def get_my_availability(
    db: Session,
    user_id: int
):

    return db.exec(
        select(AvailabilitySlot).where(
            AvailabilitySlot.user_id == user_id,
            AvailabilitySlot.is_active == True
        )
    ).all()


# =====================================
# GET TUTOR AVAILABILITY
# =====================================

def get_user_availability(
    db: Session,
    user_id: int
):

    return db.exec(
        select(AvailabilitySlot).where(
            AvailabilitySlot.user_id == user_id,
            AvailabilitySlot.is_active == True
        )
    ).all()


# =====================================
# UPDATE AVAILABILITY
# =====================================

def update_availability(
    db: Session,
    slot_id: int,
    user_id: int,
    day: str,
    start_time: str,
    end_time: str
):

    slot = db.get(
        AvailabilitySlot,
        slot_id
    )

    if not slot:
        raise Exception(
            "Availability slot not found"
        )

    if slot.user_id != user_id:
        raise Exception(
            "Unauthorized"
        )

    # Prevent overlap with other slots

    existing_slots = db.exec(
        select(AvailabilitySlot).where(
            AvailabilitySlot.user_id == user_id,
            AvailabilitySlot.day == day,
            AvailabilitySlot.id != slot_id,
            AvailabilitySlot.is_active == True
        )
    ).all()

    for existing in existing_slots:

        if (
            start_time < existing.end_time
            and
            end_time > existing.start_time
        ):
            raise Exception(
                "Time slot overlaps with existing availability"
            )

    slot.day = day
    slot.start_time = start_time
    slot.end_time = end_time

    db.add(slot)

    db.commit()

    db.refresh(slot)

    return slot


# =====================================
# DELETE AVAILABILITY
# =====================================

def delete_availability(
    db: Session,
    slot_id: int,
    user_id: int
):

    slot = db.get(
        AvailabilitySlot,
        slot_id
    )

    if not slot:
        raise Exception(
            "Availability slot not found"
        )

    if slot.user_id != user_id:
        raise Exception(
            "Unauthorized"
        )

    db.delete(slot)

    db.commit()

    return {
        "message": "Availability slot deleted successfully"
    }