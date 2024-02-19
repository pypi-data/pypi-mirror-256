import requests
from typing import Any, Dict, Callable, Optional
from datetime import datetime
import os
import time

import requests
from datetime import datetime


class A3mConnect:
    """Class representing a connection to A3m API."""

    default_option = {
        'base_url': 'base_url',
        'scope': 'scope',
    }

    default_token_data = {
        'access_token': '',
        'refresh_token': '',
        'token_type': '',
        'expires_in': 0,
        'scope': '',
    }

    def __init__(self, user_key: str, user_secret: str, options):
        """
        Initialize A3mConnect instance.

        Parameters:
        - user_key (str): User key for authentication.
        - user_secret (str): User secret for authentication.
        - options (dict): Additional options for the connection.
        """
        self.user_key = user_key
        self.user_secret = user_secret
        # Merge default options with provided options
        self.options = {**self.default_option, **options}
        self.is_init = False
        self.token_data = {**self.default_token_data}
        self.time_data = {
            'token_time': None,
            'ref_token_time': None,
        }

    def get_user_keys(self):
        """
        Get user keys.

        Returns:
        dict: Dictionary containing user_key and user_secret.
        """
        return {
            'user_key': self.user_key,
            'user_secret': self.user_secret,
        }

    def get_options(self):
        """
        Get connection options.

        Returns:
        dict: Connection options.
        """
        return self.options

    def get_token_data(self):
        """
        Get token data.

        Returns:
        dict: Token data.
        """
        if not self.is_init:
            self.init()
        return self.token_data

    def is_token_expired(self):
        """
        Check if the access token is expired.

        Returns:
        bool: True if the access token is expired, False otherwise.
        """
        cur_date = datetime.utcnow()
        return (
            (cur_date - self.time_data['token_time']).total_seconds() >
            (self.token_data['expires_in'] - 180)
        )

    def is_ref_token_expired(self):
        """
        Check if the refresh token is expired.

        Returns:
        bool: True if the refresh token is expired, False otherwise.
        """
        cur_date = datetime.utcnow()
        return (cur_date - self.time_data['ref_token_time']).days > 6

    def get_all_data(self):
        """
        Get all data related to the connection.

        Returns:
        A3mConnect: A3mConnect instance.
        """
        if not self.is_init:
            self._init()
        return self

    def is_connected(self):
        """
        Check if the instance is connected and handle token refreshing.

        Returns:
        A3mConnect: A3mConnect instance.
        """
        try:
            if not self.is_init:
                return self.init()
            elif self.is_ref_token_expired():
                return self.init()
            elif self.is_token_expired():
                return self.refresh_access_token()
            else:
                return self
        except Exception as e:
            raise Exception(e)

    def init(self):
        """
        Initialize the connection and retrieve access and refresh tokens.

        Returns:
        A3mConnect: A3mConnect instance.
        """
        try:
            params = {
                'grant_type': 'password',
                'username': self.user_key,
                'password': self.user_secret,
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }

            response = requests.post(
                f"{self.options['base_url']}/token", headers=headers,
                data=params
            )

            response_data = response.json()
            self.token_data = {**self.token_data, **response_data}
            self.time_data = {
                'token_time': datetime.utcnow(),
                'ref_token_time': datetime.utcnow(),
            }

            self.is_init = True
            return self
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error during initialization: {e}")

    def refresh_access_token(self):
        """
        Refresh the access token using the refresh token.

        Returns:
        A3mConnect: A3mConnect instance.
        """
        try:
            params = {
                'grant_type': 'refresh_token',
                'refresh_token': self.token_data['refresh_token'],
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }

            response = requests.post(
                f"{self.options['base_url']}/token", headers=headers,
                data=params
            )

            response_data = response.json()
            self.token_data = {**self.token_data, **response_data}
            self.time_data['token_time'] = datetime.utcnow()
            return self
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error refreshing access token: {e}")


