from unittest import TestCase

from events.templatetags.event_tags import split


class TestEventTags(TestCase):
    def setUp(self):
        pass

    def test_split(self):
        email = "foo@bar.com"
        resp = split(value=email, split_by="@")
        self.assertIsNotNone(resp)
        self.assertEqual(resp, "foo")

    def test_split__without_splitter(self):
        email = "foobarcom"
        resp = split(value=email, split_by="@")
        self.assertEqual(resp, email)
