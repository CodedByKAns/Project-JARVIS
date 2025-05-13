import os
import sqlite3
import shutil
from pathlib import Path
from core.registry import register_command


@register_command(r"delete chrome history", needs_input=False)
def delete_last_5_chrome_history():
    # Chrome history path (Windows)
    history_path = Path.home() / "AppData/Local/Google/Chrome/User Data/Default/History"
    backup_path = str(history_path) + "_backup"

    if not history_path.exists():
        print("Chrome history file not found.")
        return

    # Step 1: Backup original History file
    shutil.copy2(history_path, backup_path)

    # Step 2: Connect to the SQLite database
    try:
        conn = sqlite3.connect(history_path)
        cursor = conn.cursor()

        # Step 3: Get last 5 visited URLs sorted by last visit time
        cursor.execute("SELECT id FROM urls ORDER BY last_visit_time DESC LIMIT 5;")
        last_5_ids = [row[0] for row in cursor.fetchall()]

        # Step 4: Delete from visits and urls tables
        for url_id in last_5_ids:
            cursor.execute("DELETE FROM visits WHERE url = ?", (url_id,))
            cursor.execute("DELETE FROM urls WHERE id = ?", (url_id,))

        # Step 5: Save and close
        conn.commit()
        conn.close()
        print("✅ Last 5 history entries deleted successfully.")

    except Exception as e:
        print("❌ Error while deleting history:", e)

