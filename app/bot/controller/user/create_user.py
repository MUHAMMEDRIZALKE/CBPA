
import telegram

from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.schemas.telegram_user import TelegramUserCreate
from app.crud.user import user_crud
from app.crud.telegram_user import telegram_user_crud
from app.models.user import User, TelegramUser

class CreateUser:
    """ 
    Create user and telegram user

    Args:
        user_details (telegram.User): User details
    """
    def __init__(self, user_details: telegram.User):
        self.db = SessionLocal()
        self.user_details = user_details
    
    def _check_telegram_user_exists(self):
        telegram_user = telegram_user_crud.get_by_telegram_id(self.db,str(self.user_details.id))
        if telegram_user:
            return telegram_user.user
        return None

    def _create_user(self) -> User:
        """ 
        Create user

        Returns:
            User: User object
        """
        user_in = UserCreate(
            username=self.user_details.username
        )
        user_obj = user_crud.create(self.db, obj_in=user_in)
        return user_obj

    def _create_telegram_user(self, user_obj: User) -> TelegramUser:
        """ 
        Create telegram user

        Args:
            user_obj (User): User object

        Returns:
            TelegramUser: Telegram user object
        """
        telegram_user_in = TelegramUserCreate(
            telegram_id=str(self.user_details.id),
            user_id=user_obj.id,
            username=self.user_details.username,
            first_name=self.user_details.first_name,
            last_name=self.user_details.last_name,
        )
        telegram_user_obj = telegram_user_crud.create(self.db, obj_in=telegram_user_in)
        return telegram_user_obj



    def create_user(self):
        """ 
        Create user and telegram user

        Returns:
            User: User object
        """
        user = self._check_telegram_user_exists()
        if user:
            return user

        user_obj = self._create_user()
        self._create_telegram_user(user_obj)
        return user_obj
    
    def __del__(self):
        if self.db:
            self.db.close()