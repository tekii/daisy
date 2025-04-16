import pytest
from email.utils import parsedate_to_datetime


@pytest.fixture()
def the_attachment_module(test_runner_service_account_credentials):
    # remember, first monkeypatch the credentials, then import the module,
    # and i'm not sure if type annotate the return defeat the purpose
    import attachment

    yield attachment
    del attachment


def test_table_creation(the_attachment_module):
    #
    import attachment

    config = attachment.config

    table_name = the_attachment_module._TABLE + "_test"
    the_attachment_module._TABLE = table_name

    config.the_bq_client.delete_table(
        table=f"{config.PROJECT}.{config.DATASET}.{table_name}",
        not_found_ok=True,
    )

    attachment.create_table()

    config.the_bq_client.delete_table(
        table=f"{config.PROJECT}.{config.DATASET}.{table_name}", not_found_ok=False
    )


def test_insert(the_attachment_module):
    import attachment

    table_name = the_attachment_module._TABLE + "_test"
    the_attachment_module._TABLE = table_name

    attachment.create_table()

    row = attachment.AttachmentData(
        0,
        "19233f063eec1719",
        "a@b.c",
        parsedate_to_datetime("27 Sep 2024 11:43:58 -0300"),
        "the subject",
        "ANGjdJ_deHe7fENfIhMS1GHfH2zZ_Lw66velytd13TEvoFpbUVsT_xdujKFOKcL0l3O0gwmW3ihl3zTn"
        "1n1gUcLmzV_UV6Y7JlWNKr42RYCEaH0W60gCj9Ml7h5SWnpjHpjOZCDGEsA4yAc3-RnyUP7YmVzPWvzt"
        "tqghoFcSa2JIj04lJlu-HJnmYlP1HX-qN014vYR3UiwT7U5Y-su8pDpzRYAibzOyyzzvBD6I0BLJ3opG"
        "5Q0O6CCz7wa8gEpSDAzWDfppa_gh8s2Oo0LMkq67wmDNnV-IrSnMCI7HecChpFYvDVTBz_CiJSKQzvPP"
        "48QZKoNmUAAv6TTCeCOlcwCViIM7F3QfW7X87s-0xw7mj0i-puswnpj5cRCJH-MQdP_yKPe0_YgJwUY_brww",
        "TUTEUR2309240817.TXT",
    )

    attachment.insert(row)

    attachment.config.the_bq_client.delete_table(
        table=f"{attachment.config.PROJECT}.{attachment.config.DATASET}.{table_name}",
        not_found_ok=False,
    )
