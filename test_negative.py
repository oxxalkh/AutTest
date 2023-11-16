
from checkers import checkout_negative
import yaml

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_bad_arx):
        # test1
        assert checkout_negative("cd {}; 7z e bad_arx.{} -o{} -y".format(data["out"],
                                                data["type"], data["folder1"]), "ERRORS"), "test1 FAIL"

    def test_step2(self, make_bad_arx):
        # test2
        assert checkout_negative("cd {}; 7z t bad_arx.{} ".format(data["out"], data["type"]),
                                 "ERRORS"), "test2 FAIL"







