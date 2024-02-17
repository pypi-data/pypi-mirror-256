""" Copyright Xplainable Pty Ltd"""
import json
import pandas as pd
import pyperclip
import inspect
import ast
import sys
import xplainable

import requests
from urllib3.exceptions import HTTPError

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from xplainable.preprocessing.pipeline import XPipeline
from xplainable.preprocessing import transformers as xtf
from xplainable.utils.model_parsers import *
from xplainable.quality.scanner import XScan

from xplainable_client.utils.exceptions import AuthenticationError
from xplainable_client.utils.helpers import get_df_delta
from xplainable_client.utils.encoders import NpEncoder, force_json_compliant
from xplainable_client.utils.metrics import evaluate_classification, evaluate_regression

import ipywidgets

class Client:
    """ A client for interfacing with the xplainable web api (xplainable cloud).

    Access models, preprocessors and user data from xplainable cloud. API keys
    can be generated at https://beta.xplainable.io.

    Args:
        api_key (str): A valid api key.
    """

    def __init__(self, api_key=None, hostname='https://api.xplainable.io'):
        if not api_key:
            raise ValueError('A valid API Key is required. Generate one from the xplainable app.')
        
        self.api_key = api_key
        self.hostname = hostname
        self._setup_session()  # Set up the session and other initialization steps

        # Assuming get_user_data and other necessary methods are defined within this class
        self.user_data = self.get_user_data()
        self._user = self._parse_user_data(self.user_data)
        self.__org_id = self.user_data['organisation_id']
        self.__team_id = self.user_data['team_id']
        self.__ext = f'organisations/{self.__org_id}/teams/{self.__team_id}'
        
        # You can still use the _render_init_table here if you want to display it,
        # or you can return the data dict for a more script-friendly approach.
        data = self._gather_initialization_data()
        self._render_init_table(data)

    def _setup_session(self):
        """ Set up the session with retry strategy and session headers. """
        self._session = requests.Session()
        self._session.headers['api_key'] = self.api_key
        retry_strategy = Retry(total=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount(self.hostname, adapter)

    def _parse_user_data(self, data):
        """ Parse the user data received from the API. """
        return {
            'username': data['username'],
            'organisation_name': data['organisation_name'],
            'team_name': data['team_name'],
        }

    def _gather_initialization_data(self):
        """ Gather data to display or return upon initialization. """
        version_info = sys.version_info
        self.python_version = f'{version_info.major}.{version_info.minor}.{version_info.micro}'
        self.xplainable_version = xplainable.__version__
        
        return {
            "xplainable version": self.xplainable_version,
            "python version": self.python_version,
            "user": self._user['username'],
            "organisation": self._user['organisation_name'],
            "team": self._user['team_name'],
        }
    
    @staticmethod
    def _get_xplainable_version():
        """Retrieve the installed xplainable package version."""
        try:
            # Access the __version__ attribute from the xplainable package
            return xplainable.__version__
        except AttributeError:
            # Handle the case where __version__ is not defined
            return "Unknown"
    
    @staticmethod
    def _render_init_table(data):

        from xplainable.gui.components import KeyValueTable, Header
        table = KeyValueTable(
            data,
            transpose=False,
            padding="0px 45px 0px 5px",
            table_width='auto',
            header_color='#e8e8e8',
            border_color='#dddddd',
            header_font_color='#20252d',
            cell_font_color= '#374151'
            )

        header = Header('Initialised', 30, 16, avatar=False)
        header.divider.layout.display = 'none'
        header.title = {'margin':'4px 0 0 8px'}
        output = ipywidgets.VBox([header.show(), table.html_widget])
        display(output)

    def ping_server(self, hostname):
        response = self._session.get(
            f'{hostname}/v1/compute/ping',
            timeout=1
            )
        content = json.loads(response.content)
        if content == True:
            return True
        else:
            return False

    def ping_gateway(self, hostname):
        response = self._session.get(
            f'{hostname}/v1/ping',
            timeout=1
            )
        content = json.loads(response.content)
        if content == True:
            return True
        else:
            return False

    def get_response_content(self, response):
        if response.status_code == 200:
            return json.loads(response.content)

        elif response.status_code == 401:
            err_string = "401 Unauthorised"
            content = json.loads(response.content)
            if 'detail' in content:
                err_string = err_string + f" ({content['detail']})"
            
            raise HTTPError(err_string)

        else:
            raise HTTPError(response.status_code, json.loads(response.content))

    def list_models(self) -> list:
        """ Lists all models of the active user's team.

        Returns:
            dict: Dictionary of saved models.
        """

        response = self._session.get(
            url=f'{self.hostname}/v1/{self.__ext}/models'
            )

        data = self.get_response_content(response)
        
        # For better readability
        [i.pop('user') for i in data]
        [i.pop('contributors') for i in data]

        return data

    def list_model_versions(self, model_id: int) -> list:
        """ Lists all versions of a model.

        Args:
            model_id (int): The model id

        Returns:
            dict: Dictionary of model versions.
        """

        response = self._session.get(
            url=f'{self.hostname}/v1/{self.__ext}/models/{model_id}/versions'
            )

        data = self.get_response_content(response)
        [i.pop('user') for i in data]

        return data
    
    def list_preprocessors(self) -> list:
        """ Lists all preprocessors of the active user's team.

        Returns:
            dict: Dictionary of preprocessors.
        """

        response = self._session.get(
            url=f'{self.hostname}/v1/{self.__ext}/preprocessors'
            )

        data = self.get_response_content(response)
        [i.pop('user') for i in data]

        return data

    def list_preprocessor_versions(self, preprocessor_id: int) -> list:
        """ Lists all versions of a preprocessor.

        Args:
            preprocessor_id (int): The preprocessor id

        Returns:
            dict: Dictionary of preprocessor versions.
        """

        response = self._session.get(
            url=f'{self.hostname}/v1/{self.__ext}/preprocessors/{preprocessor_id}/versions'
            )
        
        data = self.get_response_content(response)
        [i.pop('user') for i in data]

        return data


    def load_preprocessor(
            self, preprocessor_id: int, version_id: int,
            gui_object: bool = False, response_only: bool = False):
        """ Loads a preprocessor by preprocessor_id and version_id.

        Args:
            preprocessor_id (int): The preprocessor id
            version_id (int): The version id
            response_only (bool, optional): Returns the preprocessor metadata.

        Returns:
            xplainable.preprocessing.pipeline.Pipeline: The loaded pipeline
        """

        def build_transformer(stage):
            """Build transformer from metadata"""

            if not hasattr(xtf, stage["name"]):
                raise ValueError(f"{stage['name']} does not exist in the transformers module")

            # Get transformer function
            func = getattr(xtf, stage["name"])

            return func(**stage['params'])
        
        try:
            preprocessor_response = self._session.get(
                url=f'{self.hostname}/v1/{self.__ext}/preprocessors/{preprocessor_id}/versions/{version_id}'
                )

            response = self.get_response_content(preprocessor_response)

            if response_only:
                return response

        except Exception as e:
            raise ValueError(
            f'Preprocessor with ID {preprocessor_id}:{version_id} does not exist')
        
        stages = response['stages']
        deltas = response['deltas']

        pipeline = XPipeline()
        pipeline.stages = [{"feature": i["feature"], "name": i["name"], \
                "transformer": build_transformer(i)} for i in stages]
        
        if not gui_object:
            return pipeline

        else:
            from ..gui.screens.preprocessor import Preprocessor
            pp = Preprocessor()
            pp.pipeline = pipeline
            pp.df_delta = deltas
            pp.state = len(pipeline.stages)

            return pp
    
    def load_classifier(self, model_id: int, version_id: int, model=None):
        """ Loads a binary classification model by model_id

        Args:
            model_id (str): A valid model_id
            version_id (str): A valid version_id
            model (PartitionedClassifier): An existing model to add partitions

        Returns:
            xplainable.PartitionedClassifier: The loaded xplainable classifier
        """

        response = self.__get_model__(model_id, version_id)
        if response['model_type'] != 'binary_classification':
            raise ValueError(f'Model with ID {model_id}:{version_id} is not a binary classification model')

        return parse_classifier_response(response, model)

    def load_regressor(self, model_id: int, version_id: int, model=None):
        """ Loads a regression model by model_id and version_id

        Args:
            model_id (str): A valid model_id
            version_id (str): A valid version_id
            model (PartitionedRegressor): An existing model to add partitions to

        Returns:
            xplainable.PartitionedRegressor: The loaded xplainable regressor
        """
        response = self.__get_model__(model_id, version_id)
        if response['model_type'] != 'regression':
            raise ValueError(f'Model with ID {model_id}:{version_id} is not a regression model')

        return parse_regressor_response(response, model)

    def __get_model__(self, model_id: int, version_id: int):
        try:
            response = self._session.get(
                url=f'{self.hostname}/v1/{self.__ext}/models/{model_id}/versions/{version_id}'
            )
            return self.get_response_content(response)

        except Exception as e:
            raise ValueError(f'Model with ID {model_id}:{version_id} does not exist')

    def get_user_data(self) -> dict:
        """ Retrieves the user data for the active user.

        Returns:
            dict: User data
        """
        
        response = self._session.get(
            url=f'{self.hostname}/v1/client-connect'
        )

        if response.status_code == 200:
            return self.get_response_content(response)
        
        else:
            raise AuthenticationError(
                f"{response.status_code} Unauthenticated. "
                f"{response.json()['detail']}"
            )

    def create_preprocessor_id(
            self, preprocessor_name: str, preprocessor_description: str) -> str:
        """ Creates a new preprocessor and returns the preprocessor id.

        Args:
            preprocessor_name (str): The name of the preprocessor
            preprocessor_description (str): The description of the preprocessor

        Returns:
            int: The preprocessor id
        """

        payoad = {
            "preprocessor_name": preprocessor_name,
            "preprocessor_description": preprocessor_description
        }

        response = self._session.post(
            url=f'{self.hostname}/v1/{self.__ext}/create-preprocessor',
            json=payoad
        )
        
        preprocessor_id = self.get_response_content(response)
            
        return preprocessor_id
    
    def create_preprocessor_version(
            self, preprocessor_id: str, pipeline: list, df: pd.DataFrame = None
            ) -> str:
        """ Creates a new preprocessor version and returns the version id.

        Args:
            preprocessor_id (int): The preprocessor id
            pipeline (xplainable.preprocessing.pipeline.Pipeline): pipeline

        Returns:
            int: The preprocessor version id
        """

        # Structure the stages and deltas
        stages = []
        deltas = []
        if df is not None:
            before = df.copy()
            deltas.append({"start": json.loads(before.head(10).to_json(
                orient='records'))})
            delta_gen = pipeline.transform_generator(before)

        for stage in pipeline.stages:
            step = {
                'feature': stage['feature'],
                'name': stage['name'],
                'params': stage['transformer'].__dict__
            }

            stages.append(step)

            if df is not None:
                after = delta_gen.__next__()
                delta = get_df_delta(before.copy(), after.copy())
                deltas.append(delta)
                before = after.copy()

        # Get current versions
        versions = {
                "xplainable_version": self.xplainable_version,
                "python_version": self.python_version
            }

        # Create payload
        payload = {
            "stages": stages,
            "deltas": deltas,
            "versions": versions
            }
        
        # Create a new version and fetch id
        url = (
            f'{self.hostname}/v1/{self.__ext}/preprocessors/'
            f'{preprocessor_id}/add-version'
            )
        
        response = self._session.post(url=url, json=payload)

        version_id = self.get_response_content(response)

        return version_id
        
    def _detect_model_type(self, model):

        if 'Partitioned' in model.__class__.__name__:
            model = model.partitions['__dataset__']

        cls_name = model.__class__.__name__

        if cls_name == "XClassifier":
            model_type = "binary_classification"

        elif cls_name == "XRegressor":
            model_type = "regression"

        else:
            raise ValueError(
                f'Model type {cls_name} is not supported')
        
        return model_type, model.target

    def create_model_id(
            self, model, model_name: str, model_description: str) -> str:
        """ Creates a new model and returns the model id.

        Args:
            model_name (str): The name of the model
            model_description (str): The description of the model
            model (XClassifier | XRegressor): The model to create.

        Returns:
            int: The model id
        """

        model_type, target = self._detect_model_type(model)

        payoad = {
            "model_name": model_name,
            "model_description": model_description,
            "model_type": model_type,
            "target_name": target,
            "algorithm": model.__class__.__name__
        }
        
        response = self._session.post(
            url=f'{self.hostname}/v1/{self.__ext}/create-model',
            json=payoad
        )
        
        model_id = self.get_response_content(response)
            
        return model_id

    def create_model_version(
            self, model, model_id: str, x: pd.DataFrame, y: pd.Series) -> str:
        """ Creates a new model version and returns the version id.

        Args:
            model_id (int): The model id
            partition_on (str): The partition column name
            ruleset (dict | str): The feeature ruleset
            health_info (dict): Feature health information
            versions (dict): Versions of current environment

        Returns:
            int: The model version id
        """

        # Get current versions
        versions = {
                "xplainable_version": self.xplainable_version,
                "python_version": self.python_version
            }

        partition_on = model.partition_on if 'Partitioned' in \
            model.__class__.__name__ else None

        payload = {
            "partition_on": partition_on,
            "versions": versions,
            "partitions": []
            }

        partitioned_models = ['PartitionedClassifier', 'PartitionedRegressor']
        independent_models = ['XClassifier', 'XRegressor']

        # get all partitions
        if model.__class__.__name__ in partitioned_models:
            for p, m in model.partitions.items():
                if p == '__dataset__':
                    part_x = x
                    part_y = y

                else:
                    part_x = x[x[partition_on].astype(str) == str(p)]
                    part_y = y[y.index.isin(part_x.index)]

                pdata = self._get_partition_data(m, p, part_x, part_y)
                payload['partitions'].append(pdata)
        
        elif model.__class__.__name__ in independent_models:
            pdata = self._get_partition_data(model, '__dataset__', x, y)
            payload['partitions'].append(pdata)
        
        # Create a new version and fetch id
        url = f'{self.hostname}/v1/{self.__ext}/models/{model_id}/add-version'
        response = self._session.post(
            url=url, json=force_json_compliant(payload))

        version_id = self.get_response_content(response)

        return version_id

    def _get_partition_data(
            self, model, partition_name: str, x: pd.DataFrame,
            y: pd.Series) -> dict:
        """ Logs a partition to a model version.

        Args:
            model_type (str): The model type
            partition_name (str): The name of the partition column
            model (mixed): The model to log
            model_id (int): The model id
            version_id (int): The version id
            evaluation (dict, optional): Model evaluation data and metrics.
            training_metadata (dict, optional): Model training metadata.

        """

        model_type, _ = self._detect_model_type(model)

        data = {
            "partition": str(partition_name),
            "profile": json.dumps(model._profile, cls=NpEncoder),
            "feature_importances": json.loads(
                json.dumps(model.feature_importances, cls=NpEncoder)),
            "id_columns": json.loads(
                json.dumps(model.id_columns, cls=NpEncoder)),
            "columns": json.loads(
                json.dumps(model.columns, cls=NpEncoder)),
            "parameters": model.params.to_json(),
            "base_value": json.loads(
                json.dumps(model.base_value, cls=NpEncoder)),
            "feature_map": json.loads(
                json.dumps({k: fm.forward for k, fm in model.feature_map.items()}, cls=NpEncoder)),
            "target_map": json.loads(
                json.dumps(model.target_map.reverse, cls=NpEncoder)),
            "category_meta": json.loads(
                json.dumps(model.category_meta, cls=NpEncoder)),
            # "constructs": model.constructs_to_json(),
            "calibration_map": None,
            "support_map": None
        }

        if model_type == 'binary_classification':
            data.update({
                "calibration_map": json.loads(
                    json.dumps(model._calibration_map, cls=NpEncoder)),
                "support_map": json.loads(
                    json.dumps(model._support_map, cls=NpEncoder))
            })

            evaluation = model.metadata.get('evaluation', {})
            if evaluation == {}:
                y_prob = model.predict_score(x)

                if model.target_map:
                    y = y.map(model.target_map)

                evaluation = {
                    'train': evaluate_classification(y, y_prob)
                }
                
        elif model_type == 'regression':
            evaluation = model.metadata.get('evaluation', {})
            if evaluation == {}:
                y_pred = model.predict(x)
                evaluation = {
                            'train': evaluate_regression(y, y_pred)
                        }
        
        data["evaluation"] = json.dumps(evaluation, cls=NpEncoder)

        training_metadata = {
            i: v for i, v in model.metadata.items() if i != "evaluation"}
        
        data["training_metadata"] = json.dumps(training_metadata, cls=NpEncoder)
        
        if x is not None:
            scanner = XScan()
            scanner.scan(x)

            results = []
            for i, v in scanner.profile.items():
                feature_info = {
                    "feature": i,
                    "description": '',
                    "type": v['type'],
                    "health_info": json.loads(json.dumps(v, cls=NpEncoder))
                }
                results.append(feature_info)

            data["health_info"] = json.dumps(results, cls=NpEncoder)

        return data
    
    def list_deployments(self):
        """ Lists all deployments of the active user's team.

        Returns:
            dict: Dictionary of deployments.
        """

        response = self._session.get(
            url=f'{self.hostname}/v1/{self.__ext}/deployments'
            )

        deployments = self.get_response_content(response)

        return deployments

    def deploy(
            self, model_id: str, version_id: str,
            hostname: str='https://inference.xplainable.io',
            location: str='syd', raw_output: bool=True) -> dict:
        """ Deploys a model partition to xplainable cloud.

        The hostname should be the url of the inference server. For example:
        https://inference.xplainable.io

        Args:
            hostname (str): The host name for the inference server
            model_id (int): The model id
            version_id (int): The version id
            partition_id (int): The partition id
            raw_output (bool, optional): returns a dictionary

        Returns:
            dict: deployment status and details.
        """
        
        url = (
            f'{self.hostname}/v1/{self.__ext}/models/{model_id}/versions/'
            f'{version_id}/deploy'
        )

        body = {
            "location": location
        }

        response = self._session.put(url, json=body)
        
        if response.status_code == 200:

            deployment_id = response.json()['deployment_id']

            data = {
                "deployment_id": deployment_id,
                "status": "inactive",
                "location": location,
                "endpoint": f"{hostname}/v1/predict"
            }

            return data

        else:
            return {
                "message": f"Failed with status code {response.status_code}"}

    def activate_deployment(self, deployment_id):
        """ Activates a model deployment.

        Args:
            deployment_id (str): The deployment id
        """

        url = (
            f'{self.hostname}/v1/{self.__ext}/deployments/{deployment_id}/activate'
        )

        response = self._session.patch(url)

        if response.status_code == 200:
            return response.json()

        else:
            return {
                "message": f"Failed with status code {response.status_code}"}
    
    def deactivate_deployment(self, deployment_id):
        """ Deactivates a model deployment.

        Args:
            deployment_id (str): The deployment id
        """

        url = (
            f'{self.hostname}/v1/{self.__ext}/deployments/{deployment_id}/deactivate'
        )

        response = self._session.patch(url)

        if response.status_code == 200:
            return response.json()

        else:
            return {
                "message": f"Failed with status code {response.status_code}"}
        
    def generate_deploy_key(
            self, description: str, deployment_id: str, 
            days_until_expiry: float = 90, clipboard: bool = True,
            surpress_output: bool = False
            ) -> None:
        """ Generates a deploy key for a model deployment.

        Args:
            description (str): Description of the deploy key use case.
            deployment_id (str): The deployment id.
            days_until_expiry (float): The number of days until the key expires.
            surpress_output (bool): Surpress output. Defaults to False.

        Returns:
            None: No key is returned. The key is copied to the clipboard.
        """

        url = f'{self.hostname}/v1/{self.__ext}/deployments/{deployment_id}/create-deploy-key'
        
        params = {
            'description': description,
            'days_until_expiry': days_until_expiry
        }
        
        response = self._session.put(
            url=url,
            json=params
            )

        deploy_key = response.json()

        if deploy_key:
            if not clipboard:
                return deploy_key
            pyperclip.copy(deploy_key['deploy_key'])
            if not surpress_output:
                print("Deploy key copied to clipboard!")
        else:
            raise ConnectionError(
                f"Falied to generate deploy key. Code: {response.status_code}")
        
    def generate_example_deployment_payload(self, deployment_id):
        """ Generates an example deployment payload for a deployment.

        Args:
            deployment_id (str): The deployment id.
        """

        url = f'{self.hostname}/v1/{self.__ext}/deployments/{deployment_id}/payload'

        response = self._session.get(url)

        return response.json()
    
    @staticmethod
    def __parse_function(func):
        """ Parses a function to a middleware function. """
        if not callable(func):
            raise Exception("Function must be callable")

        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        if len(params) != 1:
            raise Exception("Function must take one parameter")

        # Parse the source code to an AST
        source = inspect.getsource(func)
        parsed_ast = ast.parse(source)

        # Rename the function in the AST
        for node in ast.walk(parsed_ast):
            if isinstance(node, ast.FunctionDef) and node.name == func.__name__:
                node.name = "middleware"
                break

        # Store the modified source
        modified_source = ast.unparse(parsed_ast)

        # Compile the AST back to code and execute in a new namespace
        local_vars = {}
        exec(compile(
            parsed_ast, filename="<ast>", mode="exec"),
            func.__globals__, local_vars)

        middleware = local_vars['middleware']
        middleware.source = modified_source
        return middleware
        
    def add_deployment_middleware(
        self, deployment_id, func, name, description=None):
        """ Adds or replaces a middleware function to a deployment.

        Args:
            deployment_id (str): The deployment id
            func (function): The middleware function
        """

        url = (
            f'{self.hostname}/v1/{self.__ext}/deployments/{deployment_id}/add-middleware'
        )

        # Convert function to expected name
        if func.__name__ != 'middleware':
            func = self.__parse_function(func)
            source_code = func.source
        
        else:
            source_code = inspect.getsource(func)

        body = {
            "code_block": source_code,
            "name": name,
            "description": description
        }

        response = self._session.put(
            url=url,
            json=body
            )

        return response.json()
    
    def delete_deployment_middleware(self, deployment_id):
        """ Deletes a middleware function from a deployment.

        Args:
            deployment_id (str): The deployment id
        """

        url = (
            f'{self.hostname}/v1/{self.__ext}/deployments/{deployment_id}/middleware'
        )

        response = self._session.delete(url)

        return {"status_code": response.status_code}

    def _gpt_report(
            self, model_id, version_id, target_description='',
            project_objective='', max_features=15, temperature=0.5):

        url = (
            f'{self.hostname}/v1/{self.__ext}/models/{model_id}/versions/'
            f'{version_id}/generate-report'
        )

        params = {
            'target_description': target_description,
            'project_objective': project_objective,
            'max_features': max_features,
            'temperature': temperature
        }

        response = self._session.put(
            url=url,
            json=params,
            )
        
        content = self.get_response_content(response)

        return content

    @staticmethod
    def _render_init_table(data):

        from xplainable.gui.components import KeyValueTable, Header
        table = KeyValueTable(
            data,
            transpose=False,
            padding="0px 45px 0px 5px",
            table_width='auto',
            header_color='#e8e8e8',
            border_color='#dddddd',
            header_font_color='#20252d',
            cell_font_color= '#374151'
            )

        header = Header('Initialised', 30, 16, avatar=False)
        header.divider.layout.display = 'none'
        header.title = {'margin':'4px 0 0 8px'}
        output = ipywidgets.VBox([header.show(), table.html_widget])
        display(output)