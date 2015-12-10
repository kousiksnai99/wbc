#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'testing.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1)
    failures = test_runner.run_tests(['wbc.projects', 'wbc.comments','wbc.core','wbc.notifications','wbc.process','wbc.region','wbc.tags', 'wbc.stakeholder', 'wbc.events', 'wbc.accounts'])
    sys.exit(bool(failures))
