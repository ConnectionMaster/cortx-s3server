#
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#

import os
import sys
import yaml
from framework import Config
from framework import S3PyCliTest
from awsiam import AwsIamTest
from s3client_config import S3ClientConfig
from s3cmd import S3cmdTest
from s3fi import S3fiTest
import shutil

def get_arn_from_policy_object(raw_aws_cli_output):
    raw_lines = raw_aws_cli_output.split('\n')
    for _, item in enumerate(raw_lines):
        if (item.startswith("POLICY")):
            line = item.split('\t')
            arn = line[1]
        else:
            continue
    return arn

def user_tests():
    date_pattern = "[0-9|]+Z"
    #tests

    result = AwsIamTest('Create User').create_user("testUser").execute_test()
    result.command_response_should_have("testUser")

    result = AwsIamTest('CreateLoginProfile').create_login_profile("testUser","password").execute_test()
    login_profile_response_pattern = "LOGINPROFILE"+"[\s]*"+date_pattern+"[\s]*False[\s]*testUser"
    result.command_should_match_pattern(login_profile_response_pattern)
    result.command_response_should_have("testUser")

    result = AwsIamTest('GetLoginProfile Test').get_login_profile("testUser").execute_test()
    login_profile_response_pattern = "LOGINPROFILE"+"[\s]*"+date_pattern+"[\s]*False[\s]*testUser"
    result.command_should_match_pattern(login_profile_response_pattern)
    result.command_response_should_have("testUser")

    AwsIamTest('UpdateLoginProfile Test').update_login_profile("testUser").execute_test(negative_case=True).command_should_fail().command_error_should_have("InvalidRequest")

    AwsIamTest('UpdateLoginProfile with optional parameter- password').update_login_profile_with_optional_arguments\
        ("testUser","NewPassword",None,None).execute_test().command_is_successful()

    AwsIamTest('UpdateLoginProfile with optional parameter - password-reset-required').update_login_profile_with_optional_arguments\
        ("testUser",None,"password-reset-required",None).execute_test().command_is_successful()

    result = AwsIamTest('GetLoginProfile Test').get_login_profile("testUser").execute_test()
    login_profile_response_pattern = "LOGINPROFILE"+"[\s]*"+date_pattern+"[\s]*True[\s]*testUser"
    result.command_should_match_pattern(login_profile_response_pattern)
    result.command_response_should_have("True")

    AwsIamTest('Delete User').delete_user("testUser").execute_test().command_is_successful()

def policy_tests():
    #create-policy
    samplepolicy = os.path.join(os.path.dirname(__file__), 'policy_files', 'iam-policy.json')
    samplepolicy_testing = "file://" + os.path.abspath(samplepolicy)
    result = AwsIamTest('Create Policy').create_policy("iampolicy",samplepolicy_testing).execute_test()
    result.command_response_should_have("iampolicy")
    arn = (get_arn_from_policy_object(result.status.stdout))

    #create-policy fails if policy with same name already exists
    AwsIamTest('Create Policy').create_policy("iampolicy",samplepolicy_testing).execute_test(negative_case=True)\
        .command_should_fail().command_error_should_have("EntityAlreadyExists")

    #get-policy
    AwsIamTest('Get Policy').get_policy(arn).execute_test().command_is_successful()

    #list-policies
    AwsIamTest('List Policies').list_policies().execute_test().command_is_successful()

    #delete-policy
    AwsIamTest('Delete Policy').delete_policy(arn).execute_test().command_is_successful()

    #get-policy on non-existing policy
    AwsIamTest('Get Policy').get_policy(arn).execute_test(negative_case=True).command_should_fail().command_error_should_have("NoSuchEntity")

    #delete-policy on non-existing policy
    AwsIamTest('Delete Policy').delete_policy(arn).execute_test(negative_case=True).command_should_fail().command_error_should_have("NoSuchEntity")


if __name__ == '__main__':

    user_tests()
    policy_tests()
