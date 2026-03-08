"""
Модуль резервного копирования базы данных.
"""

import shutil
import os
from datetime import datetime

DB_NAME = "music_store.db"

def backup_database():
    if not os.path.exists("backups"):
        os.makedirs("backups")

    backup_name = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy(DB_NAME, backup_name)
    return backup_name
