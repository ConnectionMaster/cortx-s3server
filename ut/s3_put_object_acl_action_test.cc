/*
 * COPYRIGHT 2016 SEAGATE LLC
 *
 * THIS DRAWING/DOCUMENT, ITS SPECIFICATIONS, AND THE DATA CONTAINED
 * HEREIN, ARE THE EXCLUSIVE PROPERTY OF SEAGATE TECHNOLOGY
 * LIMITED, ISSUED IN STRICT CONFIDENCE AND SHALL NOT, WITHOUT
 * THE PRIOR WRITTEN PERMISSION OF SEAGATE TECHNOLOGY LIMITED,
 * BE REPRODUCED, COPIED, OR DISCLOSED TO A THIRD PARTY, OR
 * USED FOR ANY PURPOSE WHATSOEVER, OR STORED IN A RETRIEVAL SYSTEM
 * EXCEPT AS ALLOWED BY THE TERMS OF SEAGATE LICENSES AND AGREEMENTS.
 *
 * YOU SHOULD HAVE RECEIVED A COPY OF SEAGATE'S LICENSE ALONG WITH
 * THIS RELEASE. IF NOT PLEASE CONTACT A SEAGATE REPRESENTATIVE
 * http://www.seagate.com/contact
 *
 * Original author:  Rajesh Nambiar   <rajesh.nambiarr@seagate.com>
 * Original creation date: 03-June-2016
 */

#include "s3_put_object_acl_action.h"
#include "gtest/gtest.h"
#include "mock_s3_request_object.h"

class S3PutObjectAclActionTest : public testing::Test {
 protected:  // You should make the members protected s.t. they can be
             // accessed from sub-classes.
  S3PutObjectAclActionTest() {
    evhtp_request_t *req = NULL;
    EvhtpInterface *evhtp_obj_ptr = new EvhtpWrapper();
    mock_request = std::make_shared<MockS3RequestObject>(req, evhtp_obj_ptr);
    object_acl_put = new S3PutObjectACLAction(mock_request);
  }

  ~S3PutObjectAclActionTest() { delete object_acl_put; }

  S3PutObjectACLAction *object_acl_put;
  std::shared_ptr<MockS3RequestObject> mock_request;
};

TEST_F(S3PutObjectAclActionTest, Constructor) {
  EXPECT_NE(0, object_acl_put->number_of_tasks());
}
