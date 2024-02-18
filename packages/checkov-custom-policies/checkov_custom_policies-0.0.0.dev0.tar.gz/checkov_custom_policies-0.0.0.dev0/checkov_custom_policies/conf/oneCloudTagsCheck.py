from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckCategories, CheckResult

class oneCloudTagsCheck(BaseResourceCheck):

    def __init__(self, supported_resources=None, required_tags=None):
        name = "Ensure resources have required tags"
        id = "CUSTOM_TAGS_CHECK"
        self.supported_resources = supported_resources
        self.required_tags = required_tags
        categories = [CheckCategories.CONVENTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
            Looks for tags
        """
        if "tags" in conf:
            if isinstance(conf["tags"], list) and any(
                all(key in tag.keys() for key in self.required_tags)
                for tag in conf["tags"]
            ):
                return CheckResult.PASSED
            else:
                return CheckResult.FAILED
        else:
            return CheckResult.FAILED
