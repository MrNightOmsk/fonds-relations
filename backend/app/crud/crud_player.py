from typing import List, Optional, Dict, Any, Union
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.player import Player, PlayerContact, PlayerLocation, PlayerNickname, PlayerPaymentMethod, PlayerSocialMedia
from app.schemas.player import PlayerCreate, PlayerUpdate


class CRUDPlayer(CRUDBase[Player, PlayerCreate, PlayerUpdate]):
    def create_with_details(
        self, db: Session, *, obj_in: PlayerCreate
    ) -> Player:
        # Разделяем ФИО на составляющие, если полное имя задано
        first_name = obj_in.first_name
        last_name = obj_in.last_name
        middle_name = obj_in.middle_name
        full_name = obj_in.full_name or f"{first_name} {last_name or ''} {middle_name or ''}".strip()
        
        db_obj = Player(
            first_name=first_name,
            last_name=last_name, 
            middle_name=middle_name,
            full_name=full_name,
            birth_date=obj_in.birth_date,
            contact_info=obj_in.contact_info,
            additional_info=obj_in.additional_info,
            health_notes=obj_in.health_notes,
            created_by_user_id=obj_in.created_by_user_id,
            created_by_fund_id=obj_in.created_by_fund_id
        )
        db.add(db_obj)
        db.flush()

        # Create contacts
        if obj_in.contacts:
            for contact in obj_in.contacts:
                db_contact = PlayerContact(
                    player_id=db_obj.id,
                    type=contact.type,
                    value=contact.value,
                    description=contact.description
                )
                db.add(db_contact)

        # Create locations
        if obj_in.locations:
            for location in obj_in.locations:
                db_location = PlayerLocation(
                    player_id=db_obj.id,
                    country=location.country,
                    city=location.city,
                    address=location.address
                )
                db.add(db_location)

        # Create nicknames
        if obj_in.nicknames:
            for nickname in obj_in.nicknames:
                db_nickname = PlayerNickname(
                    player_id=db_obj.id,
                    nickname=nickname.nickname,
                    room=nickname.room,
                    discipline=nickname.discipline
                )
                db.add(db_nickname)
                
        # Create payment methods
        if obj_in.payment_methods:
            for payment_method in obj_in.payment_methods:
                db_payment_method = PlayerPaymentMethod(
                    player_id=db_obj.id,
                    type=payment_method.type,
                    value=payment_method.value,
                    description=payment_method.description
                )
                db.add(db_payment_method)
                
        # Create social media
        if obj_in.social_media:
            for social_media in obj_in.social_media:
                db_social_media = PlayerSocialMedia(
                    player_id=db_obj.id,
                    type=social_media.type,
                    value=social_media.value,
                    description=social_media.description
                )
                db.add(db_social_media)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_details(
        self,
        db: Session,
        *,
        db_obj: Player,
        obj_in: Union[PlayerUpdate, Dict[str, Any]]
    ) -> Player:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        # Update basic player info
        for field in ["first_name", "last_name", "middle_name", "full_name", "birth_date", "contact_info", "additional_info", "health_notes", "is_active"]:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
                
        # Если обновились составляющие ФИО, обновляем и полное имя для совместимости
        if any(field in update_data for field in ["first_name", "last_name", "middle_name"]) and "full_name" not in update_data:
            first_name = update_data.get("first_name", db_obj.first_name)
            last_name = update_data.get("last_name", db_obj.last_name)
            middle_name = update_data.get("middle_name", db_obj.middle_name)
            db_obj.full_name = f"{first_name} {last_name or ''} {middle_name or ''}".strip()

        # Update contacts
        if "contacts" in update_data:
            # Remove old contacts
            db.query(PlayerContact).filter(
                PlayerContact.player_id == db_obj.id
            ).delete()
            
            # Add new contacts
            for contact in update_data["contacts"]:
                db_contact = PlayerContact(
                    player_id=db_obj.id,
                    type=contact["type"],
                    value=contact["value"],
                    description=contact.get("description")
                )
                db.add(db_contact)

        # Update locations
        if "locations" in update_data:
            # Remove old locations
            db.query(PlayerLocation).filter(
                PlayerLocation.player_id == db_obj.id
            ).delete()
            
            # Add new locations
            for location in update_data["locations"]:
                db_location = PlayerLocation(
                    player_id=db_obj.id,
                    country=location["country"],
                    city=location.get("city"),
                    address=location.get("address")
                )
                db.add(db_location)

        # Update nicknames
        if "nicknames" in update_data:
            # Remove old nicknames
            db.query(PlayerNickname).filter(
                PlayerNickname.player_id == db_obj.id
            ).delete()
            
            # Add new nicknames
            for nickname in update_data["nicknames"]:
                db_nickname = PlayerNickname(
                    player_id=db_obj.id,
                    nickname=nickname["nickname"],
                    room=nickname.get("room"),
                    discipline=nickname.get("discipline")
                )
                db.add(db_nickname)
                
        # Update payment methods
        if "payment_methods" in update_data:
            # Remove old payment methods
            db.query(PlayerPaymentMethod).filter(
                PlayerPaymentMethod.player_id == db_obj.id
            ).delete()
            
            # Add new payment methods
            for payment_method in update_data["payment_methods"]:
                db_payment_method = PlayerPaymentMethod(
                    player_id=db_obj.id,
                    type=payment_method["type"],
                    value=payment_method["value"],
                    description=payment_method.get("description")
                )
                db.add(db_payment_method)
                
        # Update social media
        if "social_media" in update_data:
            # Remove old social media
            db.query(PlayerSocialMedia).filter(
                PlayerSocialMedia.player_id == db_obj.id
            ).delete()
            
            # Add new social media
            for social_media in update_data["social_media"]:
                db_social_media = PlayerSocialMedia(
                    player_id=db_obj.id,
                    type=social_media["type"],
                    value=social_media["value"],
                    description=social_media.get("description")
                )
                db.add(db_social_media)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_nickname(
        self, db: Session, *, nickname: str
    ) -> Optional[Player]:
        return (
            db.query(Player)
            .join(PlayerNickname)
            .filter(PlayerNickname.nickname == nickname)
            .first()
        )

    def get_by_contact(
        self, db: Session, *, contact_type: str, contact_value: str
    ) -> Optional[Player]:
        return (
            db.query(Player)
            .join(PlayerContact)
            .filter(
                PlayerContact.type == contact_type,
                PlayerContact.value == contact_value
            )
            .first()
        )

    def get_by_location(
        self, db: Session, *, country: str, city: Optional[str] = None
    ) -> List[Player]:
        query = (
            db.query(Player)
            .join(PlayerLocation)
            .filter(PlayerLocation.country == country)
        )
        if city:
            query = query.filter(PlayerLocation.city == city)
        return query.all()

    def get_by_fund(
        self, db: Session, *, fund_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Player]:
        return (
            db.query(Player)
            .filter(Player.created_by_fund_id == fund_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_user(
        self, db: Session, *, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Player]:
        return (
            db.query(Player)
            .filter(Player.created_by_user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


player = CRUDPlayer(Player) 