class Aimped(A3mConnect):
    """
    Class representing a connection to the Aimped API, extending A3mConnect.

    Args:
        user_key (str): User key for authentication.
        user_secret (str): User secret for authentication.
        options (dict): Additional options for the connection.
    """

    def __init__(self, user_key, user_secret, options):
        """
        Initialize Aimped instance.

        Args:
            user_key (str): User key for authentication.
            user_secret (str): User secret for authentication.
            options (dict): Additional options for the connection.
        """
        super().__init__(user_key, user_secret, options)

    def run_model(self, model_id: int, payload: Dict[str, Any]) -> Any:
        """
        Run a model prediction.

        Args:
            model_id (int): The ID of the model to run.
            payload (dict): Input payload for the model.

        Returns:
            Any: Result of the model prediction.
        """
        try:
            if self.is_connected():
                headers = {
                    'Authorization': f'Bearer {self.token_data["access_token"]}',
                    'Content-Type': 'application/json',
                }
                result = requests.request(
                    'POST',
                    f'{self.options["base_url"]}/pub/backend/api/v1/model_run_prediction/{model_id}/',
                    json=payload, headers=headers
                )

                return result.json()

        except requests.exceptions.RequestException as e:
            raise Exception(e)

    def get_pod_log_result(self, model_id: int) -> Dict[str, Any]:
        """
        Get the result of the pod logs for a specific model.

        Args:
            model_id (int): The ID of the model.

        Returns:
            dict: Result of the pod logs.
        """
        try:
            result = requests.request(
                'GET',
                f'{self.options["base_url"]}/pub/backend/get_pod_log?model_id={model_id}&instance_id=&is_dedicated='
            )
            return result.json()
        except requests.exceptions.RequestException as e:
            raise Exception(e)

    def run_model_callback(
        self,
        model_id: int,
        payload: Dict[str, Any],
        callback: Callable[[str, str, str, Optional[str]], str]
    ) -> Any:
        """
        Run a model with a callback function to monitor its progress.

        Args:
            model_id (int): The ID of the model to run.
            payload (dict): Input payload for the model.
            callback (Callable): Callback function to monitor model progress.

        Returns:
            Any: Result of the model prediction.
        """
        try:
            if self.is_connected():
                callback(
                    event='start',
                    message='start model run',
                    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

                result = self.run_model(model_id, payload)

                keep_running = True
                while keep_running:
                    time.sleep(15)
                    pod_log_result = self.get_pod_log_result(model_id)

                    waiting = pod_log_result.get('waiting', '').replace(
                        'Container', '') if pod_log_result.get('waiting') else None

                    if waiting:
                        if waiting == 'CrashLoopBackOff':
                            callback(
                                event='error',
                                message='Model is CrashLoopBackOff.',
                                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            )
                            keep_running = False
                        else:
                            callback(
                                event='proccess',
                                message=f'Model is {waiting}',
                                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            )
                    elif pod_log_result.get('error'):
                        callback(
                            event='error',
                            message=pod_log_result['error'],
                            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        )
                        keep_running = False

                    elif pod_log_result.get('running'):
                        time.sleep(10)
                        result = self.run_model(model_id, payload)
                        callback(
                            event='end',
                            message='ok',
                            data=result,
                            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        )
                        keep_running = False
                    else:
                        callback(
                            event='proccess',
                            message='Waiting for model to be ready',
                            time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        )

        except Exception as e:
            callback(
                event='error',
                message=str(e),
                time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )

    def file_upload(self, model_id: int, filepath: str):
        """
        Upload a file to the specified model.

        Args:
            model_id (int): The ID of the model.
            filepath (str): Path to the file to be uploaded.

        Returns:
            dict: Result of the file upload operation.
        """
        try:
            if self.is_connected():
                with open(filepath, 'rb') as file:
                    files = {'file': (os.path.basename(filepath), file)}
                    headers = {
                        'Authorization': f'Bearer {self.token_data["access_token"]}'
                    }
                    result = requests.post(
                        f'{self.options["base_url"]}/pub/backend/api/v1/file_upload/{model_id}',
                        files=files,
                        headers=headers,
                    )
                    return result.json()
        except requests.exceptions.RequestException as e:
            raise Exception(e)

    def file_download_and_save(self, filepath: str, destination: str):
        """
        Download a file from the specified filepath and save it to the destination.

        Args:
            filepath (str): Path to the file to be downloaded.
            destination (str): Path where the downloaded file will be saved.

        Returns:
            str: Path of the downloaded file.
        """
        try:
            if self.is_connected():
                headers = {
                    'Authorization': f'Bearer {self.token_data["access_token"]}',
                }
                result = requests.get(
                    f'{self.options["base_url"]}/pub/backend/api/v1/file_download?file={filepath}',
                    headers=headers,
                    stream=True,
                )

                with open(destination, 'wb') as file:
                    for chunk in result.iter_content(chunk_size=128):
                        file.write(chunk)
                return filepath
        except requests.exceptions.RequestException as e:
            raise Exception(e)
