import requests
import logging
import pandas as pd

from .datascience.helpers import get_ising_coeffs as feature_selection_coefs

class Client:
    """
    Python client meant to interact with the circuit composer service
    """

    def __init__(self,
                 user: str,
                 password: str,
                 api_server_url: str = "http://api.kipustack.com"):

        # Endpoint(s)
        self._api_server_url = api_server_url

        # User information (token refresh)
        self._user = requests.utils.quote(user)
        self._pasw = requests.utils.quote(password)

        # Auth header
        self._login()

    def _login(self):
        """
        Login action retrieving the token for the session
        """
        url = f"{self._api_server_url}/iam/authentication/login"
        url += f"?email={self._user}"
        url += f"&password={self._pasw}"

        headers = {"accept" : "application/json"}

        r = requests.get(url=url, headers=headers, timeout=5)

        if r.status_code == 200:
            response = r.json()
            logging.info("Successfully logged in!")
            self.header = {
                'authorization' : f"Bearer {response['access_token']}"
            }
        else:
            response = r.json()
            logging.error(f"Something went wrong: {response['detail']}")

    def refresh_token(self):
        """
        Re-login to refresh the session token
        """
        self._login()

    def optimize_portfolio(self, profit: list, risk: list, cost: list, budget: float):
        """
        Given a dataframe containing the evolution of finance instruments, builds the 
        QUBO model so that it can be solved by the DCQO endpoint obtaining best portfolio
        configuration.
        """
        # Build QUBO

        # Send to optimization endpoint

        raise NotImplementedError

    def compose_circuit(self,
                        linear_coeffs: list,
                        quadratic_coeffs : dict,
                        T:float = 0.03,
                        N:int = 3,
                        mode:str = "FULL"):
        """
        Given an Ising model gets solved by the DCQO endpoint
        """
        # Get coefficients
        ising = {
            "h" : linear_coeffs,
            "J" : quadratic_coeffs
        }

        # Send to optimization endpoint
        endpoint = f"/optimization/composer/dcqo?mode={mode}&T={T}&N={N}"
        url = f"{self._api_server_url}{endpoint}"
        r = requests.post(url=url, headers=self.header, json=ising, timeout=5)

        if r.status_code == 200:
            response = r.json()
            return response
        else:
            logging.error(f"Something went wrong: {r.status_code} {r.reason}")

    def feature_selection(self,
                          data: pd.DataFrame,
                          target:str,
                          max_features: int,
                          reg_lambda: float = 5.0):
        """
        Given a dataframe containing a dataset, builds the 
        QUBO model so that it can be solved by the DCQO endpoint
        on which features should be selected
        """
        # Get coefficients
        h, jp = feature_selection_coefs(data, target, max_features, reg_lambda)
        ising = {
            "h" : h,
            "J" : jp
        }

        # Send to optimization endpoint
        endpoint = "/optimization/composer/dcqo"
        url = f"{self._api_server_url}{endpoint}"
        r = requests.post(url=url, headers=self.header, json=ising, timeout=5)

        if r.status_code == 200:
            response = r.json()
            return response
        else:
            logging.error(f"Something went wrong: {r.status_code} {r.reason}")
