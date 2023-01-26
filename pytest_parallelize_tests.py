import pytest
import redis

parallelize_plugin = None


def pytest_configure(config):
    global parallelize_plugin
    assert parallelize_plugin is None, "Parallelize plugin already configured"
    parallelize_plugin = ParallelizePlugin(config)


def pytest_addoption(parser):
    parser.addoption('--part-id', type=str, action="store", help="unique part id used to parallelize tests")
    parser.addoption('--synchronization-id', type=str, action="store", help="unique id used to parallelize tests")
    parser.addoption('--parallelize-tests', action="store_true", default=False, help="turn on tests parallelization")
    parser.addoption('--redis-host', type=str, action="store", help="host that runs redis that handles parallelization")
    parser.addoption('--redis-port', type=str, action="store", default='6379', help="port that redis listens on")


def pytest_runtest_setup(item):
    assert isinstance(parallelize_plugin, ParallelizePlugin), parallelize_plugin
    if parallelize_plugin.parallelize_tests:
        parallelize_plugin.pytest_runtest_setup(item)


class ParallelizePlugin:
    EXPIRATION_TIME_S = 7 * 24 * 3600

    def __init__(self, config):
        self.parallelize_tests = config.getvalue('parallelize_tests')
        self.part_id = config.getvalue('part_id')
        self.synchronization_id = config.getvalue('synchronization_id')
        if self.parallelize_tests:
            assert not (
                self.part_id is None or self.synchronization_id is None
            ), "please provide --synchronization-id and --part-id"
            self.redis = redis.Redis.from_url(
                f"redis://{config.getvalue('redis_host')}:{config.getvalue('redis_port')}"
            )

    def pytest_runtest_setup(self, item):
        redis_test_key = self.synchronization_id + item.nodeid
        if self.redis.setnx(redis_test_key, self.part_id) == 0:
            pytest.skip(f"part {self.redis.get(redis_test_key).decode('utf-8')}")
        else:
            self.redis.expire(redis_test_key, self.EXPIRATION_TIME_S)
