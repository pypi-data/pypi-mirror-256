from typing import Dict, Optional

from deeploy.models import UpdateDeploymentBase


class UpdateDeployment(UpdateDeploymentBase):
    """Class that contains the options for updating a Deployment"""

    model_serverless: Optional[bool] = None
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""
    model_credentials_id: Optional[str] = None
    """str, optional: uuid of credentials generated in Deeploy to access private Blob storage or Docker repo"""
    model_instance_type: Optional[str] = None
    """str, optional: the preferred instance type for the model"""
    model_mem_request: Optional[int] = None
    """int, optional: RAM request of model pod, in Megabytes."""
    model_mem_limit: Optional[int] = None
    """int, optional: RAM limit of model pod, in Megabytes."""
    model_cpu_request: Optional[float] = None
    """float, optional: CPU request of model pod, in CPUs."""
    model_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of model pod, in CPUs."""
    explainer_serverless: Optional[bool] = None
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""
    explainer_credentials_id: Optional[str] = None
    """str, optional: Credential id of credential generated in Deeploy to access private Blob storage or Docker repo"""
    explainer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the model pod."""
    explainer_mem_request: Optional[int] = None
    """int, optional: RAM request of model pod, in Megabytes."""
    explainer_mem_limit: Optional[int] = None
    """int, optional: RAM limit of model pod, in Megabytes."""
    explainer_cpu_request: Optional[float] = None
    """float, optional: CPU request of model pod, in CPUs."""
    explainer_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of model pod, in CPUs."""
    transformer_serverless: Optional[bool] = None
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""
    transformer_credentials_id: Optional[str] = None
    """str, optional: Credential id of credential generated in Deeploy to access private Blob storage or Docker repo"""
    transformer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the model pod."""
    transformer_mem_request: Optional[int] = None
    """int, optional: RAM request of model pod, in Megabytes."""
    transformer_mem_limit: Optional[int] = None
    """int, optional: RAM limit of model pod, in Megabytes."""
    transformer_cpu_request: Optional[float] = None
    """float, optional: CPU request of model pod, in CPUs."""
    transformer_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of model pod, in CPUs."""

    def to_request_body(self) -> Dict:
        request_body = {
            **super().to_request_body(),
            "modelServerless": self.model_serverless,
            "modelCredentialsId": self.model_credentials_id,
            "modelInstanceType": self.model_instance_type,
            "modelMemRequest": self.model_mem_request,
            "modelMemLimit": self.model_mem_limit,
            "modelCpuRequest": self.model_cpu_request,
            "modelCpuLimit": self.model_cpu_limit,
            "explainerServerless": self.explainer_serverless,
            "explainerCredentialsId": self.explainer_credentials_id,
            "explainerInstanceType": self.explainer_instance_type,
            "explainerMemRequest": self.explainer_mem_request,
            "explainerMemLimit": self.explainer_mem_limit,
            "explainerCpuRequest": self.explainer_cpu_request,
            "explainerCpuLimit": self.explainer_cpu_limit,
            "transformerServerless": self.transformer_serverless,
            "transformerInstanceType": self.transformer_instance_type,
            "transformerCredentialsId": self.transformer_credentials_id,
            "transformerMemRequest": self.transformer_mem_request,
            "transformerMemLimit": self.transformer_mem_limit,
            "transformerCpuRequest": self.transformer_cpu_request,
            "transformerCpuLimit": self.transformer_cpu_limit,
        }
        request_body = {k: v for k, v in request_body.items() if v is not None}
        return {k: v for k, v in request_body.items() if v is not None and v != {}}
