import pytest
from send_email import send_email
from config import DevConfig
from faker import Faker

fake = Faker()


def test_send(text_generator, text_generator_no_whitespaces, mailbox):

    subject = text_generator_no_whitespaces
    with mailbox as outbox:
        send_email(subject,
                   DevConfig.ADMINS[0],
                   [fake.email()],
                   text_generator,
                   None)
        assert len(outbox) == 1
        msg = outbox[0]
        assert msg.subject == subject
