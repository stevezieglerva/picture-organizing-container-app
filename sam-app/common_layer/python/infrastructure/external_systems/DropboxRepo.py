import json

import dropbox


class DropboxRepo:
    def __init__(self, oauth_refresh_token: str, app_key: str):
        """Need to provide an oauth_refresh_token from the oauth process (since Dropbox does not offer long lived tokens) and the app_key from the website's registered app"""
        self.dbx = dropbox.Dropbox(
            oauth2_refresh_token=oauth_refresh_token, app_key=app_key
        )
        self.account_display_name = (
            self.dbx.users_get_current_account().name.display_name
        )
        print(f"account_info: {self.account_display_name}")

    def upload_to_nixplay(self, file_bytes: bytes, file_name: str) -> str:
        return self.upload_file_bytes(file_bytes, f"/nixplay-automatic/{file_name}")

    def clear_nixplay_folder(self):
        return self.delete_files_from_folder("/nixplay-automatic")

    def upload_file_bytes(self, file_bytes: bytes, dropbox_file_path: str) -> str:
        """Copy the given byte string to the file path"""
        results = self.dbx.files_upload(file_bytes, dropbox_file_path)
        print(f"\t\t {results}")
        return results.path_display

    def upload_file(self, local_file_path: str, dropbox_file_path: str) -> str:
        """Upload a local file"""
        with open(local_file_path, "rb") as file:
            file_bytes = file.read()
        results = self.dbx.files_upload(file_bytes, dropbox_file_path)
        print(f"\t\t {results}")
        return results.path_display

    def delete_files_from_folder(self, folder_path: str) -> int:
        """Delete all files in the given folder and return the number of files deleted"""
        files = self.list_files_in_folder(folder_path)
        if len(files) == 0:
            return 0
        for count, file in enumerate(files):
            print(f"Deleting from Dropbox #{count}: {file.path_lower}")
            self.dbx.files_delete(file.path_lower)
        return count + 1

    def list_files_in_folder(self, folder_path: str) -> list:
        """Return a list of files in the given folder"""
        file_list = []
        results = self.dbx.files_list_folder(folder_path)
        file_list.extend(results.entries)
        while results.has_more:
            results = self.dbx.files_list_folder_continue(results.cursor)
            file_list.extend(results.entries)

        return file_list
