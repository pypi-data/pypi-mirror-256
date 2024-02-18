# © Copyright 2024 Hewlett Packard Enterprise Development LP
import os
import subprocess


class TestCli:
    testdir = os.path.dirname(os.path.realpath(__file__))

    def test_version(self, setup_login: None) -> None:
        version_file = self.testdir + "/../../../../VERSION"
        expected = None
        with open(version_file, "r") as file:
            expected = file.read().rstrip()
            expected = "aioli " + expected
        assert 0 == os.system("aioli --version")
        actual = os.popen("aioli --version").read().strip()
        assert actual == expected

    def test_version_bad(self, setup_login: None) -> None:
        bad_version = "aioli 0.0.1-bad"
        assert 0 == os.system("aioli --version")
        actual = os.popen("aioli --version").read().strip()
        assert actual != bad_version

    def test_registry_list(self, setup_login: None) -> None:
        # Validating table headers, there are no entries yet
        assert os.system("aioli registry list") == 0
        expected = (
            " Name   | Type   | Access Key   | Bucket   | Secret Key   | Endpoint URL"
            "\n--------+--------+--------------+----------+--------------+----------------\n"
        )
        actual = subprocess.check_output(["aioli", "registry", "list"]).decode("utf-8")
        assert actual == expected

    def test_registry_create(self, setup_login: None) -> None:
        # Create a registry entry and test for success
        assert (
            os.system(
                "aioli registry create --type s3 --access-key minioadmin "
                "--secret-key minioadmin --bucket demo-bento-registry "
                "--endpoint-url http://10.30.91.81:30008/ bento-registry"
            )
            == 0
        )

        # The following test is expected to fail since we already created the
        # registry and we are trying to recreate the same.
        expected = (
            "ERROR: duplicate key value violates unique constraint "
            '\\"trained_model_registries_name_key\\" (SQLSTATE 23505): '
            "failed to create model registry"
        )
        try:
            subprocess.check_output(
                [
                    "aioli",
                    "registry",
                    "create",
                    "--type",
                    "s3",
                    "--access-key",
                    "minioadmin",
                    "--secret-key",
                    "minioadmin",
                    "--bucket",
                    "demo-bento-registry",
                    "--endpoint-url",
                    "http://10.30.91.81:30008/",
                    "bento-registry",
                ],
                stderr=subprocess.STDOUT,
            ).decode("utf-8")
        except subprocess.CalledProcessError as e:
            actual = (e.output).decode("utf-8")
            assert (actual.find(expected)) > 0

        # List the newly created registry entry and test for expected values
        expected = (
            "bento-registry | s3     | minioadmin   | demo-bento-registry | "
            "minioadmin   | http://10.30.91.81:30008/"
        )
        actual = subprocess.check_output(["aioli", "registry", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_registry_update(self, setup_login: None) -> None:
        # Update registry and test for expected values
        subprocess.check_output(
            [
                "aioli",
                "registry",
                "update",
                "--type",
                "s3",
                "--access-key",
                "minioadmin2",
                "--secret-key",
                "minioadmin2",
                "--bucket",
                "demo-bento-registry",
                "--endpoint-url",
                "http://10.30.91.81:30008/",
                "--name",
                "bento-registry1",
                "bento-registry",
            ],
            stderr=subprocess.STDOUT,
        ).decode("utf-8")
        expected = (
            "bento-registry1 | s3     | minioadmin2  | demo-bento-registry | "
            "minioadmin2  | http://10.30.91.81:30008/"
        )
        actual = subprocess.check_output(["aioli", "registry", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_model_list(self, setup_login: None) -> None:
        # Test header row of model table, there are no entries at this point.
        assert os.system("aioli model list") == 0
        expected = (
            " Name   | Description   | Version   | URI   | Image   | Registry"
            "\n--------+---------------+-----------+-------+---------+------------\n"
        )
        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")
        assert actual == expected

    def test_model_create(self, setup_login: None) -> None:
        # Create an entry for model table and test for expected values
        assert (
            os.system(
                "aioli model create iris_tf_keras --registry bento-registry1 "
                "--url s3://demo-bento-registry/iris_tf_keras "
                "--image fictional.registry.example/imagename "
                '--description "the model description"'
            )
            == 0
        )
        expected = (
            "iris_tf_keras | the model description |         1 | "
            "s3://demo-bento-registry/iris_tf_keras | "
            "fictional.registry.example/imagename | bento-registry1"
        )
        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_model_update(self, setup_login: None) -> None:
        # Update existing model entry and test for expected values
        assert (
            os.system(
                "aioli model update iris_tf_keras --name iris_tf_keras1 "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris_tf_keras_updated "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")
        expected = (
            "iris_tf_keras1 | the updated model description |         1 "
            "| s3://demo-bento-registry/iris_tf_keras_updated | "
            "fictional.registry.example/updated_imagename | bento-registry1"
        )
        assert (actual.find(expected)) > 0

        # Create a second version of the model
        assert (
            os.system(
                "aioli model update iris_tf_keras --name iris_tf_keras "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris_tf_keras_updated_v2 "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")
        expected = (
            "iris_tf_keras  | the updated model description |         2 "
            "| s3://demo-bento-registry/iris_tf_keras_updated_v2 | "
            "fictional.registry.example/updated_imagename | bento-registry1"
        )
        assert (actual.find(expected)) > 0

        # Try to create a third version of the model which fails without version
        assert (
            os.system(
                "aioli model update iris_tf_keras --name iris_tf_keras "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris_tf_keras_updated_v2 "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 256
        )

        # Create a third version of the model using the second version
        assert (
            os.system(
                "aioli model update iris_tf_keras --name iris_tf_keras "
                "--version 2 "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris_tf_keras_updated_v3 "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 0
        )

        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")

        expected = (
            "iris_tf_keras  | the updated model description |         3 "
            "| s3://demo-bento-registry/iris_tf_keras_updated_v3 | "
            "fictional.registry.example/updated_imagename | bento-registry1"
        )
        assert (actual.find(expected)) > 0

    def test_service_list(self, setup_login: None) -> None:
        # Test service table header row, table is empty at this point
        assert os.system("aioli service list") == 0
        expected = None
        data_file = self.testdir + "/aioli_service_list.txt"
        with open(data_file, "r") as file:
            expected = file.read()
        actual = subprocess.check_output(["aioli", "service", "list"]).decode("utf-8")
        assert actual == expected

    def test_service_create(self, setup_login: None) -> None:
        # Create a service and test for expected values
        assert (
            os.system(
                "aioli service create "
                '--description "The aioli service" '
                "--model iris_tf_keras1 iris_tf_keras_config"
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "service", "list"]).decode("utf-8")
        expected = (
            "iris_tf_keras_config | The aioli service | iris_tf_keras1 "
            "|          0 |          0 | concurrency |        0 "
            "|           |           |           |"
        )
        assert (actual.find(expected)) > 0

        # Use all supported options
        assert (
            os.system(
                "aioli service create "
                '--description "The aioli service" '
                "--model iris_tf_keras1 "
                "--autoscaling-min-replicas 1 "
                "--autoscaling-max-replicas 2 "
                "--autoscaling-target 1 "
                "--autoscaling-metric concurrency "
                "--requests-cpu 1.0 "
                "--requests-memory 1G "
                "--requests-gpu 1.0 "
                "--limits-cpu 2.5 "
                "--limits-memory 1Gi "
                "--limits-gpu 1.0 "
                "--gpu-type T4 "
                "--canary-traffic-percent 10 iris_tf_keras_config_1"
            )
            == 0
        )

        actual = subprocess.check_output(["aioli", "service", "list"]).decode("utf-8")
        expected = (
            "iris_tf_keras_config_1 | The aioli service | iris_tf_keras1 "
            "|          1 |          2 | concurrency |        1 "
            "| 1.0       | 1G        | 1.0       | 2.5     | 1Gi     "
            "| 1.0     | T4     |        10"
        )
        assert (actual.find(expected)) > 0

    def test_service_update(self, setup_login: None) -> None:
        # Update the service and test for success
        assert (
            os.system(
                "aioli service update "
                "--name iris_tf_keras_config_2 "
                "--canary-traffic-percent 20 "
                "iris_tf_keras_config_1"
            )
            == 0
        )

        # List the service and check for expected values
        actual = subprocess.check_output(["aioli", "service", "list"]).decode("utf-8")
        expected = (
            "iris_tf_keras_config_2 | The aioli service | iris_tf_keras1 "
            "|          1 |          2 | concurrency |        1 "
            "| 1.0       | 1G        | 1.0       | 2.5     | 1Gi     "
            "| 1.0     | T4     |        20"
        )
        assert (actual.find(expected)) > 0

        # Use all supported options
        assert (
            os.system(
                "aioli service update "
                "--name iris_tf_keras_config_3 "
                '--description "The aioli service" '
                "--model iris_tf_keras1 "
                "--autoscaling-min-replicas 2 "
                "--autoscaling-max-replicas 3 "
                "--autoscaling-target 2 "
                "--autoscaling-metric concurrency "
                "--requests-cpu 2.0 "
                "--requests-memory 2G "
                "--requests-gpu 1.0 "
                "--limits-cpu 3.5 "
                "--limits-memory 2Gi "
                "--limits-gpu 1.0 "
                "--gpu-type T4 "
                "--canary-traffic-percent 10 iris_tf_keras_config_2"
            )
            == 0
        )
        # List the service and check for expected values
        # All options are updated
        actual = subprocess.check_output(["aioli", "service", "list"]).decode("utf-8")
        expected = (
            "iris_tf_keras_config_3 | The aioli service | iris_tf_keras1 "
            "|          2 |          3 | concurrency |        2 "
            "| 2.0       | 2G        | 1.0       | 3.5     | 2Gi     "
            "| 1.0     | T4     |        10"
        )
        assert (actual.find(expected)) > 0

    def test_deployment_list(self, setup_login: None) -> None:
        # Test deployment table header, there are no entries at this point.
        assert os.system("aioli deployment list") == 0
        expected = (
            "Name   | Service   | Namespace   | Status   | Auth Required   | State   "
            "| Traffic %   | Secondary State   | Traffic %"
        )
        actual = subprocess.check_output(["aioli", "deployment", "list"]).decode("utf-8")
        assert actual.find(expected) > 0

    def test_deployment_create(self, setup_login: None) -> None:
        # Create a deployment and test for expected values
        assert (
            os.system(
                "aioli deployment create --service iris_tf_keras_config "
                "--namespace aioli "
                "--authentication-required true "
                "iris_tf_keras_deployment"
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "deployment", "list"]).decode("utf-8")
        expected = (
            "iris_tf_keras_deployment | iris_tf_keras_config | aioli       "
            "| Deploying | True            | Deploying |           0 "
            "| None              |           0"
        )
        assert actual.find(expected) > 0

    def test_deployment_update(self, setup_login: None) -> None:
        # Update the deployment and test for expected values.
        assert (
            os.system(
                "aioli deployment update --name iris_tf_keras_deployment_1 "
                "--authentication-required false "
                "--service iris_tf_keras_config "
                "--namespace aioli_prod iris_tf_keras_deployment"
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "deployment", "list"]).decode("utf-8")
        expected = (
            "iris_tf_keras_deployment_1 | iris_tf_keras_config | aioli_prod  "
            "| Deploying | False           | Deploying |           0 "
            "| None              |           0"
        )
        assert actual.find(expected) > 0

    def test_deployment_delete(self, setup_login: None) -> None:
        assert os.system("aioli deployment delete iris_tf_keras_deployment_1") == 0

    def test_service_delete(self, setup_login: None) -> None:
        assert os.system("aioli service delete iris_tf_keras_config") == 0
        assert os.system("aioli service delete iris_tf_keras_config_3") == 0

    def test_model_delete(self, setup_login: None) -> None:
        assert os.system("aioli model delete iris_tf_keras1 1") == 0
        assert os.system("aioli model delete iris_tf_keras 1") == 0
        assert os.system("aioli model delete iris_tf_keras 2") == 0
        assert os.system("aioli model delete iris_tf_keras 3") == 0

    def test_registry_delete(self, setup_login: None) -> None:
        # Delete the registry entry
        assert os.system("aioli registry delete bento-registry1") == 0

    def test_user_list(self, setup_login: None) -> None:
        # Test the user table header fields
        assert os.system("aioli user list") == 0
        expected = "admin      | Default Administrator | True    | True     | False"
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_user_create(self, setup_login: None) -> None:
        # create a user and test for expected values
        assert os.system("aioli user create --admin testuser") == 0
        expected = "testuser   |"
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_user_whoami(self, setup_login: None) -> None:
        assert os.system("aioli user whoami") == 0
        expected = "You are logged in as user 'admin'\n"
        actual = subprocess.check_output(["aioli", "user", "whoami"]).decode("utf-8")
        assert actual == expected

    def test_user_activate(self, setup_login: None) -> None:
        # Check activate feature
        assert os.system("aioli user activate testuser") == 0

    def test_user_deactivate(self, setup_login: None) -> None:
        # Check deactivate feature
        assert os.system("aioli user deactivate testuser") == 0

    def test_user_create_remote(self, setup_login: None) -> None:
        # create a remote user and test for expected values
        assert os.system("aioli user create --admin --remote testuser-r") == 0
        expected = "testuser-r |                       | True    | True     | True"
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0
