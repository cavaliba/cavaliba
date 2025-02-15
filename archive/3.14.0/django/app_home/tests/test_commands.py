# (c) cavaliba.com


from io import StringIO
#import io

from django.core.management import call_command
from django.test import TestCase



class FrameworkCheckTest(TestCase):

    def test_check_command(self):

        output = StringIO()
        err = StringIO()
        call_command("check", verbosity=2, stdout=output)
        assert("System check identified no issues" in output.getvalue())    



class CommandTest(TestCase):

    def test_init_command(self):

        output = StringIO()
        err = StringIO()
        call_command("cavaliba_init", verbosity=2, stdout=output)
        assert("Done" in output.getvalue())    


    def test_update_command(self):

        output = StringIO()
        err = StringIO()
        call_command("cavaliba_update", verbosity=2, stdout=output)
        assert("Done" in output.getvalue())    


    def test_load_command(self):

        output = StringIO()
        err = StringIO()
        call_command("cavaliba_load", "unknown_file", verbosity=2, stdout=output)
        assert("Done" in output.getvalue())    


    def test_log_purge_command(self):

        output = StringIO()
        err = StringIO()
        call_command("cavaliba_log_purge", verbosity=2, stdout=output)
        assert("Done" in output.getvalue())    


    def test_update_stats_command(self):

        output = StringIO()
        err = StringIO()
        call_command("cavaliba_update_stats", verbosity=2, stdout=output)
        assert("Done" in output.getvalue())    

