import json
import logging
import os
import time
from typing import Any, Optional

from google.auth.transport import requests as google_requests
from google.oauth2 import service_account
from llama_index.llms import LLM, AzureOpenAI, OpenAI, Vertex
from llama_index.llms.base import CompletionResponse
from unstract.adapters.constants import Common
from unstract.adapters.llm import adapters
from unstract.adapters.llm.llm_adapter import LLMAdapter
from unstract.sdk.adapters import ToolAdapter
from unstract.sdk.constants import LogLevel, ToolSettingsKey
from unstract.sdk.tool.base import BaseTool
from unstract.sdk.utils.service_context import ServiceContext

logger = logging.getLogger(__name__)


class ToolLLM:
    """Class to handle LLMs for Unstract Tools."""

    def __init__(
        self,
        tool: BaseTool,
        llm_id: str = "Azure OpenAI",
        tool_settings: dict[str, str] = {},
    ):
        """

        Notes:
            - "Azure OpenAI" : Environment variables required
            OPENAI_API_KEY,OPENAI_API_BASE, OPENAI_API_VERSION,
            OPENAI_API_ENGINE, OPENAI_API_MODEL

        Args:
            tool (AbstractTool): Instance of AbstractTool
            llm_id (str): The id of the LLM to use.
        """
        self.tool = tool
        self.llm_id = llm_id
        self.max_tokens = 1024 * 4
        self.llm_adapters = adapters
        self.llm_adapter_instance_id = tool_settings.get(
            ToolSettingsKey.LLM_ADAPTER_ID
        )

    @staticmethod
    def run_completion(
        llm: LLM,
        platform_api_key: str,
        prompt: str,
        retries: int = 3,
        **kwargs: Any,
    ) -> Optional[dict[str, Any]]:
        ServiceContext.get_service_context(
            platform_api_key=platform_api_key, llm=llm
        )
        for i in range(retries):
            try:
                response: CompletionResponse = llm.complete(prompt, **kwargs)
                result = {
                    "response": response,
                }

                return result
            except Exception as e:
                if i == retries - 1:
                    raise e
                time.sleep(5)
        return None

    def __get_llm(self) -> Optional[LLM]:
        # This method is deprecated.
        """Returns the LLM object for the tool.

        Returns:
            Optional[LLM]: The LLM object for the tool.
           (llama_index.llms.base.LLM)
        """
        if self.llm_id == "Azure OpenAI":
            # TODO: Retire this llm_id
            # We are using the 4k context. Change if required
            self.max_tokens = 1024 * 4
            llm = AzureOpenAI(
                # model=os.environ.get(
                #     "OPENAI_API_MODEL","gpt-3.5-turbo-16k-0613"),
                deployment_name=os.environ.get("OPENAI_API_ENGINE"),
                engine=os.environ.get("OPENAI_API_ENGINE"),
                api_key=os.environ.get("OPENAI_API_KEY"),
                api_version=os.environ.get("OPENAI_API_VERSION"),
                azure_endpoint=os.environ.get("OPENAI_API_BASE"),
                api_type="azure",
                temperature=0,
            )
            return llm
        elif self.llm_id == "azure_openai_gpt3.5":
            self.max_tokens = 1024 * 32
            llm = AzureOpenAI(
                engine=os.environ.get("OPENAI_API_ENGINE"),
                # model=os.environ.get("OPENAI_API_MODEL"),
                temperature=0.0,
                azure_endpoint=os.environ.get("OPENAI_API_BASE"),
                api_key=os.environ.get("OPENAI_API_KEY"),
                api_version=os.environ.get("OPENAI_API_VERSION"),
                max_retries=10,
            )
            return llm
        elif self.llm_id == "azure_openai_gpt4":
            llm = AzureOpenAI(
                engine=os.environ.get("OPENAI_API_ENGINE4"),
                # model=os.environ.get("OPENAI_API_MODEL4"),
                temperature=0.0,
                azure_endpoint=os.environ.get("OPENAI_API_BASE4"),
                api_key=os.environ.get("OPENAI_API_KEY4"),
                api_version=os.environ.get("OPENAI_API_VERSION4"),
                max_retries=10,
            )
            return llm

        elif self.llm_id == "openai_gpt4":
            llm: OpenAI = OpenAI(
                model=os.environ.get("OPENAI_API_MODEL_OAI", ""),
                api_key=os.environ.get("OPENAI_API_KEY_OAI"),
                api_base=os.environ.get("OPENAI_API_BASE_OAI"),
            )
            return llm
        # elif self.llm_id == "mistral":
        #     llm = MistralAI(
        #         api_key="",
        #         model="mistral-medium"
        #     )
        #     return llm
        elif self.llm_id == "vertex-ai":
            s_json = json.loads(os.environ.get("GOOGLE_SERVICE"))
            credentials = service_account.Credentials.from_service_account_info(
                info=s_json,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
            credentials.refresh(google_requests.Request())
            llm = Vertex(
                project="pandoras-tamer",
                model="text-bison",
                credentials=credentials,
                temperature=0,
                additional_kwargs={},
            )
            return llm
        else:
            self.tool.stream_log(
                f"LLM not found for id>: {self.llm_id}", level=LogLevel.ERROR
            )
            return None

    def get_max_tokens2(self) -> Optional[int]:
        if self.llm_id == "azure_openai_gpt3.5":
            return 16380
        else:
            self.tool.stream_log(
                f"LLM not found for id: {self.llm_id}", level=LogLevel.ERROR
            )
            return 0

    def get_llm(
        self, adapter_instance_id: Optional[str] = None
    ) -> Optional[LLM]:
        """Returns the LLM object for the tool.

        Returns:
            Optional[LLM]: The LLM object for the tool.
            (llama_index.llms.base.LLM)
        """
        adapter_instance_id = (
            adapter_instance_id
            if adapter_instance_id
            else self.llm_adapter_instance_id
        )
        # Support for get_llm using adapter_instance_id
        if adapter_instance_id is not None:
            try:
                llm_config_data = ToolAdapter.get_adapter_config(
                    self.tool, adapter_instance_id
                )
                llm_adapter_id = llm_config_data.get(Common.ADAPTER_ID)
                if llm_adapter_id in self.llm_adapters:
                    llm_adapter = self.llm_adapters[llm_adapter_id][
                        Common.METADATA
                    ][Common.ADAPTER]
                    llm_metadata = llm_config_data.get(Common.ADAPTER_METADATA)
                    llm_adapter_class: LLMAdapter = llm_adapter(llm_metadata)
                    llm_instance: Optional[
                        LLM
                    ] = llm_adapter_class.get_llm_instance()
                    return llm_instance
                else:
                    return None
            except Exception as e:
                self.tool.stream_log(
                    log=f"Unable to get llm instance: {e}", level=LogLevel.ERROR
                )
                return None
        else:
            logger.error("The adapter_instance_id parameter is None")
            return None

    def get_max_tokens(self, reserved_for_output: int = 0) -> int:
        """Returns the maximum number of tokens that can be used for the LLM.

        Args:
            reserved_for_output (int): The number of tokens reserved for the
                                        output.
                The default is 0.

            Returns:
                int: The maximum number of tokens that can be used for the LLM.
        """
        return self.max_tokens - reserved_for_output
