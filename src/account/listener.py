import logging
import json
import re

from watchdog.events import PatternMatchingEventHandler

logger = logging.getLogger(__name__)


class AccountListener(PatternMatchingEventHandler):
    """Listener for changes to secrets directory.
    """

    def __init__(self, account_store):
        """Constructor.

        Args:
            account_store (account.store.AccountStore): Instance of account store.
        """
        super().__init__(patterns=["*.json"])

        self._account_store = account_store

    def on_created(self, event):
        """Event callback for when new secrets are added.
        Args:
            event (watchdog.events.FileCreatedEvent): Callback event from watchdog.
        """
        if event.is_directory:  # ignore the creation of new directories
            return

        self._account_store.insert(event.src_path)
        logger.info(f'Created a GVoice number in the store.')

    def on_deleted(self, event):
        """Event callback for when new secrets are deleted.
        Args:
            event (watchdog.events.FileCreatedEvent): Callback event from watchdog.
        """
        if event.is_directory:  # ignore the deletion of directories
            return

        phone_number = re.findall('.*secrets_([0-9]*).json', event.src_path)[0]
        self._account_store.delete(phone_number)

        logger.info(f'Deleted {phone_number} from GVMS store.')

    def on_moved(self, event):
        """Event callback for when new secrets are updated.
        Args:
            event (watchdog.events.FileCreatedEvent): Callback event from watchdog.
        """
        if event.is_directory:  # ignore the creation of new directories
            return

        self._account_store.insert(event.src_path)
        logger.info(f'Updated a GVoice number in the store.')